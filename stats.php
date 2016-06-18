<?php


/*
*This is the statisic PHP script which invoke the tool with the needed info'
*In the End of the process, two charts will be created on the desktop
*/

$command = escapeshellcmd('/home/support/PycharmProjects/AnalyzerRTC/main.py');

$output = shell_exec($command);
echo nl2br(htmlspecialchars($output));


?>

