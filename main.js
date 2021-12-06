$(window).on('load', function () {
    fetch('/export/data.json')
        .then(response => response.json())
        .then(data => renderChart(data));

    /**
     * @param data
     */
    function renderChart(data) {
        data = parseData(data);
        const chart = LightweightCharts.createChart(document.body, {
            layout: {
                backgroundColor: '#253248',
                textColor: 'rgba(255, 255, 255, 0.9)',
            },
            grid: {
                vertLines: {
                    color: '#334158',
                },
                horzLines: {
                    color: '#334158',
                },
            },
            crosshair: {
                mode: 1,
            },
            rightPriceScale: {
                borderColor: '#485c7b',
                mode: 1
            },
            timeScale: {
                borderColor: '#485c7b',
            }
        });
        const close = chart.addLineSeries({
            color: 'orange'
        });
        close.setData(data.closeData);
        const predicted = chart.addLineSeries({
            color: 'aqua'
        });
        predicted.setData(data.predictedData);
    }

    /**
     * @param data
     * @returns {*[]}
     */
    function parseData(data) {
        let result = {'predictedData': [], 'closeData': []};
        if (data.data) {
            let predicted = data.data[0];
            let close = data.data[1];
            $(predicted.x).each(function (i, e) {
                let time = e.replace('T00:00:00', '');
                result.predictedData.push({
                    time: time,
                    value: predicted.y[i]
                });
                result.closeData.push({
                    time: time,
                    value: close.y[i]
                });
            });

        }
        return result;
    }
});