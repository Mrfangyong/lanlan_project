from datetime import datetime
import time
import os
 
from apscheduler.schedulers.background import BackgroundScheduler
 
 
def tick():
    print('执行任务，当前时间是: %s' % datetime.now())
 
 
# scheduler = BackgroundScheduler()
# scheduler.add_job(tick, 'interval', minutes=1)
# scheduler.start()    #这里的调度任务是独立的一个线程


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
#     scheduler.add_job(tick, 'interval', seconds=3)
    
    run_date1='2019-11-11 09:44:05'
    scheduler.add_job(tick, 'date', run_date=run_date1)#在指定的时间，只执行一次
    scheduler.start()    #这里的调度任务是独立的一个线程
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            now_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) 
            if now_time==run_date1:
                print("退出程序")
                break
            else:
                time.sleep(1)    #其他任务是独立的线程执行
                
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        print('Exit The Job!')
        
# 文字  图片  时间 

#提交任务   监控这个脚本  删除这个脚本  



