$(window).on('load', function () {
    fetch('/export/data.json')
        .then(response => response.json())
        .then(data => renderChart(data));

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
        const lineSeries = chart.addLineSeries({
            title: 'Predicted'
        });
        lineSeries.setData(data.lineData);
        const candleSeries = chart.addCandlestickSeries({
            title: 'Close',
            upColor: '#4bffb5',
            downColor: '#ff4976',
            borderDownColor: '#ff4976',
            borderUpColor: '#4bffb5',
            wickDownColor: '#838ca1',
            wickUpColor: '#838ca1',
        });
        candleSeries.setData(data.candleData);
    }

    /**
     * @param data
     * @returns {*[]}
     */
    function parseData(data) {
        let result = {'lineData': [], 'candleData': []};
        if (data.data) {
            let line = data.data[0];
            let candle = data.data[1];
            $(line.x).each(function (i, e) {
                let time = e.replace('T00:00:00', '');
                result.lineData.push({
                    time: time,
                    value: line.y[i]
                });
                result.candleData.push({
                    time: time,
                    open: candle.open[i],
                    close: candle.close[i],
                    high: candle.high[i],
                    low: candle.low[i],
                });
            });

        }
        return result;
    }
});