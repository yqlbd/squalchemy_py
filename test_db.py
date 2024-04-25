from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

db = create_engine('mysql+mysqlconnector://', connect_args={'user': 'root',
                                                            'host': 'localhost',
                                                            'port': 3306,
                                                            'database': 'py',
                                                            'charset': 'utf8'}, echo='debug')
# 建立映射关系
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'  # 设置表明
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    age = Column(Integer)


# 初始化表
Base.metadata.drop_all(db)
Base.metadata.create_all(db)

# 向表中添加记录
obj = [User(name='小丽', age=12),
       User(name='李红', age=14),
       User(name='小刚', age=10)]
# 创建会话
obj_session = sessionmaker(db)
# 打开会话
db_session = obj_session()
# 向表中添加数据,此时数据保存在内存中
db_session.add_all(obj)
# 提交数据，将数据保存到数据库中
db_session.commit()
# 关闭会话
db_session.close()
