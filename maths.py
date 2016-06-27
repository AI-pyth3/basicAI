operators=["+","-","/","*"]
inpop=input("insert input")
i=0
c=0
result=[]
while i<len(inpop):
    if inpop[i]in operators:
        result.append(inpop[c:i])
        result.append(inpop[i])
        c=i+1
    i+=1
result.append(inpop[c:i])
print(result)
 
