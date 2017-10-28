import sched
import time
import datetime
from jd.Running import run_search


# 每天定时服务，可在设定时间调用目标函数
def add_to_sched(sc, run_time, func):
    today = str(datetime.date.today())
    run_time_datetime = datetime.datetime.strptime((today + ' ' + run_time), '%Y-%m-%d %H:%M:%S')
    sec = (run_time_datetime - datetime.datetime.now()).total_seconds()
    if sec > 0:
        event = sc.enter(sec, 1, func)


# 一个sched 为一天的安排
def make_scched():
    s = sched.scheduler(time.time, time.sleep)
    add_to_sched(s, '9:00:00', run_search)
    add_to_sched(s, '22:00:00', run_search)
    s.run()


if __name__ == '__main__':
    while True:
        now_hour = datetime.datetime.now().hour
        if now_hour == 0:
            make_scched()
        time.sleep(3600)
