import numpy as np
import streamlit as st
from PIL import Image
import torch
import json

st.set_page_config(page_title="YoloV5 Demo", layout="wide")


@st.cache
def load_model(path):
    return torch.hub.load('ultralytics/yolov5', 'custom', path=path)


def load_img(img: Image.Image) -> np.ndarray:
    return np.array(img)


s_model = load_model("weights/best_yolov5s300.pt")
m_model = load_model("weights/best_yolov5m300.pt")
l_model = load_model("weights/best_yolov5l300.pt")

st.title("Signature Detection Demo using YoloV5")
st.caption("By Solan Delvenne")

st.markdown("""
This a demo showcasing 3 different YOLO Image detection models. All trained on the same parameters.

Models: yolov5s, yolov5m, yolov5l

Epochs: 300
""")

sb = st.sidebar
with sb:
    img_buff = st.file_uploader(
        label="Load a document to scan.",
        type=["png", "jpg", "tif", "bmp"]
    )

    if img_buff:
        img = Image.open(img_buff).convert('RGB')
        s_img = img.copy()
        m_img = img.copy()
        l_img = img.copy()
        st.image(img)

c1, c2, c3 = st.columns(3)

with c1:
    st.header("yolov5s")
    if img_buff:
        s_res = s_model(load_img(s_img))
        s_sigs = json.loads(s_res.pandas().xyxy[0].to_json(orient="records"))
        s_res.render()
        st.image(s_res.imgs[0])
        st.markdown(f"**Signatures**: {len(s_sigs)}")
        for sign in s_sigs:
            st.json(sign)


with c2:
    st.header("yolov5m")
    if img_buff:
        m_res = m_model(load_img(m_img))
        m_sigs = json.loads(m_res.pandas().xyxy[0].to_json(orient="records"))
        m_res.render()
        st.image(m_res.imgs[0])
        st.markdown(f"**Signatures**: {len(m_sigs)}")
        for sign in m_sigs:
            st.json(sign)

with c3:
    st.header("yolov5l")
    if img_buff:
        l_res = l_model(load_img(l_img))
        l_sigs = json.loads(l_res.pandas().xyxy[0].to_json(orient="records"))
        l_res.render()
        st.image(l_res.imgs[0])
        st.markdown(f"**Signatures**: {len(l_sigs)}")
        for sign in l_sigs:
            st.json(sign)
