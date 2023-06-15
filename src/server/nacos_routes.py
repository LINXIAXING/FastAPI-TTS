"""
====================================================
@Project:   nginx-DL -> nacos_routes
@Author:    TropicalAlgae
@Date:      2023/6/8 14:02
@Desc:
====================================================
"""
import json
import time
from collections import defaultdict
from threading import Lock
import os
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from src.utils.fastapi_utils import resp_200
import opencc


class Info(BaseModel):
    model_name: str = ''
    prediction: str = ''


class ModelRouter(object):
    def __init__(self, models: dict, check_point: str):
        self.router = APIRouter()
        self.models = models
        self.check_point = check_point
        self.apply_api()

    def apply_api(self):
        """
        初始化API
        """
        @self.router.get('/ss', name="文字转音频", tags=["模型预测"], response_model=str)
        async def run_ss(text: str):
            path = os.path.join(os.getcwd(), self.check_point)
            if not os.path.isdir(self.check_point):
                os.makedirs(self.check_point)

            file_name = time.ctime().replace('  ', ' ').replace(' ', '-') + '.wav'
            path = os.path.join(path, file_name)
            self.models['ss'](text=text, output=path)

            result = f'音频文件已保存，路径{path}'
            return resp_200(data=result)

        @self.router.get('/sr', name="音频转文字", tags=["模型预测"], response_model=str)
        async def run_sr(file: str):
            result = self.models['sr'].transcribe(file, language="Chinese")
            cc = opencc.OpenCC('t2s')  # 繁体转简体
            result = cc.convert(result["text"])
            return resp_200(data=result)
