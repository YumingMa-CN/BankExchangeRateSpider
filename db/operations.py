# --coding:UTF-8--
from .connection import SessionLocal
from .models import ExchangeRate
from sqlalchemy.exc import SQLAlchemyError

def save_exchange_rate(data: dict):
    """
    插入一条汇率数据
    :param data: 字典，键与ExchangeRate模型字段对应
    """
    session = SessionLocal()
    try:
        obj = ExchangeRate(**data)
        session.add(obj)
        session.commit()
        return obj.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"插入失败: {e}")
        raise
    finally:
        session.close()

def save_exchange_rates(batch_data: list):
    """
    批量插入汇率数据
    :param batch_data: 字典列表
    """
    session = SessionLocal()
    try:
        objs = [ExchangeRate(**item) for item in batch_data]
        session.add_all(objs)
        session.commit()
        return [obj.id for obj in objs]
    except SQLAlchemyError as e:
        session.rollback()
        print(f"批量插入失败: {e}")
        raise
    finally:
        session.close()
