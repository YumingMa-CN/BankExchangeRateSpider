import importlib
import time
from config import BANKS, SAVE_CSV, SAVE_DB, SAVE_API, API_PROVIDERS
from storage.save_csv import save_to_csv
from storage.save_db import save_to_db
from storage.save_api import save_to_api
from db.operations import save_exchange_rates
from utils.common import row_to_db

if __name__ == '__main__':
    if not SAVE_CSV and not SAVE_DB:
        print("未配置保存方式，请在 config.py 中设置 SAVE_CSV 或 SAVE_DB 为 True")
        exit(1)

    last_collect_time = {bank_code: 0.0 for bank_code in BANKS}
    while True:
        for bank_code, settings in BANKS.items():
            now = time.time()
            interval = settings.get('interval', 60)
            if now - last_collect_time[bank_code] < interval:
                print(f"距离上次采集时间不足 {interval} 秒，跳过 {settings['name']} ...")
                continue  # 未到采集间隔，跳过
            try:
                parse_module = importlib.import_module(f"parse.{bank_code}")
            except ModuleNotFoundError:
                print(f"未找到模块 parse.{bank_code}，跳过...")
                continue
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))} 采集 {settings['name']} ...")
            try:

                data = parse_module.get_data()
                if SAVE_CSV:
                    save_to_csv(data,
                                settings['output'].format(timestamp=time.strftime("%Y%m%d_%H%M%S", time.localtime(now))))
                    print("数据已保存到 {output}\n".format(
                      output=settings['output'].format(timestamp=time.strftime("%Y%m%d_%H%M%S", time.localtime(now)))))

                if SAVE_DB:
                    # 转换字段 保存到数据库
                    save_to_db(data, bank_code)
                    print("数据已写入数据库\n")
                    last_collect_time[bank_code] = now

                if SAVE_API:
                    for api_conf in API_PROVIDERS:
                        if not api_conf.get('enable', False):
                            continue  # 跳过未开启的API
                        try:
                            save_to_api(data, bank_code, api_conf)
                            print(f"数据已上传到 {api_conf['name']} 平台\n")
                        except Exception as api_err:
                            print(f"上传到 {api_conf['name']} 出错：{api_err}\n")


            except Exception as e:
                print(f"{settings['name']} 抓取/保存出错：{e}\n")
        time.sleep(10)  # 防止CPU占用过高
