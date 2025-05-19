from utils.common import fetch_html, scale_rate
from config import BANKS
import re
import time

__all__ = ['get_data']
CODE = 'bocom'


def _parse_page(html):
    """
    解析银行汇率页面的html内容，提取原始表格数据列表（未格式化，字段参考API）
    """
    # 提取所有<tr class="data">...</tr>
    row_pattern = re.compile(r'<tr class="data">(.*?)</tr>', re.S)
    td_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.S)
    rows = []
    for row_html in row_pattern.findall(html):
        tds = [re.sub(r'<.*?>', '', x).replace('&nbsp;', '').strip() for x in td_pattern.findall(row_html)]
        if len(tds) < 6:
            continue  # 跳过不完整行
        # 对应列: ["币种名称", "单位", "现汇买入价", "现汇卖出价", "现钞买入价", "现钞卖出价"]
        # 和API结构对齐 ["cur"(代码), "fe_buy_prc", "fe_sell_prc", "fc_buy_prc", "fc_sell_prc"]
        # 名称格式：阿联酋迪拉姆(AED/CNY)
        # 代码为括号里的3字母
        code_match = re.search(r'\((\w+)/CNY\)', tds[0])
        cur = code_match.group(1) if code_match else tds[0]
        rows.append({
            "cur": cur,
            "cname": tds[0].split('(')[0] if '(' in tds[0] else tds[0],
            "unit": tds[1],
            "fe_buy_prc": tds[2] if tds[2] != '-' else "",
            "fe_sell_prc": tds[3] if tds[3] != '-' else "",
            "fc_buy_prc": tds[4] if tds[4] != '-' else "",
            "fc_sell_prc": tds[5] if tds[5] != '-' else "",
        })

    if not rows:
        raise ValueError("预期结构未找到")

    # 提取更新时间
    m = re.search(r'更新时间[:：]\s*([0-9\- :]{10,20})', html)
    update_time = m.group(1).strip() if m else ""

    return {
        "rows": rows,
        "update_time": update_time
    }


def _convert_html_data(parsed):
    """
    输入_parse_html_table的结果数据，输出和API格式一致的标准化字典列表
    """
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result = []
    update_time = parsed.get("update_time", "")
    for row in parsed["rows"]:
        # 判断单位，如果不是100，需要做换算（如IDR，JPY，KRW）
        try:
            unit = int(row["unit"].replace(",", ""))
        except Exception:
            unit = 100  # fallback

        rate_scale = 100 / unit if unit != 100 else 1
        item = {
            "币种名称": row.get("cname", ''),
            "币种代码": row.get("cur", ''),
            "基准金额": 100,
            "现汇买入价": scale_rate(row.get("fe_buy_prc", ''), rate_scale, '-'),
            "现钞买入价": scale_rate(row.get("fc_buy_prc", ''), rate_scale, '-'),
            "现汇卖出价": scale_rate(row.get("fe_sell_prc", ''), rate_scale, '-'),
            "现钞卖出价": scale_rate(row.get("fc_sell_prc", ''), rate_scale, '-'),
            "更新时间": update_time,
            "采集时间": collecting_time,
            "银行": BANKS[CODE]['name'],
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
    print('parse page success')
    data = _convert_html_data(data)
    return data

