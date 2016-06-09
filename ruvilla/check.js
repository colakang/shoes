var casper = require('casper').create({
    verbose: false,
    logLevel: 'info',
    pageSettings: {
        loadImages: false,
        loadPlugins: false,
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
var cardTYPE = bank[ccd].cardTYPE;

if (cardMM.charAt(0) == '0') { 
	cardMM = cardMM.substr(1);
}

cardYY = '20'+cardYY;


casper.echo("Start At "+new Date().toLocaleString());

//casper.exit();	

function doCheckOut (thecasper,aPid,uName,fs,loop) {

	thecasper.wait(1000);

	thecasper.then(function() {

        	this.waitUntilVisible('div#success', function() {
			pageUrl = this.getCurrentUrl();
			if (pageUrl.search(/success/) != -1) {
				this.echo("Check Out Success");	
			}
        		var orderId = this.getElementsInfo('div#success p.order-id a');
	
			this.echo("Order ID:"+orderId.text);
        	        this.capture('capture/'+aPid+'_'+uName+'-05.jpg', undefined, {
                	        format: 'jpg',
                       	 quality: 75
	                });
	        }, function() {
        	        this.capture('capture/'+aPid+'_'+uName+'-05-'+loop+'-error.jpg', undefined, {
                	        format: 'jpg',
	                        quality: 75
	                });
			var file = 'log/'+aPid+"_"+uName+'_CheckError.txt';
			var res = this.getHTML();
			fs.write(file, res, 'w');
	                this.echo("CheckOut Faile!");
			if (loop<15) {
				loop = loop+1;
			        this.waitUntilVisible('div#review-buttons-container', function() {

					casper.evaluate(function() {
						review.save();
					});
	
	                		this.capture('capture/'+aPid+'_'+uName+'-04-'+loop+'.jpg', undefined, {
		                        	format: 'jpg',
        		                	quality: 75
                			});
			        }, function() {
			                this.capture('capture/'+aPid+'_'+uName+'-04-'+loop+'-error.jpg', undefined, {
			                        format: 'jpg',
                        			quality: 75
			                });
		                        this.echo("No Submit Button! Reload again");
			        },5000);

				doCheckOut(this,aPid,uName,fs,loop);
			}
	        },150000);
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

	//this.page.cookies = phantom.cookies;
	//utils.dump(phantom.cookies);
	//casper.exit();
});

casper.thenOpen('https://www.ruvilla.com/checkout/onepage/', function(response) {
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
		this.echo('Found');
		this.click('a[title="Continue Button"]');
		this.reload();
	}

	this.waitUntilVisible('div#billing-buttons-container', function() {                  //等到'.tweet-row'选择器匹配的元素出现时再执行回调函数

		casper.evaluate(function() {
			billing.save();
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
        		this.echo("No Billing Info! Reload again");
		});
	}, 50000);                                                       //超时时间,两秒钟后指定的选择器还没出现,就算失败 
});

casper.then(function() {

	if (this.exists('table#sharedCart_panel')) {
		this.echo('Found');
		this.click('a[title="Continue Button"]');
		this.reload();
	}

	this.waitUntilVisible('div#shipping-method-buttons-container', function() {
		this.click('input#s_method_fedex_FEDEX_EXPRESS_SAVER')
                casper.evaluate(function() {
                        shippingMethod.save();
                });		
		this.capture('capture/'+aPid+'_'+uName+'-02.jpg', undefined, {
        		format: 'jpg',
        		quality: 75
    		});
	}, function() {
		this.capture('capture/'+aPid+'_'+uName+'-02-error.jpg', undefined, {
        		format: 'jpg',
        		quality: 75
    		});
	       	this.reload(function() {
        		this.echo("No Shipping Method! Reload again");
		});
	},50000);
 
});

casper.then(function() {

        this.waitUntilVisible('div#payment-buttons-container', function() {
                this.click('input#p_method_authorizenet')
		this.sendKeys('form#co-payment-form input#authorizenet_cc_number', cardNo, {keepFocus: true});
		casper.evaluate(function(cardYY,cardMM,cardTYPE) {
			if (cardTYPE == 'visa') {
				document.querySelector('select#authorizenet_cc_type').value ='VI';
			} else {
				document.querySelector('select#authorizenet_cc_type').value = 'MC';
			}
			document.querySelector('select#authorizenet_expiration').value = cardMM;
			document.querySelector('select#authorizenet_expiration_yr').value = cardYY;
		},cardYY,cardMM,cardTYPE);
		this.sendKeys('form#co-payment-form input#authorizenet_cc_cid', cardCCV, {keepFocus: true});
		casper.evaluate(function() {payment.save();});		
	
                this.capture('capture/'+aPid+'_'+uName+'-03.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
//                argv = this.getFormValues('form#spcoForm');
//                var content = JSON.stringify(argv);
//                fs.write('argv/'+aPid+'_'+uName+'_post.txt', content, 'w');
        }, function() {
                this.capture('capture/'+aPid+'_'+uName+'-03-error.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
                this.reload(function() {
                        this.echo("No Payment Button! Reload again");
                });
        },50000);


});

casper.then(function() {

        this.waitUntilVisible('div#review-buttons-container', function() {

		casper.evaluate(function() {
			review.save();
		});
	
                this.capture('capture/'+aPid+'_'+uName+'-04.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
        }, function() {
                this.capture('capture/'+aPid+'_'+uName+'-04-error.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
                this.reload(function() {
                        this.echo("No Submit Button! Reload again");
                });
        },50000);


});

casper.then(function() {

	doCheckOut(this,aPid,uName,fs,0);
/*
        this.waitUntilVisible('div#success', function() {
		pageUrl = this.getCurrentUrl();
		if (pageUrl.search(/success/) != -1) {
			this.echo("Check Out Success");	
		}
        	var orderId = this.getElementsInfo('div#success p.order-id a');
	
		this.echo("Order ID:"+orderId.text);
                this.capture('capture/'+aPid+'_'+uName+'-05.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
        }, function() {
                this.capture('capture/'+aPid+'_'+uName+'-05-error.jpg', undefined, {
                        format: 'jpg',
                        quality: 75
                });
		var file = 'log/'+aPid+"_"+uName+'_CheckError.txt';
		var res = this.getHTML();
		fs.write(file, res, 'w');
                this.echo("CheckOut Faile!");
        },150000);

*/
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
