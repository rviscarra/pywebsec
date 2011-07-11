<html>
<head>
<title>PyWebSec</title>
<style>

body {
	font-family: "Verdana";
	background-color: #000;
	color: #619BD7;
	
	margin: 0;
	padding: 0;
}

div.hr {
	height: 3px;
	margin: 0 auto;
	width: 80%;
	display: block;
	background-color: #000;
}


.container {
	width: 700px;
	background-color: #F0F0F0;
	padding: 20px;
	margin: 0 auto;
	border-bottom-left-radius: 20px;
	border-bottom-right-radius: 20px;
	border: groove 5px #619BD7;
	border-top: none;
}

.header {
	padding: 10px;
	width: 100%;
	text-align: center;
}

.header h1 {
	font-weight: bold;
}

.content {
	width: 100%;
	background-color: #F4f4f4;
}

.footer {
	padding: 5px;
	text-align: center;
	width: 100%;
	font-size: 12px;

}

.centrado {
	margin: 0 auto;
	text-align: center;
}

#form_container {
	width: 200px;
	margin: 0 auto;
}

#submit_container {
	text-align: center;
}

</style>
<script src="http://localhost/js/jquery-1.5.1.min.js" type="text/javascript" />
<script type="text/javascript" >
	
\$(function(){
	if( \$('#webcam_image') ) {
		setInterval(function(){
			src = \$('#webcam_image').attr('src');
			\$('#webcam_image').attr('src', src);
		}, 500);
	}
});

</script>
</head>
<body>
<div class="container">
	<div class="header">
	<h1>PyWebSecurity Monitor</h1>
	</div>
	<div class="hr"></div>
	<div class="content">
		$yield
	</div>
	<div class="hr"></div>
	<div class="footer">
	PyWebSecurity Monitor &reg;
	</div>
</div>
</body>
</html>

