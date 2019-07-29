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
        ]
    };
    
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            // maintainAspectRatio: false,

            title: {
                display: true,
                text: "Polarity of tweets",
                fontSize: 15,

            },

            plugins: {
                datalabels: {
                    formatter: (value, ctx) => {
                        let sum = 0;
                        let dataArr = ctx.chart.data.datasets[0].data;
                        dataArr.map(data => {
                            sum += data;
                        });
                        let percentage = (value*100 / sum).toFixed(2)+"%";
                        return percentage;
                    },
                    color: '#FFFFFF',
                }
            },

            tooltips: {
                enabled: false,
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

        },

        tooltips: {
            enabled: false,
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
            }],

            yAxes: [{
                gridLines: {
                    display:false,
                },
                stacked: true,
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
                        // if(i==0){
                        //     ctx.fillText(data, 50, bar._model.y+4);
                        // } else {
                        //     ctx.fillText(data, bar._model.x-25, bar._model.y+4);
                        // }
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