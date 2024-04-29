import streamlit as st
import Ded, Helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analysis')

upload_file = st.sidebar.file_uploader('Choose a File')
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = Ded.preprocess(data)
    st.dataframe(df)

    user_list = df['Users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox(' Show Analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):
        st.title('Statistical Analysis of Whatsapp Chat')
        num_stats, words, media, num_links = Helper.fetch_stats(selected_user, df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            col1 = st.header('Total Messeages')
            col1 = st.title(num_stats)
        with col2:
            col2 = st.header('Total Words')
            col2 = st.title(words)
        with col3:
            col3 = st.header('Total Media')
            col3 = st.title(media)
        with col4:
            col4 = st.header('Total links')
            col4 = st.title(num_links)

        st.title('Monthly Timeline')
        timeline = Helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.bar(timeline['Month'], timeline['Messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Daily Timeline')
        daily_timeline = Helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(daily_timeline['Only_date'], daily_timeline['Messages'], color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.title('Day wise')
            busy_day = Helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            st.pyplot(fig)

        with col2:
            st.title('month wise')
            busy_month = Helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='aqua')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title('Weekly User Heatmap')
        user_heatmap = Helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, per = Helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='aqua')
                st.pyplot(fig)

            with col2:
                st.dataframe(per)



        emoji_df = Helper.emoji_helper(selected_user, df)
        st.title('Emojis Analysis')

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%0.2f%%')
            ax.legend()
            st.pyplot(fig)






















