var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug',
    pageSettings: {
        loadImages: true,
        loadPlugins: true,
	webSecurityEnabled: false
    }

});           //新建一个页面

var fs = require('fs');
var utils = require('utils');
var http = require('http');
var argv = [];

if (casper.cli.has('uName')) {var uName = casper.cli.get('uName');}
if (casper.cli.has('uPass')) {var uPass = casper.cli.get('uPass');}
if (casper.cli.has('cFile')) {var cFile = casper.cli.get('cFile');}
if (casper.cli.has('aPid')) {var aPid = casper.cli.get('aPid');}
if (casper.cli.has('ccd')) {var ccd = casper.cli.get('ccd');}

var data = fs.read("../ccdInfo");
var bank = JSON.parse(data);

var cardNo = bank[ccd].cardNo;
var cardMM = bank[ccd].cardMM;
var cardYY = bank[ccd].cardYY;
var cardCCV = bank[ccd].cardCCV;

casper.echo("Start At "+new Date().toLocaleString());


function doCheckOut (thecasper,aPid,uName,fs,loop) {

	thecasper.wait(1000);
	thecasper.thenOpen('https://m.footlocker.com/?uri=checkout', function(response) {
		
		var checked = false;
		var cUrl = this.getCurrentUrl();
		if ((cUrl.search(/error/i) != -1) | (cUrl.search(/cart/i) !=-1) | (cUrl.search(/403.html/i) !=-1) | (cUrl.search(/500.html/i)!=-1) ) {
			this.echo('get Error: '+loop+' : '+cUrl);
			var checked = doCheckOut(this,aPid,uName,fs,0);			
		} 

		if (checked == true) {

			return true;
		}

		this.waitUntilVisible('a#payMethodPaneContinue', function() {                  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
			this.sendKeys('input[name=CardNumber]', cardNo, {keepFocus: true});
			casper.evaluate(function(cardYY,cardCCV,cardMM) {
				$('#CardExpireDateMM').val(cardMM);
				$('#CardExpireDateYY').val(cardYY);
				$('#CardCCV').val(cardCCV);
			},cardYY,cardCCV,cardMM);
			this.capture('capture/'+aPid+'_'+uName+'-02.jpg',undefined,{
				format: 'jpg',
				quality: 75
				});                 //成功时调用的函数,给整个页面截图
		}, function() {
			this.capture('capture/'+aPid+'_'+uName+'-02-error.jpg', undefined, {
					format: 'jpg',
					quality: 75
				});
				if (this.exists('table#sharedCart_panel')) {
					this.echo('Found sharedCart_panel');
					casper.evaluate(function() {
						//sharedCart_panel.close();
						location.reload();
					});
					this.click('a#cart_checkout_button');
					goCart(this,'cart');
				}

				if (this.exists('table#persistentCart_panel')) {
					this.echo('Found persistentCart_panel');
						casper.evaluate(function() {
							persistentCart_panel.close();
						});
					//this.reload();
				}
				this.echo("No payMethodPaneContinue Button! Reload again");
				var checked = false;
				checked = doCheckOut(this,aPid,uName,fs,loop);
				if (checked == true) {

					return true;
				}
		}, 10000);                                                       //超时时间,两秒钟后指定的选择器还没出现,就算失败 
	});
	thecasper.then(function() {

		if (this.exists('table#sharedCart_panel')) {
			this.echo('Found sharedCart_panel');
			casper.evaluate(function() {
				sharedCart_panel.close();
			});
			//this.reload();
		}

		if (this.exists('table#persistentCart_panel')) {
			this.echo('Found persistentCart_panel');
			casper.evaluate(function() {
				persistentCart_panel.close();
			});
			//this.reload();
		}

	});
	thecasper.then(function() {
		this.click('a#payMethodPaneContinue');
		this.waitUntilVisible('a#orderSubmit', function() {
			this.capture('capture/'+aPid+'_'+uName+'-03.jpg', undefined, {
					format: 'jpg',
					quality: 75
				});
			argv = this.getFormValues('form#spcoForm');
			var content = JSON.stringify(argv); 
			fs.write('argv/'+aPid+'_'+uName+'_post.txt', content, 'w'); 
			this.click('a#orderSubmit');
		}, function() {
			this.capture('capture/'+aPid+'_'+uName+'-03-error.jpg', undefined, {
					format: 'jpg',
					quality: 75
				});
			this.echo("No Submit Button! Wait.......");
	       		var errorMess = this.getElementInfo('span#CC_statusCheck');
			this.echo("Error Message : "+errorMess.text);
			if (loop<15) {
				loop = loop+1;
				doCheckOut(this,aPid,uName,fs,loop);
			}
	
		},50000);
	 
	});
return true;
}

