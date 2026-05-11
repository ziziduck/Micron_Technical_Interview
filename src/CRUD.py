from sqlalchemy import create_engine, text
from pathlib import Path
import pandas as pd

engine = create_engine(
    "mssql+pyodbc://sa:Password123@127.0.0.1/Micron?driver=ODBC+Driver+17+for+SQL+Server"
)


def load_sql(file_path):
    return text(Path(file_path).read_text(encoding="utf-8"))


def insert(name, dept, salary):
    sql = load_sql("sql/insert_employee.sql")
    with engine.connect() as conn:
        conn.execute(sql, {"name": name, "dept": dept, "salary": salary})
        conn.commit()  # 務必 commit 才會真正寫入資料庫
    print(f"[Insert] 已新增: {name} {dept}")


def update(salary):
    sql = load_sql("sql/update_employee.sql")
    with engine.connect() as conn:
        conn.execute(sql, {"salary": salary})
        conn.commit()
    print(f"[Update] 已修改: {salary}")


def delete(name):
    sql = load_sql("sql/delete_employee.sql")
    with engine.connect() as conn:
        conn.execute(sql, {"name": name})
        conn.commit()
    print(f"[Delete] 已刪除: {name}")


def query_pandas(name):
    sql = load_sql("sql/query_employee.sql")
    with engine.connect() as conn:
        result = conn.execute(sql, {"name": name})
        # 我們使用 list(result.mappings()) 將所有結果轉為字典清單
        df = pd.DataFrame(result.mappings())
    print(f"[Query] 已查詢: {name}")
    return df


def query_list(name):
    sql = load_sql("sql/query_employee.sql")
    with engine.connect() as conn:
        result = conn.execute(sql, {"name": name})
        data = result.mappings().all()
    print(f"[Query] 已查詢: {name}")
    return data


df_result = query_list("test")
print(df_result)
