import os
import time
import pytz
import pandas as pd
from datetime import datetime, timedelta

import load_data

desired_timezone = pytz.timezone('Asia/Seoul')

def save_check():
    pass

def update_weather(d):
    station_info = pd.read_csv('./input/관측지점코드.csv')
    station_dct = dict(zip(station_info['지점명'], station_info['지점']))

    y = d[0:4]
    m = d[4:6]

    for name, code in station_dct.items():
        file_dir = f'./data_weather/{name}/{y}'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = os.path.join(file_dir, f'{m}.csv')

        check_flag = 0
        max_retries = 1

        while check_flag == 0 and max_retries != 0:
            d_df = load_data.request_weather_api(code, d, d)

            if not d_df.empty:
                if os.path.exists(file_path):
                    e_df = pd.read_csv(file_path)
                    u_df = pd.concat([e_df, d_df], ignore_index=True)
                    u_df = u_df.drop_duplicates(['day'])
                    u_df.to_csv(file_path, index=False)
                else:
                    d_df.to_csv(file_path, index=False)

                check_flag = 1
            else:
                max_retries = 0
                time.sleep(1)

def save_retry(re_date):
    update_weather(re_date)


def main():
    today = datetime.now(desired_timezone)
    d = (today - timedelta(days=1)).strftime('%Y%m%d')
    update_weather(d)

    # re_date = '' # %Y%m%d
    # save_retry(re_date)

if __name__ == '__main__':
    main()