function submitCheckOut (thecasper,aPid,uName,fs,loop) {

	thecasper.wait(1000);


	thecasper.then(function() {

		if (this.exists('a#orderSubmit')) {
			this.echo('Found a#orderSubmit');
			this.click('a#orderSubmit');
			submitCheckOut(this,aPid,uName,fs,0);
		}
	});
	thecasper.then(function() {
		if (this.exists('table#sharedCart_panel')) {
			this.echo('Found sharedCart_panel');
			casper.evaluate(function() {
				//sharedCart_panel.close();
				location.reload();
			});
			this.click('a#cart_checkout_button');
			goCart(this,'cart');
		}

	});
	thecasper.then(function() {
		if (this.exists('table#persistentCart_panel')) {
			this.echo('Found persistentCart_panel');
			casper.evaluate(function() {
				//persistentCart_panel.close();
				location.reload();
			});
			this.click('a#cart_checkout_button');
		}

	});
	thecasper.then(function() {
		var cUrl = this.getCurrentUrl();
		if ((cUrl.search(/error/i) != -1) | (cUrl.search(/cart/i) !=-1) ) {
			this.echo('get Error: '+loop+' : '+cUrl);
			doCheckOut(this,aPid,uName,fs,0);			
		}

	});
	thecasper.then(function() {
		while(loop<15) {
			this.wait(5000,function() {
				this.echo('cUrl:'+this.getCurrentUrl());
				this.capture('capture/'+aPid+'_'+uName+'-04-'+loop+'.jpg', undefined, {
						format: 'jpg',
						quality: 75
					});
					loop = loop+1;
					this.echo('Loop Times: '+loop);
					if (this.exists('a#orderSubmit')) {
						this.echo('Found a#orderSubmit');
						this.click('a#orderSubmit');
						submitCheckOut(this,aPid,uName,fs,0);
					}
			});
	
		}
	});
	thecasper.then(function() {
		this.capture('capture/'+aPid+'_'+uName+'-05.jpg', undefined, {
					format: 'jpg',
					quality: 75
			});
	});

return;
}

function goCart(thecasper,newurl) {

	thecasper.wait(1000);

	thecasper.thenOpen('https://m.footlocker.com/?uri=cart', function(response) {
		while (true) {
			if (response == undefined || response.status == null || response.status >= 400) {
				this.wait(5000);
				this.reload(function() {
						this.echo("loaded again");
					});
			} else {
				break;
			}
		}

		if (this.exists('table#sharedCart_panel')) {
			this.echo('Found sharedCart_panel');
			casper.evaluate(function() {
				sharedCart_panel.close();
			});
			this.wait(1000);
		}

		if (this.exists('table#persistentCart_panel')) {
			this.echo('Found persistentCart_panel');
			casper.evaluate(function() {
				persistentCart_panel.close();
			});
			this.wait(1000);
		}

		this.waitUntilVisible('a#cart_checkout_button', function() {                  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
			casper.evaluate(function() {
				processCheckout();
			});
			this.capture('capture/'+aPid+'_'+uName+'-01.jpg',undefined,{
				format: 'jpg',
				quality: 75
				});                 //成功时调用的函数,给整个页面截图
		}, function() {
			this.capture('capture/'+aPid+'_'+uName+'-01-error.jpg', undefined, {
					format: 'jpg',
					quality: 75
				});
				this.reload(function() {
					this.echo("No CheckOut Button! Reload again");
			});
		}, 50000);                                                       //超时时间,两秒钟后指定的选择器还没出现,就算失败 
	});
return;
}
	

casper.start().then(function() {
	var JsCookie = 'log/'+uName+'_JsCookies.txt';	
	if (fs.exists(JsCookie)) {
		var file = JsCookie;
		var changeDomain = false;
		this.echo('++++++');
	} else {
		var file = cFile;
		var changeDomain = true;
		this.echo('--------');
	}
	var cookies = [];
	if (fs.exists(file)) {
		cookies = fs.read(file).split("\n");
		//casper.log(cookies,'info');
		cookies.forEach(function (cookie) {
			var detail = cookie.split("\t");
				newCookie = {
					'name':   detail[5],
        				'value':  detail[6],
	        			'domain': detail[0],
        				//'path':   detail[2],
        				//'httponly': true,
        				//'secure':   true,
        				//'expires':  time
		      		};
		
			//utils.dump(detail[0]);
			phantom.addCookie(newCookie,true);
	    });
	} else {
		casper.log("Unable to load cookies from " + file + ". File doesn't exist", "warning").exit();
	}

	if (changeDomain == true) {
		phantom.cookies.forEach(function (cookie) {
			if (cookie.name.search(/TS01/) == -1) {
				if (cookie.domain.search(/.m./) != -1) {
					cookie.domain = cookie.domain.substr(1);
				}
			}
	})};
	//this.page.cookies = phantom.cookies;
	//utils.dump(phantom.cookies);
	//casper.exit();
	//goCart(this,"https://m.footlocker.com/?uri=checkout");
	//doCheckOut(this,"https://m.footlocker.com/?uri=checkout");
});

casper.userAgent('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36');

casper.then(function() {

	doCheckOut(this,aPid,uName,fs,0);

});

casper.then(function() {

	submitCheckOut(this,aPid,uName,fs,0);
});




casper.run(function() { 

	var file = 'log/'+uName+'_JsCookies.txt';	
	var res = '# Netscape HTTP Cookie File\n\n';
	var t = '';
	var time = '';
	this.page.cookies.forEach(function (cookie) {
		if (cookie.domain.charAt(0) == '.') { 
			t = 'TRUE';
		} else {
			t = "FALSE";
		}
		if (cookie.expiry) {
			time = cookie.expiry;
		}
		res += utils.format("%s\t%s\t%s\t%s\t%s\t%s\t%s\n", cookie.domain, t, cookie.path, 'FALSE', time, cookie.name, cookie.value);
	});
	fs.write(file, res, 'w');
	//var cookies = JSON.stringify((this.page.cookies)); 
	//fs.write('/root/nike/footlocker/cookies.txt', cookies, 'w'); 
	casper.echo("End at "+new Date().toLocaleString());
	this.exit();                                                                      

});
