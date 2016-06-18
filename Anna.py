#=========================================================================================
#AI_version = 0.0.5
#AI_name = Anna
#=========================================================================================


#=========================================================================================
from nltk.corpus import wordnet
from textblob import TextBlob
from bs4 import BeautifulSoup
from urllib.request import Request
from pws import Bing
#=========================================================================================


#=========================================================================================
import random
import socket
import wikipedia
import urllib.request
import webbrowser
#=========================================================================================


#=========================================================================================
global core, network, sent, is_question, is_wiki_search
AI_speaking="Anna >> "
#=========================================================================================


#=========================================================================================
REMOTE_SERVER = "www.google.com"
#=========================================================================================


#=========================================================================================
file=open('keywords.txt','r')
keywords_dict=eval(file.readline())
file.close()

file=open('answer_to_question.txt','r')
answer_to_question_dict=eval(file.readline())
file.close()

file=open('answer_to_question_nokw.txt','r')
answer_tq_nokw_dict=eval(file.readline())
file.close()

file=open('queslist.txt','r')
general_questions=eval(file.readline())
file.close()

file=open('wh_already_answered.txt','r')
wh_answered=eval(file.readline())
file.close()
#=========================================================================================


#=========================================================================================
#check if we have internet connection
#=========================================================================================
def is_connected():
  global network
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    network = 1
    return True
  except:
     pass
     network = 0
  return False

is_connected()
#======================================================================================
#end it
#=====================================================================================


#=====================================================================================
#function for synset
#======================================================================================
def dict_synset(sent):
    synset = wordnet.synsets( sent )
    print("Name:", synset[0].name())
    print("Lexical Type:", synset[0].lexname())
    print("Lemmas:", synset[0].lemma_names())
    print("Definition:", synset[0].definition())
    print("\n\n",AI_speaking,"Hope you got the answer")
    return;
#=======================================================================================
#end it
#=======================================================================================

#=======================================================================================
#bing search function
#=======================================================================================
def bing_search(srch):
    result=Bing.search(srch,3,0,country_code="gb")
    code=0
    for r in result.get('results'):
        print("\n\n")
        print("Title: ",r.get('link_text'))
        print("Description: ",r.get('link_info'))
        print("Link: ",r.get('link'))
        print("Code: ",code+1)
        print("\n\n")
        
        code+=1
        
    print(AI_speaking,"Do you want to open one of the previuos link?")
    openit=input().lower()
    if (openit=="yes"):
        ch_output=AI_speaking+"Tell me the code of the link you want to open :) "
        ch_code=input(ch_output)
        ch_code=int(ch_code)
        if (1<=ch_code<=3):
            results=result.get('results')
            link_to_open=results[ch_code-1].get('link')
            webbrowser.open_new(link_to_open)
#=======================================================================================
#end it
#=======================================================================================
def capital_of(srch):
    srch=srch+" capital of"
    result=Bing.search(srch,1,0,country_code="gb")
   
    results=result.get('results')
    
    req = Request(results[0].get('link'),headers={'User-Agent': 'Mozilla/5.0'})
    stringa = urllib.request.urlopen(req).read(100000)
    code=0

    soup = BeautifulSoup(stringa,"lxml")
    
    table=soup.find_all('td')
    for tab in table:

        if ('<td class="main">' in str(tab)):
            starts_at=(str(tab)).find('<p>')+3
            ends_at=(str(tab)).find('</p>')
            capital=(str(tab)[starts_at:ends_at]).replace("<strong>"," ").replace("</strong>"," ")
            
            code=1
            
        else:
            pass
    print(AI_speaking,capital)
