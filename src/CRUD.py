from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "mssql+pyodbc://sa:Password123@127.0.0.1/Micron?driver=ODBC+Driver+17+for+SQL+Server"
)


def insert(name, dept, salary):
    sql = text(
        "INSERT INTO Employees (Name, Department, Salary) VALUES (:name, :dept, :salary)"
    )
    with engine.connect() as conn:
        conn.execute(sql, {"name": name, "dept": dept, "salary": salary})
        conn.commit()  # 務必 commit 才會真正寫入資料庫
    print(f"[Insert] 已新增: {name} {dept}")


def update(salary):
    sql = text("UPDATE dbo.Employees SET Salary = :salary WHERE Name = 'test'")
    with engine.connect() as conn:
        conn.execute(sql, {"salary": salary})
        conn.commit()
    print(f"[Update] 已修改: {salary}")


def delete(name):
    sql = text("DELETE FROM Employees WHERE Name = :name")
    with engine.connect() as conn:
        conn.execute(sql, {"name": name})
        conn.commit()
    print(f"[Delete] 已刪除: {name}")


def query_pandas(name):
    sql = text("SELECT * FROM Employees")
    with engine.connect() as conn:
        result = conn.execute(sql)
        # 我們使用 list(result.mappings()) 將所有結果轉為字典清單
        df = pd.DataFrame(result.mappings())
    print(f"[Query] 已查詢: {name}")
    return df


def query_list(name):
    sql = text("SELECT * FROM Employees")
    with engine.connect() as conn:
        result = conn.execute(sql)
        data = result.mappings().all()
    print(f"[Query] 已查詢: {name}")
    return data


df_result = query_list("test")
print(df_result)
