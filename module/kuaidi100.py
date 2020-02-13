import requests
import json
import time
import random

user_agent = "REPLACE YOUR USER AGENT HERE"
req = requests.Session()


class Company(object):

    def __init__(self, track_number: str):
        super().__init__()
        self.nu = track_number
        self.company_list = []

    def get_res_list(self) -> list:
        raw_res = req.get(
                "https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text="+self.nu,
                headers=self.gen_header()
                )
        lists = json.loads(raw_res.text)["auto"]
        for obj in lists:
            self.company_list.append(obj["comCode"])
        return self.company_list

    def gen_header(self) -> dict:
        headers = {
                "origin": "https://www.kuaidi100.com",
                "referer": "https://www.kuaidi100.com/",
                "user-agent": user_agent,
                }
        return headers


class TrackInfo(object):

    def __init__(self, track_number, company_list, phone_number):
        super().__init__()
        self.nu = track_number
        self.company_list = company_list
        self.phone = phone_number

    def get_track_info(self) -> dict:
        if len(self.company_list)==0:
            self.company_list=["shentong"]
        for cpn in self.company_list:
            url = "https://www.kuaidi100.com/query?type="+cpn \
                    + "&postid=" + self.nu + "&temp=" + str(random.random())\
                    + "&phone="
            if cpn == "shunfeng":
                raw_res = req.get(url+self.phone, headers=self.gen_header())
            else:
                raw_res = req.get(url, headers=self.gen_header())

            if json.loads(raw_res.text)['status'] == "200":
                return json.loads(raw_res.text)
        return json.loads(raw_res.text)

    def gen_header(self) -> dict:
        headers = {
                "origin": "https://www.kuaidi100.com",
                "referer": "https://www.kuaidi100.com/",
                "user-agent": user_agent,
                }
        return headers


class BatchTrace(object):

    def __init__(self, track_infos: list):
        super().__init__()
        self.track_infos = track_infos

    def do_trace(self) -> list:
        res = []
        for info in self.track_infos:
            try:
                res.append(
                        TrackInfo(info[0], Company(info[0]).get_res_list(),
                            info[1]).get_track_info()
                        )
            except:
                res.append(
                        json.loads("{'message':'','nu':'','ischeck':'0','condition':'','com': '','status':'201','state':'0','data':[]}")
                        )
            time.sleep(0.8)
        return res


if __name__ == "__main__":
    batch = BatchTrace([["number","phone"]])
    print(batch.do_trace())
    pass
