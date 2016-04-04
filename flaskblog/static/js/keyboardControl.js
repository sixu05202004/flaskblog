/**
 * @author Chine
 */

function moveNext() {
	$('article').each(function(i){
		var top = $(this).offset().top;
		if(top > $('body').scrollTop()) {
			$('html, body').scrollTop(top);
			return false;
		}
	});
}

function movePrev() {
	var $articles = $('article');
	var $size = $articles.size();
	var beyondLast = true;
	$articles.each(function(i){
		var top = $(this).offset().top;
		if(top >= $('body').scrollTop() && i > 0) {
			$('html, body').scrollTop($($articles.get(i - 1)).offset().top);
			if(beyondLast) beyondLast = false;
			return false;
		}
	});
	if(beyondLast) {
		$('html, body').scrollTop($($articles.get($size - 1)).offset().top);
	}
}

function pageNext() {
	var $pages = $("div#Pagination a");
	if($pages.size() > 0) {
		var $next = $pages.last();
		var text = $next.text();
		if(isNaN(parseInt(text))) {
			window.location = $next.attr('href');
		}
	}
}

function pagePrev() {
	var $pages = $("div#Pagination a");
	if($pages.size() > 0) {
		var $first = $pages.first();
		var text = $first.text()
		if(isNaN(parseInt(text))) {
			window.location = $first.attr('href');
		}
	}
}

$(function() {
	$(window).keydown(function(event) {
		if(event.which === 74) {
			// 按j键
			moveNext();
		}
		else if(event.which === 75) {
			// 按k键
			movePrev();
		}
		else if(event.which === 39 && event.ctrlKey) {
			// 按ctrl + 右箭头
			pageNext();
		}
		else if(event.which === 37 && event.ctrlKey) {
			// 按ctrl + 左箭头
			pagePrev();
		}
	});
});