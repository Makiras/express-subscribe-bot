#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from module import *
from flask import Flask, request

db_addr = "./track.sqlite"
timer_d = Corntab(db_addr, inc=300)
timer_d.check_track()

app = Flask(__name__)


@app.route("/ENCRYPT_PATH", methods=["GET", "POST"])
def handle():
    db = SqLiteDb(db_addr)
    req_dict = request.get_json()["message"]
    print(json.dumps(req_dict))
    userid = req_dict["chat"]["id"]
    if userid<0:
        return ""
    userid = str(userid)
    commands = req_dict["text"].split()

    if db.check_user(userid)==False:
        sendmsg.sendMessage(userid, "请先使用 /setup 设置后四位")

    if commands[0] == "/add":
        if len(commands) == 2:
            flag = db.creat_track(userid, commands[1])
        elif len(commands) == 3:
            flag = db.creat_track(userid, commands[1], commands[2])
        else:
            flag = False
        if flag:
            sendmsg.sendMessage(userid, "添加成功")
            check_detail(db,commands[1])
        else:
            sendmsg.sendMessage(userid, "添加失败，未知错误")

    elif commands[0] == "/delete":
        if len(commands) == 2:
            flag = db.del_track(commands[1])
        else:
            flag = False
        if flag:
            sendmsg.sendMessage(userid, "删除成功")
        else:
            sendmsg.sendMessage(userid, "删除失败，未知错误")

    elif commands[0] == "/setup":
        if len(commands) == 2:
            if db.check_user(userid):
                flag = db.update_user(userid, commands[1])
            else:
                flag = db.creat_user(userid, commands[1])
        else:
            flag = False
        if flag:
            sendmsg.sendMessage(userid, "更新成功")
        else:
            sendmsg.sendMessage(userid, "更新失败，未知错误")

    elif commands[0] == "/detail":
        if len(commands) == 2:
            check_detail(db,commands[1])
        else:
            flag = False
    
    elif commands[0] == "/list":
        info_list = db.get_user_track_list(userid)
        msgStr = "受跟踪快递单号有:\n"
        for info in info_list:
            msgStr = msgStr + info[0] + "\n"
            msgStr = msgStr + \
                time.strftime("%Y-%m-%d %H:%M:%S",
                              time.localtime(info[1])) + "\n"
        sendmsg.sendMessage(userid, msgStr)

    elif commands[0] == "/start":
        sendmsg.sendMessage(userid, "欢迎使用Makiras' bugot\n"
                            "请使用 /setup 命令设置手机号后四位以用于顺丰查询")

    return ""


def check_detail(db:SqLiteDb, track_number: str):
    info_list = db.get_track(track_number)
    track_info = TrackInfo(info_list[1], Company(info_list[1]).get_res_list(),
                           info_list[2]).get_track_info()
    if track_info["status"]!="200":
        msgStr = track_info["message"] + "\n"
        msgStr = msgStr + "可能是未揽收，仍然为您添加追踪"
        db.update_track(track_number, track_info["data"])
    else:
        msgStr = "快递单号:" + track_number + "\n"
        for status in track_info["data"]:
            msgStr = msgStr + status["ftime"] + "\n" \
                + status["context"] + "\n"
        db.update_track(track_number, track_info["data"])
    sendmsg.sendMessage(info_list[0], msgStr)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1081)
