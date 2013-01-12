/**
 * @author Chine
 */

var subscribeResultTips = {
	success: "<i class='icon-ok'></i>订阅成功！",
	miss: "<i class='icon-exclamation-sign'></i>订阅失败，请填写所有必填信息！",
	fail: "<i class='icon-exclamation-sign'></i>订阅失败，信息错误或您已经订阅！"
}

$(function() {
	$('div.subscribe a:first, ul.subscribe-stuff a:last').click(function() {
		$('#subscribemodal').modal('show');
		return false;
	});
	
	$("#subscribeform").ajaxForm({
		beforeSubmit: checkSubscribe,
		success: dealSubscribeResponse
	});
});

function addSubscribeModalTip(type) {
	$('#resultmodal .modal-body p').html(subscribeResultTips[type]);
}

function checkSubscribe(arr, $form, options) {
	for(itm in arr) {
		var obj = arr[itm];
		
		var name = obj.name;
		var value = obj.value;
		
		if(name == 'username'|| name=='email_address') {
			if((name=='username' &&　value=='你的昵称')
				|| (name=='email_address' && value=='你的邮箱')) {
				value = '';
			}
			
			if(value == '' || typeof value == undefined) {
				$('#subscribemodal').modal('hide');
				
				addSubscribeModalTip('miss');
				$('#resultmodal').modal();
				
				return false;
			}
		}
		
	}

}

function dealSubscribeResponse(responseText,statusText) {
	$('#subscribemodal').modal('hide');
	
	if(responseText == "0") {
		addSubscribeModalTip('fail');
	} else {
		addSubscribeModalTip('success');
	}
	$('#resultmodal').modal();
}
