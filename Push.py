# This program is only for personal use in HKUST
import argparse
import json
import time
from datetime import datetime
import requests


class Information:
    def __init__(self):
        # input your own information(only id)
        self.ustID =
        self.date = 'None'
        self.hour = 'None'
        self.facilities = [0, 1, 2, 3]

    def initialize(self):
        parser = argparse.ArgumentParser()
        parser.description = '''
        This program is only for personal use in HKUST.
        It can help you book facilities automatically.
        Default time is Today's Next hour.
        DO NOT ABUSE THIS PROGRAM'''
        parser.add_argument("-d", "--date", help="The date you want to book.", type=str,
                            default=datetime.now().strftime("%Y-%m-%d"))
        parser.add_argument("-t", "--time", help="The hour you want to book", type=str,
                            default=str(datetime.now().hour+1)+":00")
        args = parser.parse_args()
        self.date = args.date
        self.hour = args.time

    def status(self):
        for i in range(4):
            response = requests.get(
                url="https://w5.ab.ust.hk/msapi/fbs/facilityTimeslot",
                params={
                    "facilityID": i+2,
                    "userType": "01",
                    "ustID": self.ustID,
                    "startDate": self.date,
                    "endDate": self.date,
                },
                headers={
                    "Host": "w5.ab.ust.hk",
                    "Accept": "application/json, text/plain, */*",
                    "Connection": "keep-alive",
                    "If-None-Match": "0",
                    "Cookie": "language=en-US",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhcyJ9.eyJqdGkiOiJTVC0xNDc3LXBHelRqTkRiR3hxaUtqVVVHekp6WTBXelVuTWNhczIiLCJpc3MiOiJodHRwczovL2Nhcy51c3QuaGsvY2FzL29pZGMiLCJhdWQiOiIyMDAwMiIsImV4cCI6MTY5MTE2NTQ0MCwiaWF0IjoxNjkxMTM2NjQwLCJuYmYiOjE2OTExMzYzNDAsInN1YiI6Imd5YW5hZCIsImFtciI6WyJMZGFwQXV0aGVudGljYXRpb25IYW5kbGVyIiwiSEtVU1QgQ0FTIl0sInN0YXRlIjoidDE2OTExMzY1OTQ1NDEiLCJub25jZSI6IiIsImF0X2hhc2giOiI0TDBfcnZjeV9YMkk4Nm5fZGFydFZRIiwiZGVwYXJ0bWVudE51bWJlciI6IkVDRSIsImVtYWlsIjoiZ3lhbmFkQGNvbm5lY3QudXN0LmhrIiwiZW1wbG95ZWVUeXBlIjoic3R1ZGVudCIsIm5hbWUiOiJZQU4sIEdlbiIsIm91IjpbIlBvc3RncmFkdWF0ZSIsIkFETUlTIFVzZXIiLCJTdHVkZW50IiwiVGF1Z2h0IFBvc3RncmFkdWF0ZSJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJneWFuYWQifQ.tS7iCoCg3jFikUOYUCugzP8JYjiSe_wM0UoDTcRWyiF6J1J438JJ-AB0vOEraQKw6pcznKu3Kkyo6DOyHDqbk6_gjMSHsGSKAyqeDtv-wxoQc985jex3vTNJ4ZlNxabRvY_DMlJau4QgGRXJsAokJSpM0o6SJYucGl7ZAa1AO9nbYL1PaVK7lcyGEJMnvLdVIQDizHu6hmVqkXphNW4BSHw0JDzJHsFGqO-xChfi7v4F8H7qdajxsRNIGQeWeoK5Er9E3kswQx7uc7JqDqI7lU8vjgkVYdGREBtAwAQml_7U5Mrv8LL-rNhwQFiFdGb8EfWVfG_ydJ4Y9WpkP3O4fA",
                    "Accept-Encoding": "gzip, deflate, br",
                    "User-Agent": "HKUST%20Student/2023081102 CFNetwork/1485 Darwin/23.1.0",
                },
            )
            # print('Response HTTP Status Code: {status_code}'.format(
            #     status_code=response.status_code))
            # print('Response HTTP Response Body: {content}'.format(
            #     content=response.content))
            self.facilities[i] = response.json()['timeslot']
            # print(self.facilities)

    def check(self, status):
        for i in range(4):
            # print(len(status[i]))
            # print(status[i])
            for j in range(len(status[i])):
                if status[i][j]['startTime'] == self.hour and status[i][j]['timeslotStatus']=='Available':
                    print("Check successful")
                    we_sys = SysSend()
                    # input your own wecom account
                    we_sys.send_to_wecom("HKUST FACILITIES BOOKING\n--------------\nFound the available count.\nCount: "
                                         + str(status[i][0]['facilityID']-1) + '\n' + self.date + '-' +
                                         self.hour, "", "",
                                  "",
                                  "@all")
                    return True
            print('Now is finding in Count' + str(status[i][0]['facilityID']-1) + ' in ' + self.hour)
        print('----------------'+str(datetime.now().strftime("%H:%M:%S")) + '----------------------')
        return False


class SysSend:
    @staticmethod
    def send_to_wecom(text, wecom_cid, wecom_aid, wecom_secret, wecom_touid):
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
            data = {
                "touser": wecom_touid,
                "agentid": wecom_aid,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 600
            }
            response = requests.post(send_msg_url, data=json.dumps(data)).content
            return True
        else:
            return False


if __name__ == '__main__':
    user_data = Information()
    user_data.initialize()
    user_data.status()
    while True:
        if user_data.check(user_data.facilities):
            break
        print("NO AVAILABLE")
        time.sleep(10)



