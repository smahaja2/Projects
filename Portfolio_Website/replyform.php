<?php  
              mysql_connect('localhost', 'user', 'pass');
              mysql_select_db('portfolio');

             
              
                $username =$_POST['usernameRep'];
                $message =$_POST['messageRep'];
               $isReply = $_POST["d"].' '.$_POST["t"];
                if(empty($message) or empty($username)){
                 
                  $out = "Please resubmit!";
                  echo 'FAILLLL';
                }
                else{    
                  $sql="INSERT INTO comments VALUES('$username','$message', '$isReply', now())";
                  $res=mysql_query($sql);
                  if($res)
                        echo 'Your reply has been submitted!';
                }
               
             
?>
