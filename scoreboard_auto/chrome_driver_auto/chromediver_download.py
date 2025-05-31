import json
import os
import time
import traceback
import zipfile
import subprocess
import shutil
from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
import requests
from urllib3 import Retry


def get_chrome_version():
    try:
        if os.name == 'nt':
            version_info = subprocess.check_output(
                ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stderr=subprocess.STDOUT, text=True)
        else:
            # version_info = subprocess.check_output(['google-chrome', '--version'], stderr=subprocess.STDOUT, text=True)
            version_info = subprocess.check_output(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stderr=subprocess.STDOUT,
                text=True).strip()
        version_info = version_info.strip().split()[-1]
        dyc = "JXX的谷歌驱动下载程序！\n给您一个五星级下载体验！"
        print(f"\033[31m{dyc}\033[0m")
        print(f"谷歌浏览器的版本是: {version_info}")
        return version_info
    except subprocess.CalledProcessError as e:
        print(f"无法获取Chrome版本： {e.output}")
        return None


def get_new_json():
    print("正在下载驱动json文件，寻找合适的驱动版本,请稍后...")
    file = requests.get(
        'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json').content
    with open("chromedriver.json", "w") as fp:
        json.dump(json.loads(file), fp)


def get_chromediver_url():
    local_version = get_chrome_version()
    # local_version = "130.0.8.65"

    need_info = {}

    download_version = ""
    v_url = ""
    if not os.path.exists("chromedriver.json"):
        get_new_json()
    with open("chromedriver.json", "r") as fp:
        file2 = json.load(fp)
    for v in file2["versions"]:
        file_version = v["version"]

        if local_version >= file_version:
            download_version = v["version"]
            need_info = v

        else:
            print(f"要下载的驱动版本是: {download_version}")
            if os.name == 'nt':
                v_url = need_info["downloads"]["chromedriver"][-1]["url"]
                print("操作系统是：Windows")
                print(f"驱动下载地址: \n{v_url}")
            else:
                result = subprocess.run(['system_profiler', 'SPHardwareDataType'], stdout=subprocess.PIPE)
                output = result.stdout.decode('utf-8')
                if "ARM" in output:
                    v_url = need_info["downloads"]["chromedriver"][1]["url"]
                    print("操作系统是：Mac ARM架构的")
                    print(f"驱动下载地址: \n{v_url}")
                else:
                    v_url = need_info["downloads"]["chromedriver"][2]["url"]
                    print("操作系统是：Mac")
                    print(f"驱动下载地址: \n{v_url}")
            break
    return v_url


def download_chromedriver():
    try:
        url = get_chromediver_url()
        with open("下载地址.txt", "w+") as file:
            file.write(url)
        print("正在下载驱动...")
        if os.path.exists("driver"):
            shutil.rmtree("driver")
        if url:
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504, 10054])
            session.mount('http://', HTTPAdapter(max_retries=retries))
            session.mount('https://', HTTPAdapter(max_retries=retries))

            c = session.get(url).content
            # c = requests.get(url).content
            with open("aaa.zip", "wb") as fp:
                fp.write(c)

            # with zipfile.ZipFile("aaa.zip", 'r') as zip_ref:
            #     zip_ref.extract("chromedriver-win64/chromedriver.exe")
            if os.name == "nt":
                with zipfile.ZipFile("aaa.zip", 'r') as zip_ref:
                    zip_ref.extract("chromedriver-win64/chromedriver.exe")
                os.rename("chromedriver-win64", "driver")
            else:
                with zipfile.ZipFile("aaa.zip", 'r') as zip_ref:
                    zip_ref.extract("chromedriver-mac-x64/chromedriver")
                os.rename("chromedriver-mac-x64", "driver")
            if os.path.exists("aaa.zip"):
                os.remove("aaa.zip")
            if os.path.exists("aaa.zip"):
                os.remove("aaa.zip")
            print("驱动下载完毕...  \n驱动存放在在当前目录的driver文件夹下")


            time.sleep(5)

        else:
            print("没有找到合适的驱动，正在更新json文件，请重新运行！！")
            os.remove("chromedriver.json")
            time.sleep(5)

    except Exception as e:
        msg1 = "自动下载驱动失败......【点击上面的链接进行手动下载】"
        msg2 = "\n或者手动复制【chromediver下载地址.txt】里面的网址到浏览器下载"
        print(f"\033[34m{msg1}\033[0m" + msg2)
        with open("错误信息.txt", "w", encoding="utf-8") as f:
            error = traceback.format_exc()
            f.write(error)
        time.sleep(5)


download_chromedriver()
