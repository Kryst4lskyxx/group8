<?php

//get data passed from Voice Browser
$user = $_GET['user'];
$product = $_GET['product'];
$quantity = $_GET['quantity'];
$price = $_GET['price'];
$duration = $_GET['duration'];

$date = Date('Y-m-d'); //current date at server
$time = time(); //current time (in seconds format)
$id = $user . $time; //concatenation of contact ID (phone number) and time used as unique key

//connect to MYSQL database
$con = mysql_connect("mysql7.000webhost.com","a7049946_fsd","thepassword123");
if (!$con)
{
die('Could not connect: ' . mysql_error());
}

//open the specific database
mysql_select_db("a7049946_stuff", $con);

//insert data into the specific table
$sql = "INSERT INTO eAfrica(ID, user, product, quantity, price, duration, date) VALUES ('$id','$user','$product', $quantity, $price, $duration, Now())";

//sanity check
if (!mysql_query($sql,$con))
{
die('Error: ' . mysql_error());
}

//close database
mysql_close($con);
?>
