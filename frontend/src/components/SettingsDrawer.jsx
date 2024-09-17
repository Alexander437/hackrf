import {Button, Drawer, InputNumber, Select} from "antd";
import {useState} from "react";
import {SettingFilled} from "@ant-design/icons";

export default function SettingsDrawer(props) {
    const [driverOpen, setDriverOpen] = useState(false)
    const showDrawer = () => {
        setDriverOpen(true)
    }
    const onClose = () => {
        setDriverOpen(false)
    }

    return (
        <>
        <Button
            shape="circle"
            icon={
                <SettingFilled style={{ fontSize: '24px' }} />
            }
            className="m-3"
            onClick={showDrawer}
        />
            <Drawer
                title="Настройки"
                placement={"left"}
                closable={false}
                onClose={onClose}
                open={driverOpen}
            >
                <div className="flex flex-col gap-2 pb-12">
                    Mode:
                    <Select
                        style={{width: 120}}
                        defaultValue={props.fftConfig.mode}
                        onChange={(mode) => {
                            props.setfftConfig(prevConfig => {
                                    return {...prevConfig, mode: mode}
                                }
                            )
                        }}
                        options={[
                            {value: 'psd', label: 'psd'},
                            {value: 'complex', label: 'complex'},
                            {value: 'angle', label: 'angle'},
                            {value: 'magnitude', label: 'magnitude'},
                            {value: 'phase', label: 'phase'},
                        ]}
                    />
                </div>
                <div className="flex flex-col gap-2 pb-12">
                    N FFT:
                    <InputNumber
                        style={{width: 120}}
                        min={5}
                        value={props.fftConfig.NFFT}
                        onChange={(NFFT) => {
                            props.setfftConfig(prevConfig => {
                                    return {...prevConfig, NFFT: NFFT}
                                }
                            )
                        }}
                    />
                </div>
                <div className="flex flex-col gap-2 pb-12">
                    Detrend:
                    <Select
                        style={{width: 120}}
                        defaultValue={props.fftConfig.detrend}
                        onChange={(detrend) => {
                            props.setfftConfig(prevConfig => {
                                    return {...prevConfig, detrend: detrend}
                                }
                            )
                        }}
                        options={[
                            {value: 'mean', label: 'mean'},
                            {value: 'linear', label: 'linear'},
                            {value: 'none', label: 'none'},
                        ]}
                    />
                </div>
                <div className="flex flex-col gap-2 pb-12">
                    N overlap:
                    <InputNumber
                        style={{width: 120}}
                        min={0}
                        max={props.fftConfig.NFFT - 1}
                        value={props.fftConfig.noverlap}
                        onChange={(noverlap) => {
                            props.setfftConfig(prevConfig => {
                                    return {...prevConfig, noverlap: noverlap}
                                }
                            )
                        }}
                    />
                </div>
            </Drawer>
        </>
    )
}