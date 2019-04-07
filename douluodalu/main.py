from scrapy import cmdline
# 执行爬虫 控制台输出log
cmdline.execute('scrapy crawl douluo_spider'.split())

# 导出json文件
# cmdline.execute('scrapy crawl douluo_spider -o items1.json'.split())

# 测试下载
# cmdline.execute('scrapy crawl downloadfile_spider'.split())
