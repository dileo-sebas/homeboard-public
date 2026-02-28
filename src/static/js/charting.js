// import { Colors } from 'chart.js';

// Chart.register(Colors);


var chart_data = [];

ws = new WebSocket("ws://localhost:8000/homecomms");
ws.onmessage = (data) => {
  var rawData = data.data;
  console.log(rawData)
  var splitData = rawData.split(" ")

  var temperatureData = {}
  temperatureData.datetime = splitData[1] + " " + splitData[2];
  temperatureData.temperature = splitData[3];
  addData(temperature_chart, temperatureData.datetime, parseFloat(temperatureData.temperature));
};

const options = {
  scales: {
    y: {
      suggestedMin: 20,
      suggestedMax: 50
    }
  }
};



var temperature_chart = new Chart(
  document.getElementById('temperatures'),
  {
    type: 'line',
    data: {
      labels: chart_data.map(row => row.datetime),
      datasets: [
        {
          label: 'Temperatures (°C)',
          data: chart_data.map(row => row.temperature),
          borderColor: "rgba(248, 112, 0, 1)",
          backgroundColor: 'rgba(244, 131, 37, 1)',
        }
      ]
    },
    options
  },
);

function addData(chart, label, newData) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset) => {
      dataset.data.push(newData);
  });

  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
  });
  }

  chart.update();
}