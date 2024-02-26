# This file is only for UST students to use illegally.
# v2.0
import configparser
import datetime
import json
import os
import time

import requests


class User:
    def __init__(self, cookie=None, auth=None, wecom_cid=None, wecom_secret=None, wecom_touid=None,
                 wecom_aid=None, wecom_on=None):
        self.cookie, self.auth, self.wecom_cid, self.wecom_secret, self.wecom_touid, self.wecom_aid, self.wecom_on = \
        list(zip(*self.get_config()))[1]

    def send_to_wecom(self, text):
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.wecom_cid}&corpsecret=" \
                        f"{self.wecom_secret}"
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        if access_token and len(access_token) > 0:
            send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
            data = {
                "touser": self.wecom_touid,
                "agentid": self.wecom_aid,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 600
            }
            response = requests.post(send_msg_url, data=json.dumps(data)).content
            return response
        else:
            return False

    def get_config(self):
        pre_dir = os.path.split(os.path.realpath(__file__))[0]
        config_path = os.path.join(pre_dir, 'config.ini')
        # print(config_path)
        conf = configparser.RawConfigParser()
        conf.read(config_path, encoding='utf-8')
        user_info = conf.items('user')
        # print(user_info)
        return user_info


class Booking:
    def __init__(self, booked_info=None, available_ground=[], facilityID=[2, 3, 4, 5, 79, 80, 100, 101],
                 time_status={}):
        self.booked_info = booked_info
        self.available_ground = available_ground
        self.facilityID = facilityID
        self.time_status = time_status

    def get_booked_info(self, cookie, auth):
        try:
            response = requests.get(
                url="https://w5.ab.ust.hk/msapi/fbs/bookingInfo/",
                params={
                    "ustID": "12345678",
                    "userType": "01",
                    "startDate":
                        datetime.datetime.now().strftime("%Y-%m-%d"),
                    "endDate": (datetime.datetime.now() + datetime.timedelta(days=15)).strftime("%Y-%m-%d"),
                },
                headers={
                    "Host": "w5.ab.ust.hk",
                    "Cookie": cookie,
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "USThing/6.7.4-iOS-b2de352f583a9bf2f0078f01c2547f2b",
                    "Accept-Language": "en-HK;q=1.0, zh-Hans-HK;q=0.9, zh-Hant-HK;q=0.8",
                    "Authorization": auth,
                    "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
                },
            )
            print('get_booked_info: Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            # print(response.content)
            content = response.json()
            # print(content)
            if content['message'] == 'Booking info not found':
                self.booked_info = []
                print('Booking info not found')
            else:
                self.booked_info = content['booking']
                print(f"Booking info: {self.booked_info}")
        except:
            print('get_booked_info: HTTP Request failed')

    @staticmethod
    def get_status(facility_id, cookie, auth):
        try:
            response = requests.get(
                url="https://w5.ab.ust.hk/msapi/fbs/facilityTimeslot",
                params={
                    "userType": "01",
                    "ustID": "12345678",
                    "facilityID": facility_id,
                    "startDate":
                        datetime.datetime.now().strftime("%Y-%m-%d"),
                    "endDate": (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d"),
                },
                headers={
                    "Host": "w5.ab.ust.hk",
                    "Cookie": cookie,
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": "USThing/6.7.4-iOS-b2de352f583a9bf2f0078f01c2547f2b",
                    "Accept-Language": "en-HK;q=1.0, zh-Hans-HK;q=0.9, zh-Hant-HK;q=0.8",
                    "Authorization": auth,
                    "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
                },
            )
            print('get_status: Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            content = response.json()
            print(content)
            return content
        except:
            print('get_status: HTTP Request failed')

    def release_status(self, cookie, auth):
        self.available_ground = []
        for id in self.facilityID:
            content = self.get_status(id, cookie, auth)
            for item in content['timeslot']:
                # print(item)
                if item['startTime'] == '09:00' or item['startTime'] == '10:00':
                    if item['timeslotStatus'] == 'Available':
                        self.available_ground.append(item)
                        print(self.available_ground)

    @staticmethod
    def post_booking(facilityID, timeslotDate, startTime, endTime, cookie, auth):
        try:
            response = requests.post(
                url="https://w5.ab.ust.hk/msapi/fbs/book/",
                params={
                    "userType": "01",
                    "ustID": "12345678",
                    "facilityID": facilityID,
                    "timeslotDate": timeslotDate,
                    "startTime": startTime,
                    "endTime": endTime,
                    "cancelInd": "N",
                },
                headers={
                    "Host": "w5.ab.ust.hk",
                    "Accept": "*/*",
                    "Content-Length": "0",
                    "Connection": "keep-alive",
                    "Cookie": cookie,
                    "User-Agent": "USThing/6.7.4-iOS-b2de352f583a9bf2f0078f01c2547f2b",
                    "Accept-Language": "en-HK;q=1.0, zh-Hans-HK;q=0.9, zh-Hant-HK;q=0.8",
                    "Authorization": auth,
                    "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
                },
            )
            print('post_booking: Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            if response.json()['message'] == 'Booking Result found':
                print('Booking Success')
                return True
        except requests.exceptions.RequestException:
            print('post_booking: HTTP Request failed')
            return False

    def ready_book(self, cookie, auth):
        for item in self.available_ground:
            if item['timeslotDate'] in self.time_status.keys():
                if self.time_status[item['timeslotDate']] == 'N':
                    self.post_booking(item['facilityID'], item['timeslotDate'], item['startTime'], item['endTime'],
                                      cookie, auth)
                    self.time_status[item['timeslotDate']] = "Y"

    def initial_time(self):
        for i in range(7):
            self.time_status.update({(datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d"): "N"})
        print("System initialized successfully!")

    def update_time_status(self):
        for item in self.booked_info:
            if item['timeslotDate'] in self.time_status:
                self.time_status[item['timeslotDate']] = "Y"


if __name__ == '__main__':
    user = User()
    user.get_config()
    book = Booking()
    book.initial_time()
    # print(user.auth)
    book.get_booked_info(user.cookie, user.auth)
    if user.wecom_on:
        user.send_to_wecom(f"Booked information: {book.booked_info}")
    book.update_time_status()
    while "N" in book.time_status.values():
        book.release_status(user.cookie, user.auth)
        book.ready_book(user.cookie, user.auth)
        time.sleep(30)
