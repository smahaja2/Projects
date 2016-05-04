<?php

function findSummary($rev) {
    $logxml = simplexml_load_file(dirname(__FILE__).'/svn_log.xml');
	foreach ($logxml->logentry as $e){
		
		if((string)$rev === (string)$e['revision']){
			return $e->msg;
		}
			

	}
	return "No message found";
}


	$listxml = simplexml_load_file(dirname(__FILE__).'/svn_list.xml');          
	$logxml = simplexml_load_file(dirname(__FILE__).'/svn_log.xml');
	
	 foreach ($listxml->list as $list){
				      
				      
	      $path = (string) $list['path'];
	     
	      foreach ($list->entry as $entry){
			
			$name = $entry->name;
			if (strpos($name, '/') === FALSE){
				echo '<h2>'.$name.'</h2>';
				
				$ver = $entry->commit['revision'];
				echo '<h4>Version: '.$ver.'</h4>';
				$d = (string) $entry->commit->date;
				echo '<h4>Date: '.$d.'</h4>';
				$summary = findSummary($ver);
				if($summary == "")
					$summary = "No message found";
				echo '<h4>Summary: '.$summary.'</h4>';
				echo '<h4>Files: </h4>';
				foreach ($list->entry as $entry2){
					$name2 = $entry2->name;
					if ((strpos($name2, $name) == 0) && strcmp($name2,$name) != 0 && $entry2['kind'] == 'file'){
						echo '<h5> <font color="#FF0000">'.end(explode('/',$name2)).'</font></h5>';
						echo '<h6>Size: '.$entry2->size.' bytes,  Type: '.end(explode('.',$name2)).',  Path: '.$name2.'</h6>';
					}
				}
	
			}
			

	      }
	  	 		 
	}


?>

<!-- foreach ($logentry->paths as $paths)  $rev = (string) $entry->commit->revision;
	  		{
	   			 foreach ($paths->path as $path)
	   			 {
				      $action = $path['action'];
				      $content = (string) $path;
				      echo '<p>'.$path.'</p>';
	  	 		 }
	 		} 

		foreach ($list->entry as $entry){
		  	
		echo '<p>'.$entry->name.'</p>';
		
		echo	'<p>'.$rev.'</p>';
	  	
	}

-->
