from utils.common import fetch_html, scale_rate, get_now_in_timezone
from config import BANKS
import re
import json
import time


__all__ = ['get_data']
CODE = 'abc'

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
    # {"ErrorCode": "0", "ErrorMsg": "", "Data": {"Table": [
    #     {"BenchMarkPrice": "959.43000000", "BuyingPrice": "956.07200000", "CurrName": "英镑(GBP)", "CurrId": "12",
    #      "SellPrice": "962.78800000", "PublishTime": "2025-05-19T11:14:41+08:00", "Id": "999999999999999999",
    #      "CashBuyingPrice": "956.07200000"},
    #     {"BenchMarkPrice": "92.25700000", "BuyingPrice": "92.07200000", "CurrName": "港元(HKD)", "CurrId": "13",
    #      "SellPrice": "92.44100000", "PublishTime": "2025-05-19T11:14:41+08:00", "Id": "999999999999999999",
    #      "CashBuyingPrice": "92.07200000"}
    #   ],"Table1":null,"Table2":null,"Table3":null}}
    result = []
    rows = data["Data"]["Table"]
    # headers = ["币种名称", "币种代码", "基准金额", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "更新时间", "采集时间", "银行"]
    collecting_time = get_now_in_timezone()
    for row in rows:
        item = {
            "币种名称": row.get("CurrName", "").split("(")[0].strip(),
            "币种代码": row.get("CurrName", "").split("(")[-1].replace(")", "").strip(),
            "基准金额": 100,
            "参考价": scale_rate(row.get("BenchMarkPrice", ""), filling_data='-'),
            "现汇买入价": scale_rate(row.get("BuyingPrice", "") ,filling_data='-'),
            "现钞买入价": scale_rate(row.get("CashBuyingPrice", ""),  filling_data='-'),
            "现汇卖出价": scale_rate(row.get("SellPrice", row.get("cashSell", "")),  filling_data='-'),
            "现钞卖出价": scale_rate(row.get("SellPrice", row.get("foreignSell")),  filling_data='-'),
            "更新时间": row.get("PublishTime", "").replace("T", " ").replace("+08:00", ""),
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
