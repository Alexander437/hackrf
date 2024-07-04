import {useState} from "react";
import {Button, Col, ConfigProvider, InputNumber, Row, Slider} from "antd";
import axios from "axios";


const setCenterFreq = (val) => {
    axios.post(`http://localhost:8000/sdr/set_center_freq?center_freq_m=${val}`).then(r => {
        console.log(r.data);
    })
}

function FSlider() {
    const [inputValue, setInputValue] = useState(20);
    const marks = {
        20: '20',
        5990: '5990'
    }
    const onChange = (newValue) => {
        setInputValue(newValue);
    };
    return (
        <div>
            <Row>
                <Col className="mr-7">
                    <Slider
                        min={20}
                        max={5990}
                        onChange={onChange}
                        value={typeof inputValue === 'number' ? inputValue : 80}
                        marks={marks}
                        defaultValue={20}
                        className="min-w-[400px]"
                    />
                </Col>
                <Col className="mr-3">
                    <InputNumber
                        min={20}
                        max={5990}
                        className="w-40"
                        value={inputValue}
                        onChange={onChange}
                        addonAfter="МГц"
                    />
                </Col>
                <Col className="mr-7">
                    <ConfigProvider
                        theme={{
                            components: {
                                Button: {
                                    colorPrimary: `linear-gradient(135deg, #6253E1, #04BEFE)`,
                                    colorPrimaryHover: `linear-gradient(135deg, #e75516, #ff9a44)`,
                                    colorPrimaryActive: `linear-gradient(135deg, #e75516, #ff9a44)`,
                                    lineWidth: 0,
                                },
                            },
                        }}
                    >
                        <Button
                            type="primary"
                            onClick={() => {setCenterFreq(inputValue)}}
                        >
                            Установить
                        </Button>
                    </ConfigProvider>
                </Col>
            </Row>
        </div>
    )
}

export default FSlider;