from appium import webdriver
import time
import threading
from connect import ConnectIos
from appium.webdriver.webdriver import WebDriver
from typing import List
from appium.webdriver.common.appiumby import AppiumBy
from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

devices: List[WebDriver] = []
exptTime = 6
exptFlage = threading.Event()


class state(Enum):
    Success = 1
    Fail = 2
    OtherFail = 3


# 初始化Appium driver
def connectMobile():
    global devices
    cn = ConnectIos()
    devices.append(cn.connect_ios_device())


def find_and_click_button_by_xpath(driver: WebDriver, xpath: str, timeout: int = 10) -> bool:
    try:
        # 显式等待直到按钮可点击
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
        )
        print(f"Button with XPath '{xpath}' found. Clicking it now.")
        button.click()
        # time.sleep(1)
        # button.click()

        return True
    except Exception as e:
        print(f"Error finding or clicking button with XPath '{xpath}': {str(e)}")
        return False


# 查找按钮并点击
def find_and_click_button_by_text(driver: WebDriver, button_texts):
    for button_text in button_texts:
        try:
            button = driver.find_element(by=AppiumBy.NAME, value=button_text)
            print(f"Button with text '{button_text}' found. Clicking it now.")
            button.click()
            return True
        except Exception:
            print(f"Button with text '{button_text}' not found.")

    return False


# //XCUIElementTypeButton[@name="立即升级"]
# 等待指定文本元素出现
def wait_for_elements_by_text(driver: WebDriver, texts, timeout):
    start_time = time.time()
    while True:
        if exptFlage.is_set():  # 使用线程安全的检查
            return state.OtherFail
        for text in texts:
            print('begin check1')
            print(time.time() - start_time)
            if text == '固件安装完成，请等待变色龙重启':
                timeout = exptTime
                print(exptTime)
            try:
                print('begin check2')
                print(text)
                element = driver.find_element(by=AppiumBy.NAME, value=text)
                print(element)
                print(f"Element with text '{text}' found!")
                return state.Success
            except Exception:
                continue

        if time.time() - start_time > timeout:
            print(f"Timeout reached. None of the elements with texts {texts} found.")
            if timeout == 6:
                return state.OtherFail
            return state.Fail

        time.sleep(1)


# 持续监听是否出现数据传输失败或固件安装失败弹框
def listen_for_failure_popup(driver: WebDriver,
                             failure_texts=['数据传输失败', '固件安装失败', '下载失败 (1001)', '下载失败 (1002)',
                                            '下载失败 (1003)', '下载失败 (1004)', '下载失败 (1005)',
                                            '设备已断开连接,请返回首页重新连接设备', '当前电量低，是否要继续升级？']):
    while True:
        for failure_text in failure_texts:
            try:
                popup = driver.find_element(by=AppiumBy.NAME, value=failure_text)
                if popup:
                    print(f"Failure popup with text '{failure_text}' found.")
                    exptTime = 6
                    version_number = get_version_number(driver)
                    device_name = get_device_name(driver)
                    if version_number and device_name:
                        log_upgrade_version(version_number, device_name, False, failure_text)
                    if wait_for_elements_by_text(driver, ['确定'], 5):
                        find_and_click_button_by_text(driver, ['确定'])
                        if find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="立即更新"]'):
                            print("断开连接点击确定后，变色龙已连接，点击“立即更新")
                        if find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="回退到正式版"]'):
                            print("断开连接点击确定后，变色龙已连接，点击“回退到正式版")

                    exptFlage.set()  # 设置 exptFlage 为 True

            except Exception:
                continue
        time.sleep(2)


