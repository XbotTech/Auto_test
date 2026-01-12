import time

from appium.webdriver.common.appiumby import AppiumBy as By
from common.log import Logger


'''
basepage.find/finds 方法的装饰器，用于处理黑名单弹框，保证业务进行
'''
logging = Logger(__name__).get_logger()


def handle_black(fun):
    def run(*args, **kwargs):
        # 核心修改：直接判断函数名
        # if fun.__name__ == "get_toast_text":
        #     # 直接执行并返回结果，不进行任何异常处理
        #     return fun(*args, **kwargs)

        # 原有黑名单逻辑（仅处理非Toast函数）
        black_list = [(By.XPATH, '//XCUIElementTypeButton[@name="Frame"]')]
        by_self = args[0]

        try:
            return fun(*args, **kwargs)
        except Exception as e:
            # 非Toast函数仍执行黑名单处理
            for black in black_list:
                logging.info(f"处理黑名单元素: {black}")
                eles = by_self.driver.find_elements(*black)
                if eles:
                    eles[0].click()
                    time.sleep(1)
                    return fun(*args, **kwargs)
            raise e

    return run




