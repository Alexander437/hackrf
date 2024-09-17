import React, { useState, useMemo } from "react"
import {Button, Input, notification} from "antd"
import axios from "axios"

const Context = React.createContext({
  name: 'Default',
});

export default function WriteInp() {
    const [inputValue, setInputValue] = useState("Drone model");
    const [api, contextHolder] = notification.useNotification()

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
    setInputValue(newValue.target.value)
  }
  return (
      <Context.Provider value={contextValue}>
      {contextHolder}
          <div className="flex gap-5 mb-6 w-[360px]">
                <Input
                    defaultValue={inputValue}
                    onChange={onChange}
                />
                <Button
                    type="primary"
                    onClick={() => {saveFile(inputValue)}}
                    className="w-[177px]"
                    >
                    Записать данные
                </Button>
          </div>
      </Context.Provider>
  )
}