# OTA 升级
def otaUpdate(driver: WebDriver):
    global exptTime
    exptTime = 2000
    print("exptTime = ")
    print(exptTime)
    exptFlage.clear()  # 重置 exptFlage 为 False
    try:
        texts_to_wait = ['立即更新']
        # time.sleep(5)
        # go_back(driver)

        # driver.find_elements(AppiumBy.XPATH, '//*[contains(@name, "点击检测")]')[0].click()
        find_and_click_button_by_xpath(driver,'//XCUIElementTypeStaticText[@name="点击检测"]')
        time.sleep(0.5)
        if wait_for_elements_by_text(driver, ['立即更新', '回退到正式版'], 1000):
            time.sleep(2)
            # find_and_click_button_by_text(driver, texts_to_wait):
            if find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="立即更新"]'):
                ...
            if find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="回退到正式版"]'):
                input_list = driver.find_elements(AppiumBy.CLASS_NAME, 'XCUIElementTypeTextView')
                print(input_list)
                if input_list:
                    text_to_input = '电脑发呆等你'
                    input_list[0].clear()
                    input_list[0].send_keys(text_to_input)

                    # 清空并输入文本
                    print(f"成功输入: {text_to_input}")
                    time.sleep(1)
                    find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="Done"]')
                    time.sleep(1)
                    find_and_click_button_by_xpath(driver, '//XCUIElementTypeButton[@name="确定"]')

            instllState = wait_for_elements_by_text(driver, ['固件安装完成，请等待变色龙重启'], 2000)
            if instllState == state.Success:
                version_number = get_version_number(driver)
                device_name = get_device_name(driver)
                if version_number and device_name:
                    log_upgrade_version(version_number, device_name, True, '')
                time.sleep(30)
                otaUpdate(driver)  # 假设升级后可能还需要继续升级
            elif instllState == state.Fail:
                print("111111")
                version_number = get_version_number(driver)
                device_name = get_device_name(driver)
                if version_number and device_name:
                    log_upgrade_version(version_number, device_name, False, '安装指令未发送')
                print('升级失败')
                go_back(driver)
                otaMeum(driver)
            else:
                print("ota fail")
                print("this")
                time.sleep(12)
                otaMeum(driver)
        else:
            time.sleep(10)
            go_back(driver)
            otaMeum(driver)
    except Exception as e:
        print(f"OTA update failed for device: {e}")


# 进入 OTA 菜单
def otaMeum(driver: WebDriver):
    print('进入 OTA 菜单')
    try:
        if wait_for_element_by_text(driver, '固件升级', 600):
            print('准备升级固件')
            if find_and_click_button_by_text(driver, ['固件升级']):
                print('点击固件升级按钮')
                time.sleep(2)
                find_and_click_button_by_xpath(driver, '//XCUIElementTypeStaticText[@name="点击检测"]')
                time.sleep(0.5)
                otaUpdate(driver)
    except Exception as e:
        print(f"OTA menu failed for device: {e}")


# 获取设备名称
def get_device_name(driver: WebDriver):
    try:
        device_info = driver.capabilities
        brand = device_info.get("deviceManufacturer", "unknown_device")
        serial = driver.session_id
        return f"{brand}_{serial}"
    except Exception as e:
        print(f"获取设备名称时发生错误: {e}")
        return "unknown_device"


# 记录升级日志
def log_upgrade_version(version_number, device_name, isSuccess, reason):
    log_file_name = f"{device_name}_upgrade_log.txt"

    with open(log_file_name, "a") as log_file:
        if isSuccess:
            log_file.write(
                f"Upgrade successful, version: {version_number}, timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        else:
            log_file.write(
                f"Upgrade fail reason: {reason}, version: {version_number}, timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Version {version_number} logged successfully in {log_file_name}.")


# 获取版本号
def get_version_number(driver: WebDriver):
    try:
        version_element = driver.find_element(by=AppiumBy.XPATH, value="//*[contains(@name, '当前版本')]")
        if version_element:
            full_text = version_element.text
            print(f"Found text: {full_text}")
            version_number = full_text.split("：")[-1]
            print(f"Version number: {version_number}")
            return version_number
    except Exception:
        print("Cannot find '当前版本' text.")
        return None


# 返回上一页
def go_back(driver: WebDriver):
    # driver.tap[33,86]
    # 创建 touch 指针输入（手势类型）
    driver.execute_script("mobile: tap", {"x": 33, "y": 86})


# 等待指定文本元素出现
def wait_for_element_by_text(driver: WebDriver, text, timeout):
    start_time = time.time()
    while True:
        try:
            element = driver.find_element(by=AppiumBy.NAME, value=text)
            print(f"Element with text '{text}' found!")
            return True
        except Exception:
            pass

        if time.time() - start_time > timeout:
            print(f"Timeout reached. Element with text '{text}' not found.")
            return False

        time.sleep(1)


# 启动监听失败弹框的线程
def start_failure_listener():
    threads = []
    for device in devices:
        thread = threading.Thread(target=listen_for_failure_popup, args=(device,))
        thread.daemon = True
        threads.append(thread)
        thread.start()


# 启动 OTA 升级的线程
def click_update_device(driver: WebDriver):
    print('begin check')
    otaUpdate(driver)


# 为每个设备启动一个线程来执行 OTA 更新
def click_update():
    threads = []
    for device in devices:
        thread = threading.Thread(target=click_update_device, args=(device,))
        threads.append(thread)
        thread.start()


if __name__ == '__main__':
    connectMobile()  # 假设只有一个设备
    start_failure_listener()
    click_update()
