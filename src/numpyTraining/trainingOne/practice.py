import numpy as np

# 模擬原始感測器訊號 (包含極端異常值 150.0)
raw_signals = np.array([70.5, 72.1, 150.0, 68.9, 71.2, 95.5, 88.0, 75.3, 62.1, 70.0])

# --- 現在，請開始手寫以下任務 ---

# 任務 1: 使用 np.clip() 將數值限制在 [0, 100] 之間
raw_signals = raw_signals.clip(0, 100)
print("任務 1 結束")
# 任務 2: 執行正規化，計算出新陣列 signals_norm (提示：使用 signals.min() 與 .max())
signals_norm = (raw_signals - raw_signals.min()) / (
    raw_signals.max() - raw_signals.min()
)
print("任務 2 結束")
# 任務 3: 找出高於平均值的數值個數 (提示：使用布林索引與 .sum())
over_avg = (raw_signals > raw_signals.mean()).sum()
print("任務 3 結束")
# 任務 4: 使用 .reshape() 將陣列轉為 2x5 矩陣
raw_signals = raw_signals.reshape(2, 5)
print("任務 4 結束")
