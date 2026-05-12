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

# 任務 2: 過濾出狀態，用平均值填補 NaN (缺失) 的數值

# 條件篩選：找出低效能機台。
efficiency = df["Efficiency"]  # 使用欄位選取
low_efficiency = df[  # 內層會在對應的欄位塞入布林值，外層根據內層判斷留下的資訊
    df["Efficiency"] < 0.8
]
# 多重條件：使用 & (AND) 與 | (OR)。
choose_dept = df[(df["Dept"] == "Etch") | (df["Dept"] == "Photo")]
# 缺失值處理：df.fillna() 或 df.dropna()。
avg_val = df["Efficiency"].mean()  # 會針對選定的「欄位（Series）」進行加總後除以總筆數
df["Efficiency"] = df["Efficiency"].fillna(avg_val)  # 填補缺失值NaN
df_cleaned = df.dropna()  # 只要有一欄是 NaN，就刪除該整列
df_cleaned = df.dropna(  # 只有當特定欄位（如 Machine_ID）缺失時才刪除
    subset=["Efficiency"]
)

# 過濾出所有狀態為 Offline 且 Efficiency 低於 0.5 的機台
df_answer = df[(df["Status"] == "Offline") & (df["Efficiency"] < 0.5)]
print(df_answer)
# 將所有 Efficiency 為 NaN (缺失) 的數值填補為該欄位的平均值
df["Efficiency"] = df["Efficiency"].fillna(df["Efficiency"].mean())
print(df)
print("任務 2 結束")

# 任務 3: 產出部門效能報表 (groupby + agg)
