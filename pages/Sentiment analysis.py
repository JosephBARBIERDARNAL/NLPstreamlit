import streamlit as st
from my_functions import open_file, sentiment_analysis

#TITLE
st.title("Sentiment analysis")
st.markdown(""" *Sentiment analysis (also known as opinion mining or emotion AI) is the use of natural language processing, text analysis, computational linguistics, and biometrics to systematically identify, extract, quantify, and study affective states and subjective information.* [Wikipedia](https://en.wikipedia.org/wiki/Sentiment_analysis)""")
st.markdown(""" You can use this app to analyze the sentiment of a text.
You can either upload a file or write your own text.
The app will then return the polarity and subjectivity of the text.
They are calculated thanks to the [TextBlob](https://github.com/sloria/textblob) and [VaderSentiment](https://github.com/cjhutto/vaderSentiment) libraries.""")

#SIDEBAR
st.sidebar.title("Options")
write_text = st.sidebar.checkbox("Write your own text")

#SENTIMENT ANALYSIS
st.text("")
st.text("")
st.text("")
file_name = None
if not write_text:
    st.markdown("### Upload a text")
    file_name = st.file_uploader("Only PDF files are accepted", type="pdf")
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)
    if len(page_text) > 0:
        sentiment_analysis(page_text)


if write_text:
    st.markdown("### Write your own text")
    user_text = st.text_area("It's recommend to write in English", height=200, max_chars=10000)
    if user_text:
        sentiment_analysis(user_text)
st.text("")

#INFORMATION
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.markdown("### About polarity and subjectivity")
st.markdown("- Polarity is a float within the range [-1, 1]. A score of 0 is neutral, a score of 1 is very positive, and a score of -1 is  very negative.")
st.markdown("- Subjectivity is a float within the range [0, 1] where 0 is very objective and 1 is very subjective.")







st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")

# Contact
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")