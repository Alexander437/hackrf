function createGradient(ctx, area) {
    const gradient = ctx.createLinearGradient(0, area.bottom, 0, area.top);
    gradient.addColorStop(0, "orange");
    gradient.addColorStop(0.5, "red");
    gradient.addColorStop(1, "purple");
    return gradient;
}

function getFreqs(leftFreq, rightFreq, step) {
    let arr = [];
    let left = leftFreq

    while (left < rightFreq) {
        arr.push(left);
        left += step
    }
    return arr;
}

export function getData(psd, leftFreq, rightFreq, step, chart) {
    return {
        labels: getFreqs(leftFreq, rightFreq, step),
        datasets: [{
            data: psd,
            fill: false,
            borderColor: createGradient(chart.ctx, chart.chartArea),
            tension: 0.1,
            pointRadius: 0,
        }]
    };
}

export const OPTIONS = {
    plugins: {
        legend: {
            display: false,
        }
    },
    animation: {
        duration: 0,
    },
    scales: {
        y: {
            min: -85,
            // max: -117,
            ticks: {
                stepSize: 2
            }
        },
        x: {
            ticks: {
                stepSize: 20
            }
        }
    }
}