// Load Google Charts library with corechart and controls packages
google.charts.load('current', { packages: ['corechart', 'controls'] });

// Call drawChart function once Google Charts library is loaded
google.charts.setOnLoadCallback(drawChart);

// Get weight data from window object
var wgt = window.wgt;
var ath = window.ath;
wgt.sort((a, b) => {
    const dateA = new Date(a[0]);
    const dateB = new Date(b[0]);
    return dateA - dateB;
});
var last_weight = wgt[wgt.length - 1][1];
var old_date;
var old_weight;
var date;

// Get the HTML element for result display
const resultDisplay = document.getElementById('btn-result');

// Get the HTML element for weight display
const weightDisplay = document.querySelector('.jumbotron h3');

// Draw the chart using Google Charts library
function drawChart() {
    
    // Set Data
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Weight');
    data.addRows(wgt);

    var unit = 'lbs'; // Default unit is lbs

    // Create a dashboard to bind the chart and the filter
    var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

    // Set up the date range filter
    var dateRangeSlider = new google.visualization.ControlWrapper({
        'controlType': 'DateRangeFilter',
        'containerId': 'filter_div',
        'options': {
          'filterColumnLabel': 'Date',
          'ui': {
            'labelStacking': 'vertical',
            'format': {
              'pattern': 'MMM dd YYYY'
            }
          }
        }
    });
    
    // Function to convert weight data from lbs to kg
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
                    data.setValue(i, j, kgValue.toFixed(1));
                }
            }
        }
    };
    
    // Function to convert weight data from kg to lbs
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
                    data.setValue(i, j, lbsValue.toFixed(1));
                }
            }
        }
    };

    // Create an options object for the chart
    var options = {
        titlePosition: 'none',
        height: 500,
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
                fontSize: 15,
                bold: true
            },
            titleTextStyle: {
                color: '#1a237e',
                fontSize: 15,
                bold: true
            }
        },
        legend: 'none'
    }

    // Create a chart wrapper object with the options
    var chart = new google.visualization.ChartWrapper({
        'chartType': 'LineChart',
        'containerId': 'chart_div',
        'options': options,
        'view': {'columns': [0,1]}
    });

    // Get the radio buttons for the weight unit selection
    var lbsRadio = document.querySelector('input[name="unit"][value="lbs"]');
    var kgRadio = document.querySelector('input[name="unit"][value="kg"]');
    
    // Add event listener for the lbs radio button
    lbsRadio.addEventListener('change', function() {
        unit = 'lbs';
        convertToLbs(data);
        latestWeight = window.wgt.slice(-1)[0][1];
        weightDisplay.textContent = `Your latest weight is ${latestWeight} lbs!`;
        options.vAxis.title = 'Weight (' + unit + ')';
        dashboard.draw(data);
    });
    
    // Add event listener for the kg radio button
    kgRadio.addEventListener('change', function() {
        unit = 'kg';
        convertToKg(data);
        latestWeight = Math.round(data.getValue((data.getNumberOfRows()-1), 1) * 10) / 10;
        weightDisplay.textContent = `Your latest weight is ${latestWeight} kg!`;
        options.vAxis.title = 'Weight (' + unit + ')';
        dashboard.draw(data);
    });

    // Add an event listener for the 'select' event
    google.visualization.events.addListener(chart, 'select', function() {
        // Get the selected item from the chart
        var selectedItem = chart.getChart().getSelection()[0];
        if (selectedItem) {
        // Get the date and weight values from the selected item
        var date = data.getValue(selectedItem.row, 0);
        old_date = date;
        var weight = data.getValue(selectedItem.row, 1);
        old_weight = weight;
        
        // Fill in the date and weight fields with the selected values
        document.getElementById('date-input').value = date.toISOString().substring(0,10);
        document.getElementById('weight-input').value = weight;
        }
    });

    // Draw the chart with the slider and chart wrapper
    dashboard.bind(dateRangeSlider, chart);
    dashboard.draw(data);
};


