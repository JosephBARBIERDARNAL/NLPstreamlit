from collections import Counter

import streamlit as st
from nltk.tokenize import word_tokenize

from my_functions import open_file, clean_text, word_cloud_plot, plot_top_n_words, make_space, count_words

#TITLE
st.title("Wordcloud generator")
make_space(1)

#CUSTOMIZATION
st.sidebar.markdown("## Options")
make_space(1)
remove_small_words = st.sidebar.checkbox("Remove words with less than 3 characters", value=True)
remove_punctuation = st.sidebar.checkbox("Remove the punctuation", value=True)
remove_url = st.sidebar.checkbox("Remove the urls", value=True)
remove_numbers = st.sidebar.checkbox("Remove the numbers", value=True)
lemma = st.sidebar.checkbox("Lemmatize the text", value=True)
language = st.sidebar.selectbox("Select the language of your text", ["french", "english", "spanish"])
color = st.sidebar.color_picker("Color to use for the barplot", "#E2070A")
make_space(1)



#OPEN FILE
file_name = st.file_uploader("", type=["pdf"])
page_text = "Hello world"
if file_name is not None:
    page_text = open_file(file_name)
    st.success("File uploaded")

if page_text != "Hello world":

    #COUNT WORDS
    number_of_words = count_words(page_text)
    st.markdown(f"Number of words detected: **{number_of_words}**")
    if number_of_words < 4:
        st.error(f"The file you uploaded is too short")
        st.stop()

    #CLEAN FILE TEXT
    cleaned_text = clean_text(page_text,
                              language=language,
                              remove_punctuation=remove_punctuation,
                              remove_url=remove_url,
                              remove_numbers=remove_numbers,
                              remove_small_words=remove_small_words)

    #COUNT WORDS IN CLEANED TEXT
    number_of_words_cleaned = count_words(cleaned_text)
    st.markdown(f"Number of words detected (after cleaning): **{number_of_words_cleaned}**")
    if number_of_words_cleaned < 4:
        st.error(f"The file you uploaded is too short")
        st.stop()

    #ADD USER'S STOPWORDS
    make_space(3)
    tokenized_text = word_tokenize(cleaned_text)
    word_counts = Counter(tokenized_text)
    most_common_words = dict(word_counts.most_common(100))
    stopwords_to_add = st.sidebar.multiselect("Select the words you want to remove from the graph", most_common_words.keys())

    #RE-CLEAN TEXT WITH USER'S STOPWORDS
    if stopwords_to_add:
        cleaned_text = clean_text(page_text, language=language, words_to_remove=stopwords_to_add)

    #WORDCLOUD
    make_space(1)
    number_of_word = st.slider("Number of words you want to plot", 5, 100, value=50)
    wordcloud = word_cloud_plot(cleaned_text, number_of_word)
    st.text("")

    #TOP N WORDS
    if file_name:
        plot_top_n_words(cleaned_text, number_of_word, color=color, file_name=file_name.name)
    else:
        plot_top_n_words(cleaned_text, number_of_word, color=color, file_name="Hello world")
make_space(20)

# Contact
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")