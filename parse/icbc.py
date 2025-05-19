from utils.common import fetch_html
from config import BANKS, BANK_CODE
import re
import json
import time


__all__ = ['get_data']
CODE = 'icbc'

def _parse_page(html):
    """
        根据正则提取汇率数据
    """
    m = re.search(r'<pre>(.*?)</pre>', html, re.S)
    # print(html)
    if not m:
        raise ValueError("预期结构未找到")
    return json.loads(m.group(1))


def _convert_api_data(data):
    """
    将数据转换为字典列表
    """
    # a sample of data is:
    # {"code":0,"message":"success","data":[
    # {"currencyType":"012","currencyCHName":"英镑","currencyENName":"GBP","reference":"959.48","foreignBuy":"956.70","foreignSell":"963.89","cashBuy":"956.70","cashSell":"963.89","publishDate":"2025-05-19","publishTime":"10:49:59"},
    # {"currencyType":"013","currencyCHName":"港币","currencyENName":"HKD","reference":"92.27","foreignBuy":"92.13","foreignSell":"92.51","cashBuy":"92.13","cashSell":"92.51","publishDate":"2025-05-19","publishTime":"10:49:59"}
    # ]}
    result = []
    rows = data["data"]
    # headers = ["币种名称", "币种代码", "基准金额", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "更新时间", "采集时间", "银行"]
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for row in rows:
        item = {
            "币种名称": row.get("currencyCHName", ""),
            "币种代码": row.get("currencyENName", ""),
            "基准金额": 100,
            "参考价": row.get("reference", ""),
            "现汇买入价": row.get("foreignBuy", ""),
            "现钞买入价": row.get("cashBuy", ""),
            "现汇卖出价": row.get("foreignSell", row.get("cashSell", "")),
            "现钞卖出价": row.get("cashSell", row.get("foreignSell")),
            "更新时间": row.get("publishDate", "") + ' ' + row.get("publishTime", ""),
            "采集时间": collecting_time,
            "银行": BANKS[CODE]['name'],
        }
        result.append(item)
    return result

def get_data():
    """
    获取数据
    """
    _, api_content = fetch_html(
        url_business=BANKS[CODE]['url_business'],
        url_api=BANKS[CODE]['url_api'],
        visit_business=BANKS[CODE]['visit_business'],
        visit_api=BANKS[CODE]['visit_api'],
        timeout=10000,
    )
    data = _parse_page(api_content)
    data = _convert_api_data(data)
    return data
