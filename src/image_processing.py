import cv2
import numpy as np
import matplotlib.pyplot as plt

from utils.rank import Rank

def calculate_score(img_path: str) -> Rank:
    # 画像を読み込む
    img = cv2.imread(img_path)

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 二値化
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # 輪郭を検出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 一番大きい輪郭を見つける
    largest_contour = max(contours, key=cv2.contourArea)
    contour_area = cv2.contourArea(largest_contour)

    # 輪郭に近い部分の色を取得
    mask_outer = np.zeros_like(binary)
    cv2.drawContours(mask_outer, [largest_contour], -1, 255, thickness=cv2.FILLED) # type: ignore
    
    # 輪郭から一定の距離内のピクセルを取得
    distance_transform = cv2.distanceTransform(mask_outer, cv2.DIST_L2, 5)
    mask_near_contour = ((distance_transform < 35) & (distance_transform > 10)).astype(np.uint8) * 255  # 距離20ピクセル以内の領域をマスク
    
    inner_contour_color = np.median(gray[mask_near_contour == 255]) # type: ignore
    threshold_value = inner_contour_color - 65

    # 再度二値化
    _, binary_inner = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # マスクを作成
    mask = np.zeros_like(binary_inner)
    cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED) # type: ignore

    # マスクされた領域の黒色ピクセル数をカウント
    black_pixels = np.sum((binary_inner == 0) & (mask == 255))
    
    # お皿全体のピクセル数をカウント
    total_pixels = binary_inner.size

    # 黒色ピクセルの割合を計算
    black_ratio = black_pixels / total_pixels
    
    # スコアを決定
    if black_ratio <= 0.04:
        score = Rank.GOLD
    else:
        # 輪郭の面積に基づいて距離の閾値を調整
        distance_threshold = 20 + (contour_area / 10000)  # 面積が大きいほど閾値を大きくする いじる必要あり
        # 黒色ピクセルの塊と輪郭との距離を計算
        black_pixel_distances = distance_transform[(binary_inner == 0) & (mask == 255)]
        if np.mean(black_pixel_distances) < distance_threshold: # type: ignore
            score = Rank.SILVER
        else:
            score = Rank.BRONZE

    return score


if __name__ == "__main__":
    # テスト画像のパス（ユーザーが指定した画像パスに置き換えてください）
    test_image_path = '/Users/ae/Desktop/ラーメン画像/具残し2.png'

    # 黒色部分の割合を計算して表示
    print(calculate_score(test_image_path))

