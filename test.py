import requests


def test_url():
    # 接口的url
    url = "http://172.17.0.3:9000/model/sr"
    # 接口的参数
    # params = {
    #     "text": "测试文字转语音",
    # }
    params = {
        "file": "/zzx/nacos-DL/output/Thu-Jun-8-13:53:11-2023.wav",
    }
    print('调接口')
    r = requests.request("get", url, params=params)

    # 打印返回结果
    print(r.text)


if __name__ == '__main__':
    test_url()
