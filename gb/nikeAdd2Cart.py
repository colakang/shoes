#!/usr/local/bin/python
#coding:utf-8
import urllib,urllib2,cookielib,time,sys,re,json,os,gzip,StringIO
from bs4 import BeautifulSoup
import time,webbrowser
import Cookie
from cookielib import Cookie as libcookie
from send import sendMail
class Shoe_Size_Monitor:##鞋码监控
	def __init__ (self,refUrl,refSkuid):
		self.url = refUrl
		self.second = 15
		self.skuid = refSkuid
		if self.skuid == False:
			self.skuid = "4Y,4.5Y,5Y,5.5Y,6Y,6.5Y,7Y,7.5Y,8Y,8.5Y,9Y,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,36,36.5,37,37.5,38,38.5,39,39.5,40,40.5,41,41.5,42,42.5,43,43.5,44,44.5,45"
		url_check = True
		while url_check == True:
			try:
				self.html = urllib2.urlopen(self.url).read()
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(int(self.second))
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(int(self.second))
			else:
				#something you should do
				url_check = False
				pass
		self.soup = BeautifulSoup(self.html)
		self.title = self.soup.head.title.get_text().encode('utf-8')
		print(u"您选择的鞋子型号为：%s".encode('utf-8'))%self.title
		self.pre_num = self.num = 0
		self.options= False
		for select in self.soup.find_all("select"):
			if select.get('name') == "skuAndSize": 
				self.options = select.find_all("option")
				break
		if self.options == False:
			self.options = self.soup.find_all("option")
		self.keyword1 = "exp-pdp-size-not-in-stock selectBox-disabled"
		self.keyword2 = "skuId"
		self.keyword3 = "buyingtools-add-to-cart-button"
		self.solds = []
		self.sells = []
		for option in self.options:
			#print option
			x = option.encode('utf-8').find(self.keyword1)
			if x != -1:
				self.num += 1
				self.solds.append(option.get_text().encode('utf-8').strip())
			else:
				if option.encode('utf-8').find(self.keyword2) != -1:
					self.sells.append(option.get_text().encode('utf-8').strip())
			self.pre_num = self.num
		print u"无货尺码:".encode('utf-8'),self.solds
		print u"有货尺码:".encode('utf-8'),self.sells
	def monitor(self):
		print u"监控中".encode('utf-8')
		while True:
			add_car = False
			new_html = urllib2.urlopen(self.url).read()
			new_soup = BeautifulSoup(new_html)
			new_options = False
			new_select = False
			result = {}
			#print new_soup.find(class_="add-to-cart-form nike-buying-tools")
			#sys.exit()
			if new_soup.find(class_="add-to-cart-form nike-buying-tools") == None:
				print u"skuAndSize 不存在或无货".encode('utf-8')
			else:
				skuAndSize = new_soup.find(class_="add-to-cart-form nike-buying-tools").find_all("option",attrs={'name':'skuId'},class_=False)
				for option in skuAndSize:
					#print option.get_text().encode('utf-8').strip() in self.sells
					#sys.exit()
					if self.skuid == option.get_text().encode('utf-8').strip():
						print u"新鞋码放出！！".encode('utf-8')
						for inputHidden in new_soup.find(class_="add-to-cart-form nike-buying-tools").find_all(type='hidden',value=True):
							if inputHidden['value']:
								result[inputHidden['name'].encode('utf-8').strip()] = urllib.quote_plus(inputHidden['value'].encode('utf-8').strip())
							else:
								result[inputHidden['name'].encode('utf-8').strip()] = 'null'
						for inputHidden in new_soup.find(class_="add-to-cart-form nike-buying-tools").find_all(type='hidden',value=False):
							result[inputHidden['name'].encode('utf-8').strip()] = 'null'
						#skuAndSize = new_soup.find(class_="add-to-cart-form nike-buying-tools").find("option",attrs={'name':'skuId'},class_=False)['value'].encode('utf-8').strip()
						skuAndSize = option['value'].encode('utf-8').strip()
						result['skuAndSize'] = urllib.quote_plus(skuAndSize)
						result['skuId'] = skuAndSize.split(':')[0]
						result['displaySize'] = skuAndSize.split(':')[1]
						result['qty'] = "1"
						result['rt'] = 'json'
						result['view'] = '3'
						#result['_'] = int(time.time())
						return ("&".join(["%s=%s" % (k, v) for k, v in result.items()]))
					else:
						print u"无适合码数。".encode('utf-8')				
				self.skuid = skuAndSize[0].get_text().encode('utf-8').strip()
			time.sleep(int(self.second))
