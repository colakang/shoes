#!/usr/local/bin/python
#coding:utf-8
import urllib,urllib2,cookielib,time,sys,re,json,httplib,os,subprocess,gzip,StringIO,multiprocessing
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
							"4.5":"04.5","5":"05.0",
							"5.5":"05.5","6":"06.0",
							"6.5":"06.5","4":"04.0",
							"7":"07.0","7.5":"07.5",
							"8":"08.0","8.5":"08.5",
							"9":"09.0","9.5":"09.5",
							"10":"10.0","10.5":"10.5",
							"11":"11","11.5":"11.5"
						}
	def getUrlInfo (self,refUrl,refSkuid,Mode):
		cookiePath = "./log/"+uName+"_MchampssportsCookies.txt" 
		cookie = cookielib.MozillaCookieJar(cookiePath)
		cookie.load(ignore_discard=True, ignore_expires=True)
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		req_getInfo = urllib2.Request(refUrl)
		req_getInfo.add_header('Referer', 'http://m.champssports.com')
		req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
		req_getInfo.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req_getInfo.add_header('Accept-Encoding','gzip, deflate, sdch')
		req_getInfo.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req_getInfo.add_header('Cache-Control','no-cache')
		req_getInfo.add_header('Upgrade-Insecure-Requests','1')
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
				if req2Info.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2Info.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = req2Info.read()
				getTime = int(re.findall("(?<=productLaunchTimeUntil =)[^,:]+?(?=;)",html)[0])
				if re.search('var cm_isLaunchSku = \'N\';',html) == None: 
					self.startTime = time.time()+getTime
				soupInfo = BeautifulSoup(html,'html.parser')
				result = {}
				for inputHidden in soupInfo.find(id='product_form').find_all(type='hidden'):
					if inputHidden['value']:
						result[inputHidden['name'].encode('utf-8').strip()] = urllib.quote_plus(inputHidden['value'].encode('utf-8').strip())
					else:
						try:
							result[inputHidden['name'].encode('utf-8').strip()] = self.siezList[refSkuid]
						except:
							result[inputHidden['name'].encode('utf-8').strip()] = refSkuid
				pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'_'+uName+'.txt'
				with open(pidPath, 'w') as outfile:
					json.dump(result, outfile)
				return result
				#sys.exit()

class Login_In:
	def __init__ (self):
		self.cookiefile = "./log/"+uName+"_MchampssportsCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request('https://m.champssports.com/?uri=account')
		req.add_header('Referer','https://m.champssports.com/')
		req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
		req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('Accept-Encoding','gzip, deflate, sdch')
		req.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req.add_header('Cache-Control','no-cache')
		req.add_header('Upgrade-Insecure-Requests','1')
		url_check = True
		while url_check == True:
			try:
				req2login = opener.open(req)
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
				if req2login.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2login.read())
					f = gzip.GzipFile(fileobj=buf)
					self.html = f.read()
				else:
					self.html = req2login.read()
				#something you should do
				self.soup = BeautifulSoup(self.html,'html.parser')
				self.result = {}
				for inputHidden in self.soup.find_all(type='hidden',value=True):
					if inputHidden['value']:
						self.result[inputHidden['name'].encode('utf-8').strip()] = urllib.quote_plus(inputHidden['value'].encode('utf-8').strip())
				if len(self.result) > 1:
					#print self.result
					url_check = False
				pass
	def saveCookies (self,uName,uPass):
		self.login_email = uName
		self.login_password = uPass
		self.hdr = {
					'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
					'Referer' : 'https://m.champssports.com/?uri=account',
					'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'Accept-Encoding' : 'gzip, deflate, sdch',
					'Accept-Language' : 'zh-CN,zh;q=0.8',
					'Cache-Control' : 'no-cache',
					'Upgrade-Insecure-Requests' : '1'
					}
		self.requestKey = self.result['requestKey']
		self.co_cd = self.result['companyCode']
		self.url = "https://m.champssports.com/?uri=account/accountSignIn"
		self.request_body = urllib.urlencode({
			'email':self.login_email,
			'password':self.login_password,
			'requestKey':self.requestKey,
			'companyCode':self.co_cd,
			'submit':'Continue'
			})
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request(
			self.url,
			self.request_body,
			self.hdr
			)
		url_check = True
		while url_check == True:
			try:
				reqOpen = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				print "Return content:",e.read()
				time.sleep(15)
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				if reqOpen.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(reqOpen.read())
					f = gzip.GzipFile(fileobj=buf)
					self.result = f.read()
				else:
					self.result = reqOpen.read()
				#something you should do
				if re.search('Log Out',self.result) == None:
					print "Login Error! Pls Try Again!!"
					time.sleep(5)
				else:
					url_check = False
					file_object = open('./log/'+self.login_email+'_MchampssportsLogin.txt', 'w')
					file_object.write(self.result)
					file_object.close( )
					self.cookie.save(ignore_discard=True, ignore_expires=True)
					pass
				#cs = self.parse("NIKE_COMMERCE_COUNTRY=US; NIKE_COMMERCE_LANG_LOCALE=en_US; mt.m=%7B%22membership%22%3A%5B%22us_aa-el1-ae%22%5D%7D; CONSUMERCHOICE_SESSION=t; CONSUMERCHOICE=us/en_us; nike_locale=us/en_us; cookies.js=1;",".nike.com")
				#for c in cs:
				#	self.cookie.set_cookie(c)
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

