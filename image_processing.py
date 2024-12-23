import cv2
import numpy as np
from typing import Tuple, Optional

def detect_circles(img: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ぼかしを適用
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Hough変換を使用して円を検出
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100, param1=100, param2=30, minRadius=50, maxRadius=300)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # 器の円とスープの円を区別するために、最も大きな円を器の円と仮定
        bowl_circle = max(circles, key=lambda c: c[2])
        # 残りの円の中で最も大きな円をスープの円と仮定
        soup_circle = max([c for c in circles if not np.array_equal(c, bowl_circle)], key=lambda c: c[2], default=None)
        return bowl_circle, soup_circle

    return None, None

def calculate_score(after_path: str) -> int:
    # 画像を読み込む
    after_img = cv2.imread(after_path)

    # 器の円とスープの円を検出
    bowl_circle, soup_circle = detect_circles(after_img)

    if bowl_circle is None or soup_circle is None:
        return 0  # 円が検出されなかった場合、スコアは0

    # 器の面積とスープの面積を計算
    bowl_area = np.pi * (bowl_circle[2] ** 2)
    soup_area = np.pi * (soup_circle[2] ** 2)

    # スープの割合を計算
    soup_ratio = soup_area / bowl_area

    # スコアを算出（例: 残量の割合を元に10点刻みで100点満点）
    score = int((1 - soup_ratio) * 10) * 10
    return max(score, 0)