from sqlalchemy import ForeignKey, String, Integer, create_engine, select
from typing import List, Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


engine = create_engine('mysql+mysqlconnector://', connect_args={'user': 'root',
                                                                'host': 'localhost',
                                                                'port': 3306,
                                                                'database': 'py',
                                                                'charset': 'utf8'}, echo=True)
# 定义基础类，ORM都继承此类


class Base(DeclarativeBase):
    pass

# 账户对象，继承基础对象


class User(Base):
    # 表明
    __tablename__ = "user_account"
    # 定义主键和其他字段
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    # 一对多映射
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# 地址对象


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(100))
    # 外键
    user_id = mapped_column(ForeignKey("user_account.id"))
    # 一对一映射
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# 初始化表结构
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

    # 单表查询
    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    for user in session.scalars(stmt):
        print(user)
    # 联合查询
    stmt = select(Address).join(Address.user).where(User.name == 'sandy')
    for address in session.scalars(stmt):
        print(address)