def removeCart(refUrl,uName,postData):
	cookiePath = "./log/"+uName+"_MchampssportsCookies.txt" 
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	print postData
	req_getInfo = urllib2.Request('http://m.champssports.com/?uri=cart',postData)
	req_getInfo.add_header('Referer', 'http://m.champssports.com/?uri=cart')
	req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
	req_getInfo.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req_getInfo.add_header('Accept-Encoding','gzip, deflate, sdch')
	req_getInfo.add_header('Accept-Language','zh-CN,zh;q=0.8')
	req_getInfo.add_header('Cache-Control','no-cache')
	req_getInfo.add_header('Upgrade-Insecure-Requests','1')
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
			if req2Info.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2Info.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read()
			else:
				html = req2Info.read()
			if re.search('form id="shoppingCartForm"',html) == None:
				print "Removed all Item"
				return True
			else:
				print "Some thing in cart"
				return False
			print "sleep 300"
			time.sleep(300)

def checkCart(refUrl,uName,sh):
	cookiePath = "./log/"+uName+"_MchampssportsCookies.txt" 
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	req_getInfo = urllib2.Request('http://m.champssports.com/?uri=cart')
	req_getInfo.add_header('Referer', 'http://m.champssports.com/?uri=cart')
	req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
	req_getInfo.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	req_getInfo.add_header('Accept-Encoding','gzip, deflate, sdch')
	req_getInfo.add_header('Accept-Language','zh-CN,zh;q=0.8')
	req_getInfo.add_header('Cache-Control','no-cache')
	req_getInfo.add_header('Upgrade-Insecure-Requests','1')
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
			if req2Info.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2Info.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read()
			else:
				html = req2Info.read()
			if re.search('form id="shoppingCartForm"',html) == None:
				print "Nothing in Cart"
			else:
				soupInfo = BeautifulSoup(html,'html.parser')
				result = {}
				tmp = ''
				updateIDs = soupInfo.find(id='shoppingCartForm').find_all(type='hidden',attrs={'name':'updateIDs'})
				SKUs = soupInfo.find(id='shoppingCartForm').find_all(type='hidden',attrs={'name':'SKUs'})
				allHidden = soupInfo.find(id='shoppingCartForm').find_all('input',value=True)
				for value in allHidden:
					if value['value']:
						tmp = tmp + "&" + value['name'] + '=' + urllib.quote_plus(value['value'])
				result['cartAction'] = 'remove'
				for k,inputHidden in enumerate(updateIDs):
					if re.search(inputHidden['value'],refUrl) == None:
						print "Remove this Itme:"+inputHidden['value']+ " SKUs = " +SKUs[k]['value']
						result['selectedID'] = inputHidden['value']
						postData = urllib.urlencode(result)
						postData = postData + tmp
						#print postData
						removeCart(refUrl,uName,postData)
					else:
						print "Go to checkout!!"
						child = subprocess.Popen(sh,shell=True)
						child.wait()
						return True
			print "sleep 300"
			time.sleep(300)
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
	pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'_'+uName+'.txt'
	Pid = filter(str.isdigit,refUrl)+'_'+refSkuid
	cookiePath = "./log/"+uName+"_MchampssportsCookies.txt" 
	if Mode == "3":
		print 'Mode = Login Username = '+uName
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
		sys.exit()
	elif Mode == "5":
			print 'Mode = Check Cart  Username = '+uName
			if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 1800:
				print 'Login first'
				login_test = Login_In()
				login_test.saveCookies(uName,uPass)
			pool = multiprocessing.Pool(processes = 1)
			pool.apply_async(checkCart, (refUrl,uName,'111', ))
			print "Go Go Go"
			pool.close()
			pool.join()
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
		else:
			print 'result file exits'
			result = json.loads(jsonFile.readline())
		try:
			ccdFile = open('../ccd')
		except:
			print 'No ccd Argvs'
			sys.exit()
		else:
			print 'Load ccd Argvs'
			ccd = json.loads(ccdFile.readline())
	nikeUrl = 'http://m.champssports.com/?uri=add2cart&fragment=true'
	try:
		startTime = fastMode.startTime
	except:
		startTime = 0
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	#print result
	req_add2cart_body = urllib.urlencode(result)
	#print req_add2cart_body
	#sys.exit()
	sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --aPid='"+Pid+"' --cFile='"+cookiePath+"' --ccd='"+ccd[uName]+"'"
	pool = multiprocessing.Pool(processes = 1)
	pool.apply_async(checkCart, (refUrl,uName,sh, ))
	pool.close()
	if (startTime - int(time.time())) >= 1:
		print "Start Time = "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) 
		time.sleep(startTime - int(time.time()))
	else:
		print 'start now'
	while True:
		req_add2cart = urllib2.Request(nikeUrl,req_add2cart_body)
		req_add2cart.add_header('Referer', refUrl)
		req_add2cart.add_header('Connection', 'keep-ailve')
		req_add2cart.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
		req_add2cart.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req_add2cart.add_header('Accept-Encoding','gzip, deflate, sdch')
		req_add2cart.add_header('Accept-Language','zh-CN,zh;q=0.8')
		req_add2cart.add_header('Cache-Control','no-cache')
		req_add2cart.add_header('Upgrade-Insecure-Requests','1')
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
			if req2cart.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2cart.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read().decode('utf-8')
			else:
				html = req2cart.read().decode('utf-8')
			#html = req2cart.read().decode('utf-8')
			if html.find('"success":true') == -1:
				if html.find('Unauthorized order') != -1:
					print "Renew Request Key! Old Key = " + result['requestKey']
					try:
						login_test = Login_In()
						login_test.saveCookies(uName,uPass)
						cookie.revert(ignore_discard=True, ignore_expires=True)
						fastMode = FastMode()
						result = fastMode.getUrlInfo(refUrl,refSkuid,Mode)
					except:
						print "Can't get New requestKey."
						sys.exit()
					else:
						print "New Key = " + result['requestKey']
						req_add2cart_body = urllib.urlencode(result)
						file_object = open('./log/'+Pid+'_'+uName+'_MchampssportsDebug.txt', 'w')
						file_object.write(html)
						file_object.close( )
				elif html.find('it is out of stock') != -1:
					print "SOLD OUT !!"
					file_object = open('./log/'+Pid+'_'+uName+'_MchampssportsError.txt', 'w')
					file_object.write(html)
					file_object.close( )
					break
				else:
					print "Can't add to Cart! Try again later!"
					file_object = open('./log/'+Pid+'_'+uName+'_MchampssportsError.txt', 'w')
					file_object.write(html)
					file_object.close( )
				time.sleep(3)
			else:
				file_object = open('./log/'+Pid+'_'+uName+'_MchampssportsItem.txt', 'w')
				file_object.write(html)
				file_object.close( )
				print "Check Out Now!!"
				mail = sendMail()
				mail.send_email(uName,html,"Champssports")
				#if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 299:
				#	login_test = Login_In()
				#	login_test.saveCookies(uName,uPass)
				sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --aPid='"+Pid+"' --cFile='"+cookiePath+"' --ccd='"+ccd[uName]+"'"
				print sh
				child = subprocess.Popen(sh,shell=True)
				child.wait()
				pool.join()
				break
	# checkout url = http://m.champssports.com/?uri=cart&action=checkout
	#print req_add2cart.header_items()
	#print req2cart.info()
	#print cookie
	#print req2cart.read()
#'''
