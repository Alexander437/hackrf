import React, { useState, useMemo } from "react"
import {Button, Input, notification} from "antd"
import {useSaveFileMutation} from "../stores/sdr/index.js";

const Context = React.createContext({
  name: 'Default',
});

export default function WriteInp() {
    const [inputValue, setInputValue] = useState("Drone model");
    const [api, contextHolder] = notification.useNotification()
    const [saveFilePost] = useSaveFileMutation()

    const saveFile = async (class_name) => {
        const res = await saveFilePost(class_name)
        console.log(res.data)
        api.info({
            message: `${res.data.ok}`,
            description: `${res.data.message}`,
            placement: 'bottomRight',
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