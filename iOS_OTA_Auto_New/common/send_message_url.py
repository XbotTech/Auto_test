import requests
import json
import time

from urllib3 import request


class SendReportMessage:
    @staticmethod
    def send_talk_message(data):
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a5cb1336-d6a5-4e0f-ba54-3104fe1b6f69"
        uploads = {"text": {"content": data}, "msgtype": "text"}
        response = requests.post(url=url, json=uploads)
        result = response.json()
        print(f'机器人发送结果：{result}')
    # @staticmethod
    # def send_talk_message():
    #     url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a5cb1336-d6a5-4e0f-ba54-3104fe1b6f69"
    #     uploads = {
    #         "msgtype": "template_card",
    #         "template_card": {
    #             "card_type": "text_notice",
    #             "source": {
    #                 "icon_url": "https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
    #                 "desc": "企业微信",
    #                 "desc_color": 0
    #             },
    #             "main_title": {
    #                 "title": "欢迎使用企业微信",
    #                 "desc": "您的好友正在邀请您加入企业微信"
    #             },
    #             "emphasis_content": {
    #                 "title": "丹鹭哥",
    #                 "desc": "少打点！！！"
    #             },
    #             "quote_area": {
    #                 "type": 1,
    #                 "url": "https://work.weixin.qq.com/?from=openApi",
    #                 "appid": "APPID",
    #                 "pagepath": "PAGEPATH",
    #                 "title": "引用文本标题",
    #                 "quote_text": "Jack：企业微信真的很好用~\nBalian：超级好的一款软件！"
    #             },
    #             "sub_title_text": "下载企业微信还能抢红包！",
    #             "horizontal_content_list": [
    #                 {
    #                     "keyname": "邀请人",
    #                     "value": "张三"
    #                 },
    #                 {
    #                     "keyname": "企微官网",
    #                     "value": "点击访问",
    #                     "type": 1,
    #                     "url": "https://work.weixin.qq.com/?from=openApi"
    #                 },
    #             ],
    #             "jump_list": [
    #                 {
    #                     "type": 1,
    #                     "url": "https://work.weixin.qq.com/?from=openApi",
    #                     "title": "企业微信官网"
    #                 },
    #
    #             ],
    #             "card_action": {
    #                 "type": 1,
    #                 "url": "https://work.weixin.qq.com/?from=openApi",
    #                 "appid": "APPID",
    #                 "pagepath": "PAGEPATH"
    #             }
    #         }
    #     }
    #     response = requests.post(url=url, json=uploads)
    #     result = response.json()
    #     print(f'机器人发送结果：{result}')


if __name__ == "__main__":
    # 配置企业微信Webhook URL（必须替换为实际URL）
    SendReportMessage.send_talk_message()

