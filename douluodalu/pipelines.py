# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class DouluodaluPipeline(ImagesPipeline):
    # 上边说过这个三函数都是ImagesPipeline类里的函数.
    def get_media_requests(self, item, info):
        # img_url是下载图片的地址,存放在item(具有类似字典的功能)中,
        img_urls = item["img_urls"]
        # print(img_urls)
        for image_url in img_urls.values():
            # 将下载好的图片返回给file  _path函数,图片的保存需要自己给他添加一个路径,并且要给图片起一个名字,而这些参数都在item中,file_path没有接收item的参数,所以需要将item以字典的形式传给meta,跟随下载的图片一块传给file_path函数.
            yield scrapy.Request(url=image_url, meta={"item": item, "img_url": image_url})

    # response=None,是因为file_path函数是用来保存图片的,而不是解析response的数据;官方文档中的file_path作用是将图片的下载网址给加密,并且返回图片下载的路径
    def file_path(self, request, response=None, info=None):
        # 将item取出来
        item = request.meta["item"]
        # 再从item中取出分类名称,这个name就是我们想自定义图片路径的文件名称,(如果不自定义file_path函数的话,默认会将图片下载到full文件里)
        name = item["title"]
        # 再从item中取出img_url,分隔出来图片的名称.图片的网址一般最后一个'/'后都是数字,此处用它作图片的名字
        img_url_name = request.meta["img_url"].split("/")[-1].replace("-mht.middle.webp", "")
        return "%s/%s" % (name, img_url_name)

    # 项目管道里面的每一个item最终都会经过item_completd，也就是意味着有多少个item，这个item_completed函数就会被调用多少次。(不管下载成功，还是失败都会被调用)，如果不重写该方法，item默认都会返回出去。item_completed里面的return出去的item是经过整个项目管道处理完成之后的最终的一个item。
    def item_completed(self, results, item, info):
        # 在这通过debug可以看到results里数据,分下载图片成功和下载失败两种情况.
        # 如果下载成功results的结果：[(True, {'url': 'http://pics.sc.chinaz.com/Files/pic/icons128/7152/f1.png', 'path': '人物头像图标下载/f1.png', 'checksum': 'eb7f47737a062a1525457e451c41cc99'})]
        # True:代表图片下载成功
        # url：图片的地址
        # path:图片的存储路径
        # checksum:图片内容的 MD5 hash加密字符串
        # 如果下载失败results的结果:[(False, <twisted.python.failure.Failure scrapy.pipelines.files.FileException: 'NoneType' object has no attribute 'split'>)]
        # False:代表下载失败
        # error:下载失败的原因

        # 将图片的下载路径取出来(文件夹名/图片名)
        print(results)
        image_path = results[0][1].get("path")
        if not image_path:
            # 如果图片下载失败，则取不到image_path，那就说明对应的item是有问题的，就删除这个item。
            raise DropItem("图片下载失败，删除对应的item，不让该item返回出去。")
        # 如果能取到img_path，说明该item是一个正常的item，可以返回出去。这个时候可以给item添加一个img_path的值,最后给这个item返回出去，这个item就是经过整个管道处理完成之后的最终的一个item。
        item["img_name"] = image_path
        print("item_completed函数被调用了！")
        print(item)
        # 为什么要renturn这个item，因为后面还有其他的管道(pipeline)会处理这个item，所以需要给它return出去。
        return item


