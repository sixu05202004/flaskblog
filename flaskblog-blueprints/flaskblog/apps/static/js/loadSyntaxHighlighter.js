/**
 * @author Chine
 */
$(document).ready(function(){
	SyntaxHighlighter.autoloader(
	  'cpp c                  /static/js/SyntaxHighlighter/shBrushCpp.js',
	  'c# c-sharp csharp      /static/js/SyntaxHighlighter/shBrushCSharp.js',
	  'css                    /static/js/SyntaxHighlighter/shBrushCss.js',
	  'java                   /static/js/SyntaxHighlighter/shBrushJava.js',
	  'js jscript javascript  /static/js/SyntaxHighlighter/shBrushJScript.js',
	  'text plain             /static/js/SyntaxHighlighter/shBrushPlain.js',
	  'py python              /static/js/SyntaxHighlighter/shBrushPython.js',
	  'sql                    /static/js/SyntaxHighlighter/shBrushSql.js',
	  'xml xhtml xslt html    /static/js/SyntaxHighlighter/shBrushXml.js',
	  'go                     /static/js/SyntaxHighlighter/shBrushGo.js'
	);
	SyntaxHighlighter.all();
});