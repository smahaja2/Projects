<!doctype html>
<html lang="en-US">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
  <title>Comments</title>
  <link rel="stylesheet" type="text/css" href="styles.css">
  <script type="text/javascript" src="jquery.js"></script>
  <script type="text/javascript">
		$(document).ready(function(){
		$("#submit").click(function(){
		var username = $("#username").val();
		var message = $("#message").val();
		
		// Returns successful data submission message when the entered information is stored in database.
		var dataString = 'username='+ username + '&message='+ message;
		if(username==''||message=='')
		{
		alert("Please Fill All Fields");
		}
		else
		{
		// AJAX Code To Submit Form.
		$.ajax({
		type: "POST",
		url: "form.php",
		data: dataString,
		cache: false,
		success: function(result){
			alert("Submitted");
			$('#comments').load('data.php');

		}
		});
		}
		return false;
		});
		});
		 
  </script>
  <script>
    $(document).ready(
            function() {
                setInterval(function() {
                    var randomnumber = Math.floor(Math.random() * 100);
                    $('#show').text(
                            'I am getting refreshed every 3 seconds..! Random Number ==> '
                                    + randomnumber);
                }, 3000);
            });
</script>

</head>
 
<body>
	
  <div id="board">
 	
    <h1>Comments</h1>
    <div>
            <h3>Enter a comment</h3>
                <form  id="submitComment">
               
               
               
                username : <br/>
                <input type='text' name ='username' id = 'username'/>
               
                <input type='submit' id = 'submit' name ='submit' value='Submit' />
                </form>
                Enter comment below:</br>
                <textarea rows="4" cols="50" name="message" id = 'message' form="submitComment" >
                </textarea>
               
    </div>
    <div id="container">
       
      <!--the master list of comments-->
      <ul id="comments" data-role="listview">
     
        <!--each comment-->
        <?php
          mysql_connect('localhost', 'user', 'pass');
          mysql_select_db('portfolio');

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