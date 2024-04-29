from urlextract import URLExtract
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    num_words = df.shape[0]
    words = []
    for i in df['Messages']:
        words.extend(i.split())


    # Count the occurrences of '<Media omitted>' in the 'Messages' column
    media_count = df['Messages'].str.contains('<Media omitted>').sum()



    extractor = URLExtract()
    links = []
    for i in df['Messages']:
        links.extend(extractor.find_urls(i))

    return num_words, len(words), media_count, len(links)

def most_busy_users(df):
    x = df['Users'].value_counts().head()
    per = round((df['Users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'count': 'percentage'})
    return x, per


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Users']== selected_user]

    temp = df[df['Users'] == 'group notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']


    Words = []
    for i in temp['Messages']:
        for j in i.lower().split():
            if j not in stop_words:
                Words.append(j)

    most_common_df = pd.DataFrame(Counter(Words).most_common(25))
    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users']== selected_user]

    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    timeline = df.groupby(['Month']).count()['Messages'].reset_index()



    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    daily_timeline = df.groupby('Only_date').count()['Messages'].reset_index()



    return daily_timeline


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]




    return df['Day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]




    return df['Month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    user_heatmap = df.pivot_table(index = 'Day', columns = 'Period', values = 'Messages', aggfunc = 'count' ).fillna(0)

    return user_heatmap