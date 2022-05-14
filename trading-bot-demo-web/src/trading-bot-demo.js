// ------------- START OF MY CODE --------------- //
/**
 * Npm modules required:
 * 1) node-fetch: "npm install node-fetch@2"
 * 2) cryptocompare: "npm install --save cryptocompare"
 * 3) chart.js: "npm install chart.js"
 * 4) chartjs-plugin-zoom: "npm install chartjs-plugin-zoom"
 */

import { coinList } from "./extra-data.js";
import { colors } from "./extra-data.js";
import { Chart, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
Chart.register(zoomPlugin);

 if (global == undefined) {
  var global = window;
}
global.fetch = require('node-fetch');
import cc from 'cryptocompare';
cc.setApiKey('76a059bd9813c0c3e678799f86f22cf562bc1f27ac993640c300212678377184'); // this is my api key from cryptocompare, it is free so I don't mind sharing this

const runToggle = document.querySelector(".run-button");
var crypto, currency, gap, money, fromDate, toDate, timeRangeDayChecked, 
timeRangeHourChecked, timeRangeMinuteChecked, moLossPerc, difDays; 


// initializes chart
Chart.register(...registerables);
var labels = [];
var data = {
labels: labels,
datasets: []
};
var assetPriceChartConfig = {
type: 'line',
data: data,
options: {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  stacked: false,
  plugins: {
    zoom: {
      zoom: {
        wheel: {
          enabled: true,
        },
        pinch: {
          enabled: true
        },
        mode: 'xy',
      }
    },
    title: {
      display: true,
      text: 'Asset Price and Orders'
    }
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
    },
    y1: {
      type: 'linear',
      display: true,
      position: 'right',

      // grid line settings
      grid: {
        drawOnChartArea: false, // only want the grid lines for one axis to show up
      },
    },
  }
},
};
var valuePriceChartConfig = {
  type: 'line',
  data: data,
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      zoom: {
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true
          },
          mode: 'xy',
        }
      },
      title: {
        display: true,
        text: 'Value Chart'
      }
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
  
        // grid line settings
        grid: {
          drawOnChartArea: false, // only want the grid lines for one axis to show up
        },
      },
    }
  },
  };

// renders the chart
var assetPriceChart = new Chart(
  document.querySelector(".asset-price-chart"), 
  assetPriceChartConfig);
var valuePriceChart = new Chart(
  document.querySelector(".value-price-chart"), 
  valuePriceChartConfig);

// gets all input data from user and formats it. Also calculate difference in days
function getData () {
  crypto = document.querySelector(".crypto-input").value;
  currency = document.querySelector(".currency-input").value;
  gap = Number(document.querySelector(".gap-input").value);
  money = Number(document.querySelector(".money-input").value);
  fromDate = document.querySelector(".from-date-input").value;
  toDate = document.querySelector(".to-date-input").value;
  timeRangeDayChecked = document.querySelector(".time-range-day-button").checked; 
  timeRangeHourChecked = document.querySelector(".time-range-hour-button").checked;
  timeRangeMinuteChecked = document.querySelector(".time-range-minute-button").checked;
  moLossPerc = Number(document.querySelector(".moloss-input").value);
}

function getHistPrice () {
  const toDateTimestamp = Math.floor(toDate.getTime()/1000);
  if (timeRangeDayChecked) {
    return cc.histoDay(crypto, currency, {timestamp: toDate, limit: difDays})
    .then(data => {
      return data;
    })
    .catch(console.error)
    .then(data => {
      let priceList = data.map(obj => { 
        let time = new Date(obj.time*1000);
        let close = obj.close;
        return {"time": time.toLocaleDateString(), "price": close} });
      return priceList})
      .catch(console.error)
  }
  else if (timeRangeHourChecked) {
    var difHours = difDays*24;
    return cc.histoDay(crypto, currency, {timestamp: toDate, limit: difHours})
    .then(data => {
      return data;
    }).then(data => {
      let priceList = data.map(obj => { 
        let time = new Date(obj.time*1000);
        let close = obj.close;
        return {"time": time.toLocaleDateString(), "price": close} });
      return priceList})
      .catch(console.error)
    .catch(console.error);
  }
  else if (timeRangeMinuteChecked) {
    var difMinutes = difDays*24*60;
    return cc.histoDay(crypto, currency, {timestamp: toDate, limit: difMinutes})
    .then(data => {
      return data;
    }).then(data => {
      let priceList = data.map(obj => { 
        let time = new Date(obj.time*1000);
        let close = obj.close;
        return {"time": time.toLocaleDateString(), "price": close} });
      return priceList})
      .catch(console.error)
    .catch(console.error);
  }
};

