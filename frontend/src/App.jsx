import FreqSlider from "./components/FreqSlider.jsx"
import WriteInp from "./components/WriteInp.jsx"
import SpectrChart from "./components/SpectrChart/index.jsx"
import {theme} from "./materialTheme.js";
import {Card, ConfigProvider, Drawer} from "antd"
import SettingsDrawer from "./components/SettingsDrawer.jsx";
import {useState} from "react";

function App() {
    const [fftConfig, setfftConfig] = useState({
        NFFT: 256,
        detrend: 'mean',
        noverlap: 0,
        mode: 'psd',
    })

    return (
      <ConfigProvider theme={theme}>
          <SettingsDrawer
              fftConfig={fftConfig}
              setfftConfig={setfftConfig}
          />
          <div className="flex items-center justify-center">
            <Card style={{ width: "70%" }}>
              <div className="flex flex-col items-center justify-center">
                <SpectrChart fftConfig={fftConfig} />
                <FreqSlider />
                <WriteInp />
              </div>
            </Card>
          </div>
      </ConfigProvider>
    )
}

export default App
