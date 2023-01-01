// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// function used to get the data we need for our pie. which is in our index.html
function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
}

var jsonData = loadJson('#jsonData')
var amountIn = jsonData.percentageIn
var tickers = jsonData.tickers

// Pie Chart Example
var ctx = document.getElementById("myPie");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: tickers,
    datasets: [{
      data: amountIn,
      backgroundColor: [
        '#3E5435', '#9AC791', '#8ABD91', '#228B22', '#008000', '#097969', '#AFE1AF', 
        '#50C878', '#5F8575', '#355E3B', '#2AAA8A', '#007bff', '#dc3545', '#ffc107', 
        '#28a745'],
    }],
  },
});
