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
    # 其他银行...
}
