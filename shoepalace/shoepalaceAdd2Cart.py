#!/usr/local/bin/python
#coding:utf-8
import urllib,urllib2,cookielib,time,sys,re,json,os,gzip,StringIO,multiprocessing
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
							"4":"192","4.5":"191",
							"5":"190","5.5":"189",
							"6":"188","6.5":"187",
							"7":"139","7.5":"140",
							"8":"141","8.5":"142",
							"9":"143","9.5":"144",
							"10":"145","10.5":"146",
							"11":"147","11.5":"148"
						}
	def getUrlInfo (self,refUrl,uName,refSkuid,Mode):
		cookiePath = "./log/"+uName+"_shoepalaceCookies.txt" 
		cookie = cookielib.MozillaCookieJar(cookiePath)
		cookie.load(ignore_discard=True, ignore_expires=True)
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		req_getInfo = urllib2.Request(refUrl)
		req_getInfo.add_header('Referer', 'http://www.shoepalace.com')
		req_getInfo.add_header('Cache-Control', 'max-age=0')
		req_getInfo.add_header('Connection', 'keep-ailve')
		req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		while True:
			try:
				req2Info = opener.open(req_getInfo)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(30)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(30)
			else:
				#something you should do
				#req2Info = opener.open(req_getInfo)
				html = req2Info.read()
				soupInfo = BeautifulSoup(html,'html.parser')
				result = {}
				sizeList = soupInfo.find_all('a',class_='button w32 dark')
				sizeOut = soupInfo.find_all('span',class_='button w32 disabled')
				if len(sizeList) == 0:
					if len(sizeOut) == 0: 
						print "Product Not Releasing"
						time.sleep(30)
					else:
						print "Sold Out!!"
						sys.exit()
				else:
					for inputHidden in sizeList:
						if inputHidden.get_text().encode('utf-8').strip() == refSkuid:
							nikeUrl =  inputHidden['href']
							break
					#print form.find('script').get_text().encode('utf-8').strip()
					try:
						nikeUrl
					except NameError:
						refSkuid = sizeList[0].get_text().encode('utf-8').strip()
						print 'Size Not Fount! Change Size to:' + refSkuid
						time.sleep(5)					
					else: 
						nikeUrl = "https://www.shoepalace.com/"+nikeUrl.replace('/s/','')
						pidPath = "./argv/"+filter(str.isdigit,refUrl)+'_'+refSkuid+'.txt'
						file_object = open(pidPath, 'w')
						file_object.write(nikeUrl)
						file_object.close( )
						self.nikeUrl = nikeUrl
						# Write Down Argvs
						return True
					#sys.exit()
