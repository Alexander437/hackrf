import { useRef, useEffect, useState } from 'react'
import Chart from 'chart.js/auto'
import { Chart as ChartReact} from 'react-chartjs-2'
import {getData, OPTIONS} from "./ChartUtils.js"

export default function SpectrChart() {
    const chartRef = useRef(null)
    const [chartData, setChartData] = useState({datasets: []})

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return
        }

        const ws = new WebSocket('ws://127.0.0.1:8000/sdr/ws')
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data)
            const chartData = getData(data.psd, data.freqs, chart)
            setChartData(chartData)

            chart.data = chartData
            chart.update()
        }

        return () => {
            ws.close()
        };
    }, [])
    return (
        <ChartReact ref={chartRef} type='line' data={chartData} options={OPTIONS} className="mb-8"/>
    )
}