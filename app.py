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
                    st.error(f"出错啦: {e}")