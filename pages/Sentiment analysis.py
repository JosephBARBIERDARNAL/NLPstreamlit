import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from my_functions import open_file, make_space
from sentiment_functions import sentiment_analysis, apply_sentiment_analysis, from_pdf_to_string_list, \
    csv_sentiment_analysis

#TITLE
st.title("Sentiment analysis")
st.markdown(""" *Sentiment analysis (also known as opinion mining or emotion AI) is the use of
natural language processing, text analysis, computational linguistics, and biometrics to systematically
identify, extract, quantify, and study affective states and subjective information.*
[Wikipedia](https://en.wikipedia.org/wiki/Sentiment_analysis)""")
st.markdown(""" You can use this app to analyze the sentiment of a text.
You can either upload a file or write your own text.
The app will then return the polarity and the emotion of the text.
They are calculated thanks to the [VaderSentiment](https://github.com/cjhutto/vaderSentiment) and [Text2Emotion](https://github.com/aman2656/text2emotion-library/tree/master) libraries.""")


#SENTIMENT ANALYSIS
make_space(5)
file_type = st.radio("What type of file do you want to upload?", ("PDF", "CSV", "Write my own text"))
string_list = st.checkbox("Should each sentence be analyzed individually (if not, whole text is analyzed)? (Only for PDF file)")
file_name = None

# test if the user wants to write his own text
if file_type in ["PDF", "CSV"]:
    st.markdown("### Upload a file")
    file_name = st.file_uploader("Only PDF/CSV files are accepted")
    if file_name is not None:

        # test if the user wants a string list
        if file_type == "PDF" and string_list:
            page_text = from_pdf_to_string_list(file_name) #upload the pdf as a list of strings
            st.success("File upload")
            make_space(3)
            df_SA = apply_sentiment_analysis(page_text) #compute sentiment analysis on every sentence
            remove_zeros = st.checkbox("Should sentence with exact score of 0 removed? (recommended)")
            if remove_zeros:
                df_SA = df_SA.loc[~(df_SA[['Polarity_VaderSentiment']] == 0).all(axis=1)]

            # print and make the df available as download
            st.dataframe(df_SA)
            df_to_download = df_SA.to_csv().encode('utf-8')
            st.download_button("Dowload", data=df_to_download, file_name="sentiment_analysis.csv")
            st.markdown(f"Information: all sentences have been clean and all sentences with less than {20} characters are removed.")
            st.markdown(f"Number of *different* sentences detected: **{len(df_SA.index)}**")

            # plot sentiment distribution
            make_space(3)
            plot_hist = st.checkbox("Plot distribution of the results", value=True)
            if plot_hist:
                bins = st.slider("Number of bins", min_value=10, max_value=100, value=40)
                fig, ax = plt.subplots()
                ax.hist(df_SA.Polarity_VaderSentiment, bins=bins, facecolor='cyan', edgecolor='black')
                ax.set_title('Distribution of Polarity')
                st.pyplot(fig)
            make_space(2)
            display_stat = st.checkbox("Display descriptive statistics", value=True)
            make_space(1)
            if display_stat:
                col1, col2, col3 = st.columns(3)
                average_vader = round(df_SA.Polarity_VaderSentiment.mean(),2)
                median_vader = round(df_SA.Polarity_VaderSentiment.median(),2)
                std_vader = round(df_SA.Polarity_VaderSentiment.std(),2)
                col1.metric(f"Mean", average_vader, average_vader)
                col2.metric("Median", median_vader, median_vader)
                col3.metric("Stdev", std_vader, std_vader)

        elif file_type == "PDF" and not string_list:
            page_text = open_file(file_name)
            if len(page_text) > 1:
                st.success("File upload")

                # test if the uploaded file has content
                if len(page_text) > 0:
                    sentiment_analysis(page_text)
                else:
                    st.error("Empty file")

        elif file_type == "CSV":
            if file_name.name.endswith(".csv"):
                df_csv = pd.read_csv(file_name)
                st.success("File upload")
                make_space(3)
                str_col = st.selectbox("Which column should be analyzed?", df_csv.columns)
                new_df_csv = csv_sentiment_analysis(df_csv, str_col)
                st.dataframe(new_df_csv)
                df_to_download = new_df_csv.to_csv().encode('utf-8')
                st.download_button("Dowload", data=df_to_download, file_name="sentiment_analysis.csv")
                st.markdown(f"Number of *different* sentences detected: **{len(new_df_csv.index)}**")

                # plot sentiment distribution
                make_space(3)
                plot_hist = st.checkbox("Plot distribution of the results", value=True)
                if plot_hist:
                    bins = st.slider("Number of bins", min_value=10, max_value=100, value=40)
                    fig, ax = plt.subplots()
                    ax.hist(new_df_csv.sentiment_vader, bins=bins, facecolor='cyan', edgecolor='black')
                    ax.set_title('Distribution of Polarity')
                    st.pyplot(fig)
                make_space(2)
                display_stat = st.checkbox("Display descriptive statistics", value=True)
                make_space(1)
                if display_stat:
                    col1, col2, col3 = st.columns(3)
                    average_vader = round(new_df_csv.sentiment_vader.mean(), 2)
                    median_vader = round(new_df_csv.sentiment_vader.median(), 2)
                    std_vader = round(new_df_csv.sentiment_vader.std(), 2)
                    col1.metric(f"Mean", average_vader, average_vader)
                    col2.metric("Median", median_vader, median_vader)
                    col3.metric("Stdev", std_vader, std_vader)
            else:
                st.error("File type is not csv")


else:
    st.markdown("### Write your own text")
    user_text = st.text_area("It's recommend to write in English", height=200, max_chars=10000)
    if user_text:
        st.success("Text saved!")
        sentiment_analysis(user_text)


#CONTACT
make_space(20)
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")