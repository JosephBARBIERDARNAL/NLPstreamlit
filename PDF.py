from streamlit import multiselect, slider, file_uploader, sidebar, title
import PyPDF2
from functions import *






############################################
# TITLE    START
############################################

title("Text analysis")
space(2) 

############################################
# TITLE    END
############################################







############################################
# SIDEBAR    START
############################################

#app description
sidebar.markdown("## About")
sidebar.markdown("> Some words (stopwords) are by default removed from the files")
sidebar.markdown("> The default language is French.")

#change language
space(2,side=True)
language = sidebar.selectbox("Choose the language of your text", ["french", "english", "spanish"])

############################################
# SIDEBAR    END
############################################







############################################
# WORD INPUT    START
############################################

#help = "Entrez ici le mot ou l'expression dont vous souhaitez connaître les PDF qui le contient. Par exemple, si vous cherchez les PDF sur les voitures électriques, vous pouvez écrire 'voiture' ou 'électrique' ou 'voiture électrique'. Dans ce dernier cas, uniquement les PDF contenant l'exacte séquence 'voiture électrique' seront retournés."
#word = st.text_input("Mot à chercher (exemple : 'Voiture' ou 'Panneaux solaires')", help=help)

############################################
# WORD INPUT    END
############################################







############################################
# SEARCHING    START
############################################

#define a directory
#directory = os.getcwd() #+ "/Desktop/pdfThomas"

#search for the pdfs containing 'word'
#pdf_name, page = search_pdfs(directory, word)

#output the results
#front(pdf_name, page, word)

############################################
# SEARCHING    END
############################################

















############################################
# TEXT ANALYSIS    START
############################################

#selection of the pdf the user wants to analyze GET A LIST OF PDF IN A GIVEN FOLDER
#pdf_names = get_all_pdf_name(os.getcwd())
#pdf_name = st.selectbox('Choose a file', pdf_names)
#st.write('You selected:', pdf_name)


#define the text chosen and an empy 'page_text'
pdf_name = file_uploader("Chose a file")
page_text = "Hello world hello World "*100
if pdf_name is not None:
    pdf_reader = PyPDF2.PdfReader(pdf_name)

    #iterate over the pdf, extract text and store it to 'page_text'
    for page_num in range(len(pdf_reader.pages)):
                    
        #extract the text from the page
        page = pdf_reader.pages[page_num]
        page_text += page.extract_text().lower()

#clean the text
cleaned_text = clean_text(page_text, language=language)

#add stopwords from the user
space(2)
tokenized_text = word_tokenize(cleaned_text)
word_counts = Counter(tokenized_text)
most_common_words = dict(word_counts.most_common(100))
stopwords_to_add = multiselect("Mots à supprimer", most_common_words.keys())

#test if the user wants to add new stopwords
if stopwords_to_add:
    cleaned_text = clean_text(page_text, language=language, words_to_remove=stopwords_to_add)

#word cloud
space(3)
number_of_word = slider("Select the number of words you want to plot", 5, 100)
word_cloud_plot(cleaned_text, number_of_word)

#barplot of the n most frequent word
plot_top_n_words(cleaned_text, number_of_word)

############################################
# TEXT ANALYSIS    END
############################################





