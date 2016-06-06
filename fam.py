import os, urllib, sys
filename = 'http://www.google.com/search?' + urllib.urlencode({'q': ' '.join(sys.argv[1:]) })
cmd = os.popen("lynx -dump %s" % filename)
output = cmd.read()
cmd.close()
print output
