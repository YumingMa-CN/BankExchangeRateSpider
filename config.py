BANKS = {
    'cib': {
        'code': 'cib',
        'name': '兴业银行',
        'url_business': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do',
        'url_api': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd'
                   '={timestamp}&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sort=asc',
        'output': 'data/cib_fx.csv',
        'visit_business': True,     # 是否访问业务页面，可以获取 api_url 中不包含的数据，并且可以通过访问以携带正常 cookies 等。
        'visit_api': True,
        'interval': 60, # 建议采集间隔时间（秒）
    },  # 添加新银行配置后，需在 parse/{code}.py 中添加解析函数
    'cmb': {
        'code': 'cmb',
        'name': '招商银行',
        'url_business': 'https://fx.cmbchina.com/Hq/',
        'url_api': 'https://fx.cmbchina.com/api/v1/fx/rate',
        'output': 'data/cmb_fx.csv',
        'visit_business': False,
        'visit_api': True,
        'interval': 60,
    },
    'icbc': {
        'code': 'icbc',
        'name': '工商银行',
        'url_business': 'https://open.icbc.com.cn/icbc/apip/api_list.html#',
        'url_api': 'https://papi.icbc.com.cn/exchanges/ns/getLatest',
        'output': 'data/icbc_fx.csv',
        'visit_business': False,
        'visit_api': True,
        'interval': 60,
    },
    'abc': {
        'code': 'abc',
        'name': '农业银行',
        'url_business': 'https://app.abchina.com/static/app/ll/ExchangeRate/',
        'url_api': 'https://ewealth.abchina.com/app/data/api/DataService/ExchangeRateV2',
        'output': 'data/abc_fx.csv',
        'visit_business': False,
        'visit_api': True,
        'interval': 60,
    },
    'psbc': {
        'code': 'psbc',
        'name': '中国邮政储蓄银行',
        'url_business': 'https://www.psbc.com/cn/common/bjfw/whpjcx/',
        'url_api': 'https://s.psbc.com/portal/PsbcService/foreignexchange/curr',
        'output': 'data/psbc_fx.csv',
        'visit_business': False,
        'visit_api': True,
        'interval': 60,
    },
    'ccb': {
        'code': 'ccb',
        'name': '中国建设银行',
        'url_business': 'https://ebank2.ccb.com/chn/forex/exchange-quotations.shtml',
        'url_api': 'https://www2.ccb.com/cn/home/news/jshckpj_new.xml',
        'output': 'data/ccb_fx.csv',
        'visit_business': False,
        'visit_api': True,
        'interval': 60,
    },
    'bocom': {
        'code': 'bocom',
        'name': '交通银行',
        'url_business': 'https://www.bankcomm.com/BankCommSite/zonghang/cn/newWhpj/foreignExchangeSearch_Cn.html',
        'url_api': 'https://www.bankcomm.com/BankCommSite/zh-cn/personal/forex/forexQuotation.html',
        'output': 'data/bocom_fx.csv',
        'visit_business': True,
        'visit_api': False,
        'interval': 60,
    },
    # 其他银行...
}

# 各国家货币代码对照表
abbr2cname = {
    'USD': '美元',
    'EUR': '欧元',
    'GBP': '英镑',
    'JPY': '日元',
    'AUD': '澳大利亚元',
    'CAD': '加拿大元',
    'CHF': '瑞士法郎',
    'NZD': '新西兰元',
    'CNY': '人民币',
    'HKD': '港币',
    'SGD': '新加坡元',
    'SEK': '瑞典克朗',
    'NOK': '挪威克朗',
    'MXN': '墨西哥比索',
    'INR': '印度卢比',
    'RUB': '俄罗斯卢布',
    'ZAR': '南非兰特',
    'BRL': '巴西雷亚尔',
    'TRY': '土耳其里拉',
    'PLN': '波兰兹罗提',
    'THB': '泰国铢',
    'MYR': '马来西亚林吉特',
    'IDR': '印尼盾',
    'PHP': '菲律宾比索',
    'VND': '越南盾',
    'AED': '阿联酋迪拉姆',
    'SAR': '沙特里亚尔',
    'KRW': '韩元',
    'TWD': '新台币',
    'HUF': '匈牙利福林',
    'CZK': '捷克克朗',
    'DKK': '丹麦克朗',
    'ISK': '冰岛克朗',
    'CLP': '智利比索',
    'COP': '哥伦比亚比索',
    'PEN': '秘鲁新索尔',
    'ARS': '阿根廷比索',
    'DOP': '多米尼加比索',
    'UYU': '乌拉圭比索',
    'NGN': '尼日利亚奈拉',
    'ILS': '以色列新谢克尔',
    'EGP': '埃及镑',
    'KWD': '科威特第纳尔',
    'QAR': '卡塔尔里亚尔',
    'BHD': '巴林第纳尔',
    'OMR': '阿曼里亚尔',
    'JOD': '约旦第纳尔',
    'PKR': '巴基斯坦卢比',
    'LKR': '斯里兰卡卢比',
    'BDT': '孟加拉塔卡',
    'MMK': '缅甸元',
    'KHR': '柬埔寨瑞尔',
    'LAK': '老挝基普',
    'MOP': '澳门元',
    'HRK': '克罗地亚库纳',
    'RON': '罗马尼亚列伊',
    'BGN': '保加利亚列弗',
    'UAH': '乌克兰格里夫纳',
    'KZT': '哈萨克斯坦坚戈',
    'MAD': '摩洛哥迪拉姆',
    'TND': '突尼斯第纳尔',
    'GEL': '格鲁吉亚拉里',
    'AZN': '阿塞拜疆马纳特',
    'BYN': '白俄罗斯卢布',
    'RSD': '塞尔维亚第纳尔',
    'MKD': '马其顿第纳尔',
    'ALL': '阿尔巴尼亚列克',
    'MNT': '蒙古图格里克',
    'BAM': '波黑可兑换马克',
    'XOF': '西非法郎',
    'XAF': '中非法郎',
    'XPF': '太平洋法郎',
    # 其他货币...
}

