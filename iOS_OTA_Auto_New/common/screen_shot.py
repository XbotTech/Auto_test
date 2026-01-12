import os
import allure
# import pyscreenshot as ImageGrab
# import time
from datetime import datetime

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone


def getScreenShot(driver, name):
    """
    截取屏幕截图（兼容旧版本）
    """
    try:
        print(name)

        # 确保目录存在
        screenshot_dir = os.path.join(project_path, 'screen_shot')
        os.makedirs(screenshot_dir, exist_ok=True)

        currTime = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(screenshot_dir, f"{name}_{currTime}.png")

        driver.save_screenshot(filename)
        print(f"截图成功: {filename}")

        return filename

    except Exception as e:
        print(f"截图失败: {e}")
        return None
