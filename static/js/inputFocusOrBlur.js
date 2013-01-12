/**
 * @author Chine
 */
function inputFocusOrBlur(obj, type, defaultVal) {
	if(type == 0) {
		if($(obj).val() == defaultVal) {
			$(obj).val('');
		}
	} else {
		if($(obj).val() == '') {
			$(obj).val(defaultVal);
		}
	}
}