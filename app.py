import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 页面配置 ---
st.set_page_config(page_title="PhotoVibe - AI文案助手", page_icon="📸")

st.title("📸 PhotoVibe: 让你的照片会说话")
st.write("上传一张照片，AI帮你生成适合朋友圈/小红书的文案。")

# --- 侧边栏：设置 ---
with st.sidebar:
    st.header("设置")
    # 优先尝试从云端 Secrets 读取 Key
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ API Key 已从云端加载")
    else:
        api_key = st.text_input("请输入 Google Gemini API Key", type="password")
        st.markdown("[点击这里获取免费 API Key](https://aistudio.google.com/app/apikey)")

# --- 主界面 ---
uploaded_file = st.file_uploader("选择一张照片...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示图片
    image = Image.open(uploaded_file)
    st.image(image, caption='已上传照片', use_container_width=True)

    if api_key:
        if st.button("✨ 生成高赞文案"):
            with st.spinner('AI 正在观察你的照片并构思文案...'):
                try:
                    # 【核心修正1】配置 API (兼容性写法)
                    genai.configure(api_key=api_key)

                    # 【核心修正2】使用稳定版模型名称
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    prompt = """
                    你是一位拥有百万粉丝的资深摄影博主。请仔细观察这张照片。
                    请创作 7 条不同风格的中文社交媒体文案 (每条之间请换行，清晰分隔)：

                    1. 📖 **文艺叙事风**：适合发朋友圈，带点淡淡的情绪。不过不要矫揉造作
                    2. ⚡ **硬核参数风**：评价拍摄手法、光影，适合展示专业能力。
                    3. 😎 **幽默/松弛感**：简短有趣，适合小红书。
                    4. 📷 **摄影文艺**：需要文字能反映出自身摄影品味，淡淡的大师感
                    5. 📜 **诗歌文艺**：给两三句小短诗，符合文青范儿
                    6. 🏆 **摄影大师视角**：以著名摄影大师的风格口吻点评，例如alex webb，森山大道，杉本博司等等
                    7. 🖋️ **文学跨界**：以例如史铁生或者著名欧美作家的口吻进行视觉通感描述

                    注意：
                    - 产出的文案不要太长，适合社交媒体快速阅读。
                    - 不要一眼让人看出来像AI写的，要自然。
                    - 每个文案后需要换行。

                    最后，给出 5 个相关的热门 Hashtag。
                    """

                    response = model.generate_content([prompt, image])

                    st.success("生成成功！")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"出错了: {e}")
    else:
        st.info("👈 请先在左侧输入 API Key。")