function checkInputValid() {
let valid = true;
if (!crypto) {
  document.querySelector(".crypto-input-check").innerHTML = "Enter a crypto ticker";
  valid = false;
}
else {
  if (!(crypto in coinList)) {
    document.querySelector(".crypto-input-check").innerHTML = "Cryto ticker does not exist";
    valid = false
  }
  else {
    document.querySelector(".crypto-input-check").innerHTML = "";
  } 
}
if (!currency) {
  document.querySelector(".currency-input-check").innerHTML = "Enter a currency ticker";
  valid = false;
}
else {
  document.querySelector(".currency-input-check").innerHTML = "";
}
if (!gap) {
  document.querySelector(".gap-input-check").innerHTML = "Enter a number";
  valid = false;
}
else {
  document.querySelector(".gap-input-check").innerHTML = "";
}
if (!money) {
  document.querySelector(".money-input-check").innerHTML = "Enter a number";
  valid = false;
}
else {
  document.querySelector(".money-input-check").innerHTML = "";
}
if (!fromDate) {
  document.querySelector(".from-date-input-check").innerHTML = "Enter a date";
  valid = false;
}
else {
  fromDate = fromDate.split("-");
  fromDate = new Date(fromDate[0], fromDate[1]-1, fromDate[2]);
  document.querySelector(".from-date-input-check").innerHTML = "";
}
if (!toDate) {
  document.querySelector(".to-date-input-check").innerHTML = "Enter a date";
  valid = false;
}
else {
  toDate = toDate.split("-");
  toDate = new Date(toDate[0], toDate[1]-1, toDate[2]);
  document.querySelector(".to-date-input-check").innerHTML = "";
}
if (toDate && fromDate) {
  difDays = (toDate.getTime() - fromDate.getTime())/86400000
}
if (difDays<0){ // ensures end date is later than start date
  let errorText = "Invalid date input";
  document.querySelector(".from-date-input-check").innerHTML = errorText;
  document.querySelector(".to-date-input-check").innerHTML = errorText;
  valid = false;
}
else if (toDate && fromDate) {
  document.querySelector(".from-date-input-check").innerHTML = "";
  document.querySelector(".to-date-input-check").innerHTML = "";
}
if (!timeRangeDayChecked && !timeRangeHourChecked && !timeRangeMinuteChecked) {
  document.querySelector(".time-range-input-check").innerHTML = "Choose a time range";
  valid = false;
}
else {
  if (timeRangeDayChecked && difDays>1999) {
    let errorText = "Excceeds limit";
    document.querySelector(".from-date-input-check").innerHTML = errorText;
    document.querySelector(".to-date-input-check").innerHTML = errorText;
    valid = false
  }
  else if (timeRangeHourChecked && difDays>83) {
    let errorText = "Excceeds limit";
    document.querySelector(".from-date-input-check").innerHTML = errorText;
    document.querySelector(".to-date-input-check").innerHTML = errorText;
    valid = false
  }
  else if (timeRangeMinuteChecked && difDays>1) {
    let errorText = "Excceeds limit";
    document.querySelector(".from-date-input-check").innerHTML = errorText;
    document.querySelector(".to-date-input-check").innerHTML = errorText;
    valid = false
  }
  else {
    document.querySelector(".from-date-input-check").innerHTML = "";
    document.querySelector(".to-date-input-check").innerHTML = "";
    document.querySelector(".time-range-input-check").innerHTML = "";
  }
}
if (!moLossPerc) {
  document.querySelector(".moloss-input-check").innerHTML = "Enter a number/decimal";
  valid = false;
}
else if (moLossPerc>100) {
  document.querySelector(".moloss-input-check").innerHTML = "Value cannot exceed 100";
  valid = false;
}
else {
  moLossPerc /= 100;
  document.querySelector(".moloss-input-check").innerHTML = "";
}
return valid
}

