import streamlit as st
import pymysql
import pandas as pd

st.set_page_config(
    page_title="展示表内容",
    page_icon="🎬",
    layout="wide"
)

select_table, Input_page , next_button, enter = st.columns([1, 1, 1, 1])

with Input_page:
    input_page = st.number_input("输入页数", min_value=1, max_value=100, value=1)

with select_table:
    select = st.selectbox(
        "选择表",
        ("Reviews", "Characters", "Movies", "Directors", "ProductionCompanies", "users", "Actors", "Awards", "movieawards")
    )
    st.session_state['select'] = select

page_size = 10

# 切换完表后，重置页数
if st.session_state['select'] != select:
    st.session_state['page'] = 0
    st.session_state['select'] = select

with next_button:
    if st.button("上一页"):
        if st.session_state['page'] > 0:
            st.session_state['page'] -= 1

with next_button:
    if st.button("下一页"):
        st.session_state['page'] += 1

with next_button:
    if st.button("确认"):  
        st.session_state['page'] = input_page - 1

sql = f"SELECT * FROM {select} LIMIT %s OFFSET %s"
offset = st.session_state['page'] * page_size
st.write(f"当前页数：{st.session_state['page'] + 1}")


try:
    # 使用共享变量
    conn = st.session_state['conn']
    cursor = st.session_state['cursor']
    # sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{select}'"
    sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = '{select}'"
    cursor.execute(sql_column)
    columns_name = [item[0] for item in cursor.fetchall()]
    # st.write(columns_name)
    cursor.execute(sql, (page_size, offset))
    results = cursor.fetchall()
    if results:
        df = pd.DataFrame(results, index=[i + 1 for i in range(len(results))])
        df.columns = columns_name
        st.table(df)
    else:
        st.warning("没有更多数据了！")
    
except Exception as e:
    st.error(e)
    conn.rollback()

finally:
    cursor.close()
    st.session_state['cursor'] = st.session_state['conn'].cursor()
        