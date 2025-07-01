from cProfile import label

from connect import ConnectIos
from appium.webdriver.common.appiumby import AppiumBy as By
import time

driver = ConnectIos().connect_ios_device()
print(driver)

def buttons_all(btn='XCUIElementTypeButton'):
    buttons = driver.find_elements(By.CLASS_NAME, btn)
    return buttons

def img_all(img='XCUIElementTypeImage'):
    imgs = driver.find_elements(By.CLASS_NAME, img)
    return imgs

def video_num(name="new_shexiang"):
    videos = driver.find_elements(By.NAME, name)
    return videos

time.sleep(10)

driver.find_element(By.NAME, 'center enable').click()
time.sleep(2)
driver.find_element(By.NAME, '下一步').click()
time.sleep(2)
driver.find_element(By.NAME, '开始拍摄').click()
time.sleep(2)
driver.find_element(By.NAME, '跳过').click()
time.sleep(1)
#
# driver.tap([(706,164)],100)

# 获取整个屏幕的 XML 树（可能包含系统 UI）
# source = driver.page_source  # 或 driver.execute_script("mobile: source", {"format": "xml"})

buttons = driver.find_elements(By.CLASS_NAME,'XCUIElementTypeButton' )


# name = buttons_all()[1].get_attribute("name")
# print(f"name: {name}")

# 点击拍摄
buttons_all()[1].click()
n=0
while 1:
    # 拍摄十分钟
    time.sleep(600)
    n+=1
    print(f'拍摄了{n*10}分钟')
    if n == 48:
        buttons_all()[1].click()
        print('最后结束拍摄')
        break
    else:
        # 点击暂停
        buttons_all()[2].click()
        print(f'暂停了{n}次')
        # 暂停60秒
        time.sleep(60)
        # 继续拍摄
        buttons_all()[1].click()
        print(f'继续拍摄了{n}次')


# buttons_all()[1].click()
#
# n=0
# while 1:
#     # 拍摄十分钟
#     time.sleep(5)
#     n+=1
#     print(f'拍摄了{n*10}分钟')
#     if n == 10:
#         buttons_all()[1].click()
#         print('最后结束拍摄')
#         break
#     else:
#         # 点击暂停
#         buttons_all()[2].click()
#         print(f'暂停了{n}次')
#         # 暂停60秒
#         time.sleep(2)
#         # 继续拍摄
#         buttons_all()[1].click()
#         print(f'继续拍摄了{n}次')

time.sleep(1)
driver.find_element(By.NAME, 'recordView back').click()
time.sleep(2)
print(driver.find_element(By.NAME, 'new tabIcon 2 Default'))
driver.find_element(By.NAME, 'new tabIcon 2 Default').click()
print("回到本地文件")


if len(video_num()) == 1:
    print('本地文件有一条视频数据')
    time.sleep(2)
    video_num()[0].click()
    print('打开这一条视频数据')
    if len(driver.find_elements(By.NAME,'视频加载失败, 请稍后重试'))==1:
        print('视频播放失败')
    else:
        print('视频播放成功')
else:
    print(f'本地文件有{len(video_num())}条视频数据')





















