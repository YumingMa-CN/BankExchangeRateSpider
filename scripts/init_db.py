# --coding:UTF-8--
from db.connection import engine
from db.models import Base

Base.metadata.create_all(engine)
print("数据库表已创建")
