from utils.common import fetch_html
from config import BANKS, abbr2cname
import re
import json
import time

__all__ = ['get_data']
CODE = 'psbc'


def _parse_page(html):
    """
        根据正则提取汇率数据
    """
    m = re.search(r'<body>empty\((.*?)\)</body>', html, re.S)
    # print(html)
    if not m:
        raise ValueError("预期结构未找到")
    return json.loads(m.group(1))


def _convert_api_data(data):
    """
    将数据转换为字典列表
    """
    # a sample of data is:
    # empty({"curpage":1,"globalBusiTrackNo":"12997104111932587","pageCount":1,"pageSize":10,"reqSysSriNo":"12997104113798036","requestUrl":"cache","resultList":[
    #     {"fe_sell_prc":"723.1000","effect_date":"20250519","cur":"USD","flag":"2","fc_sell_prc":"","mid_prc":"723.1000","fe_buy_prc":"720.2500","sort":"1","effect_time":"124038","fc_buy_prc":"714.9500"},
    #     {"fe_sell_prc":"809.7300","effect_date":"20250519","cur":"EUR","flag":"2","fc_sell_prc":"","mid_prc":"809.7300","fe_buy_prc":"804.0100","sort":"2","effect_time":"124038","fc_buy_prc":"782.1400"},
    #     {"reqSysSriNo":"12997104113798036","globalBusiTrackNo":"12997104111932587"}
    # ], "retCode":"000","retCodeEnum":"RET_CODE_ENUM_000","retMsg":"访问成功","totalCount":0})

    result = []
    rows = data["resultList"]
    # headers = ["币种名称", "币种代码", "基准金额", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "更新时间", "采集时间", "银行"]
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for row in rows[:-1]:
        item = {
            "币种名称": abbr2cname.get(row.get("cur", ""),
                ""),
            "币种代码": row.get("cur", ""),
            "基准金额": 100,
            "现汇买入价": row.get("fe_buy_prc", ""),
            "现钞买入价": row.get("fc_buy_prc", ""),
            "现汇卖出价": row.get("fe_sell_prc", row.get("fc_sell_prc", "")),
            "现钞卖出价": row.get("fe_sell_prc", row.get("fc_sell_prc", "")),
            "中间价": row.get("mid_prc", ""),
            # 日期每隔两个字符加一个 -
            "更新时间":
                '-'.join(
                    [row.get("effect_date", "")[i:i + 2] for i in range(0, len(row.get("effect_date", "")), 2)]
                ) + \
                " " + \
                ':'.join(
                    [row.get("effect_time", "")[i:i + 2] for i in range(0, len(row.get("effect_time", "")), 2)]
                ),
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
