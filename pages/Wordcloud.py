import streamlit as st
from my_functions import open_file, clean_text, word_cloud_plot, plot_top_n_words
from nltk.tokenize import word_tokenize
from collections import Counter

#TITLE
st.title("Wordcloud")
st.text("")

#SIDEBAR
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.markdown("## Settings") #app description
language = st.sidebar.selectbox("Choose the language of your text", ["french", "english", "spanish"]) #change language
st.sidebar.text("")
number_of_word = st.sidebar.slider("Select the number of words you want to plot", 5, 100)

#OPEN FILE
file_name = st.file_uploader("")
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)

#CLEAN FILE TEXT
cleaned_text = clean_text(page_text, language=language)

#ADD USER'S STOPWORDS
st.text("")
tokenized_text = word_tokenize(cleaned_text)
word_counts = Counter(tokenized_text)
most_common_words = dict(word_counts.most_common(100))
stopwords_to_add = st.multiselect("Words to remove", most_common_words.keys())

#RE-CLEAN TEXT WITH USER'S STOPWORDS
if stopwords_to_add:
    cleaned_text = clean_text(page_text, language=language, words_to_remove=stopwords_to_add)

#WORDCLOUD
word_cloud_plot(cleaned_text, number_of_word)

#TOP N WORDS
plot_top_n_words(cleaned_text, number_of_word)

#INFORMATION
st.text("")
st.markdown("### About file type")
st.markdown("This app supports the following file types: .txt, .csv, .xlsx, .json, .html, .xml, .pdf, .docx")




