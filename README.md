# express-subscribe-bot

A telegram bot which use kuadi100 interface for subscribing express notice. **顺丰 Support**

## Parameter need modify

|File Name|Location|Usage|
|---|---|---|
|run.py|Line7: db_addr| set database file|
|run.py|Line8: inc| set query loop time gap, in seconds|
|run.py|Line14: ENCRYPT_PATH| set query path for webhook protect|
|run.py|Line105: | set Flask param|
|module/sendmsg.py|Line3: token|tg bot token|
|module/sendmsg.py|Line10: |set query url&path for webhook|
|module/sendmsg.py|Line36: |your id for message sending test|
|module/kuaidi100.py|Line3: user_agent|user_agent for query (**TRY MACOS**)|
|module/kuaidi100.py|Line92: nu/phone|track_number for kuaidi100 test|

## Some bugs which may happen while you debuging  

1. kuaidi100 query response unknown error, such as wrong number. Try other user agent.

## Database Tables

1. user_list

    |userid| phone|
    |---|---|
    |Str|Str|

2. track_list

    |userid|track_number|phone|trace_route|ins_time|
    |---|---|---|---|---|
    |Str|Str|Str|Str|Int|

3. trace_route utf8 encode

```
[
    {
        "time": "2020-02-13 00:43:33", 
        "ftime": "2020-02-13 00:43:33", 
        "context": "\u3010\u77f3\u5bb6\u5e84\u8f6c\u8fd0\u4e2d\u5fc3\u516c\u53f8\u3011 \u5df2\u6536\u5165",
        "location": ""
    }
]
```

## Env

```
Ubuntn 18.04.3 LTS  
AWS t2.nano  
200 MB bandwith per month
```