import streamlit as st
# import streamlit.components.v1 as components

st.set_page_config(
    page_title="MovieComment",
    page_icon="🎬",
    # layout="wide"
)

st.title('影评数据库管理系统 🎬')
st.header('欢迎来到影评数据库管理系统！🎬 ')

# st.sidebar.success('Please select a page on the left.')

st.markdown(
    '''
    ## 📜 Introduction
    这是一个简单的电影评论数据库管理系统。它是用 [Streamlit](https://streamlit.io/) 构建的，Streamlit 是一个用于构建数据应用的 Python 库。
    '''
)

# 展示本地的一张图片 6.jpg
from PIL import Image
image = Image.open('6.jpg')
st.image(image, caption='阳光普照', use_column_width=True)

