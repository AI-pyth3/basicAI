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
import os
import speech_recognition as sr
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
def input_type():
    global input_mode, anna_answered
    if input_mode==0:
        sent=input(user_speaking).lower()
        return sent
    
    if input_mode==1:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(user_speaking, end=' ')
            audio = r.listen(source)
        try:
            sent=r.recognize_google(audio,key="AIzaSyCQxkevHmo0caLeAvxMnUXv1TNSOi2oxdE")
            print(sent)
            return sent
        except sr.UnknownValueError:
           
            print("\n",AI_speaking," sorry I can't understand you")
            sent=-1
            return sent
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            sent=-1
            return sent

#=====================================================================================
#function for synset
#======================================================================================
def dict_synset(sent):
    global anna_answered
    synset = wordnet.synsets( sent )
    print("Name:", synset[0].name())
    print("Lexical Type:", synset[0].lexname())
    print("Lemmas:", synset[0].lemma_names())
    print("Definition:", synset[0].definition())
    print("\n\n",AI_speaking,"Hope you got the answer")
    anna_answered=True
    return;
#=======================================================================================
#end it
#=======================================================================================

#=======================================================================================
#bing search function
#=======================================================================================
def bing_search(srch):
    global anna_answered
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
    openit=input_type()
    
    if (openit=="yes"):
        ch_output=AI_speaking+"Tell me the code of the link you want to open :) "
        
        print(ch_output, end=' ')
        ch_code=input_type()
        ch_code=int(ch_code)
        anna_answered=True
        if (1<=ch_code<=3):
            results=result.get('results')
            link_to_open=results[ch_code-1].get('link')
            webbrowser.open_new(link_to_open)
            print(AI_speaking,"Here you are :)")
        else:
            print(AI_speaking,"This is not a valid code :(")
            
    else:
        print(AI_speaking,"Oh ok :)")
        anna_answered=True
#=======================================================================================
#end it
#=======================================================================================
def capital_of(srch):
    global anna_answered
    
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
    anna_answered=True
#=======================================================================================
#a semplified bing search function for questions
#=======================================================================================
def bing_search_questions(srch):
    global wh_answered, anna_answered
    
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
        anna_answered=True
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
                anna_answered=True
            else:
                print(new[pos].getText())
        except IndexError:
                print(AI_speaking,"I have found nothing")
                anna_answered=True
    
#=======================================================================================
#end it
#=======================================================================================

