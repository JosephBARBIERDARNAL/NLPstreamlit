import streamlit as st
from textblob import TextBlob
import pandas as pd
import PyPDF2
import re
import unicodedata
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from my_functions import make_space, clean_text


@st.cache_data()
def from_pdf_to_string_list(file):
    if file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        sentences = []
        clean_sentences = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                sentences += re.split(r'(?<=\.)\s+', text)

                # clean each detected sentence
                for sentence in sentences:
                    nfkd_form = unicodedata.normalize('NFKD', sentence)
                    sentence = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
                    clean_sentence = clean_text(sentence)
                    if len(clean_sentence) > 20:
                        clean_sentences.append(clean_sentence)
    return clean_sentences

@st.cache_data()
def sentiment_analysis(text):
    blob = TextBlob(str(text)) #apply the sentiment analysis
    make_space(2)
    st.markdown(f"**Sentiment analysis, according to TextBlob:**") #display the sentiment analysis
    st.markdown(f"- Polarity score: {round(blob.sentiment.polarity,3)}") #display the polarity score
    st.markdown(f"- Subjectivity score: {round(blob.sentiment.subjectivity,3)}") #display the subjectivity score

    make_space(2)
    st.markdown(f"**Sentiment analysis, according to VADER:**") #display the sentiment analysis
    sentiment = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment.polarity_scores(text)
    st.markdown(f"- Polarity score: {round(sentiment_dict['compound'],3)}") #display the polarity score

def apply_sentiment_analysis(strings_list):
    # Initialize empty lists to store results
    string_col = []
    polarity_textblob_col = []
    subjectivity_textblob_col = []
    polarity_vader_col = []

    # Create TextBlob and VaderSentiment analyzers
    analyzer_vader = SentimentIntensityAnalyzer()

    # Loop through each string in the list
    for string in strings_list:
        # clean the string
        string = string.replace("\n", " ")

        # Perform sentiment analysis with TextBlob
        blob = TextBlob(str(string))
        polarity_textblob = blob.sentiment.polarity
        subjectivity_textblob = blob.sentiment.subjectivity

        # Perform sentiment analysis with VaderSentiment
        vader_scores = analyzer_vader.polarity_scores(string)
        polarity_vader = vader_scores['compound']

        # Append results to lists
        string_col.append(string)
        polarity_textblob_col.append(polarity_textblob)
        subjectivity_textblob_col.append(subjectivity_textblob)
        polarity_vader_col.append(polarity_vader)

    # Create DataFrame from lists
    df = pd.DataFrame({
        'String': string_col,
        'Polarity_TextBlob': polarity_textblob_col,
        'Subjectivity_TextBlob': subjectivity_textblob_col,
        'Polarity_VaderSentiment': polarity_vader_col
    })

    # Remove dupplicates row
    df2 = df.drop_duplicates(keep='first')

    return df