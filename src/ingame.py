import math
import time

# TODO: get Erozea time / Server time

epochTimeFactor = 20.571428571428573


def get_eorzea_time():
    currentTime = int(time.time())
    eHour = math.floor((currentTime * 12 / 35 / 60) % 24)
    eMinute = math.floor((currentTime * 12 / 35) % 60)
    if eMinute < 10:
        eMinute = "0" + str(eMinute)
    if eHour < 10:
        eHour = "0" + str(eHour)
    eTime = str(eHour) + " : " + str(eMinute)
    print(eTime)
    return eTime


def get_weather_forecast():
    pass


get_eorzea_time()
