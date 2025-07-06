__all__ = ["save_to_api"]

import requests
from utils.common import row_to_db


def save_to_api(data, bank_code, api_config):
    """
    将数据保存到API接口
    :param data: 数据列表
    :param bank_code: 银行代码
    :return: 响应状态码和结果
    """
    headers = {k: v.format(key=api_config['key']) for k, v in api_config['headers'].items()}
    payload = [row_to_db(item, bank_code) for item in data]
    resp = requests.post(api_config['url'], json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()
