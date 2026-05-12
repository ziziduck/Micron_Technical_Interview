import pandas as pd
import numpy as np

# --- 這是您的練習數據來源 ---
data = {
    "Machine_ID": ["M01", "M02", "M03", "M04", "M05", "M06"],
    "Dept": ["Etch", "Etch", "Photo", "Photo", "ThinFilm", "ThinFilm"],
    "Efficiency": [0.85, 0.42, 0.91, np.nan, 0.77, 0.35],
    "Status": ["Online", "Offline", "Online", "Online", "Online", "Offline"],
}
# 建立資料框。
df = pd.DataFrame(data)

# --- 現在，請開始手寫以下任務 ---
# 任務 1: 找出總筆數 (提示: df.shape 或 len())

# 看資料有幾列幾行。
total_row = df.shape  # (6, 4)
total_row = len(df)  # 6
# 檢查有沒有欄位是 NULL，或是型別錯誤（例如日期變成字串），數值會出現在 Terminal。
data_info = df.info()
# 觀察前 n 筆資料的規律。
head_row = df.head(2)

print(total_row)
print("任務 1 結束")

# 任務 2: 填補 Efficiency 的 NaN 值為平均值
# 任務 3: 產出部門效能報表 (groupby + agg)
