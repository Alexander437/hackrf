import {useState} from "react"
import {Button, InputNumber, Slider} from "antd"
import axios from "axios"


const setCenterFreq = (val) => {
    axios.post(`http://localhost:8000/sdr/set_center_freq?center_freq_m=${val}`).then(r => {
        console.log(r.data)
    })
}

export default function FSlider() {
  const [inputValue, setInputValue] = useState(20);
  const marks = {
      20: '20',
      5990: '5990'
  }
  const onChange = (newValue) => {
    setInputValue(newValue)
  };
  return (
      <>
        <Slider
          min={20}
          max={5990}
          onChange={onChange}
          value={typeof inputValue === 'number' ? inputValue : 80}
          marks={marks}
          defaultValue={20}
          className="w-[340px]"
        />
          <div className="flex gap-5 mb-6 w-[360px]">
            <InputNumber
              min={20}
              max={5990}
              value={inputValue}
              onChange={onChange}
              addonAfter="МГц"
            />
            <Button
                type="primary"
                onClick={() => {setCenterFreq(inputValue)}}
                className="w-[177px]"
                >
                Установить
            </Button>
          </div>

      </>
  )
}