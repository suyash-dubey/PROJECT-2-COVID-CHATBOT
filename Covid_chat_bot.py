import random
from newspaper import Article
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#pip install newspaper3k

nltk.download('punkt',quiet=True)


#get the Article
article=Article('https://en.wikipedia.org/wiki/COVID-19')
article.download()
article.parse()
article.nlp()
corpus=article.text


#tokenisation
test=corpus
sentence_list=nltk.sent_tokenize(test)#list of sentences



#function to return a random greeting msg to user
def greet_res(text):
    text=text.lower()
    #boots greetin response
    bot_greetings=['hello','hi','hey']
    #user greeting response
    user_greetings=['hello','hi','hey','hii','wassup','lo','hellooooooo']
    for word in text.split():
        if word in user_greetings:
            return random.choice(bot_greetings)



#function to sort index_sort
def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))
    x=list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]]>x[list_index[j]]:
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    return list_index


#function for bot response
def bot_res(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_res=''
    #convert the whole sentence in form of vector
    cm=CountVectorizer().fit_transform(sentence_list)
    #check input matches in our sentence lst or not
    s_score=cosine_similarity(cm[-1],cm)#cm[-1]means last jo hmne append kia tha input
    s_score_list=s_score.flatten()#we have conerted the s_score into a list
    index=index_sort(s_score_list)
    index=index[1:]
    res_flag=0
    j=0
    for i in range(len(index)):
        if s_score_list[index[i]]>0.0:
            bot_res=bot_res+' '+sentence_list[index[i]]
            res_flag=1
            j=j+1
        #if we want to print max 2 sentence i response not more than that
        if j>2:
            break
    if res_flag==0:
        bot_res=bot_res+' I apologise that i have not understood ur meaning plz be specific'
    sentence_list.remove(user_input)
    return bot_res



#start chat
print('Covid Helpline: I m here to help u with the information regarding corona virus. If u want to exit type nye or exit or quit')
exit_list=['bye','exit','byeee','quit']
while(True):
    user_input=input()
    if user_input.lower() in exit_list:
        print('Bot: Thanks for ur queries')
        break
    else:
        if greet_res(user_input)!=None:
            print('Bot:'+greet_res(user_input))
        else:
            print('Bot:'+bot_res(user_input))
