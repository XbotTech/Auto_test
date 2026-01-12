import time
from pickle import PROTO

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.common import TimeoutException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from connect import ConnectIos
from appium.webdriver.webelement import WebElement
from typing import List
from common.screen_shot import getScreenShot
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from common.log import Logger
logger = Logger().get_logger()

# driver_ios = ConnectIos().connect_ios_device()
def find(driver, by, locator) -> WebElement:
    by = by.lower()
    if by == "id" or by == "resource-id":  # iOS 通常用 accessibility id
        by_locator = (By.ACCESSIBILITY_ID, locator)
    elif by == "name" or by == "content-desc":  # iOS 中的 name 类似 Android 的 content-desc
        by_locator = (By.NAME, locator)
    elif by == "class" or by == "class-name":
        by_locator = (By.CLASS_NAME, locator)
    elif by == "xpath":
        by_locator = (By.XPATH, locator)
    elif by == "predicate":  # iOS 特有的 Predicate 定位，功能强大
        by_locator = (By.IOS_PREDICATE, locator)
    elif by == "class-chain":  # iOS 特有的 Class Chain 定位
        by_locator = (By.IOS_CLASS_CHAIN, locator)
    else:
        raise AttributeError(f"元素定位方式未找到，你传入的是{by}")
    # ele = self.driver.find_elements(*by_locator)
    ele = WebDriverWait(driver, 10, poll_frequency=0.05).until(EC.visibility_of_element_located(by_locator),
                                                               message="元素定位异常")
    return ele


# 查找多个元素

def finds(driver, time, by, locator) -> List[WebElement]:
    try:
        by = by.lower()
        if by == "id" or by == "resource-id":  # iOS 通常用 accessibility id
            by_locator = (By.ACCESSIBILITY_ID, locator)
        elif by == "name" or by == "content-desc":  # iOS 中的 name 类似 Android 的 content-desc
            by_locator = (By.NAME, locator)
        elif by == "class" or by == "class-name":
            by_locator = (By.CLASS_NAME, locator)
        elif by == "xpath":
            by_locator = (By.XPATH, locator)
        elif by == "predicate":  # iOS 特有的 Predicate 定位，功能强大
            by_locator = (By.IOS_PREDICATE, locator)
        elif by == "class-chain":  # iOS 特有的 Class Chain 定位
            by_locator = (By.IOS_CLASS_CHAIN, locator)
        else:
            raise AttributeError(f"元素定位方式未找到，你传入的是{by}")

        # 使用 presence_of_all_elements_located 而不是 visibility_of_all_elements_located
        # 这样即使元素不可见但存在于DOM中也会被找到
        ele_s = WebDriverWait(driver, time).until(
            EC.presence_of_all_elements_located(by_locator),
            message="元素定位异常")
        return ele_s
    except TimeoutException:
        # 超时时返回空列表
        print(f"未找到元素: {by}={locator}，返回空列表")
        return []
    except Exception as e:
        # 其他异常也返回空列表
        print(f"元素查找异常: {e}，返回空列表")
        return []


def all_elements_located(driver, locator):
    ele_list = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, locator))
    )
    return ele_list


# 刷新完成元素获取
def sx(driver):
    all_button_ele = all_elements_located(driver, '//XCUIElementTypeButton[@name="shuaxin"]')
    print(f"刷新元素:{all_button_ele}")
    return all_button_ele


def disconnect_device(driver):
    """
    断开设备连接

    Args:
        driver: WebDriver实例
    """
    # 使用 finds 函数，找不到时返回空列表
    all_button_ele = sx(driver)
    # swipe_to_top(driver)
    if len(all_button_ele):
        disconnect_btns = finds(driver, 3, "xpath", '//XCUIElementTypeButton[@name="断开连接"]')
        if disconnect_btns:
            disconnect_btns[0].click()
            try:
                # 等待弹窗出现，最多等3秒
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(f"发现系统弹窗: {alert.text}")
                logger.info(f"发现系统弹窗: {alert.text}")
                alert.accept()
                print("已点击同意")
                logger.info("已点击同意")
            except TimeoutException:
                print("没有发现弹窗，继续下一步")
                logger.info("没有发现弹窗，继续下一步")
            print("✅ 已点击断开连接")
            logger.info("✅ 已点击断开连接")
        else:
            print("ℹ️ 未找到断开连接按钮，设备可能已断开")


# def connect_device(driver, device_name):
#     """
#     断开设备连接
#
#     Args:
#         driver: WebDriver实例
#     """
#     # 使用 finds 函数，找不到时返回空列表
#
#     connect_button_xpath = f"//XCUIElementTypeCell[.//XCUIElementTypeStaticText[@name='{device_name}']]//XCUIElementTypeButton[@name='连接']"
#
#     connect_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, connect_button_xpath))
#     )
#     print(f"设备 {device_name} 的连接按钮已找到")
#     logger.info(f"设备 {device_name} 的连接按钮已找到")
#     connect_button.click()
#     print(f"点击设备 {device_name} 的连接按钮成功")
#     logger.info(f"点击设备 {device_name} 的连接按钮成功")
#
#
# def swipe_to_top(driver):
#     """
#     滑动到顶部 - 简化版
#     """
#     try:
#         # 直接使用固定坐标
#         pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
#         actions = ActionBuilder(driver, mouse=pointer)
#
#         # 从屏幕中间(500, 800)滑动到顶部(500, 100)
#         actions.pointer_action.move_to_location(500, 800)
#         actions.pointer_action.pointer_down()
#         actions.pointer_action.move_to_location(500, 100)
#         actions.pointer_action.pointer_up()
#         actions.perform()
#
#         print("✅ 已滑动到顶部")
#     except Exception as e:
#         print(f"滑动失败: {e}")

