import streamlit as st
import os
import platform
import google.generativeai as genai  # <--- 必须是这个写法！之前手机报错就是因为这里写错了
from PIL import Image

# --- 1. 智能环境配置 ---
if platform.system() == "Windows":
    # 本地运行时挂代理
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# --- 2. 页面配置 ---
st.set_page_config(page_title="PhotoVibe", page_icon="📸")
st.title("📸 PhotoVibe: 让你的照片会说话 (Ver 2.5)")

# --- 3. 侧边栏 ---
with st.sidebar:
    st.header("设置")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ 云端 Key 已加载")
    else:
        api_key = st.text_input("请输入 Key", type="password")

# --- 4. 主程序 ---
uploaded_file = st.file_uploader("选择照片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='已上传', use_container_width=True)

    if st.button("✨ 生成文案"):
        if not api_key:
            st.warning("请先输入 API Key")
        else:
            with st.spinner('AI (Gemini 2.5) 正在思考...'):
                try:
                    # 配置 API
                    genai.configure(api_key=api_key)

                    # 【这里改成了 2.5】
                    # 如果 2.5-flash 报错，可以尝试 'gemini-2.5-pro' 或者 'gemini-2.0-flash'
                    model = genai.GenerativeModel('gemini-2.5-flash')

                    prompt = "你是一位资深摄影博主。请为这张照片写3条不同风格的中文文案（文艺风、硬核风、幽默风），并加上Hashtag。"

                    response = model.generate_content([prompt, image])
                    st.success("生成成功！")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"出错啦: {e}")