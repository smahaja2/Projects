var id;
var async = require('async');
var qs = require('querystring');

module.exports = function(app, passport) {
    
    // =====================================
    // HOME PAGE (with login links) ========
    // =====================================
    app.get('/', function(req, res) {
        res.render('index.ejs'); // load the index.ejs file
    });
    
    // =====================================
    // RECIPE ==============================
    // =====================================
    app.get('/:id([0-9]+)', isLoggedIn, function(req, res) {
        var connection = connect_to_sql();
        var sql = 'select * from comments JOIN user_recipes ON rid=recipe_id JOIN USERS on USERS.user_id=user_recipes.user_id WHERE rid='+req.params.id;
        connection.query(sql, function(err, rows, fields) {
            if (!err){
                connection.end();
                res.render('recipe.ejs', { recipeNum: req.params.id, ret: rows});
            } 
          else
            console.log('Error');
        });
    });
    app.post('/:id([0-9]+)', function(req, res) {
            var connection = connect_to_sql();
            
            var sql = 'INSERT INTO comments VALUES ('+req.params.id+','+req.session.DBuserID+',\''+req.body.message+'\')';
            connection.query(sql, function(err, rows, fields) {
                if (!err){
                    connection.end();
                    res.redirect('/'+req.params.id);
                } 
              else
                console.log('Error');
            });
    });
    
    // =====================================
    // SEARCH BY INGREDIENTS ==============================
    // =====================================
    app.get('/search', function(req, res) {
        res.render('search.ejs'); // load the index.ejs file
    });

    app.post('/search', function(req, res) {
        var ids =[];
        async.waterfall([
                function(callback){
                for(var i=0;i<req.body.counter;i++){
                    search_ingredient(i,req.body['element'+i], req.body['cals'], callback);
                }
            },
            function(count,rec_ids,callback){
                ids.push(rec_ids);
                callback(null,count);
            }
            
        ], function(err, results){
            if(!err){
                if(results == req.body.counter-1){
                    console.log('Search series completed.');
                    console.log(ids);
                    var new_ids = containsAll(ids);
                    console.log(new_ids);
                    res.render('searchResults.ejs', {
                                results: new_ids
                            });
                }
                
            }
            else
            console.log('error in search waterfall' + err);
        });
        
    });
    // =====================================
    // LOGIN ===============================
    // =====================================
    // show the login form
    app.get('/login', function(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('login.ejs', { message: req.flash('loginMessage') }); 
    });

    // process the login form
    app.post('/login', passport.authenticate('local-login', {
        successRedirect : '/profile', // redirect to the secure profile section
        failureRedirect : '/login', // redirect back to the signup page if there is an error
        failureFlash : true // allow flash messages
    }));

    // =====================================
    // SIGNUP ==============================
    // =====================================
    // show the signup form
    app.get('/signup', function(req, res) {

        // render the page and pass in any flash data if it exists
        res.render('signup.ejs', { message: req.flash('signupMessage') });
    });

    // process the signup form
    app.post('/signup', passport.authenticate('local-signup', {
        successRedirect : '/profile', // redirect to the secure profile section
        failureRedirect : '/signup', // redirect back to the signup page if there is an error
        failureFlash : true // allow flash messages
    }));

    // =====================================
    // PROFILE SECTION =====================
    // =====================================
    // we will want this protected so you have to be logged in to visit
    // we will use route middleware to verify this (the isLoggedIn function)
    app.get('/profile', isLoggedIn, function(req, res) {
        
        var connection = connect_to_sql();
        
        
        //If the user signed up with facebook.
        var sql1;
        if(req.user.facebook!=undefined & req.user.facebook!=null )
        if(req.user.facebook.id!=undefined){
                
                
                    sql1 = 'select * from USERS where fbid IS NOT NULL AND fbid = '+req.user.facebook.id;

        }
        else {
                //the user has not signed up with facebook. So we find user id by email
            
                    sql1 = 'select * from USERS where email = \''+req.user.local.email+'\'';
                      
        }
        connection.query(sql1, function(err, rows, fields) {
                      if (!err){
                        id = rows[0].user_id;
                        req.session.DBuserID = id;
                        req.session.fullname = rows[0].Name;
                        req.session.lastMessage = '';
                        connection.end();
                        res.render('profile.ejs', {
                            user : req.user, // get the user out of session and pass to template
                            session: req.session
                        });
                      }
                      else
                        console.log('Error retrieving user ID from database' + err);
                    });
            
        
    });
  
    // =====================================
    // LOGOUT ==============================
    // =====================================
    app.get('/logout', function(req, res) {
        req.logout();
        res.redirect('/');
    });
    
    
    // =====================================
    // FB ROUTES ===========================
    // =====================================
    // route for facebook authentication and login
    app.get('/auth/facebook', passport.authenticate('facebook', { scope : 'email' }));

    // handle the callback after facebook has authenticated the user
    app.get('/auth/facebook/callback',
        passport.authenticate('facebook', {
            successRedirect : '/profile',
            failureRedirect : '/'
        }));

    // route for logging out
    app.get('/logout', function(req, res) {
        req.logout();
        res.redirect('/');
    });
    
    // =====================================
    // MY RECIPES ==========================
    // =====================================
    // show all recipes the user has uploaded
    app.get('/myRecipes', function(req, res) {
        
        var connection = connect_to_sql();
        var sql = 'select * from user_recipes where user_id='+req.session.DBuserID;
        connection.query(sql, function(err, rows, fields) {
            if (!err){
                connection.end();
                res.render('myRecipes.ejs', { ret: rows });
            } 
          else
            console.log('Error');
        });
    });
    
    // =====================================
    // Edit Restrictions ==========================
    // =====================================
    // show all recipes the user has uploaded
    app.get('/editRestrictions', isLoggedIn, function(req, res) {
        
        async.waterfall([
                function(callback){
                    get_allergens(req.session.DBuserID,callback);
                },
                function(results, callback){
                    
                    callback(null,results);
                }
            
            ],function(err,results){
                if(!err){
                    console.log(results);
                    console.log('Done');
                    res.render('editRestrictions.ejs', { allergens: results });
                }
                else 
                    console.log('Error in waterfall');
                
            });
        
    });
    app.post('/editRestrictions', function(req, res) {
        
        async.waterfall([
                function(callback){
                    delete_allergens(req.session.DBuserID ,callback);
                },
                function(callback){
                    callback();
                }
            
                ],function(err,results){
                    if(!err){
                        console.log(results);
                        console.log('Done');
                        for(var key in req.body){
                            insert_allergen(key,req.session.DBuserID);
                         }
                    req.session.lastMessage = 'Allergens updated successfully';
                    res.render('profile.ejs', 
                    {   
                        session: req.session,
                        user: req.user
                    });
                }
                else 
                    console.log('Error in waterfall');
                
            });
    });
    // =====================================
    // Messages ==========================
    // =====================================
    // show all messages the user has received
    app.get('/inbox', isLoggedIn, function(req, res) {
        
        async.waterfall([
                function(callback){
                    get_messages(req.session.DBuserID,callback);
                },
                function(results, callback){
                    
                    callback(null,results);
                }
            
            ],function(err,results){
                if(!err){
                    console.log(results);
                    console.log('Done');
                    res.render('inbox.ejs', { messages: results });
                }
                else 
                    console.log('Error in waterfall');
                
            });
        
    });
    
    app.get('/outbox', isLoggedIn, function(req, res) {
        
        async.waterfall([
                function(callback){
                    get_outgoing_messages(req.session.DBuserID,callback);
                },
                function(results, callback){
                    
                    callback(null,results);
                }
            
            ],function(err,results){
                if(!err){
                    console.log(results);
                    console.log('Done');
                    res.render('outbox.ejs', { messages: results });
                }
                else 
                    console.log('Error in waterfall');
                
            });
        
    });
    
    app.get('/sendMessage', isLoggedIn, function(req, res) {
        res.render('sendMessage.ejs');
    });
    app.get('/send/:tid([0-9]+)', isLoggedIn, function(req, res) {
        res.render('sendTo.ejs', {recipientID: req.params.tid});
    });
    
    app.post('/sendTo', function(req, res) {
            var connection = connect_to_sql();
            var sql = 'insert into messages (from_id,to_id,title,message,time,name)values('+req.session.DBuserID+','+req.body.recipient+',\''+req.body.msgTitle+'\',\''+req.body.content+'\',now(),\''+req.session.fullname+'\')';
            connection.query(sql, function(err, rows, fields) {
                if (!err){
                    connection.end();
                    res.redirect('/details/'+req.body.recipient);
                } 
              else
                console.log('Error');
            });
    });
    
    app.get('/delete/:mid([0-9]+)', function(req, res) {
        var connection = connect_to_sql();
        var sql = 'delete from messages where mid='+req.params.mid;
        connection.query(sql, function(err, rows, fields) {
            if (!err){
                connection.end();
                res.redirect('/inbox');
            } 
          else
            console.log('Error');
        });
    });
    
    app.get('/content/:msgID([0-9]+)', function(req, res) {
        var connection = connect_to_sql();
        
        var sql = 'select * from messages where mid = '+req.params.msgID;
        connection.query(sql, function(err, rows, fields) {
        if (!err){
            connection.end();
            res.render('message.ejs', { message: rows[0]});
        } 
        else
            console.log('Error');
        });
    });
    
    // =====================================
    // FIND USER ===========================
    // =====================================
    // find users by username
    app.get('/findUser', function(req, res) {
        res.render('findUser.ejs', { results: null});
    });
    app.post('/findUser', function(req, res) {
        var connection = connect_to_sql();
        
        var sql = 'select * from USERS where Name Like \'%'+req.body.nom+'%\'';
        connection.query(sql, function(err, rows, fields) {
        if (!err){
            connection.end();
            res.render('findUser.ejs', { results: rows});
        } 
        else
            console.log('Error');
        });
    });
    app.get('/details/:uid([0-9]+)', function(req, res) {
        var connection = connect_to_sql();
        
        var sql = 'select * from USERS where user_id = '+req.params.uid;
        connection.query(sql, function(err, rows, fields) {
        if (!err){
            connection.end();
            res.render('details.ejs', { userdata: rows[0]});
        } 
        else
            console.log('Error');
        });
    });
    // =====================================
    // UPLOAD RECIPE =======================
    // =====================================
    // show the recipe upload form
    app.get('/uploadRecipe', isLoggedIn, function(req, res) {
        res.render('uploadRecipe.ejs');
    });
    
    
    app.post('/addRecipe', function(req, res) {
             
           async.waterfall([
                function(callback){
                    get_recipe_id(req.body.recipeName, req.session.DBuserID,callback);
                }
           ], function(err,results){
                if(!err)
                console.log('results: '+results)
                if(results==null){
                    var connection = connect_to_sql();
       
                    var sql = 'insert into user_recipes (user_id, recipe_name, create_date, instructions) values (' + req.session.DBuserID + ',\''+req.body.recipeName+'\',NOW(),'+'\''+req.body.message+'\')';
              

                    connection.query(sql, function(err, rows, fields) {
                      if (!err){
                        var rec_id;
                        var calories =0;
                        async.waterfall
                            ([  
                                function (callback)
                                {
                                   rec_id = get_recipe_id(req.body.recipeName, req.session.DBuserID,callback);
                                   
                                }
                                ,  
                                function (rec_id,callback)
                                {
                                    var i;
                                    
                                    for(i=0;i<req.body.counter;i+=3){
                                        
                                        get_ingr_id(rec_id, req.body['element'+i] ,i, callback );
                                    }
                                },  
                                function (ingr_id, name, recipe_id, counter, callback)
                                {
                                    console.log('ingr id: ' +name+ ' '+ingr_id+' '+recipe_id+' '+counter+''+req.body['element'+(2+counter)]);
                                    insert_ingredient(recipe_id, ingr_id, name, req.body['element'+(counter+1)], req.body['element'+(2+counter)],counter,callback );
                                },
                                function(recID,count, cals, callback){
                                    
                                    async.waterfall([
                                    function(callback2){
                                        calories+=cals;
                                        callback2();
                                    },
                                    function(callback2){
                                        if(count >=req.body.counter-3 )
                                        callback(null,recID);
                                        callback2();
                                    }]);
                                    
                                }
                            ]
                            ,
                            function(err,results) 
                            {
                                if(!err){
                                    console.log('Updating Calories:')
                                    update_calories(results, calories);
                                    console.log(calories);
                                }
                                else
                                console.log('Async error: '+err);
                                
                            });
                     
                        
                       
                        req.session.lastMessage = 'Your recipe was successfully added!';
                        res.render('profile.ejs', {
                            user : req.user, // get the user out of session and pass to template
                            session: req.session
                        });
                        
                      }
                      
                      else{
                        console.log('Error while inserting recipe ' + err);
                        req.session.lastMessage = 'Error while adding recipe';
                        res.render('profile.ejs', {
                            user : req.user, // get the user out of session and pass to template
                            session: req.session
                        });
                      }
                    });
                    
                
                    connection.end();        
                }
                else{
                    req.session.lastMessage = 'Recipe name already exists, please try again';
                    res.render('profile.ejs', {
                        user : req.user, // get the user out of session and pass to template
                        session: req.session
                    });
                }
               
           });
            
    });

};


