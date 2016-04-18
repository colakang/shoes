var casper = require('casper').create({
    verbose: true,
    logLevel: 'debug',
    pageSettings: {
        loadImages: false,
        loadPlugins: true,
        localToRemoteUrlAccessEnabled: true,
        XSSAuditingEnabled: true,
	webSecurityEnabled: true
    }

});           //新建一个页面

var fs = require('fs');
var utils = require('utils');
var http = require('http');
var argv = [];

if (casper.cli.has('uName')) {var uName = casper.cli.get('uName');}
if (casper.cli.has('cFile')) {var cFile = casper.cli.get('cFile');}
if (casper.cli.has('uPass')) {var uPass = casper.cli.get('uPass');}
if (casper.cli.has('aPid')) {var aPid = casper.cli.get('aPid');}
if (casper.cli.has('ccd')) {var ccd = casper.cli.get('ccd');}
if (casper.cli.has('refUrl')) {var refUrl = casper.cli.get('refUrl');}


//var cardCCV = '306';

var data = fs.read("../ccdInfo");
var bank = JSON.parse(data);

var cardNo = bank[ccd].cardNo;
var cardMM = bank[ccd].cardMM;
var cardYY = bank[ccd].cardYY;
var cardCCV = bank[ccd].cardCCV;

var x = require("casper").selectXPath;

casper.echo("Start At "+new Date().toLocaleString());

casper.fillSelectOptionByText = function (selectSelector,text){
    this.evaluate(function(sel,setByText) {
        $(sel + " > option").each(function() {
            if($(this).text() === setByText) {
                $(this).attr('selected', 'selected');            
            }                        
        });
    },selectSelector,text);
};


casper.start().then(function() {

	var JsCookie = './log/'+uName+'_SnkrsCookies.txt';	

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
		
		casper.log("Unable to load cookies from " + file + ". File doesn't exist", "warning");
	}

	//this.page.cookies = phantom.cookies;
	//utils.dump(phantom.cookies);
	//casper.exit();
	//goCart(this,"https://m.eastbay.com/?uri=checkout");
	//doCheckOut(this,"https://m.eastbay.com/?uri=checkout");
});

casper.userAgent('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)  Safari/537.36');

casper.thenOpen(refUrl,function() {

	casper.wait(2000, function() {

		var cUrl = this.getCurrentUrl();
		if ((cUrl.search(/login/i) != -1)) {
			this.echo('Login First: ' + cUrl);
			this.waitUntilVisible('div#nike-unite-login-view', function() { 
	        	        this.fillSelectors('form#nike-unite-loginForm', {
        	        	        'input[name="emailAddress"]': uName,
                	       		'input[name="password"]': 'Cola12345678',
	                	}, false);
           	     		this.click("div.nike-unite-submit-button.loginSubmit.nike-unite-component input");
				//utils.dump(this.getElementsInfo('div.nike-unite-submit-button.loginSubmit.nike-unite-component input'));
				this.capture('./capture/'+uName+'_1.jpg',undefined,{
					format: 'jpg',
					quality: 75
					});                 //成功时调用的函数,给整个页面截图
				var file = './log/'+uName+'_SnkrsCookies.txt';	
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
			}, function() {
				this.capture('./capture/'+uName+'_1_E.jpg', undefined, {
					format: 'jpg',
					quality: 75
				});
			}, 5000);
			casper.wait(5000, function(){ 
				if ((this.getCurrentUrl().search(/login/i) != -1)) {
					this.echo("Pls add Mobile Phone to verify your account");	
				}
			}); 
		}
	}); 
});

casper.then(function() {

	utils.dump(this.getElementInfo('h4.js-header.ncss-brand.u-uppercase').text);
	casper.wait(500, function() {
		this.waitUntilVisible('div.buying-tools.ncss-col-sm-12.mt9-sm.full a', function() {
			this.fillSelectOptionByText("select.js-size-dropdown.size-dropdown.u-full-width.u-full-height","9");
			//utils.dump(this.getElementsInfo('select.js-size-dropdown.size-dropdown.u-full-width.u-full-height'));
       	     		this.click("a.js-buy.ncss-brand.u-align-center.u-uppercase.pt3-sm.pr5-sm.pb3-sm.pl5-sm.pt2-lg.pb2-lg.u-sm-b.u-lg-ib.test-buyable.ncss-btn.bg-black.text-color-white");
			this.capture('./capture/'+uName+'_2.jpg',undefined,{
				format: 'jpg',
				quality: 75
				});                 //成功时调用的函数,给整个页面截图
		}, function() {
			this.capture('./capture/'+uName+'_2_E.jpg', undefined, {
				format: 'jpg',
				quality: 75
			});
			this.echo(this.getHTML());
			casper.exit();
		}, 5000);
	});
});


casper.then(function() {
	this.waitForSelector('input#storedPayment0',function() {
		//utils.dump(this.getElementsInfo('input#storedPayment0'));
		if (this.exists('input#storedPayment0')) {
			this.echo('Select PayMent!!')
			this.click('input#storedPayment0');
		}
		//utils.dump(this.getElementsInfo('iframe'));
	});
});

