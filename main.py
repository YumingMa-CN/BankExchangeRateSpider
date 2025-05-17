import importlib
import time
from config import BANKS
from storage.save_csv import save_to_csv


if __name__ == '__main__':
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
            print(f"采集{settings['name']} ...")
            try:
                data = parse_module.get_data()
                save_to_csv(data, settings['output'])
                print(f"数据已保存到 {settings['output']}\n")
                last_collect_time[bank_code] = now
            except Exception as e:
                print(f"{settings['name']} 抓取/保存出错：{e}\n")
        time.sleep(10)  # 防止CPU占用过高
