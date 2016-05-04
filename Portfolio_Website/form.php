<?php  
                        mysql_connect('localhost', 'user', 'pass');
                        mysql_select_db('portfolio');
               
               
                        
                                $username =$_POST['username'];
				$username = mysql_real_escape_string($username);
                                $message =$_POST['message'];
				$message = mysql_real_escape_string($message);
				$pieces = explode(" ", $message);
                               	foreach($pieces as &$word){
					$statement="SELECT replacement FROM flags WHERE redword = '".$word."'";
					$response = mysql_query($statement);
					if (mysql_num_rows($response) > 0) {
						while ($row = mysql_fetch_array($response)) {
						    $word = $row['replacement'];
						}
					
					}
				}
				$message = implode(" ",$pieces);
                                if(empty($message) or empty($username)){
                                       
                                        $out = "Please resubmit!";
                                }
                                else{   
                                        echo "Form Submitted Succesfully".$username;

                                        $sql="INSERT INTO comments VALUES('$username','$message', 0, now())";
                                        $res=mysql_query($sql);
                                }
                        
                       
?>
