from fastapi import FastAPI
import yaml
from easydict import EasyDict
from src.server.nacos_client import NacosClient, tags_metadata
from src.server.nacos_routes import ModelRouter
from src.utils.fastapi_utils import add_exception_handler
import uvicorn
from paddlespeech.cli.tts.infer import TTSExecutor
import whisper


def _run():
    config = EasyDict(yaml.load(open('./config.yaml', 'r', encoding='utf-8'), Loader=yaml.FullLoader))

    # 初始化服务器
    print('初始化服务器')
    app = FastAPI(title=config.nacos.service_name, description='模型预测', openapi_url='/model/api-docs',
                  openapi_tags=tags_metadata)
    add_exception_handler(app)

    # 加载模型
    print('模型加载')
    ss = TTSExecutor()
    sr = whisper.load_model("base")
    models = {
        'ss': ss,
        'sr': sr
    }

    # 初始化路由
    model_router = ModelRouter(models, config.check_point.ss_output)
    app.include_router(model_router.router, prefix='/model')

    # 开启服务器
    uvicorn.run(app, host="0.0.0.0", port=config.nacos.service_port)


if __name__ == '__main__':
    _run()

    # my_awesome_api = FastAPI()
    # @my_awesome_api.get("/")
    # async def root():
    #     return {"message": "Hello World"}
    # uvicorn.run(my_awesome_api, host="0.0.0.0", port=9000)
