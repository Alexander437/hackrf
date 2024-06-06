# HackRF

https://habr.com/ru/companies/vk/articles/745016/
https://github.com/TUIlmenauAMS/MRSP_Tutorials/tree/master/seminars

ТХ:

- `sample_rate` - [8 MHz; 20 GHz]
- `center_freq` - [1 MHz + `sample_rate / 2`; 6 GHz - `sample_rate / 2`]

## Подключение

[link](https://my-gnuradio.org/2015/03/19/obzor-hackrf-one-chast-1-raspakovka-i-podklyuchenie/)

Присоедините антенну и после этого подключите `hackrf` к USB разъему.

Проверьте подключение
```bash
sudo dmesg | grep HackRF
# usb 3-3: Product: HackRF One
```

## Установка пакетов

Образ для raspberry PI с нужными драйверами:
https://github.com/luigifcruz/pisdr-image/releases

```bash
# https://my-gnuradio.org/2017/01/21/rabota-hackrf-v-rezhime-transivera-v-gnuradio/
sudo apt-get update
sudo apt-get install hackrf gr-osmosdr libhackrf-dev libhackrf0 libusb-1.0-0 libusb-1.0-0-dev libfftw3-dev
hackrf_info
pip install -r requirements.txt
# https://pypi.org/project/pyhackrf/, https://github.com/dressel/pyhackrf
# для работы блоков в gnuradio
# sudo apt-get install -y python3-soapysdr
```

## Resources

* [webradio](https://github.com/ColbyAtCRI/webradio)
* [fastapi example proj](https://github.com/artemonsh/fastapi-onion-architecture)