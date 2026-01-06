import threading
from ast import Bytes

from appium import webdriver
import time

from appium.webdriver.common.appiumby import AppiumBy as by

from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class ConnectIos:
    def __init__(self):
        pass

    def connect_ios_device(self):
        """
        通过 UDID 连接到 iOS 设备
        """
        caps = {
            "platformName": "iOS",
            "deviceName": "iPhoneauto",  # 手机名称
            "platformVersion": '18.4.1',  # 系统版本
            "udid": '00008120-001834323AD2201E',
            "automationName": "XCUITest",
            "bundleId": "Blink.Tech.Blink",  # 应用的 Bundle ID
        }
        print(f"Capabilities: {caps}")
        options = ArgOptions()
        options.set_capability("platformName", caps["platformName"])
        options.set_capability("deviceName", caps["deviceName"])
        options.set_capability("platformVersion", caps["platformVersion"])
        options.set_capability("udid", caps["udid"])
        options.set_capability("automationName", caps["automationName"])
        options.set_capability("bundleId", caps["bundleId"])
        # 这些能力对 iOS 更有效
        options.set_capability("nativeWebTap", True)
        options.set_capability("safariIgnoreFraudWarning", True)
        options.set_capability("safariAllowPopups", True)

        # 使用 options 创建 WebDriver 实例
        driver = webdriver.Remote(command_executor='http://localhost:8100', options=options)
        # try:
        #     # 等待并接受所有出现的警报
        #     WebDriverWait(driver, 10).until(EC.alert_is_present())
        #     alert = driver.switch_to.alert
        #     alert.accept()  # 或者使用 alert.dismiss() 来拒绝
        # except:
        #     print("未发现警报或处理超时")
        return driver
