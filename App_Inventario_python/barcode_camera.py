from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import numpy as np
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image
import streamlit as st

class BarcodeScannerTransformer(VideoTransformerBase):
    def __init__(self):
        self.last_code = None
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        pil_img = Image.fromarray(img)
        codes = pyzbar_decode(pil_img)
        if codes:
            self.last_code = codes[0].data.decode('utf-8')
        return img

def escanear_codigo_camara():
    st.info("Haz clic en 'Iniciar cámara' y muestra el código de barras frente a la cámara.")
    ctx = webrtc_streamer(key="barcode", video_transformer_factory=BarcodeScannerTransformer)
    if ctx.video_transformer and ctx.video_transformer.last_code:
        st.success(f"Código detectado: {ctx.video_transformer.last_code}")
        return ctx.video_transformer.last_code
    return None
