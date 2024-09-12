# HackRF

## 1. Подключение

[simple tutorial](https://my-gnuradio.org/2015/03/19/obzor-hackrf-one-chast-1-raspakovka-i-podklyuchenie/)

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
# Возможно, после установки `hackrf_info` будет работать только под sudo
# Это исправляется отключением и повторным подключением hackrf к usb
hackrf_info
# https://pypi.org/project/pyhackrf/, https://github.com/dressel/pyhackrf
# для работы блоков в gnuradio
# sudo apt-get install -y python3-soapysdr
```

## 3. Запуск приложения

### 3.1 Через исполняемый файл

Кажется, один из самых простых способов - запустить собранное в исполняемый файл приложение.

> [!WARNING]
> Для ПК с linux и windows (x64)
> Протестировано только на Ubuntu22.04, но, теоретически, дожно работать для других Linux (x64) и Windows (x64)

Для этого требуется извлечь архив в необходимую директорию и выполнить

```bash
cd hrf_ubuntu
chmod +x app/main
./app/main
```

### 3.2 Через python packege

Требуется установить python >= 3.10

Скачать пакет `hackrf-0.1.0-py3-none-any.whl` и выполнить:

```bash
pip install /путь_к_директории_с_пакетом/hackrf-0.1.0-py3-none-any.whl
```

После этого запуск осуществляется командой:

```bash
hackrf-start
```

### 3.3 Сборка из исходников

Если другие варианты не работают (а это очень возможно для raspberry и подобных),
требуется сборка из исходников.

Для управления зависимостями используется [Poetry](https://python-poetry.org/docs/).

> [!NOTE]
> Инструкции по установке Poetry: [installation](https://python-poetry.org/docs/#installation)

Установка зависимостей
```bash
cd hackrf
poetry install
cd frontend && npm i && npm run deploy && rsync -av --delete dist/* ../app/static && cd ..
 ```

Запуск без сборки
```bash
poetry run hackrf-start
```

Вы можете собрять исполняемый файл, используя

```bash
pyinstaller --distpath app --onefile backend/main.py
```
После после чего запускать:
```bash
./app/main
```

## Поддерживаемые версии браузеров
- Chrome >=87
- Firefox >=78
- Safari >=14
- Edge >=88


## ТХ
HackRF:
- `sample_rate` - [8 MHz; 20 MHz]
- `center_freq` - [1 MHz + `sample_rate / 2`; 6 GHz - `sample_rate / 2`]