class FastMode:
	def __init__ (self):
		self.startTime = False
	def getUrlInfo (self,refUrl,refSkuid):
		self.url = refUrl
		self.second = 15
		self.skuid = refSkuid
		while True:
			try:
				self.html = urllib2.urlopen(self.url+"?"+str(time.time())).read()
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
				new_html = self.html
				new_soup = BeautifulSoup(new_html)
				result = {}
				Json = json.loads(new_soup.find('script',id='product-data').get_text().encode('utf-8').strip(),encoding='utf-8')
				skuList = Json.get('skuContainer')
				for option in skuList.get('productSkus'):
					#print option
					if self.skuid == option.get('sizeDescription'):
						print u"新鞋码放出！！".encode('utf-8')
						result['passcode'] = 'null'
						result['sizeType'] = skuList.get('displaySizeType') # us = null / uk = UK / jp = JP / cn = CN
						result['siteId'] = 'null'
						result['action'] = 'addItem'
						result['lang_locale'] = 'en_GB'
						result['country'] = 'GB'

						result['catalogId'] = Json.get('catalogId')
					 	result['productId'] = Json.get('productId')
						result['price'] = Json.get('rawPrice')
						result['line1'] = urllib.quote_plus(Json.get('productTitle'))
						try:
							result['line2'] = urllib.quote_plus(Json.get('productSubTitle'))
						except:
							result['line2'] = Json.get('productSubTitle')
						result['skuAndSize'] = urllib.quote_plus(option.get('sku')+':'+option.get('displaySize'),safe='()')
						result['skuId'] = option.get('sku')
						result['displaySize'] = urllib.quote_plus(option.get('displaySize'),safe='()')
						result['qty'] = "1"
						result['rt'] = 'json'
						result['view'] = '3'
						#result['_'] = int(time.time())
						self.startTime = Json.get('startDate')
						return ("&".join(["%s=%s" % (k, v) for k, v in result.items()]))
				print 'Size Not Fount'
				sys.exit()