def connect_device(driver, device_name, max_swipes=5):
    """
    连接设备，先查找设备，如果找不到则滑动查找，最多滑动5次

    Args:
        driver: WebDriver实例
        device_name: 设备名称
        max_swipes: 最大滑动次数，默认5次
    """

    def find_and_connect():
        """查找并连接设备"""
        try:
            connect_button_xpath = f"//XCUIElementTypeCell[.//XCUIElementTypeStaticText[@name='{device_name}']]//XCUIElementTypeButton[@name='连接']"

            connect_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, connect_button_xpath))
            )
            print(f"设备 {device_name} 的连接按钮已找到")
            logger.info(f"设备 {device_name} 的连接按钮已找到")
            connect_button.click()
            print(f"点击设备 {device_name} 的连接按钮成功")
            logger.info(f"点击设备 {device_name} 的连接按钮成功")
            return True
        except Exception as e:
            print(f"未找到设备 {device_name}: {str(e)}")
            return False

    # 第一次尝试查找设备
    print(f"第一次尝试查找设备: {device_name}")
    if find_and_connect():
        return

    # 如果第一次没找到，开始滑动查找
    for swipe_count in range(1, max_swipes + 1):
        print(f"第{swipe_count}次滑动查找设备: {device_name}")

        try:
            # 滑动屏幕
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions = ActionBuilder(driver, mouse=pointer)
            actions.pointer_action.move_to_location(500, 800)
            actions.pointer_action.pointer_down()
            actions.pointer_action.move_to_location(500, 100)
            actions.pointer_action.pointer_up()
            actions.perform()

            print(f"✅ 第{swipe_count}次滑动完成")
            time.sleep(2)  # 等待滑动后的内容加载

            # 滑动后尝试查找设备
            if find_and_connect():
                print(f"✅ 第{swipe_count}次滑动后找到设备 {device_name}")
                return

        except Exception as e:
            print(f"第{swipe_count}次滑动失败: {e}")

    # 如果滑动max_swipes次后还没找到，抛出异常
    error_msg = f"滑动{max_swipes}次后仍未找到设备 {device_name}"
    print(error_msg)
    logger.error(error_msg)
    raise Exception(error_msg)

def click_connection_for_device_while(driver, device_name):
    # //XCUIElementTypeButton[@name="shuaxin"]
    while 1:
        try:
            # 使用XPath定位并等待最多5秒
            frame_button = WebDriverWait(driver_ios, 5).until(
                EC.presence_of_element_located(("xpath", "//XCUIElementTypeButton[@name='Frame']"))
            )
            frame_button.click()  # 点击元素
        except TimeoutException:
            print("Frame button not found within 5 seconds")

        driver_ios.find_element(By.XPATH, "(//XCUIElementTypeButton[@name='更多'])[1]").click()
        time.sleep(5)
        disconnect_device(driver)
        if len(sx(driver)):
            # swipe_to_top(driver)
            connect_device(driver, device_name,max_swipes=5)
            # 等待设备名称元素出现
            time.sleep(3)
            try:
                # 等待弹窗出现，最多等3秒
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(f"发现系统弹窗: {alert.text}")
                alert.accept()
                print("已点击同意")
            except TimeoutException:
                print("没有发现弹窗，继续下一步")
            time.sleep(15)
            devices_list_eles = finds(driver, 5, "xpath", "//XCUIElementTypeStaticText[@name='设备列表']")
            if len(devices_list_eles) == 1:
                getScreenShot(driver, "未跳转到文件页")
                print(f"设备{device_name}连接失败,仍在设备列表页")
                logger.error(f"设备{device_name}连接失败,仍在设备列表页")
                find(driver, "xpath", '	//XCUIElementTypeButton[@name="BaseVC back btn"]')
            else:
                falcon_file_eles = finds(driver, 5, "xpath", "//XCUIElementTypeStaticText[@name='Falcon']")
                if len(falcon_file_eles) == 1:
                    print(f"已成功连接设备{device_name},成功跳转到文件页，并显示falocn文件")
                    logger.info(f"已成功连接设备{device_name},成功跳转到文件页，并显示falocn文件")
                elif len(falcon_file_eles) == 0:
                    getScreenShot(driver, "未找到文件页")
                    print(f"连接设备{device_name},跳转文件页后未显示falcon文件")
                    logger.error(f"连接设备{device_name},跳转文件页后未显示falcon文件")
                find(driver, "xpath", '//XCUIElementTypeButton[@name="new tabIcon 1 Default"]').click()


