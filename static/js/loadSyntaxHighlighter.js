/**
 * @author Chine
 */
$(document).ready(function(){
	SyntaxHighlighter.autoloader(
	  'cpp c                  /static/blog/coolblue/js/SyntaxHighlighter/shBrushCpp.js',
	  'c# c-sharp csharp      /static/blog/coolblue/js/SyntaxHighlighter/shBrushCSharp.js',
	  'css                    /static/blog/coolblue/js/SyntaxHighlighter/shBrushCss.js',
	  'java                   /static/blog/coolblue/js/SyntaxHighlighter/shBrushJava.js',
	  'js jscript javascript  /static/blog/coolblue/js/SyntaxHighlighter/shBrushJScript.js',
	  'text plain             /static/blog/coolblue/js/SyntaxHighlighter/shBrushPlain.js',
	  'py python              /static/blog/coolblue/js/SyntaxHighlighter/shBrushPython.js',
	  'sql                    /static/blog/coolblue/js/SyntaxHighlighter/shBrushSql.js',
	  'xml xhtml xslt html    /static/blog/coolblue/js/SyntaxHighlighter/shBrushXml.js',
	  'go                     /static/blog/coolblue/js/SyntaxHighlighter/shBrushGo.js'
	);
	SyntaxHighlighter.all();
});