class Login_In:
	def saveCookies (self,uName,uPass):
		cookiefile = "./log/"+uName+"_cookies.txt" 
		self.username = uName
		self.password = uPass
		self.rememberMe = "false"
		self.url = "https://www.nike.com/profile/login?Content-Locale=en_GB"
		self.request_body = urllib.urlencode({
			'login':self.username,
			'rememberMe':self.rememberMe,
			'password':self.password
			})
		self.hdr = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}
		#self.cookie = cookielib.CookieJar()
		self.cookie = cookielib.MozillaCookieJar(cookiefile)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		#opener = urllib2.build_opener(self.proxy_support,self.cookie_support,urllib2.HTTPHandler)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		req = urllib2.Request(
			self.url,
			self.request_body,
			#self.hdr
			)
		self.result = opener.open(req).read()
		file_object = open('./log/'+self.username+'_login.txt', 'w')
		file_object.write(self.result)
		file_object.close( )
		#print (self.cookie)
		cs = self.parse("NIKE_COMMERCE_COUNTRY=GB; NIKE_COMMERCE_LANG_LOCALE=en_GB; mt.m=%7B%22membership%22%3A%5B%22us_aa-el1-ae%22%5D%7D; CONSUMERCHOICE_SESSION=t; CONSUMERCHOICE=gb/en_gb; nike_locale=gb/en_gb; cookies.js=1;",".nike.com")
		for c in cs:
			self.cookie.set_cookie(c)
		req_test = urllib2.Request('https://secure-store.nike.com/gb/checkout/html/cart.jsp')
		req_test.add_header('Referer', 'http://store.nike.com/gb/en_gb/?ipp=120')
		#req_test.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		req2 = opener.open(req_test)
		#file_object = open(self.username+'_cart.txt', 'w')
		#file_object.write(req2.read())
		#file_object.close( )
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
'''
		cookie = cookielib.CookieJar()
		cs = parse("anonymid=h7iy6p2z-l2catp; _r01_=1;","www.renren.com")
		for c in cs:
			cookie.set_cookie(c)
		print cookie
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
'''
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
	debugMode = False
	if debugMode == True:
		f_handler=open('./log/'+uName+'_debug.log', 'w')
		sys.stdout=f_handler
	if Mode == "2":
		shoe_size_monitor = Shoe_Size_Monitor(refUrl,refSkuid)
		add2CartUrl = shoe_size_monitor.monitor()
		nikeUrl = 'https://secure-store.nike.com/eu/services/jcartService?callback=nike_Cart_handleJCartResponse&'+add2CartUrl
	elif Mode == "1":
		fastMode = FastMode()
		add2CartUrl = fastMode.getUrlInfo(refUrl,refSkuid)
		nikeUrl = 'https://secure-store.nike.com/eu/services/jcartService?callback=nike_Cart_handleJCartResponse&'+add2CartUrl
	else:
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
		sys.exit()
	#print nikeUrl
	try:
		startTime = fastMode.startTime/1000
	except:
		startTime = 0
	Pid = filter(str.isdigit,refUrl)+'_'+refSkuid
	cookiePath = "./log/"+uName+"_cookies.txt" 
	if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 7200:
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	req_profile = urllib2.Request('https://secure-store.nike.com/gb/checkout/html/cart.jsp')
	req_profile.add_header('Referer', 'http://store.nike.com/gb/en_gb/?ipp=120')
	#req_profile.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
	#print cookie
	if Mode != '2':
		cookie_check = True
	while cookie_check == True:
		try:
			req2 = opener.open(req_profile)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
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
			#status = req2.getcode()
			cartContent = req2.read()
			if re.search('Nike OrderId',cartContent) == None:
				print "Pls Reload Cookies"
				login_test.saveCookies(uName,uPass)
				#file_object = open('cart_empty.txt', 'w')
				#file_object.write(cartContent)
				#file_object.close( )
				cookie.revert(ignore_discard=True, ignore_expires=True)
				#print cookie
			else:
				cookie_check = False
				file_object = open('./log/'+uName+'_cart.txt', 'w')
				file_object.write(cartContent)
				file_object.close( )
				pass
	print 'sleepTime = '+str(startTime-time.time())
	#if (startTime - time.time()) > 0:
	#	print "Start Time = "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) 
	#	time.sleep(startTime - time.time() - 0.096)
	#else:
	#	print 'start now'
	print 'Now = '+str(startTime-time.time())
	pil = ''
	psh = ''
	while True:
		newUrl = nikeUrl
		if pil != '' and pil != '-1':
			newUrl = newUrl + '&pil='+pil
		if psh != '' and psh != 'nogood':
			newUrl = newUrl + '&psh='+psh
		rTime = int(time.time())
		newUrl = newUrl+'&_='+str(rTime)
		#print newUrl
		req_add2cart = urllib2.Request(newUrl)
		req_add2cart.add_header('Referer', refUrl)
		req_add2cart.add_header('Accept','application/javascript, */*;q=0.8')
		req_add2cart.add_header('Accept-Encoding','gzip, deflate')
		req_add2cart.add_header('DNT','1')
		req_add2cart.add_header('Cache-Control', 'no-cache')
		req_add2cart.add_header('Connection', 'keep-ailve')
		#req_add2cart.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		try:
			req2cart = opener.open(req_add2cart)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
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
			if req2cart.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2cart.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read().decode('utf-8')
			else:
				html = req2cart.read().decode('utf-8')
			if (time.time() - startTime ) < 10:
				print 'Now = '+str(startTime-time.time())
			if html.find('success') == -1:
				if html.find('failure') == -1:
					#if html.find('productId') != -1:
					newHtml = re.findall(r'(?<=")[^,:]+?(?=")',html)
					for k,v in enumerate(newHtml):
						if v == "pil":
							tempPil = newHtml[k+1]
							if (tempPil == "-4") or (int(tempPil) >= 0):
								pil = tempPil
						if v == "psh":
							tempPsh = newHtml[k+1]
							if (len(tempPsh) > 6):
								psh = tempPsh
					print html
					time.sleep(8)
				elif html.find('019B-05200023') != -1:
					print html
					time.sleep(8)
				else:
					print u"添加失败，稍后再试".encode('utf-8')
					file_object = open('./log/'+uName+'_'+Pid+'_item_fail.txt', 'w')
					file_object.write(html)
					file_object.close( )
					mail = sendMail()
					mail.send_email(uName,html,"NikeUK")
					break
			else:
				file_object = open('./log/'+uName+'_'+Pid+'_item.txt', 'w')
				file_object.write(html)
				file_object.close( )
				mail = sendMail()
				mail.send_email(uName,html,"NikeUK")
				#cookie.save(ignore_discard=True, ignore_expires=True)
				break
	#print req_add2cart.header_items()
	#print req2cart.info()
	#print cookie
	#print req2cart.read()
