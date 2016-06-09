var casper = require('casper').create({
    verbose: false,
    logLevel: 'info',
    pageSettings: {
        loadImages: true,
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
if (casper.cli.has('refUrl')) {var refUrl = casper.cli.get('refUrl');}

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
				doCheckOut(this,aPid,uName,fs,loop);
			}
	        },150000);
	});
	return;
}

casper.start();

casper.userAgent('Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36');

casper.thenOpen(refUrl, function(response) {
/*
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

*/

	this.wait(25000);
       	//var orderId = this.getElementsInfo('div#success p.order-id a');

});

/*
casper.then(function() {

	this.echo(this.getHTML());

});
*/
casper.run(function() { 

	var file = 'log/'+uName+'_jimmyjazzCookies.txt';	
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
