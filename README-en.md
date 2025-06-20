# BankExchangeRateSpider
<p align="center">   <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">&nbsp;&nbsp;   <a href="README.md">     <img src="https://img.shields.io/badge/切换语言-中文-blue" alt="Switch Language">   </a> </p>

## Introduction

**BankExchangeRateSpider** is an open-source web scraping tool that automates the collection of foreign exchange rates from major banks, supporting real-time saving to local files and databases.

- **Supports 8 major banks**, including Bank of China, Agricultural Bank of China, China Industrial Bank, and China Merchants Bank.
- The framework is easily extendable to include new banks. All data is automatically standardized, supporting exports to CSV and imports into a database.
- Suitable for various scenarios such as financial data analysis, foreign exchange trend monitoring, visualization research, and business integration.

------

## Project Structure

```
BankExchangeRateSpider/
│
├── config.py                # Global configuration (database, bank list, field mappings, etc.)
├── main.py                  # Main entry point
├── README.md
├── requirements.txt
│
├── data/                    # Collected data (CSV, etc.)
├── db/                      # Database connection, models, and operations
│   ├── connection.py
│   ├── models.py
│   ├── operations.py
│   └── __init__.py
├── parse/                   # Parsing scripts for each bank
│   ├── boc.py               # Bank of China
│   ├── abc.py               # Agricultural Bank of China
│   ├── ccb.py               # China Construction Bank
│   ├── icbc.py              # Industrial and Commercial Bank of China
│   ├── cmb.py               # China Merchants Bank
│   └── __init__.py
├── scripts/
│   ├── init_db.py           # Initializes the database table structure
│   └── mysql.sql            # Optional SQL script for manual database creation
├── storage/                 # Functionality for saving data locally (CSV, etc.)
│   ├── save_csv.py
│   └── __init__.py
└── utils/                   # Common utility functions
    ├── common.py
    └── __init__.py
```

------

## Quick Start

### Option 1: **One-Click Deployment with Docker (Recommended)**

1. **Clone the repository**

   Bash

   ```
   git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git
   cd BankExchangeRateSpider
   ```

2. **Copy and configure the environment file**

   Bash

   ```
   cp .env.example .env
   ```

   - **Edit the `.env` file** as needed to fill in your **database** credentials and other configurations.

3. **Build the container image**

   Bash

   ```
   docker-compose build
   ```

4. **Start all services**

   Bash

   ```
   docker-compose up
   ```

   - The **database will be exposed on the host's port 3307** by default (this can be changed in `docker-compose.yml`). You can access the database via `localhost:3307` (using the username and password from your `.env` file).
   - To stop the services, press `Ctrl+C`. To run in the background, add the `-d` flag.

### Option 2: Manual Setup (Without Docker)

1. **Clone the repository**

   Bash

   ```
   git clone https://github.com/YumingMa-CN/BankExchangeRateSpider.git
   cd BankExchangeRateSpider
   ```

2. **Install dependencies**

   Bash

   ```
   pip install -r requirements.txt
   playwright install
   ```

3. **Configure the database**

   Edit `config.py` and set up the database connection URI according to your MySQL server settings. For example:

   Python

   ```
   DB_URI = "mysql+pymysql://username:password@localhost:3306/database_name?charset=utf8"
   ```

   > Ensure that `username`, `password`, and `database_name` are correct and that the database has been created beforehand.

4. **(For development/extension) Maintain field mappings**

   You can skip this step if you are not adding new banks. For details, see [Extending and Maintaining Bank Field Mappings](https://www.google.com/search?q=%23extending-and-maintaining-bank-field-mappings).

5. **Initialize the database table structure**

   When running for the first time or if the database schema has changed, you need to **initialize the tables**:

   Bash

   ```
   # This command MUST be run from the project root directory!
   python -m scripts.init_db
   ```

6. **Start the main scraping script**

   Bash

   ```
   python main.py
   ```

   - The program will automatically fetch and save data for all configured banks.
   - Results will be written to corresponding CSV files in the `data/` directory.
   - The data will also be bulk-imported into the `exchange_rate` table in the database.

------

## Extending and Maintaining Bank Field Mappings

To support more banks or adjust fields, you only need to update **two files** without modifying the main program logic:

1. **Maintain bank configurations and field mappings in `config.py`**

   - Add an entry for the new bank in the `BANKS` dictionary, including its module name, URL, output configuration, etc.

   - For example:

     Python

     ```
     BANKS = {
         'cib': {
             'code': 'cib',
             'name': '兴业银行', # China Industrial Bank
             'url_business': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do',
             'url_api': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd'
                        '={timestamp}&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sort=asc',
             'output': 'data/cib_fx_{timestamp}.csv',  # Output filename, {timestamp} will be replaced with the current timestamp
             'visit_business': True,   # Whether to visit the business page to get necessary data (e.g., cookies) not available in the API URL
             'visit_api': True,
             'interval': 60, # Recommended scraping interval (seconds)
         },
         # ... other banks
     }
     ```

   - Add a new field mapping for the bank in the `FIELD_MAP` dictionary.

     - The **outer key** (e.g., `'boc'`, `'abc'`) represents the bank's abbreviation or **unique code** (it must match the scraper's filename in the `parse/` directory).
     - The **inner key** is the **standardized English field name**, which is also the **database column name**.
     - The **inner value** is the corresponding field name from the data dictionary returned by the bank's `get_data()` function (and in the standard CSV file). This is typically a standardized Chinese field name, **not the raw table header from the webpage**. All banks should follow the same field conventions. If the bank does not provide a certain data item, set its value to `None`.

   - For example:

     Python

     ```
     FIELD_MAP = {
         # Bank Of China (boc)
         'boc': {
             "currency_name": "币种名称",
             "currency_code": "币种代码",
             "base_amount": "基准金额",
             "refer_price": "参考价",        # Reference price (available for some data)
             "remit_buy": "现汇买入价",
             "cash_buy": "现钞买入价",
             "remit_sell": "现汇卖出价",
             "cash_sell": "现钞卖出价",
             "convert_price": "中行折算价",  # BOC-specific conversion price
             "mid_price": None,            # Set to None if not available
             "update_time": "更新时间",
             "crawl_time": "采集时间",
             "bank": "银行"
         },
         # ... configurations for other banks follow the same pattern (see config.py for examples)
     }
     ```

2. **Create a new script for the bank in the `parse/` directory**

   - Create a new file named after the bank's abbreviation (e.g., for China Minsheng Bank: `parse/cmbc.py`). Implement a standard `get_data()` interface that returns fields corresponding to the standard items in `FIELD_MAP`. Use `None` for any missing fields.
   - This approach completely decouples the scraping logic from data processing, making it easy to maintain and extend in the future.

------

## FAQ

- Database connection failed / table not found:
  - Verify that the `DB_URI` in `config.py` is correct.
  - Ensure you have initialized the table structure by running `python -m scripts.init_db`.
- ModuleNotFoundError: No module named 'db.connection':
  - Make sure you are in the project's root directory when running the initialization script. Use `python -m scripts.init_db`, not `python scripts/init_db.py`.
- Extending or changing bank fields:
  - Maintain the `BANKS` configuration in `config.py`. You can follow the existing templates.

------

## Star History



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

This project is licensed under the MIT License. See the [LICENSE](https://github.com/YumingMa-CN/BankExchangeRateSpider/blob/main/LICENSE) file for details.

------

## Contact & Contribution

Feel free to submit issues/PRs, or contact the author [@YumingMa-CN](https://github.com/YumingMa-CN) for collaboration!

------

**Happy coding! If you have any questions, feel free to open an issue or send an email.**