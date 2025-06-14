CREATE TABLE `exchange_rate` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `currency_name` VARCHAR(32) COMMENT '币种名称',
  `currency_code` VARCHAR(8) COMMENT '币种代码',
  `base_amount` DECIMAL(12,4) COMMENT '基准金额',
  `refer_price` DECIMAL(16,6) NULL COMMENT '参考价',
  `remit_buy` DECIMAL(16,6) NULL COMMENT '现汇买入价',
  `remit_sell` DECIMAL(16,6) NULL COMMENT '现汇卖出价',
  `cash_buy` DECIMAL(16,6) NULL COMMENT '现钞买入价',
  `cash_sell` DECIMAL(16,6) NULL COMMENT '现钞卖出价',
  `mid_price` DECIMAL(16,6) NULL COMMENT '中间价',
  `convert_price` DECIMAL(16,6) NULL COMMENT '折算价',
  `update_time` DATETIME COMMENT '银行公布的更新时间',
  `crawl_time` DATETIME COMMENT '系统采集数据的时间',
  `bank` VARCHAR(32) COMMENT '银行名称',
  `ext_json` JSON NULL COMMENT '扩展字段（如后续出现的新字段）',
  KEY `idx_bank_cc_up` (`bank`, `currency_code`, `update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='各银行汇率数据，字段兼容和扩展性设计';
