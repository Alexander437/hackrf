#!/bin/bash

set -e  # Прекращать выполнение скрипта при любой ошибке

# Обновление списка пакетов и установка зависимостей
echo "Обновление списка пакетов..."
sudo apt-get update

echo "Установка необходимых пакетов..."
sudo apt-get install -y hackrf gr-osmosdr libhackrf-dev libhackrf0 libusb-1.0-0 libusb-1.0-0-dev libfftw3-dev \
    cmake g++ libpython-dev python-numpy swig soapysdr-tools python3-soapysdr \
    hackrf soapysdr-module-hackrf soapysdr-module-rfspace

# Проверка работы hackrf_info
echo "Проверка работы hackrf_info..."
hackrf_info

# Установка SoapySDR
echo "Установка SoapySDR..."
git clone https://github.com/pothosware/SoapySDR.git
cd SoapySDR
mkdir build && cd build
cmake ..
make -j"$(nproc)"
sudo make install -j"$(nproc)"
cd ..

# Обновление .bashrc
echo "Обновление .bashrc..."
if ! grep -q "export LD_LIBRARY_PATH=/usr/local/lib" ~/.bashrc; then
    echo "export LD_LIBRARY_PATH=/usr/local/lib" >> ~/.bashrc
fi

# Применение изменений в текущей сессии
export LD_LIBRARY_PATH=/usr/local/lib

echo "Проверка SoapySDR..."
SoapySDRUtil --info

# Установка SoapyHackRF
echo "Установка SoapyHackRF..."
git clone https://github.com/pothosware/SoapyHackRF.git
cd SoapyHackRF
mkdir build && cd build
cmake ..
sudo make install
cd ../..

echo "Проверка SoapyHackRF..."
SoapySDRUtil --probe="driver=hackrf"

echo "Ok"