# 各国家货币数字代码对照表
digit2abbr = {
    '840': 'USD',   # 美元
    '978': 'EUR',   # 欧元
    '826': 'GBP',   # 英镑
    '392': 'JPY',   # 日元
    '036': 'AUD',   # 澳大利亚元
    '124': 'CAD',   # 加拿大元
    '756': 'CHF',   # 瑞士法郎
    '554': 'NZD',   # 新西兰元
    '156': 'CNY',   # 人民币
    '344': 'HKD',   # 港币
    '702': 'SGD',   # 新加坡元
    '752': 'SEK',   # 瑞典克朗
    '578': 'NOK',   # 挪威克朗
    '484': 'MXN',   # 墨西哥比索
    '356': 'INR',   # 印度卢比
    '643': 'RUB',   # 俄罗斯卢布
    '710': 'ZAR',   # 南非兰特
    '986': 'BRL',   # 巴西雷亚尔
    '949': 'TRY',   # 土耳其里拉
    '985': 'PLN',   # 波兰兹罗提
    '764': 'THB',   # 泰国铢
    '458': 'MYR',   # 马来西亚林吉特
    '360': 'IDR',   # 印尼盾
    '608': 'PHP',   # 菲律宾比索
    '704': 'VND',   # 越南盾
    '410': 'KRW',   # 韩元
    '901': 'TWD',   # 新台币
    '348': 'HUF',   # 匈牙利福林
    '203': 'CZK',   # 捷克克朗
    '208': 'DKK',   # 丹麦克朗
    '352': 'ISK',   # 冰岛克朗
    '152': 'CLP',   # 智利比索
    '170': 'COP',   # 哥伦比亚比索
    '604': 'PEN',   # 秘鲁新索尔
    '032': 'ARS',   # 阿根廷比索
    '214': 'DOP',   # 多米尼加比索
    '858': 'UYU',   # 乌拉圭比索
    '566': 'NGN',   # 尼日利亚奈拉
    '376': 'ILS',   # 以色列新谢克尔
    '818': 'EGP',   # 埃及镑
    '414': 'KWD',   # 科威特第纳尔
    '634': 'QAR',   # 卡塔尔里亚尔
    '048': 'BHD',   # 巴林第纳尔
    '512': 'OMR',   # 阿曼里亚尔
    '400': 'JOD',   # 约旦第纳尔
    '586': 'PKR',   # 巴基斯坦卢比
    '144': 'LKR',   # 斯里兰卡卢比
    '050': 'BDT',   # 孟加拉塔卡
    '104': 'MMK',   # 缅甸元
    '116': 'KHR',   # 柬埔寨瑞尔
    '418': 'LAK',   # 老挝基普
    '446': 'MOP',   # 澳门元
    '191': 'HRK',   # 克罗地亚库纳
    '946': 'RON',   # 罗马尼亚列伊
    '975': 'BGN',   # 保加利亚列弗
    '980': 'UAH',   # 乌克兰格里夫纳
    '398': 'KZT',   # 哈萨克斯坦坚戈
    '504': 'MAD',   # 摩洛哥迪拉姆
    '788': 'TND',   # 突尼斯第纳尔
    '981': 'GEL',   # 格鲁吉亚拉里
    '944': 'AZN',   # 阿塞拜疆马纳特
    '933': 'BYN',   # 白俄罗斯卢布
    '941': 'RSD',   # 塞尔维亚第纳尔
    '807': 'MKD',   # 马其顿第纳尔
    '008': 'ALL',   # 阿尔巴尼亚列克
    '496': 'MNT',   # 蒙古图格里克
    '977': 'BAM',   # 波黑可兑换马克
    '952': 'XOF',   # 西非法郎
    '950': 'XAF',   # 中非法郎
    '953': 'XPF',   # 太平洋法郎
    # ...可根据需要继续补充
}