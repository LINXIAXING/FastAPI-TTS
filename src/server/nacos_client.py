"""
====================================================
@Project:   nginx-DL -> nacos_client
@Author:    TropicalAlgae
@Date:      2023/6/8 14:08
@Desc:
====================================================
"""

import nacos
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from easydict import EasyDict
from fastapi import FastAPI

from src.utils.fastapi_utils import custom_openapi_prefix


class NacosClient(object):
    def __init__(self, app: FastAPI, nacos_config: EasyDict):
        self.client = nacos.NacosClient(
            nacos_config.host,
            namespace=nacos_config.namespace
        )
        self.nacos_config = nacos_config
        self.app = app

        self.init_nacos()
        self.add_openapi_prefix()

    def init_nacos(self):
        # self._logger.log('初始化nacos')
        print('初始化nacos')
        async def beat():
            # 微服务注册nacos
            self.client.add_naming_instance(
                self.nacos_config.service_name,
                self.nacos_config.service_ip,
                self.nacos_config.service_port,
                group_name=self.nacos_config.group
            )

        @self.app.on_event('startup')
        def init_scheduler():
            scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")
            scheduler.add_job(beat, 'interval', seconds=5)
            scheduler.start()

    def add_openapi_prefix(self):
        """
        添加Swagger接口前缀
        """
        custom_openapi_prefix(self.app, self.nacos_config.service_name)


tags_metadata = [
    {
        "name": "流量管理",
        "description": "查询集群主机流量详情",
    },
    {
        "name": "服务状态",
        "description": "测试服务状态",
    },
]
