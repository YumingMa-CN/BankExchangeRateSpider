import time
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright
from datetime import datetime
from config import FIELD_MAP, TIMEZONE



# 全局变量
_browser = None
_playwright = None


def get_browser():
    global _browser, _playwright
    if _browser is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
    return _browser


def fetch_html(url_business,
               url_api,
               visit_business=True,
               visit_api=True,
               timeout=10000,
               max_try=2
               ):
    """
    用 playwright 获取网页内容。

    参数说明：
        url_business (str): 业务官网的网址
        url_api (str): API 的网址
        visit_business (bool): 是否在访问 api_url 前先访问 business_url,可用于获取api_url里没有的数据，亦可获取 cookies
        visit_api (bool): 是否需要访问 api_url （有的业务没有 API）
        timeout (int): 页面加载超时时间（毫秒）
        max_try(int) #本 地操作最多尝试次数
    """
    if not url_business and not url_api:
        raise ValueError("至少提供一个URL")
    if not visit_business and not visit_api:
        raise ValueError("至少访问一个URL")
    html = ""
    api_content = ""

    sleep_time = 5
    attempt = 0
    restart_browser_limit = 2 # 尝试 2 次后还失败就重启browser


    while attempt < max_try + restart_browser_limit:
        try:
            browser = get_browser()
            context = browser.new_context()
            page = context.new_page()
            html, api_content = "", ""
            if url_business and visit_business:
                page.goto(url_business, timeout=timeout)
                time.sleep(sleep_time)
                html = page.content()
            if url_api and visit_api:
                page.goto(url_api, timeout=timeout)
                time.sleep(sleep_time)
                api_content = page.content()
            page.close()
            context.close()
            return html, api_content

        except Exception as e:
            attempt += 1
            msg = str(e)
            print(f"[尝试第{attempt}次出现异常] {msg}")
            # 只有在触发相关关闭或"browser"关键字相关报错时才考虑重启
            if (
                "closed" in msg.lower()
                or "browser has been closed" in msg.lower()
                or "target page, context or browser has been closed" in msg.lower()
            ):
                if attempt >= max_try:
                    print("[重启browser] 多次失败后重启Playwright，继续重试……")
                    shutdown_playwright()
                else:
                    time.sleep(1)
            else:
                # 其它异常直接抛出，不盲目重启
                raise

    # 所有自动重启都没救活，直接报错
    raise RuntimeError("网页采集失败：多次尝试和浏览器重启后仍然失败。")


def shutdown_playwright():
    global _browser, _playwright
    if _browser:
        _browser.close()
        _browser = None
        print("Browser closed.")
    else:
        print("Browser is already closed.")

    if _playwright:
        _playwright.stop()
        _playwright = None
        print("Playwright stopped.")
    else:
        print("Playwright is already stopped.")

def safe_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def scale_rate(x, rate_scale=1, filling_data=''): # 处理汇率数据
    try:
        v = float(x) * rate_scale
        s = "{:.4f}".format(v).rstrip('.')
        return s

    except Exception:
        return filling_data


def row_to_db(row: dict, bank_code: str) -> dict:
    fmap = FIELD_MAP[bank_code]

    def safe_float(s):
        try:
            return float(s) if s not in ('-', '', None) else None
        except Exception:
            return None

    def time_parse(s, default=None):
        try:
            if not s: return default
            return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return default

    return {
        "currency_name": row.get(fmap['currency_name']),
        "currency_code": row.get(fmap['currency_code']),
        "base_amount": safe_float(row.get(fmap['base_amount'])),
        "remit_buy": safe_float(row.get(fmap['remit_buy'])),
        "cash_buy": safe_float(row.get(fmap['cash_buy'])),
        "remit_sell": safe_float(row.get(fmap['remit_sell'])),
        "cash_sell": safe_float(row.get(fmap['cash_sell'])),
        "convert_price": safe_float(row.get(fmap.get('convert_price'))),
        "mid_price": safe_float(row.get(fmap.get('mid_price'))) if fmap.get('mid_price') else None,
        "refer_price": safe_float(row.get(fmap.get('refer_price'))) if fmap.get('refer_price') else None,
        "update_time": time_parse(row.get(fmap['update_time'])),
        "crawl_time": time_parse(row.get(fmap['crawl_time'])),
        "bank": row.get(fmap['bank']),
        "ext_json": None, # remaining fields are not used in this version
    }
  
  
def get_now_in_timezone(timezone: str = None, fmt: str = "%Y-%m-%d %H:%M:%S"):
    """
    返回指定时区的当前时间字符串，默认为config的TIMEZONE，支持自定义fmt
    """
    tz = timezone or TIMEZONE  # 如未指定，取config默认
    return datetime.now(ZoneInfo(tz)).strftime(fmt)
