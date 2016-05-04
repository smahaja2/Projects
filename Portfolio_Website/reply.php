<!doctype html>
<html lang="en-US">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
  <title>Reply</title>
  <link rel="stylesheet" type="text/css" href="styles.css">
</head>
 
<body>
        <div>
              <h3>Enter a reply</h3>
            <form method='post' id="submitComment">
            <?php  
              mysql_connect('localhost', 'user', 'pass');
              mysql_select_db('portfolio');
              $isReply = $_GET["d"].' '.$_GET["t"];
             
              if(isset($_POST['submit'])) {
                $username =$_POST['username'];
                $message =$_POST['message'];
               
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
               
              }
             
            ?>
           
           
            username : <br/>
            <input type='text' name ='username' />
           
            <input type='submit' name ='submit' value='Submit' />
            </form>
            Enter reply below:</br>
            <textarea rows="4" cols="50" name="message" form="submitComment">
            </textarea>
            </br>
            <a href='comments.php'>Back to Comments</a>
        </div>
</body>
</html>