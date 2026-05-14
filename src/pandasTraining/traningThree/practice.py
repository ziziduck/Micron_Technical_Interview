import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

raw_data = {
    "timestamp": [
        "2026-05-14 09:00",
        "2026-05-14 09:01",
        "2026-05-14 09:02",
        "2026-05-14 09:03",
        "2026-05-14 09:04",
        "2026-05-14 09:05",
    ],
    "Dept": ["Etch", "Etch", "Photo", "Photo", "ThinFilm", "ThinFilm"],
    "Temperature": [70.5, 72.0, 88.0, 71.0, 69.5, 95.0],
    "Pressure": [100, 105, -5, 110, 102, 120],  # 注意：這裡有負值壓力
    "Efficiency": [0.9, 0.85, np.nan, 0.95, 0.88, 0.70],
}

try:
    engine = create_engine(
        "mssql+pyodbc://sa:Password123@127.0.0.1/Micron?driver=ODBC+Driver+17+for+SQL+Server"
    )
    pd.DataFrame(raw_data).to_sql(
        "Machine_Final_Logs", engine, if_exists="replace", index=False
    )
    df = pd.read_sql("SELECT * FROM Machine_Final_Logs", engine)
    print("初始資料存取成功")
except Exception as e:
    print(f"初始資料存取失敗: {e}")

# 資料防禦與清洗：
# 1. 移除 Efficiency 為空的行。
# df = df.dropna(subset=['Efficiency'])
df = df[df["Efficiency"].notna()]

# 2. 將 Pressure 欄位中所有負值（物理錯誤數據）強制修正為 0。
# def fixPressure(row):
#     if row["Pressure"] < 0:
#         return 0
#     return row["Pressure"]


# df["Pressure"] = df.apply(fixPressure, axis=1)
df["Pressure"] = df["Pressure"].clip(lower=0)
# 3. 將 Dept 轉為 category 以優化記憶體。
df["Dept"] = df["Dept"].astype("category")
print("資料防禦與清洗完成")

# 特徵與異常標註：
# 1. 計算 Temperature 的 3 期移動平均 (temp_ma)。
# 2. 建立 Warning_Score 欄位：Warning_Score = (Temperature - temp_ma) * 0.5 + (Pressure * 0.1)。
# 3. 如果 Warning_Score > 10，則將 Is_Warning 標記為 1，否則為 0。

# 報表聚合輸出：
# 1. 按 Dept 分組，計算：平均 Efficiency、異常總數 sum(Is_Warning)。
# 2. 排序輸出：找出 Is_Warning 總數最高的前 2 個部門名稱。
# 3. 交付格式：將最終的聚合報表轉換為 orient='records' 的列表格式。