function update_calories(rec_id, calories){
    var connection = connect_to_sql();
    var sql = 'update user_recipes set calories = '+calories+' WHERE recipe_id = '+rec_id;
    console.log(sql);
    connection.query(sql, function(err, rows, fields) {
          if (!err){
            console.log('calories added successfully')
          }
          else
            
            console.log('Error updating calories' + err);
    });
    connection.end();
}


function containsAll(arrays){//Assumes that we are dealing with an array of arrays of integers
  var currentValues = {};
  var commonValues = {};
  for (var i = arrays[0].length-1; i >=0; i--){//Iterating backwards for efficiency
    currentValues[arrays[0][i]] = 1; //Doesn't really matter what we set it to
  }
  for (var i = arrays.length-1; i>0; i--){
    var currentArray = arrays[i];
    for (var j = currentArray.length-1; j >=0; j--){
      if (currentArray[j] in currentValues){
        commonValues[currentArray[j]] = 1; //Once again, the `1` doesn't matter
      }
    }
    currentValues = commonValues;
    commonValues = {};
  }
  return Object.keys(currentValues).map(function(value){
    return parseInt(value);
  });
}

function search_ingredient(count,name, cals, callback){
    
    var connection = connect_to_sql();
    var sql = 'select user_recipes.recipe_id from food_ingredients JOIN user_recipes on user_recipes.recipe_id=food_ingredients.recipe_id where calories < '+cals+ ' AND ing_name LIKE \'\%'+name.toLowerCase()+'\%\'';
    console.log(sql);
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             var ids  = [];
             for(var i=0;i<rows.length;i++){
                 ids.push(rows[i].recipe_id);
             }
             callback(null,count,ids);
          }
          else
            
            console.log('Error searching for ingredient' + err);
    });
    connection.end();
}