function runTradingBot(priceList) {
  var curCurrencyAmount = money;
  var totalAssetValue = money;
  var initAssetAmt, curAssetAmt, curAssetValue = 0.0;
  var buyPrice, sellPrice = NaN; 
  var bought, sold = false;
  var firstOrder = true;
  var totalValueArr = [];
  var sellPricesArr = [];
  var buyPricesArr = [];
  var totalValueWithoutBotArr = [];
  var minVal = Number.POSITIVE_INFINITY;
  var maxVal = Number.NEGATIVE_INFINITY;

  // simulates execution of market orders
  function marketOrder(side, curPrice) {
    if (side == "buy") {
      curCurrencyAmount *= (1-moLossPerc);
      curAssetAmt = curCurrencyAmount/curPrice;
      curCurrencyAmount = 0;
      curAssetValue = curAssetAmt*curPrice;
      totalAssetValue = curCurrencyAmount + curAssetValue;
    }
    else if (side == "sell") {
      curAssetAmt *= (1-moLossPerc);
      curCurrencyAmount = curAssetAmt*curPrice;
      curAssetAmt = 0;
      curAssetValue = 0;
      totalAssetValue = curCurrencyAmount + curAssetValue
    }
  }

  // main trading bot algorithm
  priceList.forEach((price) => {
    if (firstOrder) {
      marketOrder("buy", price);
      initAssetAmt = curAssetAmt;
      firstOrder = false;
      sellPrice = price - gap;
      bought = true;
    }
    else if (bought) {
      curAssetValue = price*curAssetAmt;
      totalAssetValue = curCurrencyAmount + curAssetValue;
      if (price <= sellPrice) {
        marketOrder("sell", price);
        buyPrice = sellPrice;
        sellPrice = NaN;
        bought = false;
        sold = true;
      }
      else if ((price - sellPrice) > gap) {
        sellPrice = price - gap
      }
    }
    else if (sold) {
      if (price >= buyPrice) {
        marketOrder("buy", price);
        sellPrice = buyPrice;
        buyPrice = NaN;
        bought = true;
        sold = false;
      }
      else if ((buyPrice - price) > gap) {
        buyPrice = price + gap;
      }
    }
    let curMin = Math.min(totalAssetValue, initAssetAmt*price);
    let curMax = Math.max(totalAssetValue, initAssetAmt*price);
    if (curMin < minVal) {
      minVal = curMin;
    }
    if (curMax > maxVal) {
      maxVal = curMax;
    }
    totalValueWithoutBotArr.push(initAssetAmt*price);
    totalValueArr.push(totalAssetValue);
    sellPricesArr.push(sellPrice);
    buyPricesArr.push(buyPrice);
  })
  return [totalValueArr, totalValueWithoutBotArr, sellPricesArr, buyPricesArr, minVal, maxVal];
}

function checkValidCoinPair (result) {
  if (!result) {
    document.querySelector(".currency-input-check").innerHTML = "This is not a valid coin pair";
    document.querySelector(".crypto-input-check").innerHTML = "This is not a valid coin pair";
    return false;
  }
  else {
    document.querySelector(".currency-input-check").innerHTML = "";
    document.querySelector(".crypto-input-check").innerHTML = "";
    return true;
  }
}

// deletes old canvas and replaces it with a new, blank one
function resetCanvases () {
  document.querySelector(".asset-price-chart").remove();
  document.querySelector(".asset-price-chart-container").innerHTML = '<canvas class="asset-price-chart"></canvas>';
  document.querySelector(".value-price-chart").remove();
  document.querySelector(".value-price-chart-container").innerHTML = '<canvas class="value-price-chart"></canvas>';
}

