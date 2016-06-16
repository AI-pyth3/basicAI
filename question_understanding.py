from textblob import TextBlob
kind_of_verbs=["VB","VBZ","VBP","VBD","MD"]
wh_starts=["WRB","WP","WDT"]
sent=input("Tell me something: ")
sent=TextBlob(sent)
if "?" in sent:
    print("This is a question")
else:
    tag=sent.tags
    if tag[0][1]in kind_of_verbs:
        print("This is a question")
    elif tag[0][1]in wh_starts:
        print("This is a question")
    else:
        print("This is not a question")
