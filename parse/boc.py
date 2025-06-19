from utils.common import fetch_html, scale_rate, get_now_in_timezone
from config import BANKS, cname2abbr
import re
import time


__all__ = ['get_data']
CODE = 'boc'

def _parse_page(html):
    """
    从唯一的含“货币名称”表头的<table>精确提取行数据
    """
    # 匹配目标table
    # print(html)
    table_pattern = re.compile(
        r'<table[^>]*>(?:(?!<table).)*?<th>货币名称</th>(?:.|\n)*?</table>',
        re.S
    )
    table_match = table_pattern.search(html)
    if not table_match:
        raise ValueError("预期结构未找到")
    table_html = table_match.group(0)
    # 只处理该table下的每个<tr>
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.S)
    td_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.S)
    rows = []
    for row_html in row_pattern.findall(table_html):
        tds = [re.sub(r'<.*?>', '', x).replace('&nbsp;', '').strip() for x in td_pattern.findall(row_html)]
        # 跳过表头
        if len(tds) == 0 or tds[0] in ['货币名称', ''] or len(tds) < 8:
            continue
        rows.append({
            "cname": tds[0],
            "fe_buy_prc": tds[1] if tds[1] else "",
            "fc_buy_prc": tds[2] if tds[2] else "",
            "fe_sell_prc": tds[3] if tds[3] else "",
            "fc_sell_prc": tds[4] if tds[4] else "",
            "mid_prc": tds[5] if tds[5] else "",
            "pub_date": tds[6],
            "pub_time": tds[7],
        })
    if not rows:
        raise ValueError("预期结构未找到")
    return rows


def _convert_html_data(rows):
    """
    输入_parse_page的结果rows，输出和API格式一致的标准化字典列表
    """
    collecting_time = get_now_in_timezone()
    result = []
    for row in rows:
        cname = row["cname"]
        code = cname2abbr.get(cname, "")
        # 更新时间合并
        update_time = row.get("pub_date", "") + " " + row.get("pub_time", "")
        item = {
            "币种名称": cname,
            "币种代码": code,
            "基准金额": 100,
            "现汇买入价": scale_rate(row.get("fe_buy_prc", ""), filling_data='-'),
            "现钞买入价": scale_rate(row.get("fc_buy_prc", ""), filling_data='-'),
            "现汇卖出价": scale_rate(row.get("fe_sell_prc", ""), filling_data='-'),
            "现钞卖出价": scale_rate(row.get("fc_sell_prc", ""), filling_data='-'),
            "中行折算价": scale_rate(row.get("mid_prc", ""), filling_data='-'),
            "更新时间": update_time.strip(),
            "采集时间": collecting_time,
            "银行": BANKS[CODE]['name'],     # CODE由你的业务指定，也可直接写中文字符串
        }
        result.append(item)
    return result

def get_data():
    """
    获取数据
    """
    html, _ = fetch_html(
        url_business=BANKS[CODE]['url_business'],
        url_api=BANKS[CODE]['url_api'],
        visit_business=BANKS[CODE]['visit_business'],
        visit_api=BANKS[CODE]['visit_api'],
        timeout=10000,
    )
    data = _parse_page(html)
    data = _convert_html_data(data)
    return data
