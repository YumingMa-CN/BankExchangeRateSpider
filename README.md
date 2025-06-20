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

### 方案一：**使用 Docker 一键部署（推荐）**

1. **克隆仓库**

   ```bash
   git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git 
   cd BankExchangeRateSpider
   ```

2. **复制并配置环境变量文件**

   ```bash
   cp .env.example .env
   ```

   - **按需编辑** `.env` 文件，填写你的**数据库**等配置信息。

     

3. **构建容器镜像**

   ```bash
   docker-compose build
   ```

4. **启动所有服务**

   ```bash
   docker-compose up
   ```

   - **数据库将在主机的 3307 端口暴露**（默认，可在 [docker-compose.yml](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/docker-compose.yml) 处按需更改），你可以通过 `localhost:3307` 访问数据库（账号密码以 `.env` 为准）。
   - 关闭服务请用 `Ctrl+C`，如需后台运行加 `-d` 参数。

### 方案二：手动方式（无 Docker 环境时）

1. **克隆仓库**

   ``` bash
   git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git 
   cd BankExchangeRateSpider
   ```

2. **安装依赖**

   ``` bash
   pip install -r requirements.txt
   playwright install
   ```

3. **配置数据库**

   编辑 `config.py`，按照你的 MySQL 服务器设置好数据库连接 URI，例如：

   ```python
   DB_URI = "mysql+pymysql://username:password@localhost:3306/database_name?charset=utf8"
   ```

   > 请确保 `username`、`password`、`database_name` 填写正确、数据库预先创建。

4. **（开发或拓展时需）维护字段映射**

   不增加新银行可跳过。详见 [扩展与维护银行字段映射](#扩展与维护银行字段映射).

5. **初始化数据库表结构**

   第一次运行或数据库表结构有调整时，需**初始化建表**：

   ```bash
   # 必须在项目根目录下运行！
   python -m scripts.init_db
   ```

6. **启动采集主程序**

   ```bash
   python main.py
   ```

   - 程序自动获取和保存全部配置好的银行数据。

   - 结果会写入 `data/` 目录下的对应 csv 文件。

   - 同时批量导入到数据库 `exchange_rate` 表中。

---

## 扩展与维护银行字段映射

要支持更多银行或调整字段，请只需在 **两处文件**更新即可，无需修改主程序：

1. **[config.py](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/config.py) 维护银行配置及字段映射**

   - 在 `BANKS` 中加入新银行的模块名、URL、输出配置等条目。

     - 例如：

       ```python
       BANKS = {
           'cib': {
               'code': 'cib',
               'name': '兴业银行',
               'url_business': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do',
               'url_api': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd'
                          '={timestamp}&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sort=asc',
               'output': 'data/cib_fx_{timestamp}.csv',  # 输出文件名，{timestamp} 会被替换为当前时间戳
               'visit_business': True,     # 是否访问业务页面，可以获取 api_url 中不包含的数据，并且可以通过访问以携带正常 cookies 等。
               'visit_api': True,
               'interval': 60, # 建议采集间隔时间（秒）
           },  
           # 其他银行
       }
       ```

   - 在 `FIELD_MAP` 中新增该银行的字段映射

     - **外层键**（如 `'boc'`, `'abc'` 等）：代表银行的缩写或**唯一代码**（必须和 parse 目录下采集脚本文件名一致）。

     - **内层键**：统一标准中的**字段英文名**，也是**数据库表字段名**。

     - **内层值**：该银行 `get_data()` 返回的数据字典（以及标准 CSV 文件）中的字段名，通常为统一设定的中文字段名，而**非原始网页表头名称**。所有银行应遵循相同的字段规范。如果该银行无此数据项，请填写 `None`。

     - 例如：

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


2. **`parse/` 目录下编写新银行脚本**

   - 以新银行缩写为文件名（如民生银行： `parse/cmbc.py`），实现标准 `get_data()` 接口，返回字段需与 `FIELD_MAP` 标准项对应，缺失可用 `None`。

   - 脚本与数据解析逻辑完全解耦，便于维护和后续拓展。

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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=YumingMa-CN/BankExchangeRateSpider&type=Date)](https://www.star-history.com/#YumingMa-CN/BankExchangeRateSpider&Date)

---

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