import Chart from 'chart.js/auto';
import { Chart as ChartReact} from 'react-chartjs-2';
import {Card} from "antd";
import WriteInp from "./WriteInp.jsx";
import {getData, OPTIONS} from "../graph_utils.js";
import {useEffect, useRef, useState} from "react";
import {CloseOutlined} from "@ant-design/icons";
import axios from "axios";

const GraphCard = ({id, title, srcName, graphs, setGraphs}) => {
    const chartRef = useRef(null);
    const [chartData, setChartData] = useState({datasets: []});

    const onRemove = () => {
        axios.post(`http://localhost:8000/api/unsub`, {"graphId": [id]})
            .then(r => setGraphs(graphs.filter((graph) => graph.id !== id)))
            .catch(error => console.error(error));
    }

    useEffect(() => {
        const chart = chartRef.current;
        if (!chart) {
            console.error("GraphCard: No chart");
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
        evtSource.addEventListener(id, listener);

        return function cleanup() {
            // evtSource.removeEventListener(id, listener);
            evtSource.close();
        }

    }, [id]);


    return (
        <Card
            title={title}
            extra={<CloseOutlined onClick={onRemove} />}
            style={{ width: "33%" }}
        >
            <div className="flex flex-col justify-center items-center">
                <ChartReact ref={chartRef} type='line' data={chartData} options={OPTIONS} className="mb-8"/>
                <WriteInp id={id} srcName={srcName} />
            </div>
        </Card>
    )
}

export default GraphCard