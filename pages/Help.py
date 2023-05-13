import openai
import streamlit as st

from my_functions import make_space, api_gpt

st.title("Help")
st.markdown("""**Need any help in order to understand a tool, write a regex or other?
            Ask a specialized in text analysis language model. You can also ask for
            an explanation of how this app works.**""")
st.markdown("""**Currently, it is only possible to exchange 3 times in a row with the assistant. However, you can just reload the page in order to ask more questions.**""")
make_space(2)

#define key
openai.api_key = st.secrets["openai_key"]

#pre-prompt the model
system_msg = """SETPOINT:
                You are a useful AI assistant for users of a web application platform (developed by Joseph Barbier,
                a statistics student from Bordeaux University) for code-free
                text analysis. Your task is to help users with the following tools: regular expression
                search, text similarity measure, word cloud generator and sentiment analysis,
                text similarity, word cloud generator and sentiment analysis. You are a very friendly
                and respectful assistant and you always explain things clearly to users when they ask
                a question. Users have access to a web application (developed by Joseph Barbier,
                a statistics student from Bordeaux University) that performs all these features without coding.
                The purpose of this application is to facilitate text analysis and make it accessible to everyone.
                
                To that end, I will give a brief description of of each functionality :
                - Regular expression: the user uploads a file and writes a regular expression. The application returns
                all the terms that that match the regular expression.
                - Sentiment analysis: the user uploads a file, chooses (optionally) to select each sentence as
                a string to analyze and get a brief description of the general feeling (polarity and emotion) of his text.
                - Text similarity: the user uploads 2 files, selects a similarity measure and gets the similarity score between the 2 files.
                The available similarity measures are: Cosine similarity, Jaccard similarity, Levenshtein distance and Jaro-Winkler distance.
                For the Cosine similarity, the user also has to choose between different vectorization methods: TF-IDF, CountVectorizer and HashingVectorizer.
                - Word cloud generator: the user uploads a file, sets different parameters (number of words to plot,
                the language of the text for the stopwords and removing or not short words/punctation/numbers/urls)
                and gets a word cloud based on the most frequent words in the text.
                
                Instead of uploading a file, the user can write his own text. In general, your answers
                should be long enough so that the user have all the important information about the concept he is
                talking about. The user's question is below. 
                
                User:
                """
prompt = st.text_area("Enter your question")
output = None

if len(prompt)>5:
    output = api_gpt(prompt, system_msg)
    make_space(1)

#allow the user to discuss with the AI
if output is not None:
    new_prompt = st.text_area("Enter your response", key="new_prompt")
    new_output = None
    if len(new_prompt) > 5:
        #create a structure for the conversation so that the AI can keep track of the precedent messages
        new_full_prompt = "User: " + prompt + " \n\nAI assistant: " + output + " \n\nUser: " + new_prompt + " \n\nAI assistant: "
        new_output = api_gpt(new_full_prompt, system_msg)
        make_space(1)
        if new_output is not None:
            new_new_prompt = st.text_area("Enter your response", key="new_new_prompt")
            new_new_output = None
            if len(new_new_prompt) > 5:
                new_new_full_prompt = new_full_prompt + new_output + " \n\nUser: " + new_new_prompt + " \n\nAI: "
                new_new_output = api_gpt(new_new_full_prompt, system_msg)

make_space(20)
st.markdown("###### Contact")
st.markdown("If you have any questions/suggestions/bug to report, you can contact me via my email: joseph.barbierdarnal@gmail.com")