/*
Author: mg12
Update: 2008/05/05
Author URI: http://www.neoease.com/
*/
(function() {

function reply(commentId, commentBox) {

	var insertStr = '<a href="# ' + commentId + '</a>';

	appendReply(insertStr, commentBox);
}



function appendReply(insertStr, commentBox) {
	if(MGJS.$(commentBox) && MGJS.$(commentBox).type == 'textarea') {
		field = MGJS.$(commentBox);

	} else {
		alert("The comment box does not exist!");
		return false;
	}

	if (field.value.indexOf(insertStr) > -1) {
		alert("You've already appended this reply!");
		return false;
	}

	if (field.value.replace(/\s|\t|\n/g, "") == '') {
		field.value = insertStr;
	} else {
		field.value = field.value.replace(/[\n]*$/g, "") + '\n\n' + insertStr;
	}
	field.focus();
}



window['MGJS_CMT'] = {};
window['MGJS_CMT']['reply'] = reply;


})();
