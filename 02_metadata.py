from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import insert


engine = create_engine('mysql+mysqlconnector://', connect_args={'user': 'root',
                                                                'host': 'localhost',
                                                                'port': 3306,
                                                                'database': 'py',
                                                                'charset': 'utf8'}, echo=True)
# 表结构声明
metadata_obj = MetaData()
user_table = Table('user_account', metadata_obj,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(20)),
                   Column('fullname', String(100))
                   )
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(255), nullable=False),
)
metadata_obj.drop_all(engine)
metadata_obj.create_all(engine)

stmt = insert(user_table).values(
    name="spongebob", fullname="Spongebob Squarepants")

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()
