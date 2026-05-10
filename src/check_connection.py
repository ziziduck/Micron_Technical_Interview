import sqlalchemy
import pandas as pd

# 您的連線金鑰
CONN_STR = "mssql+pyodbc://sa:Password123@localhost/Micron_OI_Lab?driver=ODBC+Driver+17+for+SQL+Server"

try:
    engine = sqlalchemy.create_engine(CONN_STR)
    # 建立一個測試用的 DataFrame
    test_df = pd.DataFrame({"status": ["System Online"], "agent": ["Jarvis"]})
    # 寫入資料庫 (如果表已存在則覆蓋)
    test_df.to_sql("Heartbeat", engine, if_exists="replace", index=False)
    print("✅ 報告先生：Python 與 MSSQL 已成功通訊！")
except Exception as e:
    print(f"❌ 通訊失敗：{e}")