$("#add-weight-btn").click(function(event) {
    event.preventDefault(); // prevent form submission

    // get values from form inputs
    var date = $("#date-input").val();
    var weight = $("#weight-input").val();
    var unit = $("input[name='unit']:checked").val();
    //var time = new Date().toISOString().slice(10);
    //date = date + time;

    // send AJAX request to Flask endpoint
    $.ajax({
        url: "/add_weight",
        type: "POST",
        data: {
            "date": date,
            "weight": weight,
            "unit": unit,
            "user": ath,
        },
        success: function(response) {
            console.log(response);
            resultDisplay.style.color = '#333333';
            resultDisplay.textContent = response;
            wgt.push([new Date(date), Number(weight)]);
            wgt.sort((a, b) => {
                const dateA = new Date(a[0]);
                const dateB = new Date(b[0]);
                return dateA - dateB;
            });

            drawChart();

            if(wgt[wgt.length-2][1] > wgt[wgt.length-1][1]) {
                document.getElementById('weight-card').style.backgroundColor = '#90EE90';
                document.getElementById('weight-info').style.color = 'green';
            } else {
                document.getElementById('weight-card').style.backgroundColor = '#ffdddd';
                document.getElementById('weight-info').style.color = 'red';
            }
            weightDisplay.textContent = `Your latest weight is ${wgt[wgt.length-1][1]} lbs!`;
        },
        error: function(error) {
            console.log(error.responseJSON.error);
            resultDisplay.style.color = 'red';
            resultDisplay.textContent = error.responseJSON.error;
        }        
    });
});

$("#remove-weight-btn").click(function(event) {
    event.preventDefault(); // prevent form submission

    // get values from form inputs
    var date = $("#date-input").val();
    var weight = $("#weight-input").val();

    // send AJAX request to Flask endpoint
    $.ajax({
        url: "/remove_weight",
        type: "POST",
        data: {
            "date": date,
            "weight": weight,
            "user": ath,
        },
        success: function(response) {
            console.log(response);
            resultDisplay.style.color = '#333333';
            resultDisplay.textContent = response;
            const dateToRemove = new Date(date);
            wgt = wgt.filter(([date, weight]) => date.getTime() !== dateToRemove.getTime());
            wgt.sort((a, b) => {
                const dateA = new Date(a[0]);
                const dateB = new Date(b[0]);
                return dateA - dateB;
            });

            drawChart();

            if(wgt[wgt.length-2][1] > wgt[wgt.length-1][1]) {
                document.getElementById('weight-card').style.backgroundColor = '#90EE90';
                document.getElementById('weight-info').style.color = 'green';
            } else {
                document.getElementById('weight-card').style.backgroundColor = '#ffdddd';
                document.getElementById('weight-info').style.color = 'red';
            }
            weightDisplay.textContent = `Your latest weight is ${wgt[wgt.length-1][1]} lbs!`;
        },
        error: function(error) {
            console.log(error.responseJSON.error);
            resultDisplay.style.color = 'red';
            resultDisplay.textContent = error.responseJSON.error;
        }        
    });
});

// $("#edit-weight-btn").click(function(event) {
//     event.preventDefault(); // prevent form submission
// 
//     // get values from form inputs
//     //var date = $("#date-input").val();
//     var new_weight = $("#weight-input").val();
//     var unit = $("input[name='unit']:checked").val();
//     //var time = new Date().toISOString().slice(10);
//     //date = date + time;
// 
//     // send AJAX request to Flask endpoint
//     $.ajax({
//         url: "/edit_weight",
//         type: "POST",
//         data: {
//             "date": old_date,
//             "new_weight": new_weight,
//             "old_weight": old_weight,
//             "unit": unit
//         },
//         success: function(response) {
//             console.log(["1", date, (old_weight).toString()]);
//             console.log(response);
//             resultDisplay.textContent = response;
//         },
//         error: function(error) {
//             console.log(error);
//         }
//     });
// });