class Login_In:
	def saveCookies (self,uName,uPass):
		self.login_email = uName
		self.login_password = uPass
		self.cookiefile = "./log/"+uName+"_shoepalaceCookies.txt" 
		self.cookie = cookielib.MozillaCookieJar(self.cookiefile)
		self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie)
		opener = urllib2.build_opener(self.cookie_support)
		urllib2.install_opener(opener)
		self.hdr = {
					'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
					'Referer' : 'https://www.shoepalace.com/customer/account/login/'
					}
		self.url = "https://www.shoepalace.com/customer/account/loginPost/"
		self.request_body = urllib.urlencode({
			'login[username]':self.login_email,
			'login[password]':self.login_password,
			'send':''
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
					file_object = open('./log/'+self.login_email+'_shoepalaceLogin.txt', 'w')
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
class CheckOut:
	def __init__ (self):
		self.startTime = False
		self.nikeUrl = False
	def doCheckOut (self,refUrl,uName):
		try:
			ccdFile = open('../ccd')
		except:
			print 'No ccd Argvs'
			sys.exit()
		else:
			print 'Load ccd Argvs'
			ccd = json.loads(ccdFile.readline())
		try:
			ccdInfoFile = open('../ccdInfo')
		except:
			print 'No ccdInfo Argvs'
			sys.exit()
		else:
			print 'Load ccdInfo Argvs'
			ccdInfo = json.loads(ccdInfoFile.readline())
		list = int(ccd[uName])
		cc_type = ccdInfo[list]['cardTYPE']
		if cc_type == "visa":
			cc_type = 'VI'
		elif cc_type == "mastercard":
			cc_type = 'MC'
		cc_number =ccdInfo[list]['cardNo']
		cc_exp_month = ccdInfo[list]['cardMM']
		cc_exp_year = "20"+ccdInfo[list]['cardYY']
		cc_cid = ccdInfo[list]['cardCCV']
		cookiePath = "./log/"+uName+"_shoepalaceCookies.txt" 
		cookie = cookielib.MozillaCookieJar(cookiePath)
		cookie.load(ignore_discard=True, ignore_expires=True)
		cookieProc = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookieProc)
		urllib2.install_opener(opener)
		req_getInfo = urllib2.Request(refUrl)
		req_getInfo.add_header('Referer', 'https://www.shoepalace.com/checkout/cart/')
		req_getInfo.add_header('Cache-Control', 'no-cache')
		req_getInfo.add_header('Accept-Encoding', 'gzip, deflate')
		req_getInfo.add_header('Accept', 'text/html, application/xhtml+xml, */*')
		req_getInfo.add_header('Accept-Language', 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3')
		req_getInfo.add_header('Connection', 'keep-ailve')
		req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		print refUrl
		print uName
		while True:
			try:
				req2Info = opener.open(req_getInfo)
			except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
				print "The server couldn't fulfill the request"
				print "Error code:",e.code
				time.sleep(30)
				#print "Return content:",e.read()
			except urllib2.URLError,e:
				print "Failed to reach the server"
				print "The reason:",e.reason
				time.sleep(30)
			else:
				#something you should do
				#req2Info = opener.open(req_getInfo)
				if re.search('onestepcheckout',req2Info.url) == None:
					print "Page Redirect, Some Item Out of Stock!!"
					return False
				if req2Info.info().get('Content-Encoding') == 'gzip':
					buf = StringIO.StringIO(req2Info.read())
					f = gzip.GzipFile(fileobj=buf)
					html = f.read().decode('utf-8')
				else:
					html = req2Info.read().decode('utf-8')
				soupInfo = BeautifulSoup(html,'html.parser')
				shippingAddressId = soupInfo.find('input',id='shipping:address_id')
				billing_address_id = soupInfo.find('select',{'name':'billing_address_id'}).find('option',{'selected':True})
				billingCountryId = soupInfo.find('select',{'name':'billing[country_id]'}).find('option',{'selected':True})
				billingFirstname = soupInfo.find('input',id='billing:firstname')
				billingLastname = soupInfo.find('input',id='billing:lastname')
				billingTelephone = soupInfo.find('input',id='billing:telephone')
				billingStree1 = soupInfo.find('input',id='billing:street1')
				billingStree2 = soupInfo.find('input',id='billing:street2')
				billingCity = soupInfo.find('input',id='billing:city')
				billingPostcode = soupInfo.find('input',id='billing:postcode')
				billingRegion = soupInfo.find('input',id='billing:region')
				shipping_address_id = soupInfo.find('select',{'name':'shipping_address_id'}).find('option',{'selected':True})
				shipping_method = soupInfo.find('dl',class_="shipment-methods").find('input')
				giftNoName = soupInfo.find('input',type='hidden',value='quote')
				giftNo = re.findall(r"giftmessage\[(.*)\]\[type\]",giftNoName['name'].encode('utf-8').strip())
				billingRegionId = re.findall(r"\$\(\"billing:region_id\"\).setAttribute\(\"defaultValue\",  \"(\d+)\"\)",html.encode('utf-8'))
				shippingRegionId = re.findall(r"\$\(\"shipping:region_id\"\).setAttribute\(\"defaultValue\",  \"(\d+)\"\)",html.encode('utf-8'))
				#print billingRegionId
				#print shippingRegionId
				#print shippingAddressId['value']
				#print giftNo[0]
				#print billing_address_id['value']
				#print shipping_address_id['value']
				#sys.exit()
				if shippingAddressId == None:
					print "Page Error Pls Reload Again!!"
					time.sleep(5)
				else:
					request_body = urllib.urlencode({
						'billing_address_id':billing_address_id['value'],
						'billing[country_id]':billingCountryId['value'],
						'billing[firstname]':billingFirstname['value'],
						'billing[lastname]':billingLastname['value'],
						'billing[street][0]':billingStree1['value'],
						'billing[street][1]':billingStree2['value'],
						'billing[city]':billingCity['value'],
						'billing[postcode]':billingPostcode['value'],
						'billing[region_id]':billingRegionId[0],
						'billing[region]':billingRegion['value'],
						'billing[telephone]':billingTelephone['value'],
						#'billing[email]':'colakang@gmail.com',
						#'billing[confirmemail]':'colakang@gmail.com',
						#'billing[customer_password]':'',
						#'billing[confirm_password]':'',
						'billing[save_in_address_book]':'1',
						'billing[use_for_shipping]':'1',
						'shipping_address_id':shipping_address_id['value'],
						'shipping[country_id]':'US',
						'shipping[firstname]':'',
						'shipping[lastname]':'',
						'shipping[telephone]':'',
						'shipping[street][0]':'',
						'shipping[street][1]':'',
						'shipping[city]':'',
						'shipping[postcode]':'',
						'shipping[region_id]':shippingRegionId[0],
						'shipping[region]':'',
						'shipping[save_in_address_book]':'1',
						'shipping[address_id]':'',
						'shipping_method':'ups_03',
						'shipping_method':shipping_method['value'],
						'payment[method]':'firstdataglobalgateway',
						'payment[cc_type]':cc_type,
						'payment[cc_number]':cc_number,
						'payment[cc_exp_month]':cc_exp_month,
						'payment[cc_exp_year]':cc_exp_year,
						'payment[cc_cid]':cc_cid,
						'onestepcheckout-couponcode':'',
						'onestepcheckout-giftcardcode':'',
						'giftmessage['+giftNo[0]+'][type]':'quote',
						'giftmessage['+giftNo[0]+'][from]':'', 
						'giftmessage['+giftNo[0]+'][to]':'', 
						'giftmessage['+giftNo[0]+'][message]':'',
						'gift-wrapping-current':'0',
						'onestepcheckout_comments':'',
						'onestepcheckout-feedback':'_1351861518809_809',
						'onestepcheckout-feedback-freetext':'',
						'agreement[1]':'1',
					})
					#print request_body
					#sys.exit()
					req_doCheckOut = urllib2.Request('https://www.shoepalace.com/onestepcheckout/',request_body)
					req_doCheckOut.add_header('Referer', 'https://www.shoepalace.com/onestepcheckout/')
					req_doCheckOut.add_header('Cache-Control', 'no-cache')
					req_doCheckOut.add_header('Accept-Encoding', 'gzip, deflate')
					req_doCheckOut.add_header('Accept', 'text/html, application/xhtml+xml, */*')
					req_doCheckOut.add_header('Accept-Language', 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3')
					req_doCheckOut.add_header('Connection', 'keep-ailve')
					req_doCheckOut.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
					while True:
						try:
							req2CheckOut = opener.open(req_doCheckOut)
						except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
							print "The server couldn't fulfill the request"
							print "Error code:",e.code
							time.sleep(30)
							#print "Return content:",e.read()
						except urllib2.URLError,e:
							print "Failed to reach the server"
							print "The reason:",e.reason
							time.sleep(30)
						else:
							#something you should do
							if req2CheckOut.info().get('Content-Encoding') == 'gzip':
								buf = StringIO.StringIO(req2CheckOut.read())
								f = gzip.GzipFile(fileobj=buf)
								html = f.read().decode('utf-8')
							else:
								html = req2CheckOut.read().decode('utf-8')
							if re.search('Your order number is:',html) != None:
								print 'CheckOut Success!!'
								mail = sendMail()
								mail.send_email(uName,html,"Shoepalace")
								sys.exit()
								return True
							else:
								print 'CheckOut Error'
								soupInfo = BeautifulSoup(html,'html.parser')
								errorInfo = soupInfo.find('h2',class_="indentlr normal red")
								errorMsg = soupInfo.find('li',class_="error-msg")
								try: 
									print errorInfo.text
								except:
									try:
										print errorMsg.txt
									except:
										print html
									else:
										return False
								#sys.exit()
							time.sleep(30)

def checkCart(refUrl,uName):
	cookiePath = "./log/"+uName+"_shoepalaceCookies.txt" 
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	req_getInfo = urllib2.Request('https://www.shoepalace.com/checkout/cart/')
	req_getInfo.add_header('Referer', refUrl)
	req_getInfo.add_header('Cache-Control', 'no-cache')
	req_getInfo.add_header('Accept-Encoding', 'gzip, deflate')
	req_getInfo.add_header('Accept', 'text/html, application/xhtml+xml, */*')
	req_getInfo.add_header('Accept-Language', 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3')
	req_getInfo.add_header('Connection', 'keep-ailve')
	req_getInfo.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
	while True:
		try:
			req2Info = opener.open(req_getInfo)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
			print "The server couldn't fulfill the request"
			print "Error code:",e.code
			time.sleep(30)
			#print "Return content:",e.read()
		except urllib2.URLError,e:
			print "Failed to reach the server"
			print "The reason:",e.reason
			time.sleep(30)
		else:
			#something you should do
			#req2Info = opener.open(req_getInfo)
			if req2Info.info().get('Content-Encoding') == 'gzip':
				buf = StringIO.StringIO(req2Info.read())
				f = gzip.GzipFile(fileobj=buf)
				html = f.read().decode('utf-8')
			else:
				html = req2Info.read().decode('utf-8')
			values = re.findall('[http|https]://[a-zA-Z.0-9]*/(.*)',refUrl,re.I)
			if re.search(values[0],html) == None:
				print "Nothing In Cart"
			else:
				print "Item was Added, CheckOut Now!"
				checkOut = CheckOut()
				CKstatus = checkOut.doCheckOut('https://www.shoepalace.com/onestepcheckout/',uName)
				if CKstatus == True:
					return True
				else:
					print "Check Again Later!!"
			time.sleep(300)
	return False

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
	cookiePath = "./log/"+uName+"_shoepalaceCookies.txt" 
	if Mode == "3":
		print 'Mode = Login Username = '+uName
		login_test = Login_In()
		login_test.saveCookies(uName,uPass)
		sys.exit()
	elif Mode == "4":
		print 'Mode = Check Out!  Username = '+uName
		if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 7200:
			print 'Login first'
			login_test = Login_In()
			login_test.saveCookies(uName,uPass)
		checkOut = CheckOut()
		CKstatus = checkOut.doCheckOut('https://www.shoepalace.com/onestepcheckout/',uName)
		sys.exit()
	
	elif Mode == "5":
			print 'Mode = Check Cart  Username = '+uName
			if os.path.exists(cookiePath) == False or (int(time.time()) - int(os.path.getmtime(cookiePath))) >= 7200:
				print 'Login first'
				login_test = Login_In()
				login_test.saveCookies(uName,uPass)
			pool = multiprocessing.Pool(processes = 1)
			pool.apply_async(checkCart, (refUrl,uName, ))
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
			result = fastMode.getUrlInfo(refUrl,uName,refSkuid,Mode)
			nikeUrl = fastMode.nikeUrl
		else:
			print 'result file exits'
			#result = json.loads(jsonFile.readline())
			nikeUrl = jsonFile.readline()
	#print nikeUrl
	try:
		startTime = fastMode.startTime/1000
	except:
		startTime = 0
	cookie = cookielib.MozillaCookieJar(cookiePath)
	cookie.load(ignore_discard=True, ignore_expires=True)
	cookieProc = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cookieProc)
	urllib2.install_opener(opener)
	#print nikeUrl
	#req_add2cart_body = urllib.urlencode(result)
	#print req_add2cart_body
	#sys.exit()
	pool = multiprocessing.Pool(processes = 1)
	pool.apply_async(checkCart, (refUrl,uName, ))
	pool.close()
	if (startTime - int(time.time())) >= 1:
		print "Start Time = "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) 
		time.sleep(startTime - int(time.time()))
	else:
		print 'start now'
	while True:
		req_add2cart = urllib2.Request(nikeUrl)
		req_add2cart.add_header('Referer', refUrl)
		req_add2cart.add_header('Cache-Control', 'no-cache')
		req_add2cart.add_header('Connection', 'keep-ailve')
		req_add2cart.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36')
		try:
			req2cart = opener.open(req_add2cart)
		except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
			print "Error code:",e.code
			soup = BeautifulSoup(e.read().decode('utf-8'), 'html.parser')
			print soup.title.string
			time.sleep(30)
			#print "Return content:",e.read()
		except urllib2.URLError,e:
			print "Failed to reach the server"
			print "The reason:",e.reason
			time.sleep(30)
		else:
			#something you should do
			html = req2cart.read().decode('utf-8')
			if html.find('was added to your shopping cart') == -1:
				print "Can't add to Cart! Try again later!"
				file_object = open('./log/'+Pid+'_'+uName+'_shoepalaceError.txt', 'w')
				file_object.write(html)
				file_object.close( )
				time.sleep(30)
			else:
				file_object = open('./log/'+Pid+'_'+uName+'_shoepalaceItem.txt', 'w')
				file_object.write(html)
				file_object.close( )
				print "Check Out Now!!"
				mail = sendMail()
				mail.send_email(uName,html,"Shoepalace")
				cookie.save(ignore_discard=True, ignore_expires=True)
				checkOut = CheckOut()
				CKstatus = checkOut.doCheckOut('https://www.shoepalace.com/onestepcheckout/',uName)
				#cookie.save(ignore_discard=True, ignore_expires=True)
				pool.join()
				break
	#print req_add2cart.header_items()
	#print req2cart.info()
	#print cookie
	#print req2cart.read()
#'''
