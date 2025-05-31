from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random
import os
import numpy as np
from common.log import Logger

logger = Logger().get_logger()

last_clicked = None



def highlight_and_click(driver, element, duration=1.0):
    """3D按压效果的强烈点击动画"""
    original_style = element.get_attribute("style") or ""

    # 初始状态
    driver.execute_script("""
        arguments[0].style.transform = 'translateZ(0)';
        arguments[0].style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        arguments[0].style.boxShadow = '0 4px 8px rgba(0,0,0,0.2), 0 0 0 3px #FF5722';
    """, element)

    time.sleep(duration * 0.3)

    # 按下效果
    driver.execute_script("""
        arguments[0].style.transform = 'translateY(2px) scale(0.98)';
        arguments[0].style.boxShadow = '0 2px 4px rgba(0,0,0,0.2), 0 0 0 5px #FF0000';
        arguments[0].style.filter = 'brightness(0.9)';
    """, element)

    # 执行点击
    element.click()

    time.sleep(duration * 0.3)

    # 弹起效果
    driver.execute_script("""
        arguments[0].style.transform = 'translateY(0) scale(1.02)';
        arguments[0].style.boxShadow = '0 6px 12px rgba(0,0,0,0.2), 0 0 0 8px rgba(255,0,0,0.5)';
        arguments[0].style.filter = 'brightness(1.1)';
    """, element)

    time.sleep(duration * 0.4)

    # 恢复原样式
    driver.execute_script(f"""
        arguments[0].style = '{original_style}';
    """, element)


def scoreboard_automation(url):
    chrome_driver_path = os.path.dirname(os.path.abspath(__file__)) + "/chrome_driver_auto/driver/chromedriver.exe"
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    # 直接滚动1/3处
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
    home_input_ele = '//div[text()="客队得分"]/preceding::input[@class="_scoreInput_1y8f2_35"]'
    away_input_ele = '//div[text()="客队得分"]/following::input[@class="_scoreInput_1y8f2_35"]'
    home_plus_ele = '//div[text()="客队得分"]/preceding::span[@aria-label="plus"]'
    home_minus_ele = '//div[text()="客队得分"]/preceding::span[@aria-label="minus"]'
    away_plus_ele = '//div[text()="客队得分"]/following::span[@aria-label="plus"]'
    away_minus_ele = '//div[text()="客队得分"]/following::span[@aria-label="minus"]'
    try:
        while 5343645346:
            # 获取第一个输入框的值
            value1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
            # 获取第二个输入框的值
            value2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')

            # 尝试转换为整数
            num1 = int(value1)
            num2 = int(value2)

            # 检查是否都是5的倍数
            if num1 % 5 == 0 and num2 % 5 == 0:
                driver.refresh()
                # 直接滚动1/3处
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
                logger.info('两队分数都是5的倍数,刷新当前页面')
                time.sleep(3)
                v1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
                v2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')
                logger.info(f'当前主客队的比分为{v1}:{v2}')

            choice_list = ['home_plus', 'home_minus', 'away_plus', 'away_minus', 'manual_input', "section_choice"]
            # 分配权重
            probabilities = [0.2, 0.2, 0.2, 0.2, 0.1, 0.1]
            operation = np.random.choice(choice_list,p=probabilities)

            if operation == 'home_plus':
                # home_plus = driver.find_element(By.XPATH, home_plus_ele)
                highlight_and_click(driver, driver.find_element(By.XPATH, home_plus_ele))
                # home_plus.click()
                logger.info('点击了主队+按钮')
                v1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
                v2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')
                logger.info(f'当前主客队的比分为{v1}:{v2}')


            elif operation == 'home_minus':
                # home_minus = driver.find_element(By.XPATH, home_minus_ele)
                # home_minus.click()
                highlight_and_click(driver, driver.find_element(By.XPATH, home_minus_ele))
                logger.info("点击了主队-按钮")
                v1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
                v2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')
                logger.info(f'当前主客队的比分为{v1}:{v2}')

            elif operation == 'away_plus':
                # away_plus = driver.find_element(By.XPATH, away_plus_ele)
                # away_plus.click()
                highlight_and_click(driver, driver.find_element(By.XPATH, away_plus_ele))
                logger.info("点击了客队+按钮")
                v1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
                v2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')
                logger.info(f'当前主客队的比分为{v1}:{v2}')


            elif operation == 'away_minus':
                # away_minus = driver.find_element(By.XPATH, away_minus_ele)
                # away_minus.click()
                highlight_and_click(driver, driver.find_element(By.XPATH, away_minus_ele))
                logger.info("点击了客队-按钮")
                v1 = driver.find_element(By.XPATH, home_input_ele).get_attribute('value')
                v2 = driver.find_element(By.XPATH, away_input_ele).get_attribute('value')
                logger.info(f'当前主客队的比分为{v1}:{v2}')

            elif operation == 'manual_input':
                # 随机生成比分
                home_score = random.randint(0, 999)
                away_score = random.randint(0, 999)

                home_input = driver.find_element(By.XPATH, home_input_ele)
                home_input.clear()
                home_input.send_keys(str(home_score))

                away_input = driver.find_element(By.XPATH, away_input_ele)

                away_input.clear()
                away_input.send_keys(str(away_score))
                logger.info(f"手动输入比分: 主队 {home_score} - 客队 {away_score}")

            elif operation == 'section_choice':
                buttons = {
                    "1ST": (By.XPATH, '//div[text()="1ST"]'),
                    "2ND": (By.XPATH, '//div[text()="2ND"]'),
                    "3RD": (By.XPATH, '//div[text()="3RD"]')
                }

                available = [name for name in buttons.keys() if name != last_clicked]
                chosen = random.choice(available)
                locator_type, locator_value = buttons[chosen]
                driver.find_element(locator_type, locator_value).click()
                logger.info(f'这一次点击的是{chosen}')
                global last_clicked
                last_clicked = chosen
                time.sleep(1)

            # 间隔1-3秒
            time.sleep(random.uniform(1, 3))
    except Exception as e:
        logger.error(f"测试中断，错误信息{e}")
        raise e




# //div[text()="客队得分"]/preceding::span[@aria-label="plus"]
# //div[text()="客队得分"]/preceding::span[@aria-label="minus"]
# //div[text()="客队得分"]/following::span[@aria-label="plus"]
# //div[text()="客队得分"]/following::span[@aria-label="minus"]
# //div[text()="客队得分"]/preceding::input[@class="_scoreInput_1y8f2_35"]
# //div[text()="客队得分"]/following::input[@class="_scoreInput_1y8f2_35"]
if __name__ == '__main__':
    scoreboard_automation(
        "https://mix.blinktech.com.cn/scorer?region=CN&bizId=3E738D568B034266B4C9BB13A938D6CB&lang=zh_CN")
