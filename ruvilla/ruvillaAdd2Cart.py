#!/usr/local/bin/python
#coding:utf-8
import urllib,urllib2,cookielib,time,sys,re,json,httplib,os,subprocess
from bs4 import BeautifulSoup
import time,webbrowser
import Cookie
from cookielib import Cookie as libcookie
from send import sendMail
class FastMode:
	def __init__ (self):
		self.startTime = False
		self.nikeUrl = False
		self.siezList = {
							"7":"191","7.5":"190",
							"8":"189","8.5":"188",
							"9":"187","9.5":"186",
							"10":"185","10.5":"184",
							"11":"183","11.5":"182",
							"12":"181","13":"179"
						}
	def getUrlInfo (self,refUrl,refSkuid,Mode):
		cookiePath = "./log/"+uName+"_ruvillaCookies.txt" 
		cookie = cookielib.MozillaCookieJar(cookiePath)
		cookie.load(ignore_discard=True, ignore_expires=True)
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		req_getInfo = urllib2.Request(refUrl)
		req_getInfo.add_header('Referer', 'https://www.ruvilla.com')
		req_getInfo.add_header('Cache-Control', 'max-age=0')
		req_getInfo.add_header('Connection', 'keep-ailve')
		req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		while True:
			try:
				req2Info = opener.open(req_getInfo)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(5)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(5)
			else:
				#something you should do
				#req2Info = opener.open(req_getInfo)
				html = req2Info.read()
				soupInfo = BeautifulSoup(html)
				result = {}
				form = soupInfo.find('form',id='product_addtocart_form')
				relDate = form.find(class_="rel-date")
				if form == None:
					print "Product Not Releasing"
					time.sleep(5)
				elif relDate != None:
					self.startTime = float( relDate['data-release'])
					print "Start Time = "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.startTime)) 
					time.sleep(self.startTime - int(time.time()))
				else:
					for inputHidden in form.find_all(type='hidden'):
						if inputHidden['value']:
							result[inputHidden['name'].encode('utf-8').strip()] = urllib.quote_plus(inputHidden['value'].encode('utf-8').strip())
						else:
							result[inputHidden['name'].encode('utf-8').strip()] = ''
					nikeUrl =  form.get('action')
					#print nikeUrl
					#print result
					#print form.find_all('script',limit=3)[2].get_text().encode('utf-8').strip()
					newHidden = re.findall(r"(?<=\{\").*?(?=\":)",form.find_all('script',limit=3)[2].get_text().encode('utf-8').strip())
					newHidden =  newHidden[0].split(',')
					result['super_attribute[92]'] = newHidden[0]
					if Mode == "2":
						for inputInfo in form.find_all('dd',onclick=True):
							if inputInfo.find('span').get_text().encode('utf-8').strip() == refSkuid:
								result[inputInfo.find('input')['name'].encode('utf-8').strip()] = urllib.quote_plus(inputInfo.find('input')['value'].encode('utf-8').strip())
								newHidden = re.findall(r"(?<=')[^,:]+?(?=')",inputInfo.get('onclick').encode('utf-8').strip())
								result['super_attribute['+newHidden[1]+']'] = newHidden[0]
								break
					else:
						try:
							sizeItem = self.siezList[refSkuid]
						except:
							sizeItem = '186'
						else:
							#result['select_super_attribute[196]'] = sizeItem
							result['super_attribute[196]'] = sizeItem
					result['qty'] = 1
					result['isAjax'] = 1
					if len(result) < 5:
						print 'Error,No Enough arguments or Size Not Found!! Try again'
						try:
							refSkuid = form.find('dd',onclick=True).find('span').get_text().encode('utf-8').strip()
						except: 
							print 'No More Size '
							print refSkuid
							sys.exit()
						else:
							print refSkuid
						time.sleep(5)
						#sys.exit()
					else:
						pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'.txt'
						with open(pidPath, 'w') as outfile:
							json.dump(result, outfile)
						file_object = open(pidPath, 'a')
						file_object.write("\n"+nikeUrl)
						file_object.close( )
						self.nikeUrl = nikeUrl
						# Write Down Argvs
						return result
						break
					print 'Size Not Fount'
					#sys.exit()
