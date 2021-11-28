from datetime import datetime

# TODO: get Erozea time / Server time


def get_eorzea_time():
    # get current time
    # 계산식 넣기
    # /* Convert to Eorzea time */
    # /* In Eorzea, 12 game minutes = 35 real seconds */
    # if (eMin) *eMin = (currentTime * 12 / 35) % 60;
    # if (eHour) *eHour = (currentTime * 12 / 35 / 60) % 24;
    currentHour = datetime.now()
    # eHour = (currentHour * 12 / 35) % 60
    # eMinute = (currentHour * 12 / 35 / 60) % 24
    # print(eHour, eMinute)
    print(currentHour)
    pass


def get_weather_forecast():
    pass


get_eorzea_time()
