import streamlit as st
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



@st.cache_data()
def open_file(file_name):

    #open pdf file
    if file_name.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file_name)
        page_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text += page.extract_text().lower()
        return page_text

    else:
        st.error("File type not supported. Try converting to PDF.")
        return ""


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
@st.cache_data()
def clean_text(text,
               language="french",
               words_to_remove=[],
               remove_punctuation=True,
               remove_url=True,
               remove_numbers=True,
               remove_small_words=True,
               lemma=True):

    text = re.sub(r'\s+', ' ', text)  # replace multiple spaces with a single space

    if remove_punctuation:
        text = re.sub(r'[^\w\s]', ' ', text) # remove punctuation

    if remove_url:
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text) # remove url links

    if remove_numbers:
        text = re.sub(r'\d+', '', text) # remove numbers from the text

    if remove_small_words:
        text = re.sub(r'\b\w{1,2}\b', '', text) # remove words with 2 or less letters

    if lemma:
        lemmatizer = WordNetLemmatizer()
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    # remove pre-defined (from NLTK) + others user-defined stopwords
    stop_words = set(stopwords.words(language))
    stop_words.update(words_to_remove)
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    text = " ".join(words)

    # return the cleaned text
    return text

    

def word_cloud_plot(cleaned_text, n):

    st.text("") # add a space

    tokenized_text = word_tokenize(cleaned_text) # tokenize the text
    word_counts = Counter(tokenized_text) # count word occurence
    most_common_words = dict(word_counts.most_common(n)) # select the n most frequent
    wordcloud = WordCloud(width=600, height=400, background_color='white', colormap='magma') # create a word cloud

    # display word cloud
    wordcloud.generate_from_frequencies(most_common_words)
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    #download wordcloud
    name = "wordcloud.png"
    plt.savefig(name)
    with open(name, "rb") as img:
        btn = st.download_button(
            label="Download image",
            data=img,
            file_name=name,
            mime="image/png")







def plot_top_n_words(cleaned_text, n, file_name, color, figsize=(12, 6)):
    st.text("")  # add a space

    tokenized_text = word_tokenize(cleaned_text)  # tokenize the text
    word_occurrences_dict = Counter(tokenized_text)  # count word occurence

    top_n_words = sorted(word_occurrences_dict.items(), key=lambda x: x[1], reverse=True)[:n]  # select the n most frequent
    words = [word for word, count in top_n_words]  # get the words
    counts = [count for word, count in top_n_words]  # get the counts
    n = len(words)  # get the number of words

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(words, counts, color=color)
    ax.set_xticklabels(words, rotation=45, ha='right')
    ax.set_xlabel('Words')
    ax.set_ylabel('Occurrences', rotation=40)
    ax.set_title(f"Top {n} of most frequent words of {file_name}")
    st.pyplot(fig)

    # download barplot
    name = "barplot.png"
    plt.savefig(name)
    with open(name, "rb") as img:
        btn = st.download_button(
            label="Download image",
            data=img,
            file_name=name,
            mime="image/png")





@st.cache_data()
def sentiment_analysis(text):
    blob = TextBlob(text) #apply the sentiment analysis
    st.text("") #add an empty text (make 1 space)
    st.text("")  # add an empty text (make 1 space)
    st.markdown(f"Sentiment analysis, according to TextBlob:") #display the sentiment analysis
    st.markdown(f"- Polarity score: {round(blob.sentiment.polarity,3)}") #display the polarity score
    st.markdown(f"- Subjectivity score: {round(blob.sentiment.subjectivity,3)}") #display the subjectivity score

    st.text("")  # add an empty text (make 1 space)
    st.text("")  # add an empty text (make 1 space)
    st.markdown(f"Sentiment analysis, according to VADER:") #display the sentiment analysis
    sentiment = SentimentIntensityAnalyzer()
    sentiment_dict = sentiment.polarity_scores(text)
    st.markdown(f"- Polarity score: {round(sentiment_dict['compound'],3)}") #display the polarity score
    st.markdown(f"- Subjectivity score: {round(sentiment_dict['neu'],3)}") #display the subjectivity score



@st.cache_data()
def regular_expression(pattern, string):
    """
    Input: a pattern and a string
    Output: a list of all the matches
    """
    # find all matches
    pattern = re.compile(pattern)
    match = re.findall(pattern, string)
    if match:
        st.write(f"Number of matchs: {len(match)}")
        for i in match:
            st.write(i)
    else:
        st.error("No match found")
    