function delete_allergens(user_id,callback){
    
    var connection = connect_to_sql();
    var sql = 'delete from allergens where user_id = '+user_id;
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             console.log('allergens deleted');
             callback();
          }
          else
            
            console.log('Error deleting allergen' + err);
    });
    connection.end();   
}

function get_allergens( user_id, callback){
    
    var connection = connect_to_sql();
    var sql = 'select name from allergens where user_id = '+user_id;
    var results =[];
    console.log(sql);
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             console.log('allergens found');
             for(var i=0;i<rows.length;i++){
                results.push(rows[i].name);
                console.log(rows[i]);
             }
            
            console.log(results);
            callback(null, results);
             
          }
          else
            
            console.log('Error retrieving allergens' + err);
    });
    connection.end();   
    
}


function insert_allergen(allergen, user_id){
    
    var connection = connect_to_sql();
    var sql = 'insert into allergens (name,user_id) values (\''+ allergen+'\','+user_id+')';
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             console.log('allergen inserted successfully');
            
          }
          else
            
            console.log('Error inserting allergen' + err);
    });
    connection.end();   
}

function get_recipe_id( name, user, callback){
            
    var connection1 = connect_to_sql();
    var sql = 'select recipe_id from user_recipes where recipe_name = \'' + name + '\' AND user_id = ' + user ;
    connection1.query(sql, function(err, rows, fields) {
          if (!err){
            if(rows[0]){
                console.log('id:' +rows[0].recipe_id);
                if(callback)
                callback(null,rows[0].recipe_id);
               
            }
           
            else if(callback) callback(null,null);
            
          }
          else
            console.log('Error retrieving recipe ID' + err);
    });
    connection1.end();        
}

