import numpy as np

# 模擬一組 10 筆的溫度訊號
temps = np.array([65.0, 72.5, 95.2, 68.1, 88.9, 92.3, 70.0, 60.5, 91.0, 78.0])

# --- 請開始您的任務 ---

# 任務 1: 使用 np.where() 產生一個 labels 陣列，內容為 "Danger" 或 "Normal"
# 如果訊號值 $> 90$，將其標註為字串 "Danger"。
# 否則，一律標註為 "Normal"。

# 任務 2: 使用 np.where() 將 temps 中小於 70 的值改為 70，其餘保持原樣並存回 corrected_temps
# 如果訊號值 $< 70$，將其強制修正為底限值 70。
# 其餘數值保持不變。
# 註：這不是單純的 clip，而是考驗您使用 np.where(condition, x, y) 的語法。
