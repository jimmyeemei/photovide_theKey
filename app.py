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

                    请创作 30 条不同风格的中文社交媒体文案：

                    1. 📖 **带情绪的夜**：适合发朋友圈，带点淡淡的情绪。不过不要矫揉造作

                    2. ⚡ **评价有毒**：评价拍摄手法、光影，适合展示专业能力。

                    3. 😎 **幽默是我的武器**：简短有趣，适合小红书  。

                    4.**品味摄影**：需要文字能反映出自身摄影品味，淡淡的大师感

                    5.**诗歌文艺**：给两三句小短诗，符合文青范儿

                    6.**聆听大师**：以著名摄影大师的风格口吻点评，例如alex webb，森山大道，杉本博司等等

                    7.**文艺名人**：摄影与文学艺术互通，可以以例如史铁生或者著名欧美作家等的口吻

                    注意产出的文案文字不用那么多，因为需要在社交流媒体上面发帖，不要那么一眼让人看出来像ai写的，每个文案后需要换行
                    **排版严格要求：**
                    - **绝对不要**使用 Markdown 标题语法（即不要在正文中使用 # 或 ## 符号）。
                    - 正文字体大小保持一致。

                    最后，给出 5 个相关的热门 Hashtag。

                    """
                    response = model.generate_content([prompt, image])
                    st.success("生成成功！")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"出错啦: {e}")