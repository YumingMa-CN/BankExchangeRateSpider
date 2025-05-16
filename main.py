from config import BANKS
from storage.save_csv import save_to_csv
import importlib


if __name__ == '__main__':
    for bank_code, settings in BANKS.items():
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
        except Exception as e:
            print(f"{settings['name']} 抓取/保存出错：{e}\n")
