from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
engine = create_engine('mysql+mysqlconnector://', connect_args={'user': 'root',
                                                                'host': 'localhost',
                                                                'port': 3306,
                                                                'database': 'py',
                                                                'charset': 'utf8'}, echo=True)

# engine.connect() 执行sql后需要手动commit
# with engine.connect() as conn:
#     result = conn.execute(text("select 'hello world'"))
#     print(result.all())
#     conn.execute(text("CREATE TABLE  some_table (x int, y int)"))
#     conn.execute(
#         text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 1, "y": 1}, {"x": 2, "y": 4}],)
#     conn.commit()

# engine.connect() 执行sql后需要会自动commit
# with engine.begin() as conn:
#     conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [
#                  {"x": 6, "y": 8}, {"x": 9, "y": 10}],)

# with类似try catch，简化编写方式
with engine.begin() as conn:
    result = conn.execute(text("select x, y from some_table"))
    # 将结果映射成字典形式
    for dict_row in result.mappings():
        x = dict_row["x"]
        y = dict_row["y"]
        print(f'x:{x},y:{y}')

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 6, "y": 15}],
    )
    session.commit()
