import streamlit as st
import re
from my_functions import open_file, regular_expression, clean_text

#TITLE
st.title("Regular expressions")
st.markdown("*A regular expression (shortened as regex or regexp sometimes referred to as rational expression) is a sequence of characters that specifies a match pattern in text. Usually such patterns are used by string-searching algorithms for 'find' or 'find and replace' operations on strings, or for input validation. Regular expression techniques are developed in theoretical computer science and formal language theory.*")
st.markdown("*Regular expressions are used in search engines, in search and replace dialogs of word processors and text editors, in text processing utilities such as sed and AWK, and in lexical analysis. Regular expressions are supported in many programming languages.* [Wikipedia](https://en.wikipedia.org/wiki/Regular_expression)")
st.markdown("In this app, you can write your own regular expression and test it on a text of your choice. You have the choice between a text you write yourself or a text you upload. The app will then return the matches found in the text.")

#SIDEBAR
write_text = st.sidebar.checkbox("Write my own text")
st.sidebar.title("Options")
remove_small_words = st.sidebar.checkbox("Remove words with less than 3 characters")
remove_punctuation = st.sidebar.checkbox("Remove the punctuation")
remove_url = st.sidebar.checkbox("Remove the urls")
remove_numbers = st.sidebar.checkbox("Remove the numbers")

#SENTIMENT ANALYSIS
st.text("")
st.text("")
st.text("")
file_name = None
if not write_text:
    st.markdown("### Upload a text")
    file_name = st.file_uploader("Only PDF files are accepted for the moment", type="pdf")
user_text = "Hello world"
if file_name is not None:
    user_text = open_file(file_name)
    if len(user_text) > 0:
        user_text = clean_text(user_text,
                               remove_small_words=remove_small_words,
                               remove_url=remove_url,
                               remove_numbers=remove_numbers,
                               remove_punctuation=remove_punctuation)
        st.success("File uploaded")

if write_text:
    st.markdown("### Write your own text")
    user_text = st.text_area("The maximum number of character is 10000", height=200, max_chars=10000)
    if user_text:
        st.success("Text saved")

#REGEX
st.text("")
st.text("")
st.text("")
st.markdown("### Write the regex you want to test")
user_regex = st.text_area("Here comes your regex (example: '\d+' matchs any number)", height=20, max_chars=100)
if (user_regex and len(user_text) > 1):
    st.success("Regex saved")
    regular_expression(user_regex, user_text)

#HELP SECTION
st.text("")
st.text("")
st.text("")
st.text("")
st.markdown("### Regex template")
st.markdown("**Here are some regex templates you can use to test your regex:**")

st.text("")
st.markdown("Number")
st.code(r"\d+")

st.text("")
st.markdown("Word with 4 characters")
st.code(r"\b\w{4}\b")

st.text("")
st.markdown("Word with 4 characters and a number")
st.code(r"\b\w{4}\d\b")

st.text("")
st.markdown("Mail address")
st.code(r"\b[\w.-]+@[\w.-]+\.\w{2,4}\b")













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
st.text("")

# Contact
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")