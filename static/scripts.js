
google.charts.load('current', { packages: ['corechart'] });
google.charts.setOnLoadCallback(drawChart);

var wgt = window.wgt;
wgt.unshift(['Date', 'Weight']);

function drawChart() {

    function convertToKg(data) {
        for (var i = 0; i < data.getNumberOfRows(); i++) {
            for (var j = 0; j < data.getNumberOfColumns(); j++) {
                // check if the current column is the "Weight" column
                if (data.getColumnLabel(j) === "Weight") {
                    // get the current weight value in lbs
                    var lbsValue = data.getValue(i, j);

                    // convert the weight value from lbs to kg
                    var kgValue = lbsValue * 0.453592;

                    // update the weight value in the DataTable
                    data.setValue(i, j, kgValue);
                }
            }
        }
    };
      
    function convertToLbs(data) {
        for (var i = 0; i < data.getNumberOfRows(); i++) {
            for (var j = 0; j < data.getNumberOfColumns(); j++) {
                // check if the current column is the "Weight" column
                if (data.getColumnLabel(j) === "Weight") {
                    // get the current weight value in kg
                    var kgValue = data.getValue(i, j);

                    // convert the weight value from kg to lbs
                    var lbsValue = kgValue / 0.453592;

                    // update the weight value in the DataTable
                    data.setValue(i, j, lbsValue);
                }
            }
        }
    };

    // Set Data
    var data = google.visualization.arrayToDataTable(wgt);

    var unit = 'lbs'; // Default unit is lbs

    var options = {
        titlePosition: 'none',
        hAxis: {
            textStyle: {
                color: '#01579b',
                fontSize: 10,
                fontName: 'Arial',
                bold: true,
                italic: true
            },
        },
        vAxis: {
            title: 'Weight (' + unit + ')',
            textStyle: {
                color: '#1a237e',
                fontSize: 24,
                bold: true
            },
            titleTextStyle: {
                color: '#1a237e',
                fontSize: 24,
                bold: true
            }
        },
        legend: 'none'
    };

    var lbsRadio = document.querySelector('input[name="unit"][value="lbs"]');
    var kgRadio = document.querySelector('input[name="unit"][value="kg"]');
    
    lbsRadio.addEventListener('change', function() {
        unit = 'lbs';
        options.vAxis.title = 'Weight (' + unit + ')';
        convertToLbs(data);
        chart.draw(data, options);
        weightDisplay.textContent = `Your latest weight is ${window.wgt.slice(-1)[0][1]} lbs!`;
    });
    
    kgRadio.addEventListener('change', function() {
        unit = 'kg';
        options.vAxis.title = 'Weight (' + unit + ')';
        convertToKg(data);
        chart.draw(data, options);
        weightDisplay.textContent = `Your latest weight is ${Math.round(data.getValue((data.getNumberOfRows()-1), 1) * 10) / 10} kg!`;
    });

    // get the h3 element to update
    const weightDisplay = document.querySelector('.jumbotron h3');

    // Draw Chart
    var chart = new google.visualization.LineChart(document.getElementById('myChart'));
    chart.draw(data, options);
};