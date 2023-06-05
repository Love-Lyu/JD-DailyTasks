"""
京东集合签到 v1.0

cron: 26 9,14 * * *
const $ = new Env("京东集合签到");
"""

import time, requests, sys, json, re
from jdCookie import get_cookies
from datetime import datetime
import urllib.parse
import random

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

# 京东签到领京豆
def JD_collection_check_in(cookie):
    # 请求url
    url = 'https://api.m.jd.com/client.action'
    # 请求标头
    headers = {
        'user-agent': randomUserAgent(),
        'accept': '*/*',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'https://h5.m.jd.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie
    }
    # 传入参数
    params = {
        'functionId': 'signBeanAct',
        'body': get_sign_kemeng('signBeanAct', {"fp":"-1","shshshfp":"-1","shshshfpa":"-1","referUrl":"-1","userAgent":"-1","jda":"-1","rnVersion":"3.9"}),
        'appid': 'ld'
        }
    # 发送请求
    response = requests.get(url, params=params, headers=headers)
    # 异常处理
    try:
        # 实例化json
        data = response.json() 
        # 获取需要的数据
        # 京豆数量
        if 'continuityAward' in data['data'] and 'beanAward' in data['data']['continuityAward']:
            bean_count = data['data']['continuityAward']['beanAward']['beanCount']
        elif 'dailyAward' in data['data'] and 'beanAward' in data['data']['dailyAward']:
            bean_count = data['data']['dailyAward']['beanAward']['beanCount']
        # 返回签到信息
        if 'continuityAward' in data['data'] and 'title' in data['data']['continuityAward']:
            title = data['data']['continuityAward']['title']
        elif 'dailyAward' in data['data'] and 'title' in data['data']['dailyAward']:
            title = data['data']['dailyAward']['title'] + data['data']['dailyAward']['subTitle']
        # 构建返回
        result = f"京东 | {title} | {bean_count} 京豆"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "京东 | 签到失败 | 黑号"
    return result

# 京东金融双签-签到
def JD_Finance_Sign_in(cookie):
    # 分隔cookie的pt_key
    pt_key = re.findall(r'pt_key=([^;]+)', cookie)[0]
    # 分隔cookie的pt_pin
    pt_pin = re.findall(r'pt_pin=([^;]+)', cookie)[0]
    # 请求url
    url = "https://ms.jr.jd.com/gw2/generic/jrSign/h5/m/queryWeekSignSub"
    # 请求标头
    headers = {
    "User-Agent": randomUserAgent(),
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://member.jr.jd.com",
    "X-Requested-With": "com.jd.jrapp",
    "Referer": "https://member.jr.jd.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": f"pt_pin={pt_pin}; pwdt_id={pt_pin}; qid_uid=02050a75-1b97-4380-a97a-561cd7556fc2; qid_fs=1683894431337; 3AB9D23F7A4B3C9B=TPCWYIAEMIY6Z53VQN5PVTEYFDIKDY4HKELLMRJGKJUNP7K2HNWROAEY244EUVPA5GLL6LB2QKRC4UG466RZ6C52UU; pt_key={pt_key}; sid=24013361296696d6ea8bf1f96357562w; qid_ls=1685510351536; qid_ts=1685552423114; qid_vis=6; qid_sid=02050a75-1b97-4380-a97a-561cd7556fc2-6"
    }
    # 传入参数
    data = "reqData=%7B%22channelSource%22%3A%22JRAPP6.0%22%2C%22riskDeviceParam%22%3A%22%7B%5C%22eid%5C%22%3A%5C%22TPCWYIAEMIY6Z53VQN5PVTEYFDIKDY4HKELLMRJGKJUNP7K2HNWROAEY244EUVPA5GLL6LB2QKRC4UG466RZ6C52UU%5C%22%2C%5C%22fp%5C%22%3A%5C%221fa61533e25aaa4486aea2119bd09f25%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22%5C%22%2C%5C%22token%5C%22%3A%5C%22OKXJYWFSJX4QOD4Y53E72S73WICB7MHLOGLCPF3CERMIXZWC6WSRMJWMXPQQZQXYCH53TWR45TYDG%5C%22%2C%5C%22jstub%5C%22%3A%5C%22X36J2CUSQLQJQJUGETDJY3J46EAKNUDRDSXP2LZJKDH4SLEXH6KXT5AWQY4RUXKXGFCLVW7WUD7DO2EYXMIBMCMLIAELT2HUX3SBWOY%5C%22%7D%22%2C%22site%22%3A%22JD_JR_APP%22%2C%22channelLv%22%3A%22shuangqian%22%7D"
    # 发送请求
    response = requests.post(url, headers=headers, data=data)
    # 异常处理
    try:
        # 实例化json
        data = response.json()  
        # 获取需要的数据
        awards = data["resultData"]["resBusiData"]["taskDetailInfoList"][0]["awards"]
        award_real_num = awards[0]["awardRealNum"]
        # 构建返回
        result = f"京东金融 | 签到成功 | {award_real_num } 金贴"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "京东金融 | 签到失败 | 黑号"
    return result

# 京东金融双签-领取
def JD_Financial_Double_Sign(cookie):
    # 请求url
    url = 'https://nu.jr.jd.com/gw/generic/jrm/h5/m/process'
    # 请求标头
    headers = {
    'accept': 'application/json',
    'user-agent': randomUserAgent(),
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://m.jr.jd.com',
    'x-requested-with': 'com.jingdong.app.mall',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://m.jr.jd.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': cookie
    }
    # 传入参数
    reqData = {
    "actCode": "F68B2C3E71",
    "type": "3",
    "frontParam": {
        "belong": "jingdou"
        }
    }
    # 传入负荷
    body = f"reqData={urllib.parse.quote(json.dumps(reqData))}"
    # 发送请求
    response = requests.post(url, body, headers=headers)
    # 异常处理
    try:
        # 实例化json
        data = response.json()  
        # 获取需要的数据
        if 'awardListVo' in data['resultData']['data']['businessData']['businessData']:
            count = data['resultData']['data']['businessData']['businessData']['awardListVo'][0]['count']
            # 构建返回
            result = f"京东金融 | 签到领取成功 | {count} 京豆"
        else:
            business_data = data['resultData']['data']['businessData']
            business_msg = business_data['businessMsg']
            # 构建返回
            result = f"京东金融 | 签到领取异常 | {business_msg}"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "京东金融 | 签到领取失败 | 黑号"
    return result

# 执行程序
if __name__ == '__main__':
    try:
        getCk = get_cookies()
        if not getCk:
            sys.exit()
    except:
        print("未获取到有效COOKIE | 退出程序！")
        sys.exit()
    print('🔔京东集合签到')
    num = 0
    for cookie in getCk:
        num += 1
        if num % 5 == 0:
            print("⏰等待5s | 休息一下")
            time.sleep(5)
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        print(f'\ncookie {num} | {pt_pin}\n')
        print(datetime.now())

        try:
            print(JD_collection_check_in(cookie))
            #print(JD_Finance_Sign_in(cookie))
            print(JD_Financial_Double_Sign(cookie))
        except Exception as e:
            print(e)





