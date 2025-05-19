from utils.common import fetch_html, scale_rate
from config import BANKS, abbr2cname, digit2abbr
import re
import time
import xml.etree.ElementTree as ET

__all__ = ['get_data']
CODE = 'ccb'


def _parse_page(html):
    """
        根据正则提取汇率数据
    """
    m = re.search(r'<div id="webkit-xml-viewer-source-xml">(.*?)</div>', html, re.DOTALL)
    # print(html)
    if not m:
        raise ValueError("预期结构未找到")
    return ET.fromstring(m.group(1).strip())


def _convert_api_data(root):
    """
    将解析后的XML Element对象转换为标准list[dict]格式
    需要依赖全局的 DIGIT_TO_ABBR 和 CURRENCY_CODE 字典
    """
    result = []
    collecting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    for settlement in root.findall('ReferencePriceSettlement'):
        digit_code = settlement.findtext("Ofrd_Ccy_CcyCd", "").strip()  # 数字代码，如840
        abbr = digit2abbr.get(digit_code, digit_code)  # 英文缩写
        cn_name = abbr2cname.get(abbr, abbr)  # 中文名
        rate_scale = 100
        item = {
            "币种名称": cn_name,
            "币种代码": abbr,
            "基准金额": 100,
            "现汇买入价": scale_rate(settlement.findtext("BidRateOfCcy", "").strip(), rate_scale),
            "现钞买入价": scale_rate(settlement.findtext("BidRateOfCash", "").strip(), rate_scale),
            "现汇卖出价": scale_rate(settlement.findtext("OfrRateOfCcy", "").strip(), rate_scale),
            "现钞卖出价": scale_rate(settlement.findtext("OfrRateOfCash", "").strip(), rate_scale),
            "中间价": scale_rate(settlement.findtext("Mdl_ExRt_Prc", "").strip(), rate_scale),
            "更新时间":
                '{} {}:{}:{}'.format(
                    settlement.findtext("LstPr_Dt", "")[:4] + '-' +
                    settlement.findtext("LstPr_Dt", "")[4:6] + '-' +
                    settlement.findtext("LstPr_Dt", "")[6:],
                    settlement.findtext("LstPr_Tm", "")[:2],
                    settlement.findtext("LstPr_Tm", "")[2:4],
                    settlement.findtext("LstPr_Tm", "")[4:6],
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
