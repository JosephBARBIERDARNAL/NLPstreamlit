import re
import unicodedata

import PyPDF2
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import my_text2emotion as te
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

def create_pie_chart(data_dict):
    labels = list(data_dict.keys())
    values = list(data_dict.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

@st.cache_data()
def sentiment_analysis(text):
    make_space(2)
    st.markdown(f"**Sentiment analysis, according to VADER:**") #display the sentiment analysis
    sentiment = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment.polarity_scores(text)
    st.markdown(f"- Polarity score: {round(sentiment_dict['compound'],3)}") #display the polarity score

    st.text("")
    col1, col2 = st.columns([1,2])
    with col1:
        st.markdown("**Emotion analysis, according to Text2Emotion:**")
        emotion_dict = te.get_emotion(text)
        happinnes =  emotion_dict['Happy']
        sadness = emotion_dict['Sad']
        anger = emotion_dict['Angry']
        fear = emotion_dict['Fear']
        surprise = emotion_dict['Surprise']
        st.markdown(f"- Happiness: {round(happinnes,3)}")
        st.markdown(f"- Sadness: {round(sadness,3)}")
        st.markdown(f"- Anger: {round(anger,3)}")
        st.markdown(f"- Fear: {round(fear,3)}")
        st.markdown(f"- Surprise: {round(surprise,3)}")
    with col2:
        create_pie_chart(emotion_dict)



def apply_sentiment_analysis(strings_list):
    # Initialize empty lists to store results
    string_col = []
    polarity_vader_col = []

    # Create TextBlob and VaderSentiment analyzers
    analyzer_vader = SentimentIntensityAnalyzer()

    # Loop through each string in the list
    for string in strings_list:
        # clean the string
        string = string.replace("\n", " ")

        # Perform sentiment analysis with VaderSentiment
        vader_scores = analyzer_vader.polarity_scores(string)
        polarity_vader = vader_scores['compound']

        # Append results to lists
        string_col.append(string)
        polarity_vader_col.append(polarity_vader)

    # Create DataFrame from lists
    df = pd.DataFrame({
        'String': string_col,
        'Polarity_VaderSentiment': polarity_vader_col
    })

    # Remove duplicates row
    df = df.drop_duplicates(keep='first')

    return df