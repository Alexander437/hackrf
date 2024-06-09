import {useState} from "react";
import {Button, Col, ConfigProvider, Input, Row} from "antd";
import axios from "axios";

const saveFile = (class_name) => {
    axios.post(`http://localhost:8000/sdr/write_file?class_name=${class_name}`).then(r => {
        console.log(class_name);
        console.log(r.data);
    })
}

function WriteInp() {
  const [inputValue, setInputValue] = useState("Drone model");

  const onChange = (newValue) => {
    setInputValue(newValue.target.value);
  };
  return (
      <div>
        <Row>
          <Col className="mr-3">
            <Input
                defaultValue={inputValue}
                className="w-50"
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
                        Записать данные
                    </Button>
                </ConfigProvider>
            </Col>
        </Row>
      </div>
  )
}

export default WriteInp;