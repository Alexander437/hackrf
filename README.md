# HackRF

## 1. Подключение

[link](https://my-gnuradio.org/2015/03/19/obzor-hackrf-one-chast-1-raspakovka-i-podklyuchenie/)

Присоедините антенну и после этого подключите `hackrf` к USB разъему.

Проверьте подключение
```bash
sudo dmesg | grep HackRF
# usb 3-3: Product: HackRF One
```

## 2. Установка драйверов

Образ для raspberry PI с нужными драйверами:
https://github.com/luigifcruz/pisdr-image/releases

```bash
# https://my-gnuradio.org/2017/01/21/rabota-hackrf-v-rezhime-transivera-v-gnuradio/
sudo apt-get update
sudo apt-get install hackrf gr-osmosdr libhackrf-dev libhackrf0 libusb-1.0-0 libusb-1.0-0-dev libfftw3-dev
hackrf_info
# https://pypi.org/project/pyhackrf/, https://github.com/dressel/pyhackrf
# для работы блоков в gnuradio
# sudo apt-get install -y python3-soapysdr
```

## 3. Сборка и запуск приложения

Установка зависимостей
```bash
pip install -r requirements.txt
cd frontend && npm run deploy && cd ..
```

Запуск без сборки
```bash
cd backend 
uvicorn main:app
```

ИЛИ

Сборка
```bash
pyinstaller --distpath app --onefile backend/main.py
cp -r backend/app/static app
```

После сборки можно запускать так:
```bash
./app/main
```

## Запуск
- Chrome >=87
- Firefox >=78
- Safari >=14
- Edge >=88


## ТХ
HackRF:
- `sample_rate` - [8 MHz; 20 MHz]
- `center_freq` - [1 MHz + `sample_rate / 2`; 6 GHz - `sample_rate / 2`]
