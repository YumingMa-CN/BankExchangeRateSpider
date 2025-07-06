__all__ = ['save_to_db']

from db.operations import save_exchange_rates
from utils.common import row_to_db

def save_to_db(data, bank_code):
    db_batch = [row_to_db(item, bank_code) for item in data]
    save_exchange_rates(db_batch)
