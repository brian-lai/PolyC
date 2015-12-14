import mongoose

/*
* Script to read new users from file, parse, create JSON -> dump into MongoDB user_profiles collection
*/

var mongoose = require('mongoose');   // Extract the mongoose, and call constructor

var db = mongoose.connection;     // Open up a connection with Mongo-DB

db.on('error', console.error);
db.once('open', function() {
  // Creating the schema and the model for the user-Profile
  var userProfile = new mongoose.Schema({
    name : {type: String},
    political_party : {type: String},
    short_bio : {type : String},
    
  })

})

mongoose.connect('mongodb://localhost/test')
