import threading
from ast import Bytes

from appium import webdriver
import time

from appium.webdriver.common.appiumby import AppiumBy as by

from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions




class ConnectIos:
    def __init__(self):
        pass
    def connect_ios_device(self):
        """
        通过 UDID 连接到 iOS 设备
        """
        caps = {
            "platformName": "iOS",
            "deviceName": "iPhone14A", # 手机名称
            "platformVersion": '18.4.1', # 系统版本
            "udid": '00008120-000A49C22E0A401E',
            "automationName": "XCUITest", 
            "bundleId": "Blink.Tech.Blink"  # 应用的 Bundle ID
        }
        print(f"Capabilities: {caps}")
        options = ArgOptions()
        options.set_capability("platformName", caps["platformName"])
        options.set_capability("deviceName", caps["deviceName"])
        options.set_capability("platformVersion", caps["platformVersion"])
        options.set_capability("udid", caps["udid"])    
        options.set_capability("automationName", caps["automationName"])
        options.set_capability("bundleId", caps["bundleId"])

    # 使用 options 创建 WebDriver 实例
        driver = webdriver.Remote(command_executor='http://localhost:8100', options=options)
        return driver