function get_ingr_id(recipe_id, ingr_name, count, callback){
    
    var connection = connect_to_sql();
    var name = ingr_name.toLowerCase();
    var sql = 'select ingr_id from ingredients where name = \'' + name + '\'';
    
    connection.query(sql, function(err, rows, fields) {
                  if (!err){
                    if(rows[0]){
                        console.log('ingr_id found:' +rows[0].ingr_id);
                        callback(null, rows[0].ingr_id,ingr_name,recipe_id,count);
                    }
                   
                    else {
                        console.log('ingr_id not found, creating one now.');
                        var connection2 = connect_to_sql();
                        var sql2 = 'insert into ingredients(name) values (\''+ingr_name+'\')';
                        connection2.query(sql2, function(err, rows, fields) {
                              if (!err){
                                  get_ingr_id(recipe_id,ingr_name, count, callback);
                              }
                              else
                                  console.log('Error inserting ingredient into database' + err);
                                  
                        });
                        connection2.end();
                    }
                  }
                  else
                    console.log('Error retrieving ingredient id: ' + err);
                    
            });
    connection.end();
}
    
function insert_ingredient(recipe_id, ingr_id, name, measure, unit, counter, callback){
    var connection = connect_to_sql();
    var sql ='insert into food_ingredients (recipe_id,ingredient_id, ing_name,measure,unit) values ('+recipe_id+','+ingr_id+',\''+name+'\','+measure+',\''+unit+'\')';
    async.waterfall(
    [
        function(callback1) {
            connection.query(sql, function(err, rows, fields) {
              if (!err){
                console.log('ingredient inserted successfully');
                callback1();
              }
              else
            console.log('Error inserting into food_ingredients' + err);
            });
        },
        function(callback1) {
             get_calories(name,measure,unit,callback1);
        }],
        function(err,cals){
            if(!err){
             connection.end();
             console.log('insert done' + cals);
             callback(null, recipe_id,counter, cals);
            }
            else
            console.log('error');
        }
        
    
    );

   
   
    
}

