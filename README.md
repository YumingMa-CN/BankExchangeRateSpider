# BankExchangeRateSpider

## 介绍

BankExchangeRateSpider 是一个支持多家主流银行外汇牌价自动采集的开源爬虫工具。

本项目已实现对包括**兴业银行、招商银行**等8家主要银行的汇率数据抓取，便于批量获取、对比和分析各大银行的外汇牌价。

- 以“兴业银行（CIB）”为演示模板，框架设计灵活，便于扩展至其他银行。
- 采集结果可一键输出为标准CSV文件，方便后续数据分析和自动化处理。
- 适用于金融数据分析、外汇研究、业务对接等多种场景。

欢迎数据分析、量化交易、财务管理等领域的开发者参与使用或贡献扩展！

## 项目结构

```
BankExchangeRateSpider 
 ├─ config.py 
 ├─ main.py 
 ├─ README.md 
 ├─ requirements.txt 
 │ 
 ├─ data 
 │   └─ cib_fx.csv 
 │ 
 ├─ parse 
 │   ├─ cib.py 
 │   └─ __init__.py 
 │ 
 ├─ storage 
 │   ├─ save_csv.py 
 │   └─ __init__.py 
 │ 
 └─ utils 
     ├─ common.py 
     └─ __init__.py 
```

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

运行后会抓取最新汇率数据，并保存到 `data/{bank_code}.csv`

## 如何扩展新银行

1. 在 [config.py](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/config.py) 中添加新的银行配置（含模块名、url等）。
2. 在 [parse/](https://github.com/YumingMa-CN/BankExchangeRateSpider/tree/main/parse) 目录下新建银行同名 py 文件，实现标准 `get_data()` 函数对外提供数据。
3. 主程序会自动遍历采集，无需手动修改 [main.py](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/main.py)。

---

## 免责声明

本项目所有源代码及相关内容仅用于个人学习、学术研究与技术交流。请勿用于任何违反中华人民共和国及/或您所在国家和地区法律法规的用途。

1. **禁止高频、大规模、恶意采集行为**：请合理设置请求频率，尊重目标网站的 robots 协议和使用条款，严禁利用本项目进行影响目标网站正常运营、高并发访问等行为。
2. **商业用途须获授权**：如需将本项目用于商业目的，请事先获得目标网站或数据版权所有者的明确授权。
3. **后果自负**：因使用本项目代码或其衍生作品导致的任何数据滥用、网站被封禁、法律纠纷、经济损失等后果，均由使用者本人承担，与本项目作者及贡献者无关。
4. **仅供合法合规目的**：使用者需确保采集和使用的数据不侵犯第三方合法权益，并严格遵守相关法律法规。

如您不同意以上条款，请勿使用或传播本项目。

------

## Disclaimer

This project and all related source code are intended **solely for personal study, academic research, and technical exchange**. Do not use this project for any activities that violate the laws and regulations of the People's Republic of China and/or your local jurisdiction.

1. **Prohibited High-Frequency or Malicious Crawling**: Please set a reasonable request rate, respect robots.txt and the terms of use of the target website. Using this project for high-frequency, large-scale, or disruptive activities is strictly forbidden.
2. **Commercial Use Requires Permission**: You must obtain explicit permission from the target website or data owner before any commercial use of this project.
3. **Use at Your Own Risk**: The author(s) shall not be held responsible for any misuse of this project, including but not limited to data abuse, account or IP bans, legal disputes, or economic losses. All consequences are borne solely by the user.
4. **Only for Legal and Compliant Purposes**: Users must ensure that the data collection and usage do not infringe on the rights of third parties and must comply with all applicable laws and regulations.

**If you do not agree with these terms, do not use or distribute this project.**

------