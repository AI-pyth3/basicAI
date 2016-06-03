from textblob import TextBlob
cdvalue={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6}
elements={'father':[],'mother':[],'sister':[],'brother':[]}
sent=""
count_nn=0
count_nnp=0
family=["father","brother","sister","mother"]
while(sent!="exit"):
    sent=TextBlob(input("Tell me something about your family "))
    count_start=0
    count_nnp=0
    count_hm_nnp=0
    count_current_nns=0
    count_total_nns=0
    for i in sent.tags:

       
        if (i[1]=='NN' and i[0] in family):
      
            count_hm_nnp=count_hm_nnp+1
            for j in sent.tags:
                if (j[1]=='NNP'):
                   
                    if (count_start<=count_nnp<count_hm_nnp):
                        print("Your ",i[0]," is ", j[0])
                        elements[i[0]].append(j[0])
                       
                        break
                    count_nnp=count_nnp+1
            count_start=count_start+1
            count_nnp=0
                
            
        elif (i[1]=='CD'):
            count_hm_nnp=count_hm_nnp+cdvalue.get(i[0])
          
            
            for j in sent.tags:
                
             
                if (j[1]=='NNS' and j[0].singularize() in family ):
                    if(count_total_nns==count_current_nns):
                
                         
                        for k in sent.tags:
                           
                            if (count_nnp==count_hm_nnp):
                                
                                break
                            if (k[1]=='NNP'):
                                
                                if (count_start<=count_nnp<count_hm_nnp):
                                    print("Your ",j[0].singularize()," is ", k[0])
                                    elements[j[0].singularize()].append(k[0])
                                    
                                count_nnp=count_nnp+1
                    count_current_nns=count_current_nns+1
            count_start=count_start+cdvalue.get(i[0])
            count_nnp=0
            count_total_nns=count_total_nns+1
            count_current_nns=0
                    
                    
            
            
print(elements.items())
