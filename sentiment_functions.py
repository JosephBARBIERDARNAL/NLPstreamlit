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
    try:
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    except ValueError:
        st.error("No emotions detected in the text.")

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


@st.cache_data()
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


@st.cache_data()
def csv_sentiment_analysis(df, str_col):
    df[str_col] = df[str_col].astype(str)
    df = df[[str_col]]
    df = df.drop_duplicates(keep='first')
    with st.spinner("Performing sentiment analysis"):
        sentiment_scores = []
        fear_scores = []
        anger_scores = []
        sadness_scores = []
        surprise_scores = []
        happiness_scores = []
        analyzer_vader = SentimentIntensityAnalyzer()
        for string in df[str_col]:
            emotion_dict = te.get_emotion(string)
            happiness_scores.append(emotion_dict['Happy'])
            sadness_scores.append(emotion_dict['Sad'])
            anger_scores.append(emotion_dict['Angry'])
            fear_scores.append(emotion_dict['Fear'])
            surprise_scores.append(emotion_dict['Surprise'])
            sentiment = analyzer_vader.polarity_scores(string)
            sentiment_scores.append(sentiment['compound'])
        df['sentiment_vader'] = sentiment_scores
        df['happiness'] = happiness_scores
        df['sadness'] = sadness_scores
        df['anger'] = anger_scores
        df['fear'] = fear_scores
        df['surprise'] = surprise_scores
    return df
