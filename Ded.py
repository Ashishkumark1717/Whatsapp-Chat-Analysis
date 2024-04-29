import re
import pandas as pd
import seaborn as sns

def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'Date': dates, 'Messages': messages})
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %H:%M - ')
    users = []
    m = []
    for i in df['Messages']:
        entry = re.split(r'([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            m.append(' '.join(entry[2:]))
        else:
            users.append('group notification')
            m.append(entry[0])

    df['Users'] = users
    df['Messege'] = m
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['Mon_num'] = df['Date'].dt.month
    df['Only_date'] = df['Date'].dt.date
    df['Day_name'] = df['Date'].dt.day_name()

    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str(00))
        elif hour == 0:
            period.append(str(00) + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['Period'] = period

    return df