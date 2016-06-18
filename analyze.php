<?php 

/*
*This is a PHP function which invoke the main  program
*Input are the arguments from the index.html page
*/

$raceNo = $_POST['RaceNo'];
$ts = $_POST['timestamp'];

//Define legal range for RACE No.
$race = array(
	'options' => array(
                      'min_range' => 999,
                      'max_range' => 9999,
                     	  )
);

//If Input was not provide retuurn to home-page
if ( !isset($raceNo)  || !isset($ts)){
	header('Location: index.html');
}

//If race No. Input wrong retuurn to home-page
if (filter_var($raceNo, FILTER_VALIDATE_INT, $race) == FALSE ){
	header('Location: index.html');
}

//If timestamp Input wrong retuurn to home-page
if (preg_match ("/^\d{1,2}\s\d{1,2}\s\d{4}\s\d{2}\:\d{2}\:\d{2}", $ts) == FALSE){
	echo "Input not valid! ";

}

	//Invoke the Analyzer tool with provided arguments


		$command = escapeshellcmd('/home/support/PycharmProjects/AnalyzerRTC/main.py ' .$raceNo .' ' .$ts);
		$output = shell_exec($command);
		echo nl2br(htmlspecialchars($output)); 



?>