def click_frame_button_optional(driver, timeout=5, debug=False):
    """
    点击Frame按钮，可控制是否显示调试信息

    Args:
        driver: WebDriver实例
        timeout: 等待超时时间
        debug: 是否显示调试信息，默认False

    Returns:
        bool: 是否成功点击
    """
    try:
        frame_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(("xpath", "//XCUIElementTypeButton[@name='Frame']"))
        )
        frame_button.click()
        if debug:
            print("✅ Frame按钮点击成功")
        return True
    except TimeoutException:
        if debug:
            print(f"⚠️ Frame按钮在{timeout}秒内未找到")
        pass
    except Exception as e:
        if debug:
            print(f"❌ 点击Frame按钮时发生错误: {str(e)}")
        pass
    return False


def click_connection_for_device(driver, device_name, max_retries=3):
    """
    连接设备，失败后重试指定次数，无论成功与否都会点击new tab按钮

    Parameters:
    driver: WebDriver实例
    device_name: 设备名称
    max_retries: 最大重试次数，默认3次

    Returns:
    bool: 连接是否成功
    """
    connection_success = False

    # 重试循环
    for retry_count in range(max_retries):
        try:
            click_frame_button_optional( driver)
            print(f"\n=== 第{retry_count + 1}次尝试连接设备{device_name} ===")
            click_frame_button_optional(driver)
            driver.find_element(By.XPATH, "(//XCUIElementTypeButton[@name='更多'])[1]").click()
            time.sleep(5)
            disconnect_device(driver)

            if len(sx(driver)):
                # swipe_to_top(driver)
                connect_device(driver, device_name,max_swipes=5)
                # 等待设备名称元素出现
                time.sleep(3)

                try:
                    # 等待弹窗出现，最多等3秒
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    print(f"发现系统弹窗: {alert.text}")
                    alert.accept()
                    print("已点击同意")
                except TimeoutException:
                    print("没有发现弹窗，继续下一步")

                time.sleep(15)
                devices_list_eles = finds(driver, 5, "xpath", "//XCUIElementTypeStaticText[@name='设备列表']")

                if len(devices_list_eles) == 1:
                    getScreenShot(driver, "未跳转到文件页")
                    print(f"设备{device_name}连接失败,仍在设备列表页")
                    logger.error(f"设备{device_name}连接失败,仍在设备列表页")
                    find(driver, "xpath", '//XCUIElementTypeButton[@name="BaseVC back btn"]')

                    # 如果重试次数未用完，继续重试
                    if retry_count < max_retries - 1:
                        print(f"连接失败，准备第{retry_count + 2}次重试...")
                        continue
                    else:
                        connection_success = False
                        break
                else:
                    falcon_file_eles = finds(driver, 5, "xpath", "//XCUIElementTypeStaticText[@name='Falcon']")
                    if len(falcon_file_eles) == 1:
                        print(f"已成功连接设备{device_name},成功跳转到文件页，并显示falcon文件")
                        logger.info(f"已成功连接设备{device_name},成功跳转到文件页，并显示falcon文件")
                        connection_success = True
                        break  # 连接成功，跳出重试循环

                    elif len(falcon_file_eles) == 0:
                        getScreenShot(driver, "未找到文件页")
                        print(f"连接设备{device_name},跳转文件页后未显示falcon文件")
                        logger.error(f"连接设备{device_name},跳转文件页后未显示falcon文件")
                        connection_success = False

                        # 如果重试次数未用完，继续重试
                        if retry_count < max_retries - 1:
                            print(f"连接异常，准备第{retry_count + 2}次重试...")
                            continue
                        else:
                            break

            else:
                print("没有找到可连接的设备")
                if retry_count < max_retries - 1:
                    print(f"准备第{retry_count + 2}次重试...")
                    time.sleep(2)  # 重试前等待
                    continue
                else:
                    connection_success = False
                    break

        except Exception as e:
            print(f"连接过程中出现异常: {str(e)}")
            logger.error(f"连接设备{device_name}时出现异常: {str(e)}")

            if retry_count < max_retries - 1:
                print(f"异常发生，准备第{retry_count + 2}次重试...")
                time.sleep(2)  # 异常后等待
                continue
            else:
                connection_success = False
                break

    # 无论连接成功与否，都点击new tab按钮
    try:
        print("\n=== 尝试点击new tab按钮 ===")
        new_tab_btn = driver.find_element(
            By.XPATH, '//XCUIElementTypeButton[@name="new tabIcon 1 Default"]'
        )
        new_tab_btn.click()
        print("已点击new tab按钮")
    except Exception as e:
        print(f"点击new tab按钮失败: {str(e)}")

    # 返回连接结果


# driver = webdriver.Remote(...)  # 初始化Appium driver
# click_connection_for_device(driver, "XbotGo-3efd93")```

if __name__ == '__main__':
    driver_ios = ConnectIos().connect_ios_device()
    driver_ios.implicitly_wait(5)
    # click_connection_for_device_while(driver_ios, "aaaa")
    click_connection_for_device(driver_ios, "Xbt-F-5127")
