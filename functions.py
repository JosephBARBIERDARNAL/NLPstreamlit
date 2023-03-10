import nltk
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import streamlit as st
from wordcloud import WordCloud







def plot_top_n_words(cleaned_text, n, figsize=(12,6), color="red"):
    """
    Based on a dictionnary full of word occurence, this function (bar-)plots the top `n` words
    """
    #
    tokenized_text = word_tokenize(cleaned_text)
    word_occurrences_dict = Counter(tokenized_text)
    
    # Get the words and their occurrence
    top_n_words = sorted(word_occurrences_dict.items(), key=lambda x: x[1], reverse=True)[:n]
    words = [word for word, count in top_n_words]
    counts = [count for word, count in top_n_words]

    # Create figure and axes
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the data
    ax.bar(words, counts, color=color)

    # Set x-axis label properties
    ax.set_xticklabels(words, rotation=45, ha='right')
    ax.set_xlabel('Words')

    # Set y-axis label properties
    ax.set_ylabel('Occurrences', rotation=40)

    # Set title properties
    ax.set_title(f"Top {n} of most frequent words")

    # Display the plot
    st.pyplot(fig)
    
    
    
    
    
    
    
    
    
    
    
    
    

def word_cloud_plot(cleaned_text, n):
    
    #tokenize the text
    tokenized_text = word_tokenize(cleaned_text)
    
    #count word occurence
    word_counts = Counter(tokenized_text)
    
    #select the n most frequent
    most_common_words = dict(word_counts.most_common(n))
    
    #create a word cloud
    wordcloud = WordCloud(width=600, height=400, background_color='white', colormap='magma')
    wordcloud.generate_from_frequencies(most_common_words)
    
    fig, ax = plt.subplots(figsize=(14,8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    
    
    
    
    





    
nltk.download('stopwords')
nltk.download('punkt')
st.cache_data()
def clean_text(text, language="french", words_to_remove=[]):
    """
    Remove from a text:
    - punctuations signs
    - multiple spaces
    - numbers
    - stopwords
    - url links
    - words with 1 or 2 letters
    """
    
    #remove punctuation signs and replace them with a space
    punctuation_regex = r'[^\w\s]'
    text = re.sub(punctuation_regex, ' ', text)
    
    #remove url links
    url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    text = url_regex.sub('', text)

    #replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    #remove numbers from the text
    pattern = r'\d+'
    text = re.sub(pattern, '', text)
    
    #keep only words with 3 or more letters
    text = re.findall(r'\b\w{3,}\b', text)
    text = " ".join(text)
    
    #remove pre-defined (from NLTK) + others french stopwords
    stop_words = set(stopwords.words(language))
    other_stop_words = {"https", "http", "www", "com", "car"}
    stop_words.update(other_stop_words)
    stop_words.update(words_to_remove)
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)
    
    #return the cleaned text
    return text







def space(n:int, side = False):
    """
    Input: the number of spaces desired
    Apply: apply the streamlit command that skips 'n' spaces
    Output: None
    """
    
    #import the streamlit package
    import streamlit as st
    
    #iterate n times
    for _ in range(n):
        
        #sidebar or not
        if side:
            
            #add an empty text (make 1 space)
            st.sidebar.text("")
        
        else:
            
            #add an empty text (make 1 space)
            st.text("")