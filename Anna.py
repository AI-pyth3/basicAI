#=========================================================================================
#AI_version = 0.0.5
#AI_name = Anna
#=========================================================================================


#=========================================================================================
from nltk.corpus import wordnet
from textblob import TextBlob
#=========================================================================================


#=========================================================================================
import random
import socket
import wikipedia
#=========================================================================================


#=========================================================================================
global core, network, sent, is_question, is_wiki_search
#=========================================================================================


#=========================================================================================
REMOTE_SERVER = "www.google.com"
#=========================================================================================


#=========================================================================================
file=open('keywords.txt','r')
keywords_dict=eval(file.readline())
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
def reply_question():
    print ("fixme add random reply blobs here")
    return;
#===========================================================================================


#============================================================================================

how_are_you_array=["how are you?","what's up?","how are you doing?","how have you been?","how's it going?"]

AI_speaking="Anna >> "
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
            print(AI_speaking,"This is cool!")
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
               reply_question()
            else:
               print (AI_speaking, "cool")
        core=1
    else:
        sent=input(user_speaking).lower()
        input_keywords=check_keywords(sent)
        output_keywords(input_keywords)

#=============================================================================================
#=============================================================================================
