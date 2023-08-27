import streamlit as st
from my_functions import open_file, make_space, run_all

#preprocessing
st.title("Clean, modify and pre-process")
st.markdown("""*explain how this section can be useful*""")

make_space(5)
st.markdown("### Upload a file")
file = None
file = st.file_uploader("Only PDF files are accepted", type="PDF")
if file is not None and file.name.endswith(".pdf"):
    page_text = open_file(file)
    if len(page_text) > 1:
        st.success("File upload")



make_space(3)
run = st.button("Apply")
if run:
    run_all()