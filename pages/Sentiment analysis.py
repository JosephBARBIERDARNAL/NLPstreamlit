import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from my_functions import open_file, make_space, clean_text
from sentiment_functions import sentiment_analysis, apply_sentiment_analysis, from_pdf_to_string_list

#TITLE
st.title("Sentiment analysis")
st.markdown(""" *Sentiment analysis (also known as opinion mining or emotion AI) is the use of
natural language processing, text analysis, computational linguistics, and biometrics to systematically
identify, extract, quantify, and study affective states and subjective information.*
[Wikipedia](https://en.wikipedia.org/wiki/Sentiment_analysis)""")
st.markdown(""" You can use this app to analyze the sentiment of a text.
You can either upload a file or write your own text.
The app will then return the polarity and subjectivity of the text.
They are calculated thanks to the [TextBlob](https://github.com/sloria/textblob) and [VaderSentiment](https://github.com/cjhutto/vaderSentiment) libraries.""")


#SENTIMENT ANALYSIS
make_space(5)
string_list = st.checkbox("Should each sentence be analyzed individually? (Only for uploaded file)")
write_text = st.checkbox("Write my own text")
file_name = None

# test if the user wants to write his own text
if not write_text:
    st.markdown("### Upload a text")
    file_name = st.file_uploader("Only PDF files are accepted", type="pdf")
    if file_name is not None:

        # test if the user wants a string list
        if string_list:
            page_text = from_pdf_to_string_list(file_name) #upload the pdf as a list of strings
            st.success("File upload")
            make_space(3)
            df_SA = apply_sentiment_analysis(page_text) #compute sentiment analysis on every sentence
            remove_zeros = st.checkbox("Should sentence with exact score of 0 removed? (recommended)")
            if remove_zeros:
                df_SA = df_SA.loc[~(df_SA[['Polarity_TextBlob', 'Subjectivity_TextBlob', 'Polarity_VaderSentiment']] == 0).all(axis=1)]

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
                fig, ax = plt.subplots()
                ax.hist(df_SA.Polarity_VaderSentiment, bins=40, facecolor='cyan', edgecolor='black')
                ax.set_title('Distribution of Polarity (VaderSentiment)')
                st.pyplot(fig)
            make_space(2)
            display_stat = st.checkbox("Display VaderSentiment descriptive statistics", value=True)
            make_space(1)
            if display_stat:
                col1, col2, col3 = st.columns(3)
                average_vader = round(df_SA.Polarity_VaderSentiment.mean(),2)
                median_vader = round(df_SA.Polarity_VaderSentiment.median(),2)
                std_vader = round(df_SA.Polarity_VaderSentiment.std(),2)
                col1.metric(f"Mean", average_vader, average_vader)
                col2.metric("Median", median_vader, median_vader)
                col3.metric("Stdev", std_vader, std_vader)
                #make_space(2)
                #average1_bob = df_SA.Polarity_TextBlob.mean()
                #median1_bob = df_SA.Polarity_TextBlob.median()
                #std1_bob = df_SA.Polarity_TextBlob.std()
                #col1.metric(f"Mean polarity", round(average1_bob, 2), "TextBlob")
                #col2.metric("Median polarity", round(median1_bob, 2), "TextBlob")
                #col3.metric("Stdev polarity", round(std1_bob, 2), "TextBlob")
                #make_space(2)
                #average2_bob = df_SA.Subjectivity_TextBlob.mean()
                #median2_bob = df_SA.Subjectivity_TextBlob.median()
                #std2_bob = df_SA.Subjectivity_TextBlob.std()
                #col1.metric(f"Mean subjectivity", round(average2_bob, 2), "TextBlob")
                #col2.metric("Median subjectivity", round(median2_bob, 2), "TextBlob")
                #col3.metric("Stdev subjectivity", round(std2_bob, 2), "TextBlob")

        else:
            page_text = open_file(file_name)
            st.success("File upload")

            # test if the uploaded file has content
            if len(page_text) > 0:
                sentiment_analysis(page_text)
            else:
                st.error("Empty file")

else:
    st.markdown("### Write your own text")
    user_text = st.text_area("It's recommend to write in English", height=200, max_chars=10000)
    if user_text:
        st.success("Text saved!")
    if user_text:
        sentiment_analysis(user_text)
make_space(1)

#INFORMATION
make_space(20)
st.markdown("### About polarity and subjectivity")
st.markdown("- Polarity is a float within the range [-1, 1]. A score of 0 is neutral, a score of 1 is very positive, and a score of -1 is  very negative.")
st.markdown("- Subjectivity is a float within the range [0, 1] where 0 is very objective and 1 is very subjective.")

#CONTACT
make_space(5)
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")