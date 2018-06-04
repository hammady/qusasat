<?php
    $cleardb_url = parse_url(getenv("CLEARDB_DATABASE_URL"));
    $host = $cleardb_url["host"];
    $user = $cleardb_url["user"];
    $password = $cleardb_url["pass"];
    $database = substr($cleardb_url["path"],1);

    $conn = mysql_connect($host, $user, $password);

	if($conn){
		mysql_set_charset('utf8');

		mysql_select_db($database, $conn);

		$query = "SELECT * FROM `qusasat` AS q,`categories` AS c "
			. "WHERE q.category=c.id ORDER BY RAND() LIMIT 0,1";
		$resultID = mysql_query($query, $conn);
		$row = mysql_fetch_assoc($resultID);

		$qusasa = $row['qusasa'];
		$category = $row['category'];
	} else {
		$qusasa = "مصر غارقة في دوامة: كيف أعمل وأنت لا تعطيني مالاً؟.. كيف أعطيك مالاً وأنت لا تعمل؟";
		$category = "قصاصات عن السياسة";
	}

    echo $qusasa;
?>
<!--
<html>
	<head>
		<meta charset="utf-8"></meta>
	</head>
	<body>
		<center>
			<div style="height:300px; width:100%; background-color:#FFFFFF; color:#000000; background-image:url('paper.png')">
				<font size="4">
					<b><i><center>
						<div id="div_category"><?php echo $category;?></div>
					</center></i></b>
					<br/>
					<div id="div_qusasa" dir="rtl" align="justify" style="width:95%;"><?php echo $qusasa;?></div>
					<br/>
				</font>
			</div>
		</center>
	</body>
</html>
-->