runToggle.addEventListener('click', async function () {
  getData(); // retrieves input from user
  if (!checkInputValid()) {return}
  //console.log(typeof(crypto), typeof(currency), typeof(gap), typeof(money), typeof(fromDate), typeof(toDate), typeof(difDays), typeof(timeRangeDayChecked), typeof(timeRangeHourChecked), typeof(timeRangeMinuteChecked), typeof(moLossPerc));
  let timePriceList = await getHistPrice(); // retrieves historical data from cryptocompare
  if (!checkValidCoinPair(timePriceList)) {return}
  let timeList = timePriceList.map(data => data.time);
  let priceList = timePriceList.map(data => data.price);

  // running trading bot
  let buyPrices, sellPrices, totalValueWithBot, totalValueWithoutBot, minVal, maxVal;
  [totalValueWithBot, totalValueWithoutBot, sellPrices, buyPrices, minVal, maxVal] = runTradingBot(priceList);

  // charts data
  let yAxisMin = minVal*0.9
  let yAxisMax = maxVal*1.1
  labels = timeList;
  var assetPriceChartData = {
    labels: labels,
    datasets: [
      {
        label: "Cryptocurrency Price",
        data: priceList,
        borderColor: colors.yellow,
        backgroundColor: colors.yellowTp,
        yAxisID: 'y1',
      },
      {
        label: 'Buy Price Orders',
        data: buyPrices,
        borderColor: colors.green,
        backgroundColor: colors.greenTp,
        yAxisID: 'y2',
      },
      {
        label: 'Sell Price Orders',
        data: sellPrices,
        borderColor: colors.red,
        backgroundColor: colors.redTp,
        yAxisID: 'y3',
      },
    ]
  };
  assetPriceChartConfig = {
    type: 'line',
    data: assetPriceChartData,
    options: {
      maintainAspectRatio: false,
      scales: {
        display: true,
      },
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      plugins: {
        zoom: {
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true
            },
            mode: 'xy',
          }
        },
        title: {
          display: false,
          text: 'Asset Price and Orders'
        }
      },
      scales: {
        y1: {
          type: 'linear',
          display: true,
          position: 'left',
        },
        y2: {
          type: 'linear',
          display: false,
          position: 'right',
  
          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
        y3: {
          type: 'linear',
          display: false,
          position: 'right',
  
          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        }
      }
    }
  };
  var valuePriceChartData = {
    labels: labels,
    datasets: [
      {
        label: 'Total Value Without Trading Bot',
        data: totalValueWithoutBot,
        borderColor: colors.orange,
        backgroundColor: colors.orangeTp,
        yAxisID: 'y1',
      },
      {
        label: 'Total Value With Trading Bot',
        data: totalValueWithBot,
        borderColor: colors.purple,
        backgroundColor: colors.purpleTp,
        yAxisID: 'y2',
      },
    ]
  };
  valuePriceChartConfig = {
    type: 'line',
    data: valuePriceChartData,
    options: {
      maintainAspectRatio: false,
      scales: {
        display: true,
      },
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      plugins: {
        zoom: {
          zoom: {
            wheel: {
              enabled: true,
            },
            pinch: {
              enabled: true
            },
            mode: 'xy',
          }
        },
        title: {
          display: false,
          text: 'Value Chart'
        }
      },
      scales: {
        y1: {
          type: 'linear',
          display: true,
          min: yAxisMin,
          max: yAxisMax,
          position: 'left',
        },
        y2: {
          type: 'linear',
          display: false,
          min: yAxisMin,
          max: yAxisMax,
          position: 'right',
  
          // grid line settings
          grid: {
            drawOnChartArea: false, // only want the grid lines for one axis to show up
          },
        },
      }
    },
  };
  // deletes old chart and draws new chart
  resetCanvases();
  assetPriceChart = new Chart(
    document.querySelector(".asset-price-chart"),
    assetPriceChartConfig
  );
  valuePriceChart = new Chart(
    document.querySelector(".value-price-chart"), 
    valuePriceChartConfig);
});

// to reset zoom. Basically recreates the chart
document.querySelector(".asset-price-chart-reset-zoom-button").onclick = () => {
  assetPriceChart.resetZoom();
}
  

// ------------- END OF MY CODE --------------- //