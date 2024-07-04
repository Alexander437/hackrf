import React, { useState, useMemo } from "react";
import {Button, Col, ConfigProvider, Input, notification, Row} from "antd";
import axios from "axios";

const Context = React.createContext({
    name: 'Default',
});

function WriteInp() {
    const [inputValue, setInputValue] = useState("Drone model");
    const [api, contextHolder] = notification.useNotification();

    const saveFile = (class_name) => {
        axios.post(`http://localhost:8000/sdr/write_file?class_name=${class_name}`).then(r => {
            console.log(r.data);
            api.info({
                message: `${r.data.ok}`,
                description: `${r.data.message}`,
                placement: 'bottomRight',
            });
        })
    }

    const contextValue = useMemo(
        () => ({
            name: 'Ant Design',
        }),
        [],
    );

    const onChange = (newValue) => {
        setInputValue(newValue.target.value);
    };
    return (
        <Context.Provider value={contextValue}>
            {contextHolder}
            <div>
                <Row>
                    <Col className="mr-3">
                        <Input
                            defaultValue={inputValue}
                            className="w-32"
                            onChange={onChange}
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
                                onClick={() => {saveFile(inputValue)}}
                            >
                                Записать
                            </Button>
                        </ConfigProvider>
                    </Col>
                </Row>
            </div>
        </Context.Provider>
    )
}

export default WriteInp;