#=======================================================================================
#basic maths function
#=======================================================================================
def basic_maths(sent):
    global anna_answered
    AI_speaking="Anna >> "
    words = sent.split()
    countin = len(sent.split())
    dig = []
    count = 0
    check = 0
    checkdup = 0
    checksub = 0
    check_maths = 0
    for i in range(0, countin):
        if (words[i] == "add"):
            check = 1
            checkdup = checkdup + 1
        if (words[i] == "multiply"):
            check = 2
            checkdup = checkdup + 1
        if (words[i] == "subtract"):
            for i in range(0, countin):
                if (words[i] == "from"):
                    checksub = 13
                    break
            check = 3
            checkdup = checkdup + 1
        if (words[i] == "divide"):
            check = 4
            checkdup = checkdup + 1
    if (checkdup > 1):
        check = 0	
    for i in range(0, countin):
        try:
            x = words[i]
            try:
                x = int(x)
            except:
                count = 1
            x = x+1
            x = x-1
            dig.append(x)
        except TypeError:
            count = 1
    count = len(dig)
    addit = 0
    if (checkdup == 1):
        if (check == 1):
            for i in range(0, count):
                addit = addit + dig[i]
            print (AI_speaking,"answer is :", addit )
            check_maths = 1
            return check_maths;
        if (check == 2):
            addit = 1
            for i in range(0, count):
                addit = addit * dig[i]
            print (AI_speaking," answer is :", addit )
            anna_answered=True
            check_maths = 1
            return check_maths;
        if (check == 3):
            if (checksub == 0):
                addit = dig[0] - addit
                for i in range(1, count):
                    addit = addit - dig[i]
            else:
                addit = dig[1] - dig [0]
                print (AI_speaking," answer is :", addit )
                anna_answered=True
            check_maths = 1
            return check_maths;
        if (check == 4):
            if (dig[1] == 0):
                print (AI_speaking," division by zero not possible")
                anna_answered=True
            else:
                addit = dig[0]/dig[1]
                print (AI_speaking," answer is :", addit )
                anna_answered=True
            check_maths = 1
            return check_maths;
        anna_answered=True
    return check_maths;
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
    global anna_answered
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
      newword = input_type()
      print ("\n")
      print (wikipedia.summary(newword))
      
    else:
      return;
    print("\n\n",AI_speaking,"Hope you got the answer")
    anna_answered=True
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
    global anna_answered
    like_general_answers=["I'm not interested in it","I don't know a lot about it","Idk it"]
    general_answers=["What do you think?","I like potatoes","I like the stars","Are you really asking me this?"]
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

    if status==0:
        print(AI_speaking,random.choice(general_answers))
        status=1
        
    if status==1:
        anna_answered=True
        
                
              
                    
      
    
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
    
    global sentiment, core, anna_answered
    if (len(keywords)!=0):
        w=keywords[0]
        if w in keywords_dict.get("regards"):
            print(AI_speaking,random.choice(how_are_you_array))
            anna_answered=True
        elif w in keywords_dict.get("hwy positive"):
            print(AI_speaking,"This is cool! I'm always fine (for now)")
            print(AI_speaking,"Tell me something you like for example ")
            anna_answered=True
        elif w in keywords_dict.get("hwy negative"):
            print("Come'on everythings will be good!")
            print(AI_speaking,"Tell me something new ")
            anna_answered=True
            
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
                print(AI_speaking,random.choice(keywords_dict.get('positive answers')))
                anna_answered=True
            elif sentiment==-1:
                print(AI_speaking,random.choice(keywords_dict.get('negative answers')))
                anna_answered=True
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
    global user_speaking, anna_answered
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
                    answer=input_type()
                    questions_dict['team sports'][key_question].append({w:answer})
                    array_kq[0]=1
                    
                    
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                    anna_answered=True
                
                elif array_kq[0]==1:
                    for saved_ans in array_kq:
                        if (type(saved_ans)==dict):
                            sport=list(saved_ans.keys())
                            
                            if sport[0]==w:
                                print(AI_speaking,"I know, I asked you'",(key_question %w),"' and you said '",saved_ans.get(sport[0]),"'")
                                anna_answered=True
                                found=True
                                break
                    
                    if found==False:
                        print(AI_speaking,(key_question %w))
                        answer=input_type()
                        questions_dict['team sports'][key_question].append({w:answer})
                        array_kq[0]=1
                        pos=keywords_dict.get('positive answers')
                        
                        print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                        
                        anna_answered=True
                else:
                    print(AI_speaking,(key_question %w))
                    answer=input_type()
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                    anna_answered=True
                    
                
            else:
               # print(AI_speaking,random.choice(negative_sport_questions))
                questions=questions_dict.get('negative sports')
                key_question=random.choice(list(questions.keys()))
                print(AI_speaking,(key_question))
                answer=input_type()
                print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))
                anna_answered=True

                
        if w in keywords_dict.get('single sports'):
            if sentiment==1:
                questions=questions_dict.get('single sports')
                key_question=random.choice(list(questions.keys()))
                array_kq=questions.get(key_question)
                
                if array_kq[0]==0:
                    print(AI_speaking,(key_question %w))
                    answer=input_type()
                    questions_dict['single sports'][key_question].append({w:answer})
                    array_kq[0]=1
                    
                    
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                    anna_answered=True
                
                elif array_kq[0]==1:
                    for saved_ans in array_kq:
                        if (type(saved_ans)==dict):
                            sport=list(saved_ans.keys())
                            
                            if sport[0]==w:
                                print(AI_speaking,"I know, I asked you'",(key_question %w),"' and you said '",saved_ans.get(sport[0]),"'")
                                anna_answered=True
                                found=True
                                break
                    
                    if found==False:
                        print(AI_speaking,(key_question %w))
                        answer=input_type()
                        questions_dict['team sports'][key_question].append({w:answer})
                        array_kq[0]=1
                        pos=keywords_dict.get('positive answers')
                        
                        print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                        
                        anna_answered=True
                else:
                    print(AI_speaking,(key_question %w))
                    answer=input_type()
                    print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                    anna_answered=True

            else:
                questions=questions_dict.get('negative sports')
                key_question=random.choice(list(questions.keys()))
                print(AI_speaking,(key_question))
                answer=input_type()
                print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))
                anna_answered=True
                
        if w in keywords_dict.get('tendences'):
            if sentiment==1:
                questions=questions_dict.get('tendences')
                key_question=random.choice(list(questions.keys()))
                array_kq=questions.get(key_question)
               # print(AI_speaking,(random.choice(tendence_questions)%w))
                print(AI_speaking,(key_question %w))
                answer=input_type()
                print(AI_speaking,(random.choice(keywords_dict.get('positive answers'))))
                anna_answered=True
            else:
               # print(AI_speaking,random.choice(negative_tendences_questions))
               questions=questions_dict.get('negative tendences')
               key_question=random.choice(list(questions.keys()))
               print(AI_speaking,(key_question))
               answer=input_type()
               print(AI_speaking,(random.choice(keywords_dict.get('negative answers'))))
               anna_answered=True
        
                
    file=open("questions.txt","w")
    file.write(str(questions_dict))
    file.close()
