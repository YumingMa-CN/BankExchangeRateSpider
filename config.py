BANKS = {
    'cib': {
        'code': 'cib',
        'name': '兴业银行',
        'url_business': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do',
        'url_api': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd'
                   '={timestamp}&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sort=asc',
        'output': 'data/cib_fx.csv',
        'visit_api': True,
        'visit_business': True,
        'interval': 60, # 建议采集间隔时间（秒）
    },
    'cmb': {
        'code': 'cmb',
        'name': '招商银行',
        'url_business': 'https://fx.cmbchina.com/Hq/',
        'url_api': 'https://fx.cmbchina.com/api/v1/fx/rate',
        'output': 'data/cmb_fx.csv',
        'visit_api': True,
        'visit_business': False,
        'interval': 60, # 建议采集间隔时间（秒）
    },
    # 其他银行...
}
