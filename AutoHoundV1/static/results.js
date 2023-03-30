function downloadCSV() {
    const tableData = [];
    const rows = document.querySelectorAll('#car-data tbody tr');
    const headers = [];
    document.querySelectorAll('#car-data thead th').forEach(header => {
      headers.push(header.innerText);
    });
    tableData.unshift(headers.join(','));
    rows.forEach(row => {
      const rowData = [];
      row.querySelectorAll('td').forEach(cell => {
        rowData.push(cell.innerText);
      });
      tableData.push(rowData.join(','));
    });
    const csvContent = 'data:text/csv;charset=utf-8,' + tableData.join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'car_data.csv');
    document.body.appendChild(link);
    link.click();
  }

 // Get the car data from the Flask app
const carData = {{ car_data_list | safe }};
// Create an object to store the average price by year
const averagePriceByYear = {};
// Loop through the car data and calculate the average price for each year
carData.forEach((car) => {
  if (!averagePriceByYear[car.year]) {
    averagePriceByYear[car.year] = {
      count: 0,
      total: 0,
      average: 0,
    };
  }
  averagePriceByYear[car.year].count += 1;
  averagePriceByYear[car.year].total += Number(car.price);
});
Object.keys(averagePriceByYear).forEach((year) => {
  averagePriceByYear[year].average =
    averagePriceByYear[year].total / averagePriceByYear[year].count;
});
// Create an array of objects with the year and average price for each year
const chartData = Object.keys(averagePriceByYear).map((year) => ({
  year: year,
  price: averagePriceByYear[year].average,
}));
// Sort the chart data by year in descending order
chartData.sort((a, b) => b.year - a.year);
// Get the canvas element for the chart
const ctx = document.getElementById('chart').getContext('2d');
// Create the chart
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: chartData.map((data) => data.year),
    datasets: [
      {
        label: 'Average Price by Year',
        data: chartData.map((data) => data.price),
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function (value, index, values) {
            return 'R' + value.toLocaleString();
          },
        },
      },
    },
    plugins: {
      legend: {
        labels: {
          color: 'black' // set the color of the legend labels
        }
      }
    }
  },
});

function toggleTable() {
  const table = document.getElementById('car-data');
  if (table.style.display === 'none') {
    table.style.display = 'table';
  } else {
    table.style.display = 'none';
  }
}

// slope trendline

