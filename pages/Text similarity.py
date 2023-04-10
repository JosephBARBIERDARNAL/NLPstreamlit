import streamlit as st
from my_functions import open_file, display_similarity

#TITLE
st.title("Text similarity measurement")
st.markdown(""" *Sentence Similarity is the task of determining how similar two texts are.
Sentence similarity models convert input texts into vectors (embeddings) that capture semantic information
and calculate how close (similar) they are between them.
This task is particularly useful for information retrieval and clustering/grouping.* [HuggingFace](https://huggingface.co/tasks/sentence-similarity)""")
st.markdown("Since there are lots of different way to measure the similarity between two texts, this app propose different methods to do so.")
st.text("")
st.text("")
st.text("")
st.text("")
write_text = st.checkbox("Write my own texts")

#COLUMNS
col1, col2 = st.columns(2, gap="medium")

#OPEN FILE 1
if not write_text:
    with col1:
        file_name1 = None
        st.markdown("### Drop the 1st file")
        file_name1 = st.file_uploader("PDF only", type="pdf", key="1")
        page_text1 = "  "
        if file_name1 is not None:
            page_text1 = open_file(file_name1)

#OPEN FILE 2
    with col2:
        file_name2 = None
        st.markdown("### Drop the 2nd file")
        file_name2 = st.file_uploader("PDF only", type="pdf", key="2")
        page_text2 = " "
        if file_name2 is not None:
            page_text2 = open_file(file_name2)

    if file_name1 is not None and file_name2 is not None:
        st.success("Files uploaded")
else:
    with col1:
        st.markdown("### Write the 1st text")
        page_text1 = st.text_area("", height=200, max_chars=10000, key="1")
    with col2:
        st.markdown("### Write the 2nd text")
        page_text2 = st.text_area("", height=200, max_chars=10000, key="2")

st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
if len(page_text1)>2 and len(page_text2)>2:
    select = st.selectbox("Select the method you want to use", ["Jaccard similarity", "Cosine similarity", "Levenshtein distance", "Jaro-Winkler Distance"])
    display_similarity(select, page_text1, page_text2)
















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