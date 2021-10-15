const port = 3000;

var express = require('express');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');
var app = express();

app.set('view engine', 'ejs');
app.use(express.static(__dirname+'/public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
app.use(methodOverride('_method'));


// 라우터 설정파일 호출
var router = require('./routes/home');

// 주소가 / 로 시작하면 ./routes/home.js 호출하라는 의미
app.use('/', router);

/*
// Router 안 쓸 경우
app.get('/', function(req, res) {
    res.render('./home/welcome');
});

app.get('/about', function(req, res) {
    res.render('./home/about');
});
*/

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});