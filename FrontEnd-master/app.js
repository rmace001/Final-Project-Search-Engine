

var express = require("express");
var bodyParser = require('body-parser');
var path = require('path');
var app = express();
var elasticsearch = require('elasticsearch');
 var elasticClient = new elasticsearch.Client({
   hosts: 'http://rogith:%5Finalproject@127.0.0.1:9200/'

 });
module.exports = elasticClient;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extend: true}));

elasticClient.ping({
  requestTimeout: 30000,
}, function(error){
  if (error){
    console.error('elasticsearch is down');
  } else {
    console.log('all is well');
  }
});

//view engine
app.set('view engine','ejs');
app.set('views',path.join(__dirname,'views'));

// bodyParser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extend:true}));

// Results
var hits = [];
var pages = [];


// static path
app.use(express.static(path.join(__dirname,'public')));

app.get("/",function(req,res){
  //res.send("homePage yall");

  res.render("s",{ pages:pages });
});

app.post("/search",function(req,res){
  //testing output
  console.log(req.body.query);
  var str = req.body.query;
  //query.web_title=str;
  //res.render("s",{ pages:pages });
  //below is for testing when lucne is properly loaded
  elasticClient.search({
      index: 'webdocs',
      type: 'webdoc',
      body:{
        query: {
            match: {"title": str}
        },
        highlight: {
            fields: {
                
                title: {}
            }
        }
      }

  }).then(function (resp){
      hits = resp.hits.hits;

      res.render("s",{ pages:hits});

     console.log(hits);
     },function (err) {
         console.trace(err.message);
      });

  console.log("searched");

});


app.listen(3000, function(){
  console.log("server is on port 3000");
});
