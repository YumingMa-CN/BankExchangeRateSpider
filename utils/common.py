import time

import requests
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


def fetch_html(url_html, url_api, timeout=10000):
    """
    用 playwright获取网页内容
    """
    sleep_time = 5
    browser = get_browser()
    context = browser.new_context()
    page = context.new_page()

    page.goto(url_html, timeout=timeout)
    time.sleep(sleep_time)
    html = page.content()
    # print(html)

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
