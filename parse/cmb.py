from utils.common import fetch_html
from config import BANKS
import re
import json
import time


__all__ = ['get_data']

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
    #  {"returnCode": "SUC0000", "errorMsg": null, "body": [
    #     #     {"ccyNbr": "港币", "ccyNbrEng": "港币 HKD", "rtbBid": "92.39", "rthOfr": "92.57", "rtcOfr": "92.57",
    #     #      "rthBid": "92.21", "rtcBid": "92.21", "ratTim": "20:51:57", "ratDat": "2025年05月17日", "ccyExc": "10"},
    #     #     {"ccyNbr": "新西兰元", "ccyNbrEng": "新西兰元 NZD", "rtbBid": "424.68", "rthOfr": "426.38", "rtcOfr": "426.38",
    #     #      "rthBid": "422.98", "rtcBid": "422.98", "ratTim": "20:51:57", "ratDat": "2025年05月17日", "ccyExc": "10"},
    #     #     ]}
    result = []
    rows = data["body"]
    # headers = ["币种名称", "币种代码", "基准金额", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "更新时间", "采集时间", "银行"]
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for row in rows:
        item = {
            "币种名称": row.get("ccyNbr", ""),
            "币种代码": row.get("ccyNbrEng", "").split(" ")[-1],
            "基准金额": 100,
            "现汇买入价": row.get("rthBid", ""),
            "现钞买入价": row.get("rtcBid", ""),
            "现汇卖出价": row.get("rthOfr", row.get("rtcOfr", "")),  # 若无rtbOfr则用rthOfr
            "现钞卖出价": row.get("rtcOfr", row.get("rthOfr")),
            "更新时间": row.get("ratDat", "").replace("年", "-").replace("月", "-").replace("日", " ") + row.get("ratTim", ""),
            "采集时间": collecting_time,
            "银行": "招商银行"
        }
        result.append(item)
    return result

def get_data():
    """
    获取数据
    """
    _, api_content = fetch_html(
        url_business=BANKS['cmb']['url_business'],
        url_api=BANKS['cmb']['url_api'],
        visit_business=BANKS['cmb']['visit_business'],
        visit_api=BANKS['cmb']['visit_api'],
        timeout=10000,
    )
    data = _parse_page(api_content)
    data = _convert_api_data(data)
    return data
