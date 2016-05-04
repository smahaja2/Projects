 <?php
          mysql_connect('localhost', 'user', 'pass');
          mysql_select_db('portfolio');

        $comments_query = mysql_query("SELECT * FROM comments WHERE isReply = '0' ORDER BY time desc");   
        $counter = 0;
        while($row = mysql_fetch_array($comments_query)){
                if($row['isReply'] == '0'){
                        $name = $row['username'];
                        $text = $row['message'];
                        $time = $row['time'];
                        echo
                                '<li class="cmmnt"><div class="cmmnt-content"><h4>';
                        echo    $name;
                        echo    ' wrote:</h4>';
                        echo    $text;
                        echo    '<h5>';
                        echo    $time;
                        $params = explode(" ", $time);
                        $d = $params[0];
                        $t = $params[1];
			$counter++;
                        $url = 'reply.php?d='.$d.'&'.'t='.$t;
			
			echo 	'<a  name = \''.$t.' '.$d.'\' id = \'replybutton'.$t.$d.'\' onclick=createReply(this.id) class="button small">Reply</a>';	
                        echo    '</h5></div></li>';
                        echo 	'<div id= \'replyformdiv'.$t.$d.'\' > </div>';
                        echo '<ul class="replies">';
                       	
                       	echo '<blockquote>';
                        $replies_query = mysql_query("SELECT * FROM comments WHERE isReply = '$time'");

                        while ($row = mysql_fetch_array($replies_query)){
                                $name = $row['username'];
                                $text = $row['message'];
                                $time = $row['time'];
                                echo    '<li class="cmmnt"><div class="cmmnt-content"><h4>';
                                echo    $name;
                                echo    ' wrote:</h4><blockquote>';
                                echo    $text;
                                echo    '</blockquote><h5>';
                                echo    $time;
                                echo    '</h5></div></li>';
				
                        }
			echo 	'</blockquote>';
                        echo '</ul>';
                       	
                }
        }
               
        ?>
