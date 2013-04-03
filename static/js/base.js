
/*
Author: mg12
Update: 2008/05/05
Author URI: http://www.neoease.com/
*/
(function() {
function $(id) {
return document.getElementById(id);
}
function setStyleDisplay(id, status) {
$(id).style.display = status;
}
function goTop(a, t) {
a = a || 0.1;
t = t || 16;
var x1 = 0;
var y1 = 0;
var x2 = 0;
var y2 = 0;
var x3 = 0;
var y3 = 0;
if (document.documentElement) {
x1 = document.documentElement.scrollLeft || 0;
y1 = document.documentElement.scrollTop || 0;
}
if (document.body) {
x2 = document.body.scrollLeft || 0;
y2 = document.body.scrollTop || 0;
}
var x3 = window.scrollX || 0;
var y3 = window.scrollY || 0;
var x = Math.max(x1, Math.max(x2, x3));
var y = Math.max(y1, Math.max(y2, y3));
var speed = 1 + a;
window.scrollTo(Math.floor(x / speed), Math.floor(y / speed));
if(x > 0 || y > 0) {
var f = "MGJS.goTop(" + a + ", " + t + ")";
window.setTimeout(f, t);
}
}
function switchTab(showPanels, hidePanels, activeTab, activeClass, fadeTab, fadeClass) {
$(activeTab).className = activeClass;
$(fadeTab).className = fadeClass;
var panel, panelList;
panelList = showPanels.split(',');
for (var i = 0; i < panelList.length; i++) {
var panel = panelList[i];
if ($(panel)) {
setStyleDisplay(panel, 'block');
}
}
panelList = hidePanels.split(',');
for (var i = 0; i < panelList.length; i++) {
panel = panelList[i];
if ($(panel)) {
setStyleDisplay(panel, 'none');
}
}
}
function loadCommentShortcut() {
$('comment').onkeydown = function (moz_ev) {
var ev = null;
if (window.event){
ev = window.event;
} else {
ev = moz_ev;
}
if (ev != null && ev.ctrlKey && ev.keyCode == 13) {
$('submit').click();
}
}
$('submit').value += ' (Ctrl+Enter)';
}
function getElementsByClassName(className, tag, parent) {
parent = parent || document;
var allTags = (tag == '*' && parent.all) ? parent.all : parent.getElementsByTagName(tag);
var matchingElements = new Array();
className = className.replace(/\-/g, '\\-');
var regex = new RegExp('(^|\\s)' + className + '(\\s|$)');
var element;
for (var i = 0; i < allTags.length; i++) {
element = allTags[i];
if (regex.test(element.className)) {
matchingElements.push(element);
}
}
return matchingElements;
}
window['MGJS'] = {};
window['MGJS']['$'] = $;
window['MGJS']['setStyleDisplay'] = setStyleDisplay;
window['MGJS']['goTop'] = goTop;
window['MGJS']['switchTab'] = switchTab;
window['MGJS']['loadCommentShortcut'] = loadCommentShortcut;
window['MGJS']['getElementsByClassName'] = getElementsByClassName;
})(); 