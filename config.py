BANKS = {
    'cib': {
        'code': 'cib',
        'name': '兴业银行',
        'url_html': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do',
        'url_api': 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery/list?_search=false&dataSet.nd'
                   '={timestamp}&dataSet.rows=80&dataSet.page=1&dataSet.sidx=&dataSet.sort=asc',
        'output': 'data/cib_fx.csv'
    },
    # 其他银行...
}
