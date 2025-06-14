# --coding:UTF-8--
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_URI

# 创建数据库引擎
engine = create_engine(DB_URI, pool_pre_ping=True, echo=False)

# 创建Session类，用于ORM操作
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
