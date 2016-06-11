from pws import Bing
import webbrowser
srch=input("What are you looking for??")
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
print("Do you want to open one of the previuos link?")
openit=input().lower()
if (openit=="yes"):
    ch_code=input("Tell me the code of the link you want to open :) ")
    ch_code=int(ch_code)
    if (1<=ch_code<=3):
        results=result.get('results')
        link_to_open=results[ch_code-1].get('link')
        webbrowser.open_new(link_to_open)
        
