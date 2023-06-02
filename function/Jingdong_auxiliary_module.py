import random
import requests

# 随机UA
def randomUserAgent():
    # 生成一个随机的 UUID
    uuid = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789abcz', 40))
    # 生成一个随机的地址 ID
    addressid = ''.join(random.sample('1234567898647', 10))
    # 随机选择一个 iOS 版本号
    ios_ver = random.choice(['15.1.1', '14.5.1', '14.4', '14.3', '14.2', '14.1', '14.0.1'])
    # 将 iOS 版本号中的点号替换为下划线
    ios_v = ios_ver.replace('.', '_')
    # 随机选择一个客户端版本号
    client_ver = random.choice(['10.3.0', '10.2.7', '10.2.4'])
    # 随机选择一个 iPhone 型号
    iphone = random.choice(['8', '9', '10', '11', '12', '13'])
    # 生成一个随机的地理位置信息
    area = '_'.join([''.join(random.sample('0123456789', n)) for n in [2, 4, 5, 4]])
    # 生成一个随机的 ADID
    adid = '-'.join([''.join(random.sample('0987654321ABCDEF', n)) for n in [8, 4, 4, 4, 12]])
    # 生成一个随机的经度和纬度
    lng = '119.31991256596' + str(random.randint(100, 999))
    lat = '26.1187118976' + str(random.randint(100, 999))

    # 构造 UserAgent 字符串
    user_agent = f'jdapp;iPhone;10.0.4;{ios_ver};{uuid};network/wifi;ADID/{adid};model/iPhone{iphone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {ios_v} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
    return user_agent

# 请求sign服务
def get_sign_kemeng(fn, body):
    str_sign = ''
    data = {
        "fn": fn,
        "body": body
    }
    url = 'http://47.120.9.145:3000/M-sign'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }
    response = requests.post(url,headers=headers,json=data)
    try:
        if response.status_code == 200:
            data = response.json()
            if data and data.get('body'):
                if data['body']:
                    str_sign = data['body']
                    if str_sign != '':
                        return str_sign
                    else:
                        print("签名获取失败.")
            else:
                print("签名获取失败.")
        else:
            print("签名获取失败.")
    except Exception as e:
        print(f"解析数据出错: {e}")
    return str_sign