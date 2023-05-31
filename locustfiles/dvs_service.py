import locust_plugins
import csv
import logging

import os

from locust import HttpUser, task, between, SequentialTaskSet, events, runners
from locust.exception import StopUser
import json
import src

agentidFileName = "agentId.csv"

userData = []

agentIdData = None
store_code = "03003014055"

client_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzVG9rZW4iOiJkdnNFbmNyeXB0S2V5MTIzIiwic2VydmVyTmFtZSI6IkRTT19TZXJ2ZXIiLCJleHAiOjMzMjEyNTIxOTc2LCJpYXQiOjE2NzY1MjE5NzZ9.72BKK4Nx__rkVSkbhP8x-AmdIX0X_2b5tcjCbLJ3n_Y"

def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def checkFile(filename):
    if not os.path.exists(filename):
        f =open(filename, 'w')
        f.close()

class DVS_Login(SequentialTaskSet):
    publicKeyExponent = "10001"
    publicKeyModulus = ""
    access_token = ""

    username = ""

    agentId = ""

    pushServerId = ""

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        logging.info("======on_test_start=====")
        with open("data\\userdata100.csv", 'r') as file:
            logging.info("read cvs")
            reader = csv.reader(file)
            global userData
            userData = list(reader)

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        logging.info("======on_test_stop=====")


    def on_start(self):
        print('-----------on_start-----------')

    def on_stop(self):
        print('-----------on_stop-----------')

    @task
    def login(self):

        if len(userData) > 0:
            self.username = userData.pop()[0]
            logging.info("username : " + self.username)

        with self.client.get("/api/agent/auth", name='auth', catch_response=True) as response:
            if response.status_code != 200:
                response.failure("getToken Fail!!!!!!!!!")
            else:
                respJson = json.loads(response.content)
                self.publicKeyModulus = respJson['publicKeyModulus']
                self.access_token = respJson['accessToken']

        #login
        password = src.rsaEncryption.encryptText(self.publicKeyExponent, self.publicKeyModulus, "rc5x2013")
        with self.client.post("/api/agent/login", name='loginUser', catch_response=True,
                              headers={"private_access_token": self.access_token},
                              json={"username": self.username, "password": password}) as response:

            jsonParse = json.loads(response.content)
            try:
                # logging.info("agent/login : " + jsonParse['agentId'])
                self.agentId = jsonParse['agentId']
            except:
                # logging.info("username : " + self.username)
                logging.info("password : " + password)
                logging.info("publicKeyModulus : " + self.publicKeyModulus)
                logging.info("access_token : " + self.access_token)
                logging.info("agent/login : " + str(jsonParse))

        #loginOK
        with self.client.post("/api/agent/loginOk", name='loginOK', catch_response=True,
                              headers={"access_token": self.access_token},
                              json={"agentId": self.agentId, "pushServerId": self.pushServerId}) as response:

            jsonParse = json.loads(response.content)
            if jsonParse['retcode'] != '100':
                logging.info("loginok error : " + str(jsonParse))
                logging.info("agentId error : " + self.agentId)
                response.failure("loginok fail")

    @task
    def logout(self):
        response = self.client.post("/api/agent/logout", name='logout',
                                    headers={"access_token": self.access_token},
                                    json={"agentId": self.agentId})


class DVS_staff_assign(SequentialTaskSet):

    access_url = ""

    def on_start(self):
        print('-----------test Start-----------')

    @task
    def staffStatus(self):
        with self.client.post("/api/dso/staffStatus", name='staffStatus', catch_response=True,
                              headers={"access_token": client_access_token},
                              json={"storeCode": store_code, "serviceCategory": "0"}) as response:
            respJson = json.loads(response.content)
            #logging.info("staffStatus : " + str(respJson))
            if respJson['retcode'] != '100':
                response.failure("staff status return value error!!")
                raise StopUser()
            elif respJson['availability'] == '0':
                response.failure("availability is 0")
                #logging.info("staffStatus fail. availibility is 0")
                raise StopUser()

    @task
    def staffAssign(self):
        with self.client.post("/api/dso/staffAssign", name='staffAssign', catch_response=True,
                              headers={"access_token": client_access_token},
                              json={"serviceCategory": "0", "usedAvatar": "0"}) as response:
            respJson = json.loads(response.content)
            #logging.info("staffStatus : " + str(respJson))
            if respJson['retcode'] != '100':
                response.failure("staffAssign Fail!!!!!!!!!")
                raise StopUser()
            else:
                #logging.info("staffAssign return : " + str(respJson))
                self.access_url = respJson['accessURL'].split('=')[1]

    @task
    def get_info(self):
        with self.client.get("/api/host/dso/info/" + self.access_url, name='getInfo', catch_response=True,
                              json={"serviceCategory": "0", "usedAvatar": "0"}) as response:
            respJson = json.loads(response.content)
            #logging.info("access_url : " + str(respJson))
            if respJson['retcode'] != '100':
                response.failure("getInfo Fail!!!!!!!!! : " + str(respJson))
                raise StopUser()
            else :
                #logging.info("get_info return : " + str(respJson))
                assigned_agent = respJson['agentId']


class DVS_login_logout(HttpUser):
    host = "https://stapdcm.remotevs.com"
    #checkFile(agentidFileName)

    tasks = [DVS_Login]
    # task간 5~10초 대기
    wait_time = between(5, 10)


class DVS_staff_assign(HttpUser):
    host = "https://stapdcm.remotevs.com"

    tasks = [DVS_staff_assign]
    # task간 5~10초 대기
    #wait_time = between(5, 10)

