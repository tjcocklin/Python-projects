#@author: Jeffrey Cocklin
#@version: 1.0
#description: Script downloads a mp3 from the latest avialabe at
#Ocremix.org

#!usr/bin/python3

import sys
import urllib.request
#import json
#import textwrap
from html.parser import HTMLParser

# Class inherits for HTMLParser and redefines handle start tag
class MyHtmlParser(HTMLParser):
	
	def __init__(self):
		super(MyHtmlParser,self).__init__()
		self.count =0
		self.path= []
		self.titles=[]
	
	#Methond that retrieves the song title from a tuple in an 'a' tag
	def handle_starttag(self, tag, attrs):
		
		if(tag == 'a'):
			for i in attrs:
				if(i[0] == 'href' and
				i[1].startswith('/remix/')):
					
					self.path.append(i[1])
				
				if(i[0] == 'title'and
				i[1].startswith('ReMix')):
					
					print(str(self.count)+':',i[1])
					#, self.path[-1])
					
					self.count += 1
					self.titles.append(i[1])
	#unused				#print(i)
	def handle_endtag(self, tag):
		pass
	#unused
	def handle_data(self,data):
		pass
	
	#unused mutator that returns path list	
	def getPath(self):
		return self.path
	
	#mututator that returns title list
	def getTitles(self):
		return self.titles

#Saves the mp3 retrieved from url in the given outFile
def open_n_write(loc, outFile):

	mp3File= urllib.request.urlopen(loc)


	File= open(outFile+".mp3", 'wb+')
	data= mp3File.read()
	File.write(data)

	File.close()


#Prompts the user for input.
def prompt( options):
	
	res = -2		
	while(res >= len(options) or res <= -2  ):
	
		res= input("\nenter number to download or type -1 to exit:" )
		res= int(res)
        
	return res

#Removes characters from a string based on ascii decimal value
def cleanStr(str):
	
	
	str = str.replace('ReMix: ','')
	str=  str.replace('\'','',1)
	
	str=  str.strip()
	str= str.rstrip('\'')
	
	#print("after rstrip ", str)
	
	for eachItem in str:
		val= ord(eachItem)
		if(val == 32):
			str =str.replace(eachItem,'_')
		
		elif( val >=34 and val <= 47):
			
			if(val == 39 or val ==36 or val == 38):
				continue	
				
	
			else:
				str= str.replace(eachItem, '')
		
		elif(val >=58 and val <=64 ):
			str= str.replace(eachItem, '')

		elif(val >=91 and val<= 96):
			str= str.replace(eachItem, '')

		elif(val >= 123 and val<= 127):
			str= str.replace(eachItem, '')

	
	return str
	
# Program opens url to OCRemx.org and retrieves the latest remixs.
# and downloads the requested song.
def main():
	
	print("Here are the lastest remixs from OCRemix.org")
	url= "http://ocremix.org"
		
	f= urllib.request.urlopen(url) 
	text= f.read()
	
	decodedtext= text.decode('utf-8')
	
	parser= MyHtmlParser()
	parser.feed(decodedtext)

	options= parser.getTitles()
	
	response = prompt(options)
        
	#Evaluate the user response and/or retrieve song
	if (response == -1):
		sys.exit("\nExiting script goodbye.")
	else:
		
		selection= cleanStr(options[response])
		print("\nSelection: ",selection)
		url2Start= "http://ocrmirror.org/files/music/remixes/"
		
		url2end=url2Start+"{}{}".format(selection, "_OC_ReMix.mp3")
		print("\nretrieving mp3 from:",url2end)	
				
		open_n_write(url2end,selection)
		print("\nAll done! Your files is named", selection+".mp3")
	



if __name__ == "__main__": main() 
