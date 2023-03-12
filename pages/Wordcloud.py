import streamlit as st
from my_functions import open_file, clean_text, word_cloud_plot, plot_top_n_words
from nltk.tokenize import word_tokenize
from collections import Counter

#TITLE
st.title("Wordcloud")
st.text("")

#SIDEBAR
st.sidebar.text("")

#CUSTOMIZATION
st.sidebar.markdown("## Settings")
st.sidebar.text("")
remove_punctuation = st.sidebar.checkbox("Remove the punctuation?", value=True)
remove_url = st.sidebar.checkbox("Remove the urls?", value=True)
remove_numbers = st.sidebar.checkbox("Remove the numbers?", value=True)
remove_small_words = st.sidebar.checkbox("Remove the small words? (1 or 2 letters)", value=True)
st.sidebar.text("")
language = st.sidebar.selectbox("Choose the language of your text", ["french", "english", "spanish"])
st.sidebar.text("")
number_of_word = st.sidebar.slider("Number of words you want to plot", 5, 100)
st.sidebar.text("")
color = st.sidebar.color_picker("Color to use for the barplot", '#00f900')
st.sidebar.text("")



#OPEN FILE
file_name = st.file_uploader("")
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)
st.text("")
st.text("")

if page_text != "Hello world":
    #CLEAN FILE TEXT
    cleaned_text = clean_text(page_text,
                              language=language,
                              remove_punctuation=remove_punctuation,
                              remove_url=remove_url,
                              remove_numbers=remove_numbers,
                              remove_small_words=remove_small_words)

    #ADD USER'S STOPWORDS
    st.text("")
    tokenized_text = word_tokenize(cleaned_text)
    word_counts = Counter(tokenized_text)
    most_common_words = dict(word_counts.most_common(100))
    stopwords_to_add = st.sidebar.multiselect("Select the words you want to remove from the graph", most_common_words.keys())

    #RE-CLEAN TEXT WITH USER'S STOPWORDS
    if stopwords_to_add:
        cleaned_text = clean_text(page_text, language=language, words_to_remove=stopwords_to_add)

    #WORDCLOUD
    wordcloud = word_cloud_plot(cleaned_text, number_of_word)

    #TOP N WORDS
    if file_name:
        plot_top_n_words(cleaned_text, number_of_word, color=color, file_name=file_name.name)
    else:
        plot_top_n_words(cleaned_text, number_of_word, color=color, file_name="Hello world")

#INFORMATION
st.text("")
st.markdown("### About file type")
st.markdown("This app supports the following file types: .txt, .csv, .xlsx, .json, .html, .xml, .pdf, .docx")




