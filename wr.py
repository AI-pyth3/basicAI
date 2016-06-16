from collections import defaultdict
keywords_dict=defaultdict(list)
scelta=-1
while (scelta!=0):
    file=open('keywords.txt','r')       #CHANGE this with the other files. Create it before and add an empty dict in it
    keywords_dict=eval(file.readline())
    file.close()
    print("Keywords insert Script")
    print("What do you want to do?")
    print("1. View all keywords.")
    print("2. Insert a new keyword.")
    print("3. Insert a new key with new keywords. ")
    print("4. Delete a keyword.")
    print("5. Delete a key of the keyword's dict.")
    print("0. Exit. ")
    scelta=input("Input: ")
    if scelta=="1":

        for key in list(keywords_dict.keys()):
            print(key,": ",keywords_dict.get(key))
        
    if scelta=="2":
        newkw=False
        while newkw==False:
            print("Type the key of the new keyword")
            for key in list(keywords_dict.keys()):
                print(key)
            array_key=input("Key: ")
            if array_key in keywords_dict.keys():
                new_keyword=input("Insert new keyword: ")
                keywords_dict[array_key].append(new_keyword)
                newkw=True
            else:
                print("Key not found! Reinsert key")
        file=open('keywords.txt','w')
        file.write(str(keywords_dict))
        file.close()
        
    if scelta=="3":
        new_key=input("Insert the new key: ")
        if new_key in keywords_dict.keys():
            print("This key already exists!")
        else:
            new_value=input("Do you want to insert a new value for new key?").lower()
            while new_value!="no":
                value=input("Insert new value: ")
                keywords_dict.setdefault(new_key,[]).append(value)
                new_value=input("Do you want to insert a new value for new key?").lower()
            
        file=open('keywords.txt','w')
        file.write(str(keywords_dict))
        file.close()

    if scelta=="4":
        for key in list(keywords_dict.keys()):
            print(key,": ",keywords_dict.get(key))
        newkw=False
        while newkw==False:
            print("Type the key of the keyword to delete")
            for key in list(keywords_dict.keys()):
                print(key)
            array_key=input("Key: ")
            if array_key in keywords_dict.keys():
                old_keyword=input("Insert the keyword you want to delete: ")
                if old_keyword in keywords_dict[array_key]:
                    keywords_dict[array_key].remove(old_keyword)
                    newkw=True
                else:
                    print(old_keyword," can't be found in this key")
            else:
                print("Key not found! Reinsert key")
        file=open('keywords.txt','w')
        file.write(str(keywords_dict))
        file.close()
        

    if scelta=="5":
        for key in list(keywords_dict.keys()):
            print(key,": ",keywords_dict.get(key))
        old_key=input("Insert the key to be removed: ")
        if old_key in list(keywords_dict.keys()):
            print("This will REMOVE all the value for this key!")
            delkey=input("Are you sure you want remove it? (YES) ").upper()
            if (delkey=="YES"):
                keywords_dict.pop(old_key,None)
        else:
            print("Key not found!")
        
        file=open('keywords.txt','w')
        file.write(str(keywords_dict))
        file.close()        