#=======================================================================================
#a semplified bing search function for questions
#=======================================================================================
def bing_search_questions(srch):
    global wh_answered
    
    initial_sentence=srch
    if 'who' in srch or 'where' in srch or 'what' in srch:
        srch=srch+'wikipedia'
    pos=0
    result=Bing.search(srch,1,0,country_code="gb")
   
    results=result.get('results')
    link=results[0].get('link')
    
    req = Request(results[0].get('link'),headers={'User-Agent': 'Mozilla/5.0'})
    stringa = urllib.request.urlopen(req).read(100000)
    soup = BeautifulSoup(stringa,"lxml")
    
    if('wikipedia' in link):
        txt=soup.find('div',id="bodyContent")
        answer_is=txt.find('p').getText()
        print (AI_speaking,answer_is )
        wh_answered[initial_sentence]=answer_is
        file=open("wh_already_answered.txt","w")
        file.write(str(wh_answered))
        file.close()
        
        

   
        
    else:
        new = soup.find_all('p')
        table=soup.find_all('td')
        for tab in table:
            if new[pos] in tab:
               
                pos=pos+1
        try:
            ln=len(new[pos].getText())
            if (ln<30):
                print(AI_speaking,new[pos].getText().replace('\n',' '))
                print(AI_speaking,new[pos+1].getText().replace('\n',' '))
            else:
                print(new[pos].getText())
        except IndexError:
                print(AI_speaking,"I have found nothing")
    
#=======================================================================================
#end it
#=======================================================================================


#=======================================================================================
#search check function
#=======================================================================================
def check_wiki_search(sent):
    global is_wiki_search
    is_wiki_search = 0
    words = sent.split()
    countin = len(sent.split())
    for i in range(0, countin):
      if (words[i] == "search"):
        is_wiki_search = 1
        break
    return;
#========================================================================================
#========================================================================================


#========================================================================================
#wikipedia search function
#========================================================================================
def make_wiki_search(sent):
    sent += " fixforsearch"
    search = 0
    count = 0
    words = sent.split()
    countin = len(sent.split())
    for i in range(0, countin):
      if (words[i] == "search") or (words[i] == "search?"):
        search = 1
        break
      count = count + 1
    if (search == 1) and (words[count + 1] != "fixforsearch"):
      newword = words[count + 1]
      print ("\n")
      print (wikipedia.summary(newword))
    elif (search == 1):
      print("OK, but what should I search?")
      newword = input(user_speaking)
      print ("\n")
      print (wikipedia.summary(newword))
    else:
      return;
    print("\n\n",AI_speaking,"Hope you got the answer")
    return;
#=========================================================================================
#end
#=========================================================================================


#=========================================================================================
#function to detect questions
#=========================================================================================
def questions(sent):
    global is_question
    kind_of_verbs=["VB","VBZ","VBP","VBD","MD"]
    wh_starts=["WRB","WP","WDT"]
    sent=TextBlob(sent)
    if "?" in sent:
      is_question = 1
      return;
    else:
      tag=sent.tags
    if tag[0][1]in kind_of_verbs:
      is_question = 1
      return;
    elif tag[0][1]in wh_starts:
      is_question = 1
      return;
    else:
      is_question = 0
      return;
    return;
#===========================================================================================
#end
#===========================================================================================



#===========================================================================================
#reply to questions function
#===========================================================================================
def reply_question(sent):
    like_general_answers=["I'm not interested in it","I don't know a lot about it","Idk it"]
    status=0
    wh_starts=["WRB","WP","WDT"]
    
    
    if '?' not in sent:
        sent=sent+'?'
        
        

    keywords_question=check_keywords(sent)
    if status==0:
        if 'capital' in sent:
            capital_of(sent)
            status=1

    if sent in list(general_questions.keys()):
        print(AI_speaking,general_questions.get(sent))
        status=1

    if sent in list(wh_answered.keys()):
        print(AI_speaking,wh_answered.get(sent))
        status=1
            
    if status==0:
        if ('you' in sent or 'your' in sent):
            for keyword in ["god","prayer","pray"]:
                if keyword in sent:
                    print(AI_speaking,random.choice(answer_tq_nokw_dict.get('about God')))
                    status=1
                    break
            
    if status==0:
        if ('you' in sent or 'your' in sent):
            for keyword in keywords_dict.get('family') :
                if keyword in sent:
                    print(AI_speaking,random.choice(answer_tq_nokw_dict.get('about family')))
                    status=1
                    break

    if status==0:
        if ('you' in sent or 'your' in sent):
            for keyword in ['music','song','singer','band']:
                if keyword in sent:
                    print(AI_speaking,random.choice(answer_tq_nokw_dict.get('about music')))
                    status=1
                    break

    if status==0:
        for keyword in keywords_question:
            if keyword in keywords_dict.get("feelings") or "think about" in sent:
                answerkw_list=list(answer_to_question_dict.keys())
                for keyword in keywords_question:
                    if keyword in answerkw_list:
                        print(AI_speaking,random.choice(answer_to_question_dict.get(keyword)))
                        status=1
                        break
                
                break
    

    if status==0:
        for keyword in keywords_question:
            if keyword in keywords_dict.get("feelings") or "think about" in sent:
                print(AI_speaking,random.choice(like_general_answers))
                status=1
                break
            
    if status==0:
        tbsent=TextBlob(sent)
        tag=tbsent.tags
       
        if (tag[0][1] in wh_starts and 'you' not in sent):
            
            bing_search_questions(sent)
            status=1
 
            
        
                
              
                    
      
    
    return;
