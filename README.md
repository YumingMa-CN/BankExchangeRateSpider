# BankExchangeRateSpider

## 介绍

**BankExchangeRateSpider** 是一个支持多家主流银行外汇牌价自动采集、可实时保存到本地与数据库的开源爬虫工具。

- 已支持包括中国银行、农业银行、兴业银行、招商银行等**8家主流银行**。
- 框架可轻松扩展新银行，所有数据自动标准化，支持 CSV 导出与数据库导入。
- 适用于金融数据分析、外汇走势监控、可视化研究、业务接入等多种场景。

------

## 项目结构

```
BankExchangeRateSpider/
│
├── config.py                  # 全局配置（数据库、银行列表、字段映射等）
├── main.py                    # 主入口
├── README.md
├── requirements.txt
│
├── data/                      # 采集到的数据（CSV等）
├── db/                        # 数据库连接、模型与操作
│   ├── connection.py
│   ├── models.py
│   ├── operations.py
│   └── __init__.py
├── parse/                     # 各银行对应解析脚本
│   ├── boc.py                 # 中国银行
│   ├── abc.py                 # 农业银行
│   ├── ccb.py                 # 建设银行
│   ├── icbc.py                # 工商银行
│   ├── cmb.py                 # 招商银行
│   └── __init__.py
├── scripts/
│   ├── init_db.py             # 初始化数据库表结构
│   └── mysql.sql              # 可选，手动建库用SQL
├── storage/                   # 数据文件本地保存功能（CSV等）
│   ├── save_csv.py
│   └── __init__.py
└── utils/                     # 公共方法
    ├── common.py
    └── __init__.py
```

------

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git 
cd BankExchangeRateSpider
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
playwright install
```

### 3. 配置数据库

编辑 `config.py`，根据你的 MySQL 服务器设置好数据库连接 URI。例如：

```python
DB_URI = "mysql+pymysql://username:password@localhost:3306/database_name?charset=utf8"
```

- **请确保 username、password、database_name 填写正确，且此数据库已提前创建好。**

### 4. 字段映射维护（如无需扩展银行，则跳过本步骤）

config.py 需维护各银行字段与标准数据库字段的映射。

- **外层键**（如 `'boc'`, `'abc'` 等）：代表银行的缩写或**唯一代码**（必须和 parse 目录下采集脚本文件名一致）。
- **内层键**：统一标准中的**字段英文名**，也是**数据库表字段名**。
- **内层值**：该银行 `get_data()` 返回的数据字典（以及标准 CSV 文件）中的字段名，通常为统一设定的中文字段名，而**非原始网页表头名称**。所有银行应遵循相同的字段规范。如果该银行无此数据项，请填写 `None`。

例如：

```python
FIELD_MAP = {
    # 中国银行 Bank Of China (boc)
    'boc': {
        "currency_name": "币种名称",
        "currency_code": "币种代码",
        "base_amount": "基准金额",
        "refer_price": "参考价",      # 部分数据有参考价
        "remit_buy": "现汇买入价",
        "cash_buy": "现钞买入价",
        "remit_sell": "现汇卖出价",
        "cash_sell": "现钞卖出价",
        "convert_price": "中行折算价",  # 特有
        "mid_price": None,             # 无则置None
        "update_time": "更新时间",
        "crawl_time": "采集时间",
        "bank": "银行"
    },
    # 其他银行配置同理（详见 config.py 示例）
}
```

- 新增银行时，**务必参照已有格式补充对应字段**。
- 字段名如有变更，也在这里统一修改即可。

### 5. 初始化数据库表结构（首次部署或表结构变更后执行）

第一次运行或数据库表结构有调整时，需**初始化建表**：

```bash
# 必须在项目根目录下运行！
python -m scripts.init_db
```

- 此操作只需执行一次（或数据库结构有更动时）。

### 6. 启动采集主程序

```bash
python main.py
```

- 程序自动获取和保存全部配置好的银行数据。
- 结果会写入 `data/` 目录下的对应 csv 文件。
- 同时批量导入到数据库 `exchange_rate` 表中。

------

## 如何扩展新银行

只需两步，无需改主程序！

1. **在 config.py 的 BANKS、FIELD_MAP 中补充新银行配置**（模块名、采集url、输出文件名、字段映射等）。
2. 在 `parse/` 目录下新增同名的 Python 文件（例如 `parse/minsheng.py`），实现标准 `get_data()` 接口。
   - 返回字段须覆盖 FIELD_MAP 所列的标准项，未覆盖也可为 None。

------

## 常见问题

- **数据库连接失败/无表：**
  - 确认 config.py 的 DB_URI 配置信息准确
  - 确认已通过 `python -m scripts.init_db` 初始化表结构
- **模块找不到 db/connection：**
  - 请务必在项目根目录下，用 `python -m script.init_db`，不要直接 `python script/init_db.py`
- **扩展或更改银行字段:**
  - 配置 ```BANKS``` 在 config.py 维护，参照现有模板即可。

------

## 免责声明 

本项目所有源代码及相关内容仅用于个人学习、学术研究与技术交流。请勿用于任何违反中华人民共和国及/或您所在国家和地区法律法规的用途。 

1. **禁止高频、大规模、恶意采集行为**：请合理设置请求频率，尊重目标网站的 robots 协议和使用条款，严禁利用本项目进行影响目标网站正常运营、高并发访问等行为。 
2. **商业用途须获授权**：如需将本项目用于商业目的，请事先获得目标网站或数据版权所有者的明确授权。 
3. **后果自负**：因使用本项目代码或其衍生作品导致的任何数据滥用、网站被封禁、法律纠纷、经济损失等后果，均由使用者本人承担，与本项目作者及贡献者无关。
4. **仅供合法合规目的**：使用者需确保采集和使用的数据不侵犯第三方合法权益，并严格遵守相关法律法规。 

**如您不同意以上条款，请勿使用或传播本项目。** 

------

## Disclaimer 

This project and all related source code are intended **solely for personal study, academic research, and technical exchange**. Do not use this project for any activities that violate the laws and regulations of the People's Republic of China and/or your local jurisdiction.

1. **Prohibited High-Frequency or Malicious Crawling**: Please set a reasonable request rate, respect robots.txt and the terms of use of the target website. Using this project for high-frequency, large-scale, or disruptive activities is strictly forbidden. 
2. **Commercial Use Requires Permission**: You must obtain explicit permission from the target website or data owner before any commercial use of this project.
3. **Use at Your Own Risk**: The author(s) shall not be held responsible for any misuse of this project, including but not limited to data abuse, account or IP bans, legal disputes, or economic losses. All consequences are borne solely by the user.
4. **Only for Legal and Compliant Purposes**: Users must ensure that the data collection and usage do not infringe on the rights of third parties and must comply with all applicable laws and regulations. 

**If you do not agree with these terms, do not use or distribute this project.** 

------

## LICENSE

本项目开源协议遵循 MIT，详情见 [LICENSE](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/LICENSE) 文件。

------

## 联系&贡献

欢迎提交 issues/PR，或联系作者 [@YumingMa-CN](https://github.com/YumingMa-CN) 交流合作！

------

**祝您用得开心！有疑问欢迎随时发 issue 或邮件反馈。**