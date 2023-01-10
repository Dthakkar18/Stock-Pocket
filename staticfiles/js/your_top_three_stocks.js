// function used to get the data we need for our pie. which is in our index.html
function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

var jsonData = loadJson('#topThreePricesJsonData')
var prices = jsonData.top_three_price_changes
var first_stock = document.getElementById("first_best_stock")
var second_stock = document.getElementById("second_best_stock")
var third_stock = document.getElementById("third_best_stock")
if(prices[0] > 0){
    first_stock.style.borderColor = "green";
}else{
    first_stock.style.borderColor = "red";
}
if(prices[1] > 0){
    first_stock.style.borderColor = "green";
}else{
    first_stock.style.borderColor = "red";
}
if(prices[2] > 0){
    first_stock.style.borderColor = "green";
}else{
    first_stock.style.borderColor = "red";
}
