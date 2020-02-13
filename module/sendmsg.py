import requests

token = "SET YOUR TELEGRAM TOKEN"
rurl = "https://api.telegram.org/bot{}/{}"
req = requests.Session()

req.post(
    url=rurl.format(token, "setWebhook"),
    data={
        "url":"https://YOUR_WEB_URL/ENCRYPT_PATH"
    }
)

def sendTrackUpdate(userid, trackinfo):
    '''
    track info : (track_number, diff_route)
    '''
    msgStr = "快递单号:"+trackinfo[0]+"\n"
    msgStr = msgStr + "物流更新:\n"
    for status in trackinfo[1]:
        msgStr = msgStr + status["ftime"] + "\n" \
            + status["context"] + "\n"

    sendMessage(userid, msgStr)


def sendMessage(userid, msgStr):
    req.post(
        url=rurl.format(token, "sendMessage"),
        data={
            "chat_id": userid,
            "text": msgStr}
    )
    
if __name__ == "__main__":
    sendMessage("","TEST MSG\n for format")    