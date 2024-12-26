from cv2.typing import MatLike
from utils.rank import Rank
import cv2
import numpy as np

def analyze_loss(img: MatLike, color: str = "white")-> Rank:
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 二値化
    if(color == "white"):
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    elif(color == "black"):
        _, binary = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
    else:
        print("colorはwhiteかblackを選択してください")
        return Rank.ERROR

    # 輪郭を検出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 一番大きい輪郭を見つける
    largest_contour = max(contours, key=cv2.contourArea)

    # 輪郭に近い部分の色を取得
    mask_outer = np.zeros_like(binary)
    cv2.drawContours(mask_outer, [largest_contour], -1, 255, thickness=cv2.FILLED) # type: ignore
    
    # 輪郭から一定の距離内のピクセルを取得
    distance_transform = cv2.distanceTransform(mask_outer, cv2.DIST_L2, 5)
    mask_near_contour = ((distance_transform < 35) & (distance_transform > 10)).astype(np.uint8) * 255  # 距離20ピクセル以内の領域をマスク
    
    inner_contour_color = np.median(gray[mask_near_contour == 255]) # type: ignore
    if(color == "white"):
        threshold_value = inner_contour_color - 65 
    elif(color == "black"):
        threshold_value = inner_contour_color + 65
    

    
    # 背景が白すぎる場合の例外処理（画像の4隅を使用）
    h, w = gray.shape
    corners = [gray[:10, :10].flatten(), gray[:10, -10:].flatten(), gray[-10:, :10].flatten(), gray[-10:, -10:].flatten()]
    
    corner_means = [np.mean(corner) for corner in corners] # type: ignore
    
    top_two_white_corners_mean = np.mean(sorted(corner_means)[-2:])
    
    if(color == "white"):
        if top_two_white_corners_mean > 190:  # 閾値は適宜調整してください
            print("背景が白すぎると判断されました。")
            return  Rank.ERROR
    

    # お皿が黒い場合の例外処理
    if(color == "white"):
        if threshold_value < 112:
            print("解析できませんでした。")
            return Rank.ERROR
    if(color == "black"):
        if threshold_value < 65:
            print("解析できませんでした。")
            return Rank.ERROR

    # 再度二値化
    if(color == "white"):
        _, binary_inner = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    elif(color == "black"):
        _, binary_inner = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)

    # マスクを作成
    mask = np.zeros_like(binary_inner)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED) # type: ignore

    # マスクされた領域の黒色ピクセル数をカウント
    black_pixels = np.sum((binary_inner == 0) & (mask == 255))
    
    # お皿全体のピクセル数をカウント
    total_pixels = binary_inner.size

    # 黒色ピクセルの割合を計算
    black_ratio = black_pixels / total_pixels
    print(black_ratio)
    
    # スコアを決定
    if black_ratio <= 0.04:
        score = Rank.GOLD
    else:
        # 輪郭の面積に基づいて距離の閾値を調整
        distance_threshold = 170  # 面積が大きいほど閾値を大きくする いじる必要あり
        # 黒色ピクセルの塊と輪郭との距離を計算
        black_pixel_distances = distance_transform[(binary_inner == 0) & (mask == 255)]
        if(color == "white"):
            if np.mean(black_pixel_distances) < distance_threshold: # type: ignore
                score = Rank.SILVER
            else:
                score = Rank.BRONZE
        if(color == "black"):
            if(black_ratio < 0.4):
                score = Rank.SILVER
            else:
                score = Rank.BRONZE

    return score # type: ignore