casper.then(function() {
	this.wait(2000);

///	this.wait(500,function() {
//		utils.dump(this.getElementsInfo('iframe'));
//	});
});


casper.withFrame(0, function() {
	casper.wait(500, function() {
		this.waitUntilVisible('input#cvNumber', function() {  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
			this.echo(cardCCV);
		        this.fillSelectors('form#creditCardForm', {
       	        	        'input[id="cvNumber"]': cardCCV,
                	}, false);
			//utils.dump(this.getElementsInfo('body'));
			//this.captureSelector('./capture/'+uName+'_3_1.jpg','body');
			this.capture('./capture/'+uName+'_3.jpg',undefined,{
				format: 'jpg',
				quality: 75
				});                 //成功时调用的函数,给整个页面截图
		}, function() {
			//utils.dump(this.getElementsInfo('div.js-selection.selection.u-ws-e.p-sm.u-va-t.u-no-ws-e.pr8-sm'));
			this.echo(this.getCurrentUrl());
			//this.captureSelector('./capture/'+uName+'_3_1_E.jpg','body');
       			this.capture('./capture/'+uName+'_3_E.jpg', undefined, {
				format: 'jpg',
				quality: 75
			});
		}, 5000);
	});
});

/*	Debug Only
casper.then(function() {
	casper.wait(2000, function() {

	       	//this.click("section.js-payment.section-layout.border-top-light-grey.active-section div.save-button a");
		utils.dump(this.getElementsInfo('section.js-payment.section-layout.border-top-light-grey.active-section div.save-button'));
		utils.dump(this.getElementsInfo('div.js-selection.selection.u-ws-e.p-sm.u-va-t.u-no-ws-e.pr8-sm'));
	       	//this.click("section.js-payment.section-layout.border-top-light-grey.active-section div.save-button a");
	});


});
*/
casper.then(function() {

	this.waitUntilVisible('div.payment a.test-save-button.ncss-btn.bg-black.text-color-white.ncss-brand.pr5-sm.pl5-sm.pt3-sm.pb3-sm.pt2-lg.pb2-lg.u-uppercase.u-sm-b.u-lg-ib', function() {  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
		
       	     	this.click("div.payment a.test-save-button.ncss-btn.bg-black.text-color-white.ncss-brand.pr5-sm.pl5-sm.pt3-sm.pb3-sm.pt2-lg.pb2-lg.u-uppercase.u-sm-b.u-lg-ib");
		this.capture('./capture/'+uName+'_4.jpg',undefined,{
			format: 'jpg',
			quality: 75
			});                 //成功时调用的函数,给整个页面截图
	}, function() {
		this.capture('./capture/'+uName+'_4_E.jpg', undefined, {
				format: 'jpg',
				quality: 75
			});
	}, 5000);
	
	

});

casper.then(function() {

	this.waitUntilVisible('div.order-summary-component a.test-save-button.ncss-btn.bg-black.text-color-white.ncss-brand.pr5-sm.pl5-sm.pt3-sm.pb3-sm.pt2-lg.pb2-lg.u-uppercase.u-sm-b.u-lg-ib', function() {  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
		
		//utils.dump(this.getElementsInfo('div.js-selection.selection.u-ws-e.p-sm.u-va-t.u-no-ws-e.pr8-sm'));
       	     	//this.click("div.order-summary-component a.test-save-button.ncss-btn.bg-black.text-color-white.ncss-brand.pr5-sm.pl5-sm.pt3-sm.pb3-sm.pt2-lg.pb2-lg.u-uppercase.u-sm-b.u-lg-ib");
		this.capture('./capture/'+uName+'_5.jpg',undefined,{
			format: 'jpg',
			quality: 75
			});                 //成功时调用的函数,给整个页面截图
	}, function() {
		//utils.dump(this.getElementsInfo('div.js-selection.selection.u-ws-e.p-sm.u-va-t.u-no-ws-e.pr8-sm'));
		this.capture('./capture/'+uName+'_5_E.jpg', undefined, {
				format: 'jpg',
				quality: 75
			});
	}, 5000);
	
	

});

casper.then(function() {

	this.waitUntilVisible('h3.test-modal-header.ncss-brand.u-uppercase', function() {  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数
		utils.dump(this.getElementInfo('h3.test-modal-header.ncss-brand.u-uppercase').text);
		utils.dump(this.getElementInfo('p.test-confirmation.text-color-grey.u-align-center').text); 
		
		this.capture('./capture/'+uName+'_6.jpg',undefined,{
			format: 'jpg',
			quality: 75
			});                 //成功时调用的函数,给整个页面截图
	}, function() {
		this.capture('./capture/'+uName+'_6_E.jpg', undefined, {
				format: 'jpg',
				quality: 75
			});
	}, 5000);
	
	

});






casper.run(function() { 

	var file = './log/'+uName+'_SnkrsCookies.txt';	
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
	//fs.write('/root/nike/eastbay/cookies.txt', cookies, 'w'); 
	casper.echo("End at "+new Date().toLocaleString());
	this.exit();                                                                      

});