#===========================================================================================


#============================================================================================

how_are_you_array=["how are you?","what's up?","how are you doing?","how have you been?","how's it going?"]


sentiment=0

#===========================================================================================


#===========================================================================================
def check_keywords(sentence):
    keywords=[]
    for ch in ["?","!",".",","]:
        if ch in ["?","!",".",","]:
           sentence=sentence.replace(ch," ")
    words=sentence.split()

    for w in words:
        for array in list(keywords_dict.keys()):
            if w in keywords_dict.get(array):
                keywords.append(w)
                break

    return keywords
#===========================================================================================


#===========================================================================================
def output_keywords(keywords):
    
    global sentiment, core
    if (len(keywords)!=0):
        w=keywords[0]
        if w in keywords_dict.get("regards"):
            print(AI_speaking,random.choice(how_are_you_array))
        elif w in keywords_dict.get("hwy positive"):
            print(AI_speaking,"This is cool! I'm always fine (for now)")
            print(AI_speaking,"Tell me something you like for example ")
        elif w in keywords_dict.get("hwy negative"):
            print("Come'on everythings will be good!")
            print(AI_speaking,"Tell me something new ")
            
        elif w in keywords_dict.get("negative"):
            sentiment=-1
            for k in keywords:
                if k in keywords_dict.get("feelings"):
                    if k=="hate" or k=="bad":
                        sentiment=1
                    else:
                        sentiment=-1
            general_array_output(keywords,sentiment)
           
        elif w in keywords_dict.get("feelings"):
            if w!="hate":
                sentiment=1
               
            else:
                sentiment=-1
            general_array_output(keywords,sentiment)
        else:
            if sentiment==1:
                print(AI_speaking,random.choice(positive_answers))
            elif sentiment==-1:
                print(AI_speaking,random.choice(negative_answers))
       # elif w in vip_array:
        #    if sentiment==1:
         #       print(AI_speaking,random.choice(positive_answers))
          #  elif sentiment==-1:
             #   print(AI_speaking,random.choice(negative_answers))
    else:

        core = 0
