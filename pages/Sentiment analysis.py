import streamlit as st
from my_functions import open_file, sentiment_analysis

#TITLE
st.title("Sentiment analysis")
st.markdown(""" Sentiment analysis (or opinion mining) is a natural language processing (NLP)
technique used to determine whether data is positive, negative or neutral. Sentiment analysis is
often performed on textual data to help businesses monitor brand and product sentiment in customer
feedback, and understand customer needs.""")

#SENTIMENT ANALYSIS
st.text("")
st.markdown("### Upload a text")
file_name = st.file_uploader("")
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)
    sentiment_analysis(page_text)
    st.text("")
st.text("")
st.text("")
st.markdown("### Or write your own text")
user_text = st.text_input("")
if user_text:
    sentiment_analysis(user_text)
st.text("")

#INFORMATION
st.text("")
st.markdown("### About polarity and subjectivity")
st.markdown("- Polarity is a float within the range [-1, 1]. A score of 0 is neutral, a score of 1 is very positive, and a score of -1 is  very negative.")
st.markdown("- Subjectivity is a float within the range [0, 1] where 0 is very objective and 1 is very subjective.")
st.markdown("- They are calculated thanks to the [TextBlob library](https://textblob.readthedocs.io/en/dev/quickstart.html).")

#INFORMATION
st.text("")
st.text("")
st.markdown("### About file type")
st.markdown("This app supports the following file types: .txt, .csv, .xlsx, .json, .html, .xml, .pdf, .docx")