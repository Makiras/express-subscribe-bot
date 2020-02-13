import sqlite3
import time
from module.kuaidi100 import *

'''
    Table: user_list, track_list
    Co: user_list   -> userid, phone
        track_list  -> userid, track_number, phone, trace_route, ins_time
'''


class SqLiteDb(object):

    def __init__(self, db_addr):
        super().__init__()
        try:
            self.db = sqlite3.connect(db_addr, check_same_thread=False)
            self.cursor = self.db.cursor()
        except:
            print("[ERROR]: NO DB FILE FOUND.")
            assert False

    def __del__(self):
        self.db.close()

    def creat_user(self, userid: str, phone: str) -> bool:
        print("C")
        try:
            assert len(phone) == 4
            self.cursor.execute(
                "INSERT INTO user_list (userid, phone) VALUES (?,?)",
                (userid, phone)
            )
            self.db.commit()
        except:
            return False
        return True

    def del_user(self, userid: str) -> bool:
        try:
            self.cursor.execute(
                "DELETE FROM user_list WHERE userid=?",
                (userid,)
            )
            self.cursor.execute(
                "DELETE FROM track_list WHERE userid=?",
                (userid,)
            )
            self.db.commit()
        except:
            return False
        return True

    def check_user(self, userid: str) -> bool:
        try:
            cursor_ = self.cursor.execute(
                "SELECT * FROM user_list WHERE userid=?",
                (userid,))
            return bool(len([i for i in cursor_]))
        except:
            return False

    def update_user(self, userid: str, phone: str) -> bool:
        try:
            assert len(phone) == 4
            self.cursor.execute(
                "UPDATE user_list SET phone=? WHERE userid=?",
                (phone, userid)
            )
            self.db.commit()
        except:
            return False
        return True

    def creat_track(self, userid: str, track_number: str, phone="aaaa") -> bool:
        try:
            if phone == "aaaa":
                cursor_ = self.cursor.execute(
                    "SELECT phone FROM user_list WHERE userid=?", (userid,))
                phone = [i for i in cursor_][0][0]
            self.cursor.execute(
                "INSERT INTO track_list (userid, track_number, phone, ins_time, trace_route) VALUES (?,?,?,?,?)",
                (userid, track_number, phone, int(time.time()), ""))
            self.db.commit()
        except:
            return False
        return True

    def get_track(self, track_number: str) -> list:
        '''
        (userid, track_number, phone, trace_route, time)
        '''
        try:
            cursor_ = self.cursor.execute(
                "SELECT userid, track_number, phone, trace_route, ins_time FROM track_list WHERE track_number=?",
                (track_number,))
            info_list = [i for i in cursor_][0]
        except:
            return []
        return info_list

    def update_track(self, track_number: str, trace_route: list) -> bool:
        try:
            self.cursor.execute(
                "UPDATE track_list SET trace_route=? WHERE track_number=?",
                (json.dumps(trace_route), track_number))
            self.db.commit()
        except:
            return False
        return True

    def del_track(self, track_number: str) -> bool:
        try:
            self.cursor.execute(
                "DELETE FROM track_list WHERE track_number=?",
                (track_number,)
            )
            self.db.commit()
        except:
            return False
        return True

    def get_user_track_list(self, userid: str):
        try:
            cursor_ = self.cursor.execute(
                "SELECT track_number, ins_time FROM track_list WHERE userid=?",
                (userid,))
            info_list = [i for i in cursor_]
        except:
            return []
        return info_list

    def get_track_list(self) -> list:
        '''
        track_number, phone, trace_route
        '''
        try:
            cursor_ = self.cursor.execute(
                "SELECT track_number, phone, trace_route, userid FROM track_list")
            track_list = [i for i in cursor_]
        except:
            return []
        return track_list
