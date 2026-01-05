import streamlit as st
import os
import platform
import google.generativeai as genai # <--- 必须是这个写法
from PIL import Image

# 1. 本地代理 (仅Windows生效)
if platform.system() == "Windows":
    # 如果你本地不用代理也能连通(比如用了VPN全局)，这行其实可以注释掉
    # 但为了保险先留着，注意端口对应
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

st.set_page_config(page_title="PhotoVibe", page_icon="📸")
st.title("📸 PhotoVibe: 让你的照片会说话")

with st.sidebar:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ 云端 Key 已加载")
    else:
        api_key = st.text_input("请输入 Key", type="password")

uploaded_file = st.file_uploader("选择照片", type=["jpg", "png"])

if uploaded_file and st.button("生成文案"):
    if not api_key:
        st.error("请输入 API Key")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            res = model.generate_content(["写一段中文文案", Image.open(uploaded_file)])
            st.write(res.text)
        except Exception as e:

            st.error(f"错误: {e}")
