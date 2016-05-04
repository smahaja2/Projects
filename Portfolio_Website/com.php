<!doctype html>
<html lang="en-US">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
  <title>Comments</title>
  <link rel="stylesheet" type="text/css" href="styles.css">
</head>
 
<body>
  <div id="board">
 
    <h1>Comments</h1>
    <div>
        <h3>Enter a comment</h3>
        <form method='post' id="submitComment">
        <?php  
            mysql_connect('engr-cpanel-mysql.engr.illinois.edu', 'dlee121_user', 'dleepw');
            mysql_select_db('dlee121_portfolio');
       
       
            if(isset($_POST['submit'])) {
                $username =$_POST['username'];
                $message =$_POST['message'];
               
                if(empty($message) or empty($username)){
                   
                    $out = "Please resubmit!";
                }
                else{          
                    $sql="INSERT INTO comments VALUES('$username','$message', 0, now())";
                    $res=mysql_query($sql);
                }
               
            }
           
        ?>
       
       
        username : <br/>
        <input type='text' name ='username' />
       
        <input type='submit' name ='submit' value='Submit' />
        </form>
        Enter comment below:</br>
        <textarea rows="4" cols="50" name="message" form="submitComment">
        </textarea>
       
    </div>
    <div id="container">
   
      <!--the master list of comments-->
      <ul id="comments">
     
        <!--each comment-->
        <?php
        $comments_query = mysql_query("SELECT * FROM comments WHERE isReply = '0'");   
           
    while($row = mysql_fetch_array($comments_query)){
        if($row['isReply'] == '0'){
            $name = $row['username'];
            $text = $row['message'];
            $time = $row['time'];
            echo
                '<li class="cmmnt"><div class="cmmnt-content"><h2>';
            echo    $name;
            echo    ' wrote:</h2><p>';
            echo    $text;
            echo    '</p><h5>';
            echo    $time;
            $params = explode(" ", $time);
            $d = $params[0];
            $t = $params[1];
            $url = 'reply.php?d='.$d.'&'.'t='.$t;
            echo    '</h5></div></li>';
            echo    '<a href='.$url.'>Reply to this comment</a>';
           
            echo '<ul class="replies">';
           
            $replies_query = mysql_query("SELECT * FROM comments WHERE isReply = '$time'");
            while ($row = mysql_fetch_array($replies_query)){
                $name = $row['username'];
                $text = $row['message'];
                $time = $row['time'];
                echo    '<li class="cmmnt"><div class="cmmnt-content"><h2>';
                echo    $name;
                echo    ' wrote:</h2><p>';
                echo    $text;
                echo    '</p><h5>';
                echo    $time;
                echo    '</h5></div></li>';
            }
            echo '</ul>';
           
        }
    }
       
        ?>
   
      </ul>
    </div>
  </div>
</body>
</html>

