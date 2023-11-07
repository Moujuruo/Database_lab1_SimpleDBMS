import streamlit as st

st.set_page_config(
    page_title="MovieComment",
    page_icon="🎬",
)

st.title('影评数据库管理系统 🎬')
st.header('欢迎来到影评数据库管理系统！🎬 ')

st.sidebar.success('Please select a page on the left.')

st.markdown(
    '''
    ## 📜 Introduction
    This is a simple management system for the MovieComment 🎬 database. It is built with [Streamlit](https://streamlit.io/), a Python library for building data apps. 
    这是一个简单的电影评论数据库管理系统。它是用 [Streamlit](https://streamlit.io/) 构建的，Streamlit 是一个用于构建数据应用的 Python 库。
    '''
)