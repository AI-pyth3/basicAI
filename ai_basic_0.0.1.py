import random
family_array=["mother","mum","father","dad","brother","brothers","sister","sisters","parent","cousin","cousins",
              "son","daughter","uncle","aunt","children","mom","grandfather","grandmother","family"]
team_sport_array=["football","soccer","rugby","baseball","basketball","volleyball", "cricket", "hockey"]
single_sports_array=["golf","tennis","ping pong","pool","billiards"]
feelings_array=["like","love","hate","prefer", "angry","sad","happy","cool"]
tendences_array=["google","facebook","twitter","google+","blogs","blog","youtube","telegram","whatsapp","hike"]
vip_arrays=[]
yes_answers_array=["yes","yup","yea","ja","yes i am","sure","surely"]
no_answers_array=["no","nope","nix","nah","no i am not","negative"]
regards_array=["hi","hello","hey","yo","sup"]
negative_array=["isn't","don't","mustn't","not"]
hwy_positive_answer=["not bad","fine","fine thanks","very well","i'm fine","thank you","lovely","sexy","I am good","not good"]
hwy_negative_answer=["so-so","not well","i have been better","really bad","you can't even imagine","its really bad","I am sad for you"]
positive_answers=["oh ok","sweet","nice","good","hmm ok ","this is cool","cool","great","that seems nice","wow"]
negative_answers=["oh yes","hmm you are right","oh understood.."," I get it..","mmh","maybe.."]
keywords_array=[family_array,team_sport_array,single_sports_array,feelings_array,tendences_array,
                yes_answers_array,no_answers_array,regards_array,negative_array,hwy_positive_answer,
                hwy_negative_answer]
how_are_you_array=["how are you?","what's up?","how are you doing?","how have you been?","how's it going?"]

AI_speaking="Easter >> "
sentiment=0
def check_keywords(sentence):
    keywords=[]
    for ch in ["?","!",".",","]:
        if ch in ["?","!",".",","]:
           sentence=sentence.replace(ch," ")
    words=sentence.split()

    for w in words:
        for array in keywords_array:
            if w in array:
                keywords.append(w)
    
    return keywords

def output_keywords(keywords):
    global sentiment
    if (len(keywords)!=0):
        w=keywords[0]
        if w in regards_array:
            print(AI_speaking,random.choice(how_are_you_array))
        elif w in hwy_positive_answer:
            print(AI_speaking,"This is cool!")
            print(AI_speaking,"Tell me something you like for example ")
        elif w in hwy_negative_answer:
            print("Come'on everythings will be good!")
            print(AI_speaking,"Tell me something you like for example ")
            
        elif w in negative_array:
            sentiment=-1
            for k in keywords:
                if k in feelings_array:
                    if k=="hate":
                        sentiment=1
                    else:
                        sentiment=-1
            general_array_output(keywords,sentiment)
           
        elif w in feelings_array:
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
    else:
        if sentiment==1:
            print(AI_speaking,random.choice(positive_answers))
        elif sentiment==-1:
            print(AI_speaking,random.choice(negative_answers))
            
def general_array_output(kw,sentiment):
    word=""
    team_sport_questions=["Why do you like %s ?","Which is your favourite %s team?","Who is your favourite %s player?",
                          "Have you ever seen a %s match?","Do you play %s ??"]
    single_sports_questions=["Why do you like %s ?","Who is your favourite %s player?","Have you ever seen a %s match?","Do you play %s ?"]
    tendence_questions=["Why do you like %s ?","How many times a day do you visit %s ?","What do you think about %s ?"]
    negative_sport_questions=["Why not?","So what sport do you like?","Why don't you like it ?"]
    negative_tendences_questions=["Why don't you like it ?","What social network do you like?","Why not?"]
    for w in kw:
        if w in team_sport_array:
            if sentiment==1:
                print(AI_speaking,(random.choice(team_sport_questions)%w))
            else:
                print(AI_speaking,random.choice(negative_sport_questions))
        if w in single_sports_array:
            if sentiment==1:
                print(AI_speaking,(random.choice(single_sports_questions)%w))
            else:
                print(AI_speaking,random.choice(negative_sport_questions))
        if w in tendences_array:
            if sentiment==1:
                print(AI_speaking,(random.choice(tendence_questions)%w))
            else:
                print(AI_speaking,random.choice(negative_tendences_questions))

        
                
                
            

print(AI_speaking,"Hi I'm Easter, a virtual AI. You can talk with me for example if you don't know what to do..")
print(AI_speaking,"But first of all I need to know your name..")
user_name=input("So what's your name? ")
user_speaking=user_name+" >> "
print(AI_speaking,random.choice(regards_array)," ",user_name)
while True:
    sent=input(user_speaking).lower()
    input_keywords=check_keywords(sent)
    output_keywords(input_keywords)
    
    
