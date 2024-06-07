import streamlit as st
st.set_page_config(page_title="Сегментация спектра")

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.sdr import get_sdr, list_sdr
from src.settings import settings


# Sidebar
# select_sdr = st.sidebar.selectbox(
#     "SDR приемник:",
#     list_sdr()
# )
select_sdr = "HackRF"
NFFT = st.sidebar.slider(
    label="N FFT",
    min_value=4,
    max_value=1024,
    step=1,
    value=settings.INIT_NFFT,
)
noverlap = st.sidebar.slider(
    label="N overlap",
    min_value=0,
    max_value=NFFT,
    step=2,
    value=settings.INIT_NOVERLAP,
)
detrend = st.sidebar.selectbox(
    "Detrend",
    ("none", "mean", "linear")
)

sdr = get_sdr(select_sdr)
center_freq = st.slider(
    label="F_0 (МГц)",
    min_value=10,
    max_value=5990,
    step=10,
    value=settings.INIT_CENTER_FREQ_M,
)
sdr.set_center_freq(center_freq)
graph_placeholder = st.empty()

while True:

    res = sdr.get_graphs(NFFT, detrend, noverlap)
    graph_placeholder.pyplot(res)
