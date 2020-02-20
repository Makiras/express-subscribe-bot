import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from module.kuaidi100 import *
from module.db import *
from module.sendmsg import *


class Corntab(object):

    def __init__(self, db_name: str, inc: int):
        '''
        db instance & time gap(s)
        '''
        super().__init__()
        self.db = SqLiteDb(db_name)
        self.inc = inc
        self.timer = BackgroundScheduler(timezone='Asia/Shanghai')
        self.timer.add_job(self.check_track, 'interval', id="Corntab_Check", seconds=self.inc, coalesce=True, misfire_grace_time=self.inc-20)

    def check_track(self):
        os.system("echo $(date '+%m/%d/%Y %H:%M:%S') 'Corntab Running' >> corntab.log")
        try:
            track_list = self.db.get_track_list()
            query_infos = BatchTrace(track_list).do_trace()
            
            return_diffs = []
            # old_ : str , new_ : list
            for ( tl , new_) in zip(track_list, query_infos):
                nu, userid, old_ = tl[0], tl[3], tl[2]
                # prevent empty str
                if old_ != "":
                    old_ = json.loads(old_)
                else:
                    old_ = []
                # compare and set diff
                if len(old_) == len(new_["data"]):
                    pass
                else:
                    self.db.update_track(nu, new_["data"])
                    sendTrackUpdate(userid, (nu, new_["data"][::-1][len(old_):]))
                    os.system("echo $(date '+%m/%d/%Y %H:%M:%S') '"+ json.dumps(new_["data"][::-1][len(old_):]) +"' >> corntab.log")
        except Exception as e:
            print(e)
            os.system("echo $(date '+%m/%d/%Y %H:%M:%S') 'Corntab ERR' >> corntab.log")


    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.shutdown()
