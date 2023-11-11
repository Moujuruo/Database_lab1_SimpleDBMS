import streamlit as st
import pymysql
import pandas as pd
from streamlit.components.v1 import html

def confirm_delete(Username, conn):
    try:
        with st.session_state['conn'].cursor() as cursor:
            delete_sql = f"DELETE FROM Users WHERE Username = '{Username}'"
            cursor.execute(delete_sql)
            st.session_state['conn'].commit()
            st.success('删除成功！')
            # 删除成功后，我们需要清除session_state中的查询结果
            st.session_state.pop('query_result', None)
            st.session_state.pop('query_columns', None)
    except Exception as e:
        st.error('删除失败！')
        st.session_state.pop('query_result', None)
        st.session_state.pop('query_columns', None)
        st.error(str(e))
        st.session_state['conn'].rollback()
    finally:
        st.session_state['cursor'].close()
        # st.session_state['conn'].close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

def delete_users():
    Username = st.text_input('准备删除的用户名')
    conn = st.session_state['conn']
    cursor = st.session_state['cursor']
    if st.button("增加触发器"):
        sql_trigger = '''
                CREATE TRIGGER before_user_delete
                BEFORE DELETE ON Users FOR EACH ROW
                BEGIN
                    DELETE FROM Reviews WHERE UserID = OLD.UserID;
                END;
        '''
        try:
            cursor.execute(sql_trigger)
            conn.commit()
            st.success('触发器创建成功！')
        except Exception as e:
            st.error('触发器创建失败！')
            st.error(e)
            conn.rollback()
    if st.button("删除触发器"):
        sql_trigger = '''
                DROP TRIGGER before_user_delete;
        '''
        try:
            cursor.execute(sql_trigger)
            conn.commit()
            st.success('触发器删除成功！')
        except Exception as e:
            st.error('触发器删除失败！')
            st.error(e)
            conn.rollback()
    sql = f"SELECT * FROM Users WHERE Username = '{Username}'"
    if st.button("确认查询"):
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                query_result = cursor.fetchall()
                if query_result:
                    sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = 'Users'"
                    cursor.execute(sql_column)
                    query_columns = [item[0] for item in cursor.fetchall()]
                    df = pd.DataFrame(query_result, columns=query_columns)
                    # st.write(df)
                    st.session_state['query_result'] = query_result
                    st.session_state['query_columns'] = query_columns
                    # 提交删除的确认按钮
                    # if st.button('确认删除'):
                        # confirm_delete(Username, conn)
                else:
                    st.error('用户名不存在！')
            except Exception as e:
                st.error('查询失败！')
                st.error(e)
                conn.rollback()
    if 'query_result' in st.session_state and 'query_columns' in st.session_state:
        df = pd.DataFrame(st.session_state['query_result'], columns=st.session_state['query_columns'])
        st.write(df)
        if st.button('确认删除'):
            confirm_delete(Username, conn)

def delete_charactors():
    Charactor_name = st.text_input('准备删除的角色名')
    conn = st.session_state['conn']
    cursor = st.session_state['cursor']
    sql = f"SELECT * FROM Characters WHERE Name = '{Charactor_name}'"
    if st.button("确认查询"):
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                query_result = cursor.fetchall()
                if query_result:
                    sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = 'Characters'"
                    cursor.execute(sql_column)
                    query_columns = [item[0] for item in cursor.fetchall()]
                    df = pd.DataFrame(query_result, columns=query_columns)
                    # st.write(df)
                    st.session_state['query_result'] = query_result
                    st.session_state['query_columns'] = query_columns
                    # 提交删除的确认按钮
                    # if st.button('确认删除'):
                        # confirm_delete(Username, conn)
                else:
                    st.error('角色名不存在！')
            except Exception as e:
                st.error('查询失败！')
                st.error(e)
                conn.rollback()
    if 'query_result' in st.session_state and 'query_columns' in st.session_state:
        df = pd.DataFrame(st.session_state['query_result'], columns=st.session_state['query_columns'])
        st.write(df)
        if st.button('确认删除'):
            try:
                with st.session_state['conn'].cursor() as cursor:
                    delete_sql = f"DELETE FROM Characters WHERE Name = '{Charactor_name}'"
                    cursor.execute(delete_sql)
                    st.session_state['conn'].commit()
                    st.success('删除成功！')
                    # 删除成功后，我们需要清除session_state中的查询结果
                    st.session_state.pop('query_result', None)
                    st.session_state.pop('query_columns', None)
            except Exception as e:
                st.error('删除失败！')
                st.session_state.pop('query_result', None)
                st.session_state.pop('query_columns', None)
                st.error(str(e))
                st.session_state['conn'].rollback()
            finally:
                st.session_state['cursor'].close()
                # st.session_state['conn'].close()
                st.session_state['cursor'] = st.session_state['conn'].cursor()

st.set_page_config(
    page_title="删除表内容",
    page_icon="🎬",
    layout="wide"
)

select = st.selectbox(
        "选择表",
        ("Users", "Characters")
    )
st.session_state['select'] = select


if select == 'Users':
    delete_users()

if select == 'Characters':
    delete_charactors()