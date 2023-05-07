import streamlit as st
from my_functions import make_space

#TITLE
st.title("A simple NLP app")

#ABOUT APP
make_space(1)
st.markdown("##### New feature: an AI help assistant specialized in text analysis and knowing how the application works. Just ask your question direclty in the Help section.")
st.markdown("##### **This app was created in order to simplify text manipulation and analysis. You can perform the tasks listed below without writing a single line of code.**")

st.markdown("- Sentiment analysis")
st.markdown("- Wordcloud generator")
st.markdown("- Regular expression search")
st.markdown("- Text similarity measurement")

make_space(1)
st.markdown("### **How to use this app**")
st.markdown("- 1. Select the task you want to perform on the sidebar")
st.markdown("- 2. Upload a pdf file (or write/copy-paste your text in the text area)")
st.markdown("- 3. Select the parameters (if any)")
st.markdown("- 4. Get the results!")

make_space(1)
st.markdown("### **Upcoming features**")
st.markdown("- Capable of reading other file types")
st.markdown("- More customization and a better presentation of results")
make_space(20)

# Contact
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")