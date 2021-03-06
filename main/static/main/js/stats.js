function polarityChart(chart_id, positive, negative) {

    var ctx = document.getElementById(chart_id).getContext('2d');

    var data = {
        datasets: [{
            data: [positive, negative],
            backgroundColor: [
                    '#2554C7',
                    '#DC143C'
                ],
        }],
        labels: [
            'Positive Tweets',
            'Negative Tweets'
        ],
    };

    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            // maintainAspectRatio: false,
            legend: {
              display: false
            },

            title: {
                display: true,
                text: "Polarity of tweets",
                fontSize: 15,
                fontColor: "black"

            },

            tooltips: {
                enabled: true,
            },
        }
    });
}

function keywordsChart(canvas_id, keywords, key_pos, key_neg){

    var ctx = document.getElementById(canvas_id);

    var barOptions_stacked = {

        plugins: {
            datalabels: {
                color: '#FFFFFF',
            }
        },

        responsive: true,

        title: {
            display: true,
            text: "Polarity of top 5 keywords",
            fontSize: 15,
            fontColor: "black"


        },

        tooltips: {
            enabled: true,
        },

        hover :{
            animationDuration:0,
        },

        scales: {
            xAxes: [{
                gridLines: {
                    display: false,
                },
                stacked: true,
                ticks: {
                  fontColor: "black"
                }

            }],

            yAxes: [{
                gridLines: {
                    display:false,
                },
                stacked: true,
                ticks: {
                  fontColor: "black"
                },
                scaleLabel: {
                    fontStyle: "bold",
                },
            }]
        },

        legend: {
            display: true,
            labels: ['Positive Tweets', 'Negative Tweets']
        },

        animation: {
            onComplete: function () {
                var chartInstance = this.chart;
                var ctx = chartInstance.ctx;
                ctx.textAlign = "left";
                ctx.font = "9px Open Sans";
                ctx.fillStyle = "#fff";

                Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
                    var meta = chartInstance.controller.getDatasetMeta(i);
                    Chart.helpers.each(meta.data.forEach(function (bar, index) {
                        data = dataset.data[index];
                    }),this)
                }),this);
            }
        },

        pointLabelFontFamily : "Quadon Extra Bold",

        scaleFontFamily : "Quadon Extra Bold",


    };

    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: keywords,
            datasets: [{
                label: 'Positive Tweets',
                data: key_pos,
                backgroundColor: "#2554C7",
                hoverBackgroundColor: "#1569C7"
            },{
                label: 'Negative Tweets',
                data: key_neg,
                backgroundColor: "#DC143C",
                hoverBackgroundColor: "#C24641"
            }]
        },
        options: barOptions_stacked
    });
}


function hashtagChart(canvas_id, hashtags, hashcount){

    var ctx = document.getElementById(canvas_id);

    var barOptions_stacked = {

        plugins: {
            datalabels: {
                color: '#FFFFFF',
            }
        },

        responsive: true,

        title: {
            display: true,
            text: "Top 5 most used hashtags",
            fontSize: 15,
            fontColor: "black"


        },

        tooltips: {
            enabled: true,
        },

        hover :{
            animationDuration:0,
        },

        scales: {
            xAxes: [{
                gridLines: {
                    display: false,
                },
                stacked: true,
                ticks: {
                  fontColor: "black"
                },
            }],

            yAxes: [{
                gridLines: {
                    display:false,
                },
                stacked: true,
                ticks: {
                  fontColor: "black"
                },
                scaleLabel: {
                    fontStyle: "bold",
                },
            }]
        },

        legend: {
            display: true,
            labels: ['Hashtags'],
            labels : {
              fontColor: "black"
            }
        },

        animation: {
            onComplete: function () {
                var chartInstance = this.chart;
                var ctx = chartInstance.ctx;
                ctx.textAlign = "left";
                ctx.font = "9px Open Sans";
                ctx.fillStyle = "#fff";

                Chart.helpers.each(this.data.datasets.forEach(function (dataset, i) {
                    var meta = chartInstance.controller.getDatasetMeta(i);
                    Chart.helpers.each(meta.data.forEach(function (bar, index) {
                        data = dataset.data[index];
                    }),this)
                }),this);
            }
        },

        pointLabelFontFamily : "Quadon Extra Bold",

        scaleFontFamily : "Quadon Extra Bold",

    };

    var myChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: hashtags,

            datasets: [{
                label: 'Hashtags',
                data: hashcount,
                backgroundColor: "#FF1493",
                hoverBackgroundColor: "#FF69B4"
            }]
        },
        options: barOptions_stacked
    });
}

function resetCanvas(canvas_id) {
    id = "#" + canvas_id
    canvas = $(id);
    canvas.remove();
    $('#stats').append('<canvas id="'+ canvas_id + '"></canvas><br>');
}
