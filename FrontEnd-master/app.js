var d3 = require("d3"),
    cloud = require("../");

var layout = cloud()
    .size([500, 500])
    .words([
      "Hello", "world", "normally", "you", "want", "more", "words",
      "than", "this"].map(function(d) {
      return {text: d, size: 10 + Math.random() * 90, test: "haha"};
    }))
    .padding(5)
    .rotate(function() { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .fontSize(function(d) { return d.size; })
    .on("end", draw);

layout.start();

function draw(words) {
  d3.select("body").append("svg")
      .attr("width", layout.size()[0])
      .attr("height", layout.size()[1])
    .append("g")
      .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
    .selectAll("text")
      .data(words)
    .enter().append("text")
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Impact")
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });
}





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
