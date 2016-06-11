import urllib.request
import urllib.parse
import re
import requests
import webbrowser
a=input("Which song do you want to listen to? ")
query_string = urllib.parse.urlencode({"search_query" : a})
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
link="http://www.youtube.com/watch?v=" + search_results[0]
message="Do you want to open "+a+" in a web browser?"
openit=input(message).lower()
if openit=="yes":
    webbrowser.open_new(link)
else:
    print("Oh ok..")