class Login_In:
	def __init__ (self):
		self.cookiefile = "./log/"+uName+"_ruvillaCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request('https://www.ruvilla.com/customer/account/login')
		req.add_header('Referer','https://www.ruvilla.com/')
		req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		url_check = True
		while url_check == True:
			try:
				self.html = opener.open(req).read()
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(5)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(5)
			else:
				#something you should do
				self.soup = BeautifulSoup(self.html)
				self.formKey = self.soup.find(type='hidden',attrs={'name':'form_key'})
				self.formKey = self.formKey['value'].encode('utf-8').strip()
				url_check = False
				pass
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def saveCookies (self,uName,uPass):
		self.login_email = uName
		self.login_password = uPass
		self.cookiefile = "./log/"+uName+"_ruvillaCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie.load(ignore_discard=True, ignore_expires=True)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
					'Referer' : 'https://www.ruvilla.com/customer/account/login/'
					}
		self.url = "https://www.ruvilla.com/customer/account/loginPost/"
		self.request_body = urllib.urlencode({
			'login[username]':self.login_email,
			'login[password]':self.login_password,
			'form_key':self.formKey
			})
		req = urllib2.Request(
			self.url,
			self.request_body,
			self.hdr
			)
		while True:
			try:
				reqOpen = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(5)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(5)
			else:
				#something you should do
				self.result = opener.open(req).read()
				if re.search(uName,self.result) == None:
					print 'login faile! Try again!!'
					time.sleep(5)
				else:
					file_object = open('./log/'+self.login_email+'_ruvillaLogin.txt', 'w')
					file_object.write(self.result)
					file_object.close()
					break
		#cs = self.parse("NIKE_COMMERCE_COUNTRY=US; NIKE_COMMERCE_LANG_LOCALE=en_US; mt.m=%7B%22membership%22%3A%5B%22us_aa-el1-ae%22%5D%7D; CONSUMERCHOICE_SESSION=t; CONSUMERCHOICE=us/en_us; nike_locale=us/en_us; cookies.js=1;",".nike.com")
		#for c in cs:
		#	self.cookie.set_cookie(c)
		#print(self.cookie)
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def parse(self,rawstr,url):
		url = '.'+'.'.join(url.split('.')[1:])
		c = Cookie.SimpleCookie()
		c.load(rawstr)
		ret = []
		for k in c:
			#get v as Morsel Object
			v = c[k]
			ret.append(libcookie(
						name=v.key,
						value = v.value,
						version=0,
						port=None,
						port_specified = False,
						domain=url, 
						domain_specified=True, 
						domain_initial_dot=True, 
						path='/', 
						path_specified=True, 
						secure=False, 
						expires=None, 
						discard=False, 
						comment=None, 
						comment_url=None, 
						rest={'HttpOnly': None}, 
						rfc2109=False,
			))
		return ret

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("UTF8")

	try: 
		Mode = sys.argv[1] 
	except IndexError:
		Mode = raw_input(u"1.Fast\n2.Normal\n3.Login\n请输入抢购模式:".encode('utf-8'))
	try: 
		uName = sys.argv[2] 
	except IndexError:
		uName = raw_input(u"请输入账号:".encode('utf-8'))
	try: 
		uPass = sys.argv[3] 
	except IndexError:
		uPass = raw_input(u"请输入密码:".encode('utf-8'))
	try: 
		refUrl = sys.argv[4] 
	except IndexError:
		refUrl = raw_input(u"请将鞋子页面的链接复制过来\n".encode('utf-8'))
	try:
		refSkuid = sys.argv[5]
	except IndexError:
		refSkuid = raw_input(u"请输入抢购码数:".encode('utf-8'))
	pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'.txt'
	Pid = filter(str.isdigit,refUrl)+'_'+refSkuid
	cookiePath = "./log/"+uName+"_ruvillaCookies.txt" 
	if Mode == "3":
		print 'Mode = Login Username = '+uName
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
		sys.exit()
	else:
		if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 7200:
			print 'Login first'
			login_test = Login_In()
			login_test.saveCookies(uName,uPass)
		try:
			jsonFile = open(pidPath)
		except:
			print 'get result'
			fastMode = FastMode()
			result = fastMode.getUrlInfo(refUrl,refSkuid,Mode)
			nikeUrl = fastMode.nikeUrl
		else:
			print 'result file exits'
			result = json.loads(jsonFile.readline())
			nikeUrl = jsonFile.readline()
		try:
			ccdFile = open('../ccd')
		except:
			print 'No ccd Argvs'
			sys.exit()
		else:
			print 'Load ccd Argvs'
			ccd = json.loads(ccdFile.readline())
	#print nikeUrl
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	#print result
	req_add2cart_body = urllib.urlencode(result)
	#print req_add2cart_body
	#sys.exit()
	print 'start now'
	while True:
		req_add2cart = urllib2.Request(nikeUrl,req_add2cart_body)
		req_add2cart.add_header('Referer', refUrl)
		req_add2cart.add_header('Cache-Control', 'no-cache')
		req_add2cart.add_header('Connection', 'keep-ailve')
		req_add2cart.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		try:
			req2cart = opener.open(req_add2cart)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
			print "The server couldn't fulfill the request"
			print "Error code:",e.code
			time.sleep(5)
			#print "Return content:",e.read()
		except urllib2.URLError,e:
			print "Failed to reach the server"
			print "The reason:",e.reason
			time.sleep(5)
		else:
			#something you should do
			html = req2cart.read().decode('utf-8')
			if html.find('out of stock') != -1:
				print "Sold Out!"
				file_object = open('./log/'+Pid+'_'+uName+'_ruvillaError.txt', 'w')
				file_object.write(html)
				file_object.close( )
				break
			elif html.find('was added to your shopping cart') == -1:
				print "Can't add to Cart! Try again later!"
				file_object = open('./log/'+Pid+'_'+uName+'_ruvillaError.txt', 'w')
				file_object.write(html)
				file_object.close( )
				time.sleep(4)
			else:
				file_object = open('./log/'+Pid+'_'+uName+'_ruvillaItem.txt', 'w')
				file_object.write(html)
				file_object.close( )
				print "Check Out Now!!"
				mail = sendMail()
				mail.send_email(uName,html,"Ruvilla")
				cookie.save(ignore_discard=True, ignore_expires=True)
				sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --aPid='"+Pid+"' --cFile='"+cookiePath+"' --ccd='"+ccd[uName]+"'"
				child = subprocess.Popen(sh,shell=True)
				child.wait()
				print sh
				break
	#print req_add2cart.header_items()
	#print req2cart.info()
	#print cookie
	#print req2cart.read()
#'''
