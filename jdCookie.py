import os
import time
from functools import partial
print = partial(print, flush=True)


def get_cookies():
    CookieJDs = []
    if os.environ.get("JD_COOKIE"):
        print("已获取并使用Env环境 Cookie")
        if '&' in os.environ["JD_COOKIE"]:
            CookieJDs = os.environ["JD_COOKIE"].split('&')
        elif '\n' in os.environ["JD_COOKIE"]:
            CookieJDs = os.environ["JD_COOKIE"].split('\n')
        else:
            CookieJDs = [os.environ["JD_COOKIE"]]
        # return CookieJDs
    else:
        if os.path.exists("JD_COOKIE.txt"):
            with open("JD_COOKIE.txt", 'r') as f:
                JD_COOKIEs = f.read().strip()
                if JD_COOKIEs:
                    if '&' in JD_COOKIEs:
                        CookieJDs = JD_COOKIEs.split('&')
                    elif '\n' in JD_COOKIEs:
                        CookieJDs = JD_COOKIEs.split('\n')
                    else:
                        CookieJDs = [JD_COOKIEs]
                    CookieJDs = sorted(set(CookieJDs), key=CookieJDs.index)
                    # return CookieJDs
        else:
            print("未获取到正确✅格式的京东账号Cookie")
            return

    print(f"获取到{len(CookieJDs)}个 | 京东Cookie")
    print(f"程序运行 | {time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}\n")
    return CookieJDs