import pandas as pd
import numpy as np

# 模擬原始資料
data = {
    "timestamp": pd.date_range(start="2026-05-15 09:00", periods=6, freq="T"),
    "Dept": ["Etch", "Etch", "Photo", "Photo", "ThinFilm", "ThinFilm"],
    "Temperature": [70.5, 92.0, 88.0, 95.0, 69.5, 91.5],
    "Pressure": [100, 115, -5, 120, 102, 108],  # 包含負值
    "Efficiency": [
        0.9123,
        0.8544,
        np.nan,
        0.9567,
        0.8812,
        0.7034,
    ],  # 包含空值與多位小數
}

df = pd.DataFrame(data)

# --- 請開始您的綜合演練 ---

# 1. [NumPy 階段] 訊號清洗與特徵生成
# 斷訊過濾：使用 np.where() 將 Pressure 中小於 0 的數值強制修正為 0。
# 極速標註：使用 np.where() 建立一個 NumPy 陣列 status_tags。
# 如果 Temperature > 90 且 Pressure > 110，標註為 "Critical"。否則標註為 "Normal"。
df["Pressure"] = np.where(df["Pressure"] < 0, 0, df["Pressure"])
status_tags = np.where(
    (df["Temperature"] > 100) & (df["Pressure"] > 110), "Critical", "Normal"
)
print("任務 1 結束")

# [Pandas 階段] 資料整合與時序分析
# 資料對齊：將上述 NumPy 處理完的 Pressure 與 status_tags 塞回 DataFrame。
# 空值防禦：移除 Efficiency 為空的行。
# 移動特徵：計算 Temperature 的 3 期移動平均 (temp_ma)。
df["Pressure"] = np.where(df["Pressure"] < 0, 0, df["Pressure"])
df["status_tags"] = status_tags
df = df[df["Efficiency"].notna()].reset_index(drop=True)
df["temp_ma"] = df["Temperature"].rolling(3).mean()

print("任務 2 結束")
# [綜合輸出] 風險報表
# 聚合統計：按 Dept 與 status_tags 分組。
# 關鍵指標：計算各組的平均 Efficiency 與 Pressure 的最大值。
# API 交付：將結果四捨五入到小於兩位，並轉為 orient='records' 的格式。
