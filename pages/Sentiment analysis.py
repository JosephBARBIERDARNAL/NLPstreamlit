import streamlit as st
from my_functions import open_file, sentiment_analysis

#TITLE
st.title("Sentiment analysis")

#OPEN FILE
file_name = st.file_uploader("")
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)

#SENTIMENT ANALYSIS
if page_text != "Hello world":
    sentiment_analysis(page_text)

#INFORMATION
st.text("")
st.markdown("### About polarity and subjectivity")
st.markdown("- Polarity is a float within the range [-1, 1]. A score of 0 is neutral, a score of 1 is very positive, and a score of -1 is  very negative.")
st.markdown("- Subjectivity is a float within the range [0, 1] where 0 is very objective and 1 is very subjective.")
st.markdown("- They are calculated thanks to the [TextBlob library](https://textblob.readthedocs.io/en/dev/quickstart.html).")

