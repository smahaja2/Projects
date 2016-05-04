<!DOCTYPE html>
<!--
    Interphase by TEMPLATED
    templated.co @templatedco
    Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
    -->
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Projects</title>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <meta name="description" content="" />
        <meta name="keywords" content="" />
        <!--[if lte IE 8]><script src="css/ie/html5shiv.js"></script><![endif]-->
        <script src="js/jquery.min.js"></script>
        <script src="js/skel.min.js"></script>
        <script src="js/skel-layers.min.js"></script>
        <script src="js/init.js"></script>
        <noscript>
            <link rel="stylesheet" href="css/skel.css" />
            <link rel="stylesheet" href="css/style.css" />
            <link rel="stylesheet" href="css/style-xlarge.css" />
        </noscript>
        <!--[if lte IE 8]>
        <link rel="stylesheet" href="css/ie/v8.css" />
        <![endif]-->
	<!-- Futnion to add another comment -->        
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
        <script type="text/javascript">
            $(document).ready(function(){
            
            	$('#commits').load('commitData.php');
                  	
            });
            
        </script>
	<!-- Funtion to dynamically create reply form when reply button is clicked -->
        <script>
            function createReply(id){
             
            var s = "replyformdiv"+id.substring(11);
            var tag = id.substring(11);
            a = document.getElementById(s);
            $(a).append( '<div>' + 
            				'<h3>Enter a reply</h3>' +
            			 '<form  id= \'submitRep\'>' +
            				      
            			 'username : <br/\> ' + 
            			'<input type=\'text\' name =\'usernameRep\' id = \'usernameRep\'/\>' +
            				       
            
            			'Enter comment below:</br>' +
            		'<textarea rows="4" cols="50" name="messageRep" id = \'messageRep\' form=\'submitRep\' >'+
            		'</textarea>' +
            		'<input type=\'button\' onclick = submitReply(this.id) id = \'submitRep'+tag+'\' name =\'submitRep\' value=\'Submit Reply\' /\>' +
            		'</form>'+
            				       
            		'</div>' );
            
            }
        </script>
	<!-- Funtion to actually submit the reply to a comment -->
        <script>
            function submitReply(id){
            
            var t = id.substring(9,17);
            var d = id.substring(17);
            
            var username = $("#usernameRep").val();
            var message = $("#messageRep").val();
            
            // Returns successful data submission message when the entered information is stored in database.
            var dataString = 'usernameRep='+ username + '&messageRep='+ message + '&d=' + d + '&t=' +t;
            if(username==''||message=='')
            {
            alert("Please Fill All Fields");
            }
            else
            {
            // AJAX Code To Submit Form.
            $.ajax({
            type: "POST",
            url: "replyform.php",
            data: dataString,
            cache: false,
            success: function(result){
            	alert("Submitted Reply");
            	$('#comments').load('data.php');
            
            }
            });
            }
            
            }
        </script>
    </head>
    <body>
        <!-- Header -->
        <header id="header">
            <h1><a href="index.html">Siddharth Mahajan</a></h1>
            <nav id="nav">
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="generic.html">About Me</a></li>
                    <li><a href="elements.php">Projects</a></li>
                </ul>
            </nav>
        </header>
        <!-- Main -->
        <section id="main" class="wrapper">
            <div class="container">
                <header class="major">
                    <h2>Projects</h2>
                    <p>This is a quick svn parse of my repository</p>
                </header>
                <section>
                    <div id = 'commits'> 
                    </div>
                </section>
                <!-- Text -->
                <section>
                    <h2>Comments</h2>
                    <div>
                        <h3>Enter a comment</h3>
                        <form  id="submitComment">
                            username : <br/>
                            <input type='text' name ='username' id = 'username'/>
                            Enter comment below:</br>
                            <textarea rows="4" cols="50" name="message" id = 'message' form="submitComment" >
                            </textarea>
                            <input type='submit' id = 'submit' name ='submit' value='Submit' />
                        </form>
                    </div>
                    <div id="container">
                        <!--the master list of comments-->
                        <ul id="comments" data-role="listview">
                            <!--each comment-->
                            <?php
                                mysql_connect('localhost', 'user', 'pass');
                                mysql_select_db('portfolio');
                                
                                $comments_query = mysql_query("SELECT * FROM comments WHERE isReply = '0' ORDER by time desc");   
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
                                              echo    $time." ";
                                              $params = explode(" ", $time);
                                              $d = $params[0];
                                              $t = $params[1];
                                $counter++;
                                   
                                echo 	'<a  name = \''.$t.' '.$d.'\' id = \'replybutton'.$t.$d.'\' onclick=createReply(this.id) class="button small"> Reply</a>';	
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
                        </ul>
                    </div>
                </section>
            </div>
        </section>
        <!-- Footer -->
        <footer id="footer">
            <div class="container">
                <div class="row">
                    <section class="4u$ 12u$(medium) 12u$(small)">
                        <h3>Contact Me</h3>
                        <ul class="icons">
                            <li><a href="#" class="icon rounded fa-twitter"><span class="label">Twitter</span></a></li>
                            <li><a href="#" class="icon rounded fa-facebook"><span class="label">Facebook</span></a></li>
                            <li><a href="#" class="icon rounded fa-pinterest"><span class="label">Pinterest</span></a></li>
                            <li><a href="#" class="icon rounded fa-google-plus"><span class="label">Google+</span></a></li>
                            <li><a href="#" class="icon rounded fa-linkedin"><span class="label">LinkedIn</span></a></li>
                        </ul>
                        <ul class="tabular">
                            <li>
                                <h3>Address</h3>
                                #9<br>
                                309 E Healey Street<br>
                                Champaign, Illinois 61820
                            </li>
                            <li>
                                <h3>EMail</h3>
                                <a href="#">smahaja2@illinois.edu</a>
                            </li>
                            <li>
                                <h3>Phone</h3>
                                (217)-278-0056
                            </li>
                        </ul>
                    </section>
                </div>
            </div>
    </body>
</html>
