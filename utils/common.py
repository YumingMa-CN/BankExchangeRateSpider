import time
from playwright.sync_api import sync_playwright


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
               ):
    """
    用 playwright 获取网页内容。

    参数说明：
        url_business (str): 业务官网的网址
        url_api (str): API 的网址
        timeout (int): 页面加载超时时间（毫秒）
        visit_business (bool): 是否在访问 api_url 前先访问 business_url,可用于获取api_url里没有的数据，亦可获取 cookies
        visit_api (bool): 是否需要访问 api_url （有的业务没有 API）
    """
    if not url_business and not url_api:
        raise ValueError("至少提供一个URL")
    if not visit_business and not visit_api:
        raise ValueError("至少访问一个URL")
    html = ""
    api_content = ""

    sleep_time = 5
    browser = get_browser()
    context = browser.new_context()
    page = context.new_page()
    if url_business and visit_business:
        page.goto(url_business, timeout=timeout)
        time.sleep(sleep_time)
        html = page.content()
        # print(html)
    if url_api and visit_api:
        page.goto(url_api, timeout=timeout)
        time.sleep(sleep_time)
        api_content = page.content()
    page.close()
    context.close()
    return html, api_content


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