#===========================================================================================                        


#===========================================================================================
if (os.path.isfile('user_name.txt')==False):
    print(AI_speaking,"Hi I'm Anna, a virtual AI. You can talk with me for example if you don't know what to do..")
    print(AI_speaking,"But first of all I need to know your name..")
    it_is_a_name=False
    while it_is_a_name==False:
        pos_name=input("So what's your name? : ").title()
        pos_name=TextBlob(pos_name)
        nnp=False
        for tag in pos_name.tags:
            if tag[1]=='NNP':
                nnp=True
        
        for tag in pos_name.tags:
            
            if nnp==False:
                if  tag[1]== 'NN':
                    user_name=tag[0]
                    print(AI_speaking,random.choice(keywords_dict.get('regards'))," ",user_name)
                    file=open('user_name.txt','a')
                    file.write(user_name)
                    file.close()
                    it_is_a_name=True
            if nnp==True:
                if tag[1]=='NNP':
                    user_name=tag[0]
                    print(AI_speaking,random.choice(keywords_dict.get('regards'))," ",user_name)
                    file=open('user_name.txt','a')
                    file.write(user_name)
                    file.close()
                    it_is_a_name=True
                    
        if it_is_a_name==False:
            print(AI_speaking,"This can't be your name! Are you already kidding me??? >.>")

else:
    file=open('user_name.txt','r')
    user_name=file.read()
    file.close()
    print(AI_speaking," Welcome back ",user_name,"!")
    print(AI_speaking," How are you?? :)")
    
    
    
        

            
if_not_answered=["Life is good","Life is too short","Na na Na na","Why not?","Psss, yes you..","yeah","coool","ah ah ah"]
user_speaking=user_name+" >> "

core=1
input_mode=0
while True:

    sent=input_type()
    
    if sent=="change input type":
        if input_mode==0:
            input_mode=1
            print(AI_speaking," okay, now you have to use your voice :P")
        elif input_mode==1:
            input_mode=0
            print(AI_speaking," okay, now you have to type :P")
        sent=-1
   
    if sent!=-1:
        anna_answered=False
        dep = basic_maths(sent)
        is_question = 0
        if (dep == 0):
            questions(sent)
        if (is_question == 1):
            reply_question(sent)
        else:
            input_keywords=check_keywords(sent)
            output_keywords(input_keywords)
        if anna_answered==False:
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
        if anna_answered==False:
          print (AI_speaking,random.choice(if_not_answered))
          anna_answered=True
    else:
        pass
          

#=============================================================================================
#=============================================================================================
