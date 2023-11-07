# 这个界面实现streamlit的数据库连接功能 mysql
import streamlit as st
import pymysql
# import foo

st.set_page_config(
    page_title="连接数据库",
    page_icon="🎬",
)

# 在页面中（不是边栏）建立几个输入框，输入host, port, user, password, db
host = st.text_input('host', 'localhost')
port = st.text_input('port', '3306')
user = st.text_input('user', 'root')
password = st.text_input('password', 'root')
# db = st.text_input('db')
db = st.selectbox(
    'db',
    ('company', 'moviecomment', 'atguigudb'),
    1
)

# 点击按钮后，连接数据库
if st.button('连接数据库'):
    db_config = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "db": db
    }
    try:
        # 建立数据库连接
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        # 共享变量
        st.session_state['cursor'] = cursor
        st.session_state['conn'] = conn
        st.session_state['page'] = 0
        st.session_state['db'] = db
        st.success('连接成功！')
    except Exception as e:
        # st.error(e)
        st.error('连接失败！')
        st.write('以下是错误信息')
        st.error(e)
        conn.rollback()
    # finally:
    #     cursor.close()
    #     conn.close()

