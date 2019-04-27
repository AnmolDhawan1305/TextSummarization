

import nltk
import bs4 as bs  
import urllib.request  
import re
import heapq 
from PIL import Image
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"D:\ML\New_Anaconda\Tesseract\tesseract.exe"
f=open('summarized_text_from_web.txt','w+')


def text_from_web(url):
    raw = urllib.request.urlopen(url)  
    article = raw.read()
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:  
     article_text += p.text
    return article_text 


def text_from_image(img):
    im=Image.open(img)
    article_text=pytesseract.image_to_string(im,lang='eng')
    return article_text


def evaluate_score(article_text):
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = re.sub(r'\s+', ' ', article_text)  
    
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    
    sentence_list = nltk.sent_tokenize(article_text)  
    
    stopwords = nltk.corpus.stopwords.words('english')
    
    word_frequencies = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
                
    maximum_frequncy = max(word_frequencies.values())
    
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    return sentence_scores
    
def store_summary(sentence_scores,n):
    summary_sentences = heapq.nlargest(n, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)  
    #print(summary)  
    f.write(summary)



n=int(input('Enter number of lines to summarize from web: '))
url='https://en.wikipedia.org/wiki/Avengers:_Endgame'   
text=text_from_web(url)
sentence_scores=evaluate_score(text)
store_summary(sentence_scores,n)
print('Done')
f.close()

n=int(input('Enter number of lines to summarize from image: '))  
f=open('summarized_text_from_image.txt','w+')
img='text.png'
text=text_from_image(img)
sentence_scores=evaluate_score(text)
store_summary(sentence_scores,n)
print('Done')
f.close()