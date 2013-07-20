import urllib2, socket, time, re
#settings
channel = "#426699k"
server = "irc.freenode.net"
port = 6667 #6667 is the default irc port
nick = "TaiiwoBot_"
user = "Taiiwo__"
loginmessage = "-- TaiiwoBot v1.33.7 ONLINE --" #Leave blank for no message
urltolog = "http://m3ps.blogspot.de/"
maxchanges = 3 #maximum number of changes to log to IRC in one go.
interval = 0.1 #time in seconds allow for inaccuracies. raise to reduce rescource usage.
debug = False #turn debugging on and off
ignorelines = [-1,-2]#add lines for the script to ignore. This is useful for constantly
#		changing lines.
#define stuff
def geturl(recv):#parse an URL from a string
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', recv)
def pong(recv):#respond to ping req in a string --Not perfect, but works
        if "ping" or "PING" in recv:
                url = str(geturl(str(recv)))
                if url != "":
                        s.send("PONG " + url + "\n\r")
#connect to IRC
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #making socket
print "[ ]Connecting to server..."
try:
        s.connect((server,port)) #connect to server
except:
        print "[-]Could not connect to host. Please check and try again."
print "[ ]Logging in..."
s.send('nick ' + nick + '\r\n')
time.sleep(1)
s.send('user 8 * ' + user + ' my name\r\n')
time.sleep(1)
print "[ ]Joining channel..."
s.send('join ' + channel + '\r\n')
time.sleep(1)
print "Sending login message..."
s.send('privmsg ' + channel + ' :' + loginmessage + "\n\r")
time.sleep(1)

#set variables
oldhtml = urllib2.urlopen(urltolog).read().splitlines()

#starting loop
pongcount = 0
while 1:
	if pongcount >= 10:
		s.send('PONG irc.freenode.net\r\n')
		pongcount = 0
	pongcount = pongcount + 1
	if debug == True:
		print 'starting loop'
	i = 0
	changes = []
	newhtml = urllib2.urlopen(urltolog).read().splitlines()
	if debug == True:
        	print str(len(newhtml)) + 'lines in newhtml'
	while i <= len(newhtml) - 1:
		for x in ignorelines:
			if i == x:
				ignore = 1
				if debug == True:
					print 'Flagged line to ignore'
			else:
				ignore = 0
				if debug == True:
					print 'Line passed ignore test'
		if newhtml[i] != oldhtml[i] and ignore == 0:
			print 'Line changed: ' + str(i)
			if debug == True:
				print "Line didn't change."
			changes.append(i)
			oldhtml = newhtml
		i = i + 1
	linelong = 0
	for p in changes:
		if len(newhtml[p]) >= 200:
			linelong = 1
	if changes != [] and len(changes) <= maxchanges and linelong == 0:
		for y in changes:
			s.send('PRIVMSG ' + channel + ' :Line ' + str(y) + ' changed from:\r\n')
               		s.send('PRIVMSG ' + channel + ' :' + oldhtml[y] + '\r\n')
               		s.send('PRIVMSG ' + channel + ' :To:')  
               		s.send('PRIVMSG ' + channel + ' :' + newhtml[y] + '\r\n')
	elif changes != [] and linelong == 0:
		s.send('PRIVMSG ' + channel + ' :Multiple line changes. First '+ str(maxchanges) +':\r\n')
		for y in changes[:maxchanges]:
			s.send('PRIVMSG ' + channel + ' :From: ' + oldhtml[y] + '\r\n')
			s.send('PRIVMSG ' + channel + ' :To: ' + newhtml[y] + '\r\n')
	if linelong == 1 and changes != []:
		s.send('PRIVMSG ' + channel + ' :Changes were too long to post. File changes are in lines: ' + str(changes) + '\r\n')
	time.sleep(interval)
	changes = []
		
