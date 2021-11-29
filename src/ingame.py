from datetime import datetime
import time

# TODO: get Erozea time / Server time

epochTimeFactor = 20.571428571428573


def get_eorzea_time():
    # get current time
    # 계산식 넣기
    # /* Convert to Eorzea time */
    # /* In Eorzea, 12 game minutes = 35 real seconds */
    # if (eMin) *eMin = (currentTime * 12 / 35) % 60;
    # if (eHour) *eHour = (currentTime * 12 / 35 / 60) % 24;
    currentTime = round(time.time() * 1000) * epochTimeFactor
    # currentHour = datetime.now()
    eHour = currentTime / 360000
    eMinute = (currentTime * 12 / 35 / 60) % 24
    # print(eHour, eMinute)
    print(currentTime)
    print(eHour)
    print(eMinute)
    pass


def get_weather_forecast():
    pass


get_eorzea_time()

# MEMO
# 밀리세컨드 -> 변환식?
