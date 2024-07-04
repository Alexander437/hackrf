import { useRef, useEffect, useState } from 'react';
import Chart from 'chart.js/auto';
import { Chart as ChartReact} from 'react-chartjs-2';

import {getData, OPTIONS} from "../graph_utils.js";
import {Card} from "antd";
import WriteInp from "./WriteInp.jsx";

function GraphCard() {
    const chartRef = useRef(null);
    const [chartData, setChartData] = useState({datasets: []});

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            return;
        }

        const listener = (event) => {
            const data = JSON.parse(event.data);
            const chartData = getData(
                data.powerArray.data,
                data.leftFreq,
                data.rightFreq,
                data.step,
                chart);
            setChartData(chartData);

            chart.data = chartData;
            chart.update();
        }
        const evtSource = new EventSource("http://127.0.0.1:8000/api/stream");


        evtSource.addEventListener("1", listener)

        return () => {};
    }, []);


    return (
        <Card
            title="example"
            extra={<a href="#">Закрыть</a>}
            style={{ width: "33%" }}
        >
            <div className="flex flex-col justify-center items-center">
                <ChartReact ref={chartRef} type='line' data={chartData} options={OPTIONS} className="mb-8"/>
                <WriteInp className=""/>
            </div>
        </Card>
    )
}

export default GraphCard