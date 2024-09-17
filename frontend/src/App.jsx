import FSlider from "./components/FSlider.jsx"
import WriteInp from "./components/WriteInp.jsx"
import SpectrChart from "./components/SpectrChart/index.jsx"
import {theme} from "./materialTheme.js";
import {ConfigProvider} from "antd"

function App() {



    return (
      <ConfigProvider theme={theme}>
          <div className="flex flex-col items-center justify-center">
            <SpectrChart />
            <FSlider />
            <WriteInp />
          </div>
      </ConfigProvider>
    )
}

export default App
