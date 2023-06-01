import time, requests, sys, json, re
from jdCookie import get_cookies
from datetime import datetime
import urllib.parse

# 京东签到领京豆
def JD_collection_check_in(cookie):
    # 请求url
    url = 'https://api.m.jd.com/client.action'
    # 请求标头
    headers = {
        'user-agent': 'jdapp;android;11.6.4;;;appBuild/98704;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1685499076768%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJC%3D%22%2C%22ad%22%3A%22CNU5YzZvDzK1EWDuYwOmCm%3D%3D%22%2C%22od%22%3A%22YwG2Ytq3YzdrCzCyZNS2EK%3D%3D%22%2C%22ov%22%3A%22CzC%3D%22%2C%22ud%22%3A%22CNU5YzZvDzK1EWDuYwOmCm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 13; M2007J1SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046248 Mobile Safari/537.36',
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
        'body': '{"fp":"-1","shshshfp":"-1","shshshfpa":"-1","referUrl":"-1","userAgent":"-1","jda":"-1","rnVersion":"3.9"}',
        'appid': 'ld',
        'client': 'android',
        'clientVersion': '11.6.4',
        'networkType': 'wifi',
        'osVersion': '13',
        'loginType': '2',
        'screen': '393*770',
        'uuid': '0353933663567303-5393364626160333',
        'eu': '0353933663567303',
        'fv': '5393364626160333',
        'openudid': '0353933663567303-5393364626160333',
        'd_model': 'Mi 10 Ultra',
        'jsonp': 'jsonp_1685499111584_48445'
        }
    # 发送请求
    response = requests.get(url, params=params, headers=headers)
    # 异常处理
    try:
        # 将返回内容分隔为json格式
        json_data = re.search(r'\((.*)\)', response.text).group(1)
        # 实例化json
        data = json.loads(json_data)
        # 获取需要的数据
        bean_count = data['data']['dailyAward']['beanAward']['beanCount']
        # 构建返回
        result = f"京东签到成功 | {bean_count} 京豆"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "京东签到失败 | 黑号"
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
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2007J1SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046247 Mobile Safari/537.36/application=JDJR-App&clientType=android&src=xiaomi&version=6.5.50&clientVersion=6.5.50&osVersion=13&osName=M2007J1SC&isUpdate=0&HiClVersion=&netWork=1&netWorkType=1&CpayJS=UnionPay/1.0 JDJR&sPoint=MTAwMDYjIw%3D%3D%0A&*#@jdPaySDK*#@jdPayChannel=jdFinance&jdPayChannelVersion=6.5.50&jdPaySdkVersion=1.1.3&androidBrand=Xiaomi&androidManufacturer=Xiaomi&jdPayClientName=Android*#@jdPaySDK*#@",
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
        result = f"金融签到成功 | {award_real_num } 金贴"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "金融签到失败 | 黑号"
    return result

# 京东金融双签-领取
def JD_Financial_Double_Sign(cookie):
    # 请求url
    url = 'https://nu.jr.jd.com/gw/generic/jrm/h5/m/process'
    # 请求标头
    headers = {
    'accept': 'application/json',
    'user-agent': 'jdapp;android;11.6.4;;;appBuild/98704;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1685500271701%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJC%3D%22%2C%22ad%22%3A%22CNU5YzZvDzK1EWDuYwOmCm%3D%3D%22%2C%22od%22%3A%22YwG2Ytq3YzdrCzCyZNS2EK%3D%3D%22%2C%22ov%22%3A%22CzC%3D%22%2C%22ud%22%3A%22CNU5YzZvDzK1EWDuYwOmCm%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 13; M2007J1SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046248 Mobile Safari/537.36',
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
        if "京豆" in data:
            count = re.search(r"\"count\":\"?(\d.*?)\"?,", data).group(1)
            # 构建返回
            result = f"金融签到领取成功 | {count}京豆"
        else:
            business_data = data['resultData']['data']['businessData']
            business_msg = business_data['businessMsg']
            # 构建返回
            result = f"金融签到领取异常 | {business_msg}"
    except (KeyError, ValueError, TypeError):
        # 构建返回
        result = "金融签到领取失败 | 黑号"
    return result

# 执行程序
if __name__ == '__main__':
    try:
        getCk = get_cookies()
        if not getCk:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    print('🔔京东集合签到')
    num = 0
    for cookie in getCk:
        num += 1
        if num % 10 == 0:
            print("⏰等待5s,休息一下")
            time.sleep(5)
        try:
            pt_pin = re.compile(r'pt_pin=(.*?);').findall(cookie)[0]
        except IndexError:
            pt_pin = re.compile(r'pin=(.*?);').findall(cookie)[0]
        print(f'\ncookie {num} | {pt_pin}\n')
        print(datetime.now())

        try:
            print(JD_collection_check_in(cookie))
            print(JD_Finance_Sign_in(cookie))
            print(JD_Financial_Double_Sign(cookie))
        except Exception as e:
            print(e)





