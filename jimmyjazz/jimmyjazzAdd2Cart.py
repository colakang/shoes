#!/usr/local/bin/python
#coding:utf-8
import urllib,urllib2,cookielib,time,sys,re,json,httplib,os,subprocess,StringIO,gzip
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
		cookiePath = "./log/"+uName+"_jimmyjazzCookies.txt" 
		cookie = cookielib.MozillaCookieJar(cookiePath)
		cookie.load(ignore_discard=True, ignore_expires=True)
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		req_getInfo = urllib2.Request(refUrl)
		req_getInfo.add_header('Referer', 'http://www.jimmyjazz.com')
		req_getInfo.add_header('Connection', 'keep-ailve')
		req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		req_getInfo.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req_getInfo.add_header('accept-encoding','gzip, deflate, sdch')
		req_getInfo.add_header('accept-language','zh-CN,zh;q=0.8')
		while True:
			try:
				req2Info = opener.open(req_getInfo)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
					print e.read()
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				print req2Info.info()
				break
				time.sleep(15)
			else:
				#something you should do
				#req2Info = opener.open(req_getInfo)
				if req2Info.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2Info.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = req2Info.read()
				soupInfo = BeautifulSoup(html,'html.parser')
				result = {}
				skuList = soupInfo.find('div',class_='psizeoptioncontainer')
				if skuList == None:
					print "Product Not Releasing"
					time.sleep(15)
				else:
					for skuid in skuList.find_all('a'):
						if (skuid.get_text() == refSkuid):
							id = skuid['id'].split('_')
							id = id[1].strip()
							nikeUrl = "http://www.jimmyjazz.com/request/cart/add/"+id+"/1"
							print nikeUrl
							break
					try:
						id
					except NameError:
						print 'Error,No Enough arguments or Size Not Found!! Try again'
						time.sleep(15)
						#sys.exit()
					else:
						pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'.txt'
						file_object = open(pidPath, 'w')
						file_object.write(nikeUrl)
						file_object.close( )
						# Write Down Argvs
						return nikeUrl
						break
					print 'Size Not Fount'
					#sys.exit()
class Login_In:
	def __init__ (self):
		self.cookiefile = "./log/"+uName+"_jimmyjazzCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request('https://www.jimmyjazz.com/customer/account/login')
		req.add_header('Referer','https://www.jimmyjazz.com/')
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
				self.soup = BeautifulSoup(self.html,'html.parser')
				self.formKey = self.soup.find(type='hidden',attrs={'name':'form_key'})
				self.formKey = self.formKey['value'].encode('utf-8').strip()
				url_check = False
				pass
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def saveCookies (self,uName,uPass):
		self.login_email = uName
		self.login_password = uPass
		self.cookiefile = "./log/"+uName+"_jimmyjazzCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie.load(ignore_discard=True, ignore_expires=True)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
					'Referer' : 'https://www.jimmyjazz.com/customer/account/login/'
					}
		self.url = "https://www.jimmyjazz.com/customer/account/loginPost/"
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
					file_object = open('./log/'+self.login_email+'_jimmyjazzLogin.txt', 'w')
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


