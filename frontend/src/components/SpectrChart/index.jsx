import { useRef, useEffect, useState } from 'react'
import Chart from 'chart.js/auto'
import { Chart as ChartReact} from 'react-chartjs-2'
import {getData, OPTIONS} from "./ChartUtils.js"
import {BACKEND_DOMAIN} from "../../stores/constants.js";

export default function SpectrChart(props) {
    const chartRef = useRef(null)
    const [chartData, setChartData] = useState({datasets: []})

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return
        }

        const ws = new WebSocket(`ws://${BACKEND_DOMAIN}/sdr/ws`)
        ws.onopen = () => {
            ws.send(JSON.stringify(props.fftConfig))
        }

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
    }, [props.fftConfig])
    return (
        <ChartReact
            ref={chartRef}
            type='line'
            data={chartData}
            options={OPTIONS}
        />
    )
}