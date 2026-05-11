from sqlalchemy import create_engine, text

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
    print(f"[Create] 已新增: {name} {dept}")


insert("test", "test", 1000)