class checkOut:
	def __init__ (self):
		self.cookiefile = "./log/"+uName+"_jimmyjazzCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie.load(ignore_discard=True, ignore_expires=True)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request('https://www.jimmyjazz.com/cart/checkout')
		req.add_header('Referer','https://www.jimmyjazz.com/')
		req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		req.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('accept-encoding','gzip, deflate, sdch')
		req.add_header('accept-language','zh-CN,zh;q=0.8')
		url_check = True
		while url_check == True:
			try:
				req2checkout = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					self.cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				#something you should do
				if req2checkout.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2checkout.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = req2checkout.read()
	
				soup = BeautifulSoup(html,'html.parser')
				self.form_build_id = soup.find('form',id='cart-checkout-form').find(type='hidden',attrs={'name':'form_build_id'})
				self.form_build_id = self.form_build_id['value'].encode('utf-8').strip()
				self.form_id = 'cart_checkout_form'
				url_check = False
				#print self.form_build_id
				#print self.form_id
				pass
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def doCheckOut (self,uName,uPass,refUrl):
		self.login_email = uName
		self.login_password = uPass
		key = int(ccd[uName])
		try:
			phone = ccdInfo[key]['phone']
			first = ccdInfo[key]['first']
			last = ccdInfo[key]['last']
			cardNo = ccdInfo[key]['cardNo']
			cardMM = ccdInfo[key]['cardMM']
			cardYY = ccdInfo[key]['cardYY']
			cardCCV = ccdInfo[key]['cardCCV']
			cardTYPE = ccdInfo[key]['cardTYPE'].capitalize()
		except:
			print "No ccdInfo. Using Default Info"
			phone = "5105655803"
			first = "neng"
			last = "kang"
			cardNo = "4392258701551857"
			cardMM = "11"
			cardYY = "19"
			cardCCV = "326"
			cardTYPE = "Visa"
		cardNo = re.sub('(....)', r' \1', cardNo).strip()
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
					'Referer' : refUrl,
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'accept-encoding':'gzip, deflate',
					'accept-language':'zh-CN,zh;q=0.8',
					}
		self.url = "https://www.jimmyjazz.com/cart/checkout"
		self.request_body = urllib.urlencode({
			'billing_email':self.login_email,
			'billing_email_confirm':self.login_email,
			'billing_phone':phone,
			'email_opt_in':'1',
			'shipping_first_name':first,
			'shipping_last_name':last,
			'shipping_address1':'4122 lombard ave. apt b',
			'shipping_address2':'',
			'shipping_city':'fremont',
			'shipping_state':'CA',
			'shipping_zip':'94536',
			'shipping_method':'0',
			'billing_same_as_shipping':'1',
			'billing_first_name':'',
			'billing_last_name':'',
			'billing_country':'US',
			'billing_address1':'',
			'billing_address2':'',
			'billing_city':'',
			'billing_state':'',
			'billing_zip':'',
			'cc_type':cardTYPE,
			'cc_number':cardNo,
			'cc_exp_month':cardMM,
			'cc_exp_year':cardYY,
			'cc_cvv':cardCCV,
			'gc_num':'',
			'form_build_id':self.form_build_id,
			'form_id' :self.form_id
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
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					self.cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				#something you should do
				if reqOpen.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(reqOpen.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = reqOpen.read()
				#print html
				soup = BeautifulSoup(html,'html.parser')
				print soup.find_all('div',class_="messages error")
				print soup.find_all('div',class_="jj_error")
				print soup.find_all('a',class_='remove')
				print soup.find('div',class_="confirm_price_right_grand")
				form_build_id = soup.find('form',id='cart-confirm-form').find(type='hidden',attrs={'name':'form_build_id'})
				form_build_id = form_build_id['value'].encode('utf-8').strip()
				form_id = 'cart_confirm_form'
				try:
					form_build_id
				except NameError:
					print 'Error,Form_build_id Not Found!! Try again'
					time.sleep(5)
					#sys.exit()
				else:
					# Write Down Argvs
					argvs = {}
					argvs['form_build_id'] = form_build_id
					argvs['form_id'] = form_id
					print argvs
					#self.submit(refUrl,argvs) 
					break
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def submit (self,refUrl,argvs):
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
					'Referer' : refUrl,
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'accept-encoding':'gzip, deflate',
					'accept-language':'zh-CN,zh;q=0.8',
					}
		self.url = "https://www.jimmyjazz.com/cart/confirm"
		self.request_body = urllib.urlencode(argvs)
		req = urllib2.Request(
			self.url,
			self.request_body,
			self.hdr
			)
		while True:
			try:
				reqOpen = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					self.cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				#something you should do
				if reqOpen.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(reqOpen.read())
					f = gzip.GzipFile(fileobj=buf)
					self.result = f.read()
				else:
					self.result = reqOpen.read()
				if re.search('sucess',self.result) == None:
					print 'Submit Faile! Try again!!'
					file_object = open('./log/'+self.login_email+'_jimmyjazzSubmit.txt', 'w')
					file_object.write(self.result)
					file_object.close()
					break
					time.sleep(15)
				else:
					file_object = open('./log/'+self.login_email+'_JimmyjazzSubmit.txt', 'w')
					file_object.write(self.result)
					file_object.close()
					break
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	
class RemoveCart:
	def __init__ (self):
		self.cookiefile = "./log/"+uName+"_jimmyjazzCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie.load(ignore_discard=True, ignore_expires=True)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request('http://www.jimmyjazz.com/cart/')
		req.add_header('Referer','https://www.jimmyjazz.com/')
		req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		req.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req.add_header('accept-encoding','gzip, deflate, sdch')
		req.add_header('accept-language','zh-CN,zh;q=0.8')
		url_check = True
		while url_check == True:
			try:
				req2checkout = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					self.cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				#something you should do
				if req2checkout.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2checkout.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = req2checkout.read()
				soup = BeautifulSoup(html,'html.parser')
				for removeId in soup.find_all('a',class_='remove'):
					removeUrl = 'http://www.jimmyjazz.com'+removeId['href']
					print removeUrl
					self.delete(refUrl,removeUrl)
				url_check = False
				pass
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	def delete (self,refUrl,delUrl):
		#self.cookiefile = "./log/"+uName+"_jimmyjazzCookies.txt" 
		#self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		#self.cookie.load(ignore_discard=True, ignore_expires=True)
		#self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36',
					'Referer' : refUrl,
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'accept-encoding':'gzip, deflate',
					'accept-language':'zh-CN,zh;q=0.8',
					}
		self.url = delUrl
		self.request_body = None
		req = urllib2.Request(
			self.url,
			self.request_body,
			self.hdr
			)
		while True:
			try:
				reqOpen = opener.open(req)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				if re.search('hidden',e.read()) != None:
					print "Renew Cookies"
					sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
					child = subprocess.Popen(sh,shell=True)
					child.wait()
					cookie.revert(ignore_discard=True, ignore_expires=True)
				else:
					print "The server couldn't fulfill the request"
					print "Error code:",e.code
				time.sleep(15)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(15)
			else:
				#something you should do
				if reqOpen.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(reqOpen.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read()
				else:
					html = reqOpen.read()
				#print html
				break
		self.cookie.save(ignore_discard=True, ignore_expires=True)
	

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
	cookiePath = "./log/"+uName+"_jimmyjazzCookies.txt" 
	if Mode == "3":
		print 'Mode = Login Username = '+uName
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
		sys.exit()
	elif Mode == "4":
		print 'Mode = Remove Cart'
		removeCart = RemoveCart()		
		sys.exit()
	else:
		if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 3600:
			print 'Get Cookie first'
			sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
			child = subprocess.Popen(sh,shell=True)
			child.wait()
		try:
			jsonFile = open(pidPath)
		except:
			print 'get result'
			fastMode = FastMode()
			nikeUrl = fastMode.getUrlInfo(refUrl,refSkuid,Mode)
		else:
			print 'result file exits'
			nikeUrl = jsonFile.readline()
		try:
			ccdFile = open('../ccd')
		except:
			print 'No ccd Argvs'
			sys.exit()
		else:
			print 'Load ccd Argvs'
			ccd = json.loads(ccdFile.readline())
		try:
			ccdInfoF = open('../ccdInfo')
		except:
			print 'No ccdInfo Argvs'
			sys.exit()
		else:
			print 'Load ccdInfo Argvs'
			ccdInfo = json.loads(ccdInfoF.readline())
	#print nikeUrl
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	#print result
	#req_add2cart_body = urllib.urlencode(result)
	#print req_add2cart_body
	#sys.exit()
	print 'start now'
	while True:
		req_add2cart = urllib2.Request(nikeUrl)
		req_add2cart.add_header('Referer', refUrl)
		req_add2cart.add_header('Cache-Control', 'no-cache')
		req_add2cart.add_header('Connection', 'keep-ailve')
		req_add2cart.add_header('accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		req_add2cart.add_header('accept-encoding','gzip, deflate, sdch')
		req_add2cart.add_header('accept-language','zh-CN,zh;q=0.8')
		req_add2cart.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		try:
			req2cart = opener.open(req_add2cart)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
			if re.search('hidden',e.read()) != None:
				print "Renew Cookies"
				sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --refUrl='"+refUrl+"'"
				child = subprocess.Popen(sh,shell=True)
				child.wait()
				cookie.revert(ignore_discard=True, ignore_expires=True)
			else:
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
			time.sleep(10)
			#print "Return content:",e.read()
		except urllib2.URLError,e:
			print "Failed to reach the server"
			print "The reason:",e.reason
			time.sleep(10)
		else:
			#something you should do
			if req2cart.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2cart.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read()
			else:
				html = req2cart.read()
			if html.find('success') == -1:
				print "Can't add to Cart! Try again later!"
				file_object = open('./log/'+Pid+'_'+uName+'_jimmyjazzError.txt', 'w')
				file_object.write(html)
				file_object.close( )
				time.sleep(10)
			else:
				file_object = open('./log/'+Pid+'_'+uName+'_jimmyjazzItem.txt', 'w')
				file_object.write(html)
				file_object.close( )
				cookie.save(ignore_discard=True, ignore_expires=True)
				print "Check Out Now!!"
				checkout = checkOut()
				checkout.doCheckOut(uName,uPass,refUrl)
				mail = sendMail()
				mail.send_email(uName,html,"Jimmyjazz")
				#sh = "casperjs check.js --uName='"+uName+"' --uPass='"+uPass+"' --aPid='"+Pid+"' --cFile='"+cookiePath+"' --ccd='"+ccd[uName]+"'"
				#child = subprocess.Popen(sh,shell=True)
				#child.wait()
				#print sh
				break
	#print req_add2cart.header_items()
	#print req2cart.info()
	#print cookie
	#print req2cart.read()
#'''
