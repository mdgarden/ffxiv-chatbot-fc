import math
import time

# TODO: get Erozea time / Server time

epochTimeFactor = 20.571428571428573


def get_eorzea_time():
    currentTime = int(time.time())
    eHour = math.floor((currentTime * 12 / 35 / 60) % 24)
    eMinute = math.floor((currentTime * 12 / 35) % 60)
    print(eHour)
    print(eMinute)
    pass


def get_weather_forecast():
    pass


get_eorzea_time()
