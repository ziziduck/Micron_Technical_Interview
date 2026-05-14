# Micron Technical Interview - 開發環境說明

本專案專為美光 (Micron) Data Science Engineer 面試準備，採用 **Python 3.13 全域環境** 進行配置，並整合 Docker MSSQL 資料庫。

## 1. 環境配置 (Environment)
* **Python 版本**: 3.13.13
* **環境模式**: 全域環境 (Global Environment)
* **IDE**: Visual Studio Code (已禁用 AI 插件如 Copilot/Tabnine)

## 2. Python 核心套件與工具
由於系統環境變數設定，建議統一使用 `py -m` 指令確保版本正確：

| 套件類別 | 推薦指令 | 用途說明 |
| :--- | :--- | :--- |
| **數據處理** | `py -m pip install pandas numpy` | 處理 DataFrame 與科學運算 |
| **資料庫連線**| `py -m pip install pyodbc sqlalchemy` | 負責與 MSSQL 建立連線 (ETL) |
| **數據視覺化**| `py -m pip install matplotlib seaborn` | 繪製趨勢圖與異常分析圖 |
| **進階分析** | `py -m pip install scipy ipykernel` | 統計檢定與 Jupyter Notebook 支援 |

若需重新配置環境，請在啟動虛擬環境後執行：
`pip install pandas numpy pyodbc sqlalchemy matplotlib seaborn scipy ipykernel`

## 3. 資料庫配置 (MSSQL via Docker)
本專案使用 Docker 容器化部署數據庫，以便快速重置測試環境。

| 項目 | 設定值 | 指令 / 用途 |
| :--- | :--- | :--- |
| **容器名稱** | `db` |
| **對外埠號** | `1433` | 預設標準埠號 |
| **管理帳號** | `sa` | 系統最高權限 |
| **登入密碼** | `Password123` | 符合安全規範之預設密碼 |
| **練習庫名** | `Micron_OI_Lab` | 存放生產線模擬數據 |


```powershell
docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Password123" `
   -p 1433:1433 --name db `
   -d [mcr.microsoft.com/mssql/server:2022-latest](https://mcr.microsoft.com/mssql/server:2022-latest)
```

---

## 4. 快速執行指令
若要執行專案腳本，請於根目錄 `D:\Code\Project\Micron_Technical_Interview` 執行：

* **啟動環境**: `docker start db`
* **關閉環境**: `docker stop db`
* **檢查狀態**: `docker ps`
* **執行測試**: `py src/final_check.py`

## 5. Python 與 MSSQL 通訊

下載 Microsoft ODBC Driver 17 for SQL Server (x64)

```python
from sqlalchemy import create_engine      # 1. 連線引擎工具

# 2. 定義通關密語 (連線字串)，資料庫類型+驅動://帳號:密碼@伺服器位址/資料庫名稱?driver=驅動程式名稱
conn_str = "mssql+pyodbc://sa:Password123@127.0.0.1/Micron_OI_Lab?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)         # 3. 建立連線引擎

# 4. 執行讀取
df = pd.read_sql("SELECT * FROM Employees", engine)
```

## 6. Python 套件練習
1. 數據處理與清洗（核心基礎）
- Pandas: 毫無疑問的霸主。用於處理生產線的時序資料（Time-series）、機台 Log。
- NumPy: 用於高效能的數值運算，特別是處理感測器回傳的矩陣數據。
- SQLAlchemy / pyodbc: 如我們之前討論的，這是您與資料庫（如 SQL Server, Oracle）溝通的橋樑。

2. 數據分析與統計推論（Intelligence 來源）
- SciPy: 用於科學計算，特別是製程控制中的機率分佈與統計檢定（如：判斷這批次的良率下降是否具備統計顯著性）。
- Statsmodels: 用於更深入的統計模型，例如時間序列分析（ARIMA），預測未來的產能需求。