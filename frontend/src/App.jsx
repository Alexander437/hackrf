import GraphCard from "./components/GraphCard.jsx";
import {Card, Form, Input, InputNumber, Modal, Row, Select} from "antd";
import {PlusCircleOutlined} from "@ant-design/icons"
import {useState} from "react";
import axios from "axios";

const formItemLayout = {
    labelCol: { span: 12 },
    wrapperCol: { span: 15 },
};


function App() {
    const [form] = Form.useForm();
    const [formValues, setFormValues] = useState();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [maxId, setMaxId] = useState(0);
    const [graphs, setGraphs] = useState([]);


    function addCard(values, graphs) {
        const newId = maxId + 1;
        axios.post(`http://localhost:8000/api/sub`, {
            "id": newId,
            "sectorId": 1,
            "srcName": values.srcName,
            "targetFps": values.targetFps,
            "width": values.width,
            "leftFreq": values.leftFreq,
            "rightFreq": values.rightFreq,
        })
            .then(r => {
                setMaxId(newId)
                setGraphs([...graphs, {id: newId, title: values.title, srcName: values.srcName}]);
            })
            .catch((error) => console.error(error));
    }


    const onCreate = (values) => {
        setFormValues(values);
        addCard(values, graphs);
        setIsModalOpen(false);
    };


    return (
        <>
            <Row>
                {graphs.map((graph) => (
                    <GraphCard key={graph.id} id={graph.id} title={graph.title}
                               srcName={graph.srcName} graphs={graphs} setGraphs={setGraphs} />)
                )
                }
                { (graphs.length < 6) && <Card
                    hoverable
                    style={{ width: "33%" }}
                    className="content-center"
                    onClick={() => setIsModalOpen(true)}
                >
                    <div className="flex flex-col justify-center items-center">
                        <PlusCircleOutlined style={{ height: '36vh', fontSize: '4rem', color: '#ccc' }} />
                    </div>
                </Card>
                }
            </Row>
            <Modal
                open={isModalOpen}
                title="Добавить диапазон"
                okText="Добавить"
                cancelText="Отмена"
                okButtonProps={{
                    autoFocus: true,
                    htmlType: 'submit',
                }}
                onCancel={() => setIsModalOpen(false)}
                destroyOnClose
                modalRender={(dom) => (
                    <Form
                        layout="horizontal"
                        form={form}
                        name="form_in_modal"
                        initialValues={{
                            width: 50,
                            srcName: "ins",
                            targetFps: 1,
                        }}
                        clearOnDestroy
                        onFinish={(values) => onCreate(values)}
                    >
                        {dom}
                    </Form>
                )}
            >
                <Form.Item
                    {...formItemLayout}
                    name="title"
                    label="Название"
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    {...formItemLayout}
                    name="leftFreq"
                    label="Нижняя частота"
                    rules={[
                        {
                            required: true,
                            message: 'Определите нижнюю частоту',
                        },
                    ]}
                >
                    <InputNumber min={0} max={6000} addonAfter="МГц"/>
                </Form.Item>

                <Form.Item
                    {...formItemLayout}
                    name="rightFreq"
                    label="Верхняя частота"
                    rules={[
                        {
                            required: true,
                            message: 'Определите верхнюю частоту',
                        },
                    ]}
                >
                    <InputNumber min={0} max={6000} addonAfter="МГц"/>
                </Form.Item>

                <Form.Item
                    {...formItemLayout}
                    name="srcName"
                    label="Способ получения спектра"
                >
                    <Select options={[
                        { value: 'ins', label: 'Мгновенная мощность' },
                        { value: 'avg', label: 'Средняя мощность' },
                        { value: 'coh', label: 'Средняя мощность когерентным способом'},
                        { value: 'max', label: 'Максимальная мощность'},
                        { value: 'min', label: 'Минимальная мощность'}
                    ]}
                    />
                </Form.Item>

                <Form.Item
                    {...formItemLayout}
                    name="width"
                    label="Разрешение по горизонтали"
                >
                    <InputNumber min={1} className="w-full" />
                </Form.Item>

                <Form.Item
                    {...formItemLayout}
                    name="targetFps"
                    label="FPS"
                >
                    <InputNumber min={1} max={10} className="w-full" />
                </Form.Item>

            </Modal>
        </>
    )
}

export default App