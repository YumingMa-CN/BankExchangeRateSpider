from utils.common import fetch_html
from config import BANKS
import re
import json
import time

__all__ = ['get_data']
CODE = 'cib'


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
    数据格式示例：
    {"page":"1","records":"13","total":"1","sidx":"","sort":"asc","rows":[{"cell":
        ["欧元","EUR","100.00","808.87","815.36","783.30","814.96"],"id":"0"},
        {"cell":["英镑","GBP","100.00","960.48","968.19","930.12","967.71"],"id":"1"},
    ]}
    """
    result = []
    rows = data["rows"]
    headers = ["币种名称", "币种代码", "基准金额", "现汇买入价", "现汇卖出价", "现钞买入价", "现钞卖出价"]
    for row in rows:
        cells = []
        for idx, v in enumerate(row["cell"]):
            if idx<=2:
                v = str(v).strip().rstrip('0').rstrip('.')
            else:
                try:
                    # 尝试将值转为 float 并保留四位小数
                    f = float(v)
                    v = f"{f:.4f}"
                except ValueError:
                    pass
            cells.append(v)
        d = dict(zip(headers, cells))
        result.append(d)
    return result


def _attach_metadata_to_table(table, update_time, **kwargs):
    """
    增加元数据（如采集时间/银行等）到所有行
    table: list[dict]
    time: 时间字符串
    kwargs: 预留，未来加其他元数据
    """
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for row in table:
        row['更新时间'] = update_time
        row['采集时间'] = collecting_time
        row['银行'] = BANKS[CODE]['name']
        for k, v in kwargs.items():
            row[k] = v
    return table


def _extract_time_from_html(html):
    """
    从html中提取时间字符串，返回类似 '2025-05-16 16:23:35'
    """
    # 匹配"日期： 2025年05月16日 星期五 16:23:35"
    m = re.search(r'日期：\s*(\d{4})年(\d{2})月(\d{2})日.*?(\d{1,2}):(\d{1,2}):(\d{1,2})', html)
    if not m:
        return ""
    # 提取年月日时分秒
    y, mo, d, h, mi, s = m.groups()
    date_str = f"{y}-{mo}-{d} {int(h):02d}:{int(mi):02d}:{int(s):02d}"
    return date_str


def get_data():
    """
    获取兴业银行的汇率数据
    :return : list[dict]，每个字典代表一行数据
    """
    timestamp = int(time.time() * 1000)  # 获取当前时间戳
    url_business = BANKS[CODE]['url_business']  # 兴业银行的汇率业务官网页面
    url_api = BANKS[CODE]['url_api'].format(timestamp=timestamp)  # 兴业银行的API数据链接
    visit_business = BANKS[CODE]['visit_business']  # 是否访问业务官网
    visit_api = BANKS[CODE]['visit_api']  # 是否访问API
    html, api_data = fetch_html(url_business, url_api, visit_business, visit_api, timeout=10000)  # 获取网页内容,api数据内容
    update_time = _extract_time_from_html(html)  # 提取时间字符串
    json_data = _parse_page(api_data)
    data_list_of_dict = _convert_api_data(json_data)
    pure_data = _attach_metadata_to_table(data_list_of_dict, update_time)
    return pure_data
