# BankExchangeRateSpider

一个多银行外汇牌价自动采集爬虫。
 以“兴业银行（cib）”为Demo，支持方便扩展其它银行，输出为CSV文件，便于数据分析或后续处理。

## 项目结构

 BankExchangeRateSpider

├─ config.py

├─ main.py

├─ README.md

├─ requirements.txt

│

├─data

│      cib_fx.csv

│

├─parse

│  ├─  cib.py

│  └─  \_\_init\_\_.py

├─storage

│  ├─  save_csv.py

│  └─  \_\_init\_\_.py

│ 

│

└─utils

​     ├─ common.py

​     └─ \_\_init\_\_.py

## 快速开始

### 一、克隆仓库

```bash
git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git 
cd BankExchangeRateSpider
```

### 二、依赖包下载

```bash
pip install -r requirements.txt
```

### 三、运行采集

```bash
python main.py
```

运行后会抓取最新汇率数据，并保存到 `data/cib_fx.csv`

## 如何扩展新银行

1. 在 [config.py](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/config.py) 中添加新的银行配置（含模块名、url等）。
2. 在 [parse/](https://github.com/YumingMa-CN/BankExchangeRateSpider/tree/main/parse) 目录下新建银行同名 py 文件，实现标准 `get_data()` 函数对外提供数据。
3. 主程序会自动遍历采集，无需手动修改 [main.py](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/main.py)。

## 其它说明

- 输出数据仅供学习研究，切勿用于商业或违法用途。