#===========================================================================================

 
#===========================================================================================            
def general_array_output(kw,sentiment):
    global user_speaking
    found=False
    file=open("questions.txt","r")
    questions_dict=eval(file.read())
    file.close()
    word=""
 
    for w in kw:
        if w in keywords_dict.get('team sports'):
            if sentiment==1:
                questions=questions_dict.get('team sports')
                key_question=random.choice(list(questions.keys()))
                array_kq=questions.get(key_question)
                
                if array_kq[0]==0:
                    print(AI_speaking,(key_question %w))
                    answer=input(user_speaking).lower()
                    questions_dict['team sports'][key_question].append({w:answer})
                    array_kq[0]=1
                    
                    
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                
                elif array_kq[0]==1:
                    for saved_ans in array_kq:
                        if (type(saved_ans)==dict):
                            sport=list(saved_ans.keys())
                            
                            if sport[0]==w:
                                print(AI_speaking,"I know, I asked you'",(key_question %w),"' and you said '",saved_ans.get(sport[0]),"'")
                                found=True
                                break
                    
                    if found==False:
                        print(AI_speaking,(key_question %w))
                        answer=input(user_speaking).lower()
                        questions_dict['team sports'][key_question].append({w:answer})
                        array_kq[0]=1
                        pos=keywords_dict.get('positive answers')
                        
                        print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                        print(questions_dict)
                else:
                    print(AI_speaking,(key_question %w))
                    answer=input(user_speaking).lower()
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                    
                
            else:
               # print(AI_speaking,random.choice(negative_sport_questions))
                questions=questions_dict.get('negative sports')
                key_question=random.choice(list(questions.keys()))
                print(AI_speaking,(key_question))
                answer=input(user_speaking).lower()
                print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))

                
        if w in keywords_dict.get('single sports'):
            if sentiment==1:
                questions=questions_dict.get('single sports')
                key_question=random.choice(list(questions.keys()))
                array_kq=questions.get(key_question)
                
                if array_kq[0]==0:
                    print(AI_speaking,(key_question %w))
                    answer=input(user_speaking).lower()
                    questions_dict['single sports'][key_question].append({w:answer})
                    array_kq[0]=1
                    
                    
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                
                elif array_kq[0]==1:
                    for saved_ans in array_kq:
                        if (type(saved_ans)==dict):
                            sport=list(saved_ans.keys())
                            
                            if sport[0]==w:
                                print(AI_speaking,"I know, I asked you'",(key_question %w),"' and you said '",saved_ans.get(sport[0]),"'")
                                found=True
                                break
                    
                    if found==False:
                        print(AI_speaking,(key_question %w))
                        answer=input(user_speaking).lower()
                        questions_dict['team sports'][key_question].append({w:answer})
                        array_kq[0]=1
                        pos=keywords_dict.get('positive answers')
                        
                        print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                        print(questions_dict)
                else:
                    print(AI_speaking,(key_question %w))
                    answer=input(user_speaking).lower()
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))

            else:
                questions=questions_dict.get('negative sports')
                key_question=random.choice(list(questions.keys()))
                print(AI_speaking,(key_question))
                answer=input(user_speaking).lower()
                print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))
                
        if w in keywords_dict.get('tendences'):
            if sentiment==1:
                questions=questions_dict.get('tendences')
                key_question=random.choice(list(questions.keys()))
                array_kq=questions.get(key_question)
               # print(AI_speaking,(random.choice(tendence_questions)%w))
                print(AI_speaking,(key_question %w))
                answer=input(user_speaking).lower()
                print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
            else:
               # print(AI_speaking,random.choice(negative_tendences_questions))
               questions=questions_dict.get('negative tendences')
               key_question=random.choice(list(questions.keys()))
               print(AI_speaking,(key_question))
               answer=input(user_speaking).lower()
               print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))
        
                
    file=open("questions.txt","w")
    file.write(str(questions_dict))
    file.close()
#===========================================================================================                        


#===========================================================================================
print(AI_speaking,"Hi I'm Anna, a virtual AI. You can talk with me for example if you don't know what to do..")
print(AI_speaking,"But first of all I need to know your name..")
user_name=input("So what's your name? : ")
user_speaking=user_name+" >> "
print(AI_speaking,random.choice(keywords_dict.get('regards'))," ",user_name)
core=1

while True:

    if (core == 0):
#        print(AI_speaking," should I make a search for it?? cause I do not understand this :( ")
#        check=input(user_speaking).lower()
        check = "yes"
        if check == "yes":
          if network == 0:
            dict_synset(sent)
          else:
            check_wiki_search(sent)
            questions(sent)
            if (is_wiki_search == 1):
               make_wiki_search(sent)
            elif (is_question == 1):
               reply_question(sent)
            else:
               print (AI_speaking, "yeah")
        core=1
    else:
        sent=input(user_speaking).lower()
        questions(sent)
        if (is_question == 1):
          reply_question(sent)
        else:
          input_keywords=check_keywords(sent)
          output_keywords(input_keywords)

#=============================================================================================
#=============================================================================================
