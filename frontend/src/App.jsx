import { useRef, useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Chart } from 'react-chartjs-2';

import { getData, OPTIONS } from "./graph_utils.js";
import FSlider from "./components/FSlider.jsx";
import WriteInp from "./components/WriteInp.jsx";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Legend,
);

function App() {
    const chartRef = useRef(null);
    const [chartData, setChartData] = useState({datasets: []});

    useEffect(() => {
        const chart = chartRef.current;
            if (!chart) {
                return;
            }

        const ws = new WebSocket('ws://127.0.0.1:8000/sdr/ws');
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            const chartData = getData(data.psd, data.freqs, chart);
            setChartData(chartData);

            chart.data = chartData;
            chart.update();
        }

        return () => {
            ws.close();
        };
    }, []);


    // <Chart ref={chartRef} type='line' data={chartData} options={OPTIONS} className="mb-8"/>
    return (
    <div className="h-screen max-h-[95vh] overflow-auto flex flex-col justify-center items-center">
        <Chart ref={chartRef} type='line' data={chartData} options={OPTIONS} className="mb-8"/>
        <FSlider />
        <WriteInp />
    </div>
    )
}

export default App