function get_calories(name,measure,unit,callback1){
    var request = require("request");
	var cheerio = require("cheerio");
	var url = 'https://www.google.com/search?q=how+many+calories+in+'+measure+'+'+unit+'+of+'+name;
	console.log(url);
    request(url, function (error, response, body) {
    	if (!error) {
    		var $ = cheerio.load(body);
    		var $body = $('body');
    		var cals = $('div._Oqb').text();
    		var int = parseInt(cals);
    		console.log('scraped cals: '+int);
    		callback1(null,int);
        	}
        else {
    		   console.log("We’ve encountered an error: " + error);
	    }
    });
}

function connect_to_sql (){
          var mysql      = require('mysql');
          var connection = mysql.createConnection({
          host     : 'localhost',
          user     : 'team',
          password : 'password',
          database : 'smartchef'
        });
        
        connection.connect(); 
        
        return connection;
    
}    
    
function get_messages( user_id, callback){
    
    var connection = connect_to_sql();
    var sql = 'select * from messages where to_id = '+user_id;
    var results =[];
    console.log(sql);
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             console.log('messages found');
             for(var i=0;i<rows.length;i++){
                results.push(rows[i]);  //results[i].from, results[i].to, results[i].message, results[i].time
                console.log(rows[i]);
             }
            
            console.log(results);
            callback(null, results);
             
          }
          else
            
            console.log('Error retrieving messages' + err);
    });
    connection.end();   
    
}

function get_outgoing_messages( user_id, callback){
    
    var connection = connect_to_sql();
    var sql = 'select * from messages where from_id = '+user_id;
    var results =[];
    console.log(sql);
    connection.query(sql, function(err, rows, fields) {
          if (!err){
             console.log('messages found');
             for(var i=0;i<rows.length;i++){
                results.push(rows[i]);
                console.log(rows[i]);
             }
            
            console.log(results);
            callback(null, results);
             
          }
          else
            
            console.log('Error retrieving messages' + err);
    });
    connection.end();   
    
}
    
// route middleware to make sure a user is logged in
function isLoggedIn(req, res, next) {

    // if user is authenticated in the session, carry on 
    if (req.isAuthenticated())
        return next();

    // if they aren't redirect them to the home page
    res.redirect('/');
}



