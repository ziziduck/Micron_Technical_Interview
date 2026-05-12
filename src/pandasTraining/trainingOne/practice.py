import pandas as pd
import numpy as np

# --- 這是您的練習數據來源 ---
data = {
    "Machine_ID": ["M01", "M02", "M03", "M04", "M05", "M06"],
    "Dept": ["Etch", "Etch", "Photo", "Photo", "ThinFilm", "ThinFilm"],
    "Efficiency": [0.85, 0.42, 0.91, np.nan, 0.77, 0.35],
    "Status": ["Online", "Offline", "Online", "Online", "Online", "Offline"],
}
df = pd.DataFrame(data)

# --- 現在，請開始手寫以下任務 ---
# 任務 1: 找出總筆數 (提示: df.shape 或 len())
# 任務 2: 填補 Efficiency 的 NaN 值為平均值
# 任務 3: 產出部門效能報表 (groupby + agg)
