import streamlit as st
import pymysql
import pandas as pd
import datetime

st.set_page_config(
    page_title="修改表内容",
    page_icon="🎬",
    layout="wide"
)

select = st.selectbox(
        "选择表",
        ("Reviews", "Characters", "Movies", "Directors", "ProductionCompanies", "users", "Actors", "Awards", "movieawards")
    )
st.session_state['select'] = select

if select == "Directors":
    directorName = st.text_input("导演名字")
    Birthday = st.date_input("出生日期", datetime.date(1990, 1, 1))
    Nationality = st.text_input("国籍")

    # directorID是主键
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            sql = f"INSERT INTO `Directors` (`Name`, `Birthday`, `Nationality`) VALUES ('{directorName}', '{Birthday}', '{Nationality}')"
            cursor.execute(sql)
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "Reviews":
    # Content内容可能比较多，所以用text_area
    Content = st.text_area("评论内容")
    Rating = st.slider(
        "评分",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
    )
    MovieName = st.text_input("电影名字")
    PublicDate = st.date_input("评论日期", datetime.date(2021, 1, 1))
    PublicTime = st.time_input("评论时间", datetime.time(12, 0, 0))
    PublicDate = datetime.datetime.combine(PublicDate, PublicTime)
    Username = st.text_input("用户名")
    # 要用MovieName去查MovieIDm，要用Username去查UserID
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            # 若查不到MovieID或UserID，要报错
            # sql = f"INSERT INTO `Reviews` (`Content`, `Rating`, `MovieID`, `PublicationDate`, `UserID`) VALUES ('{Content}', '{Rating}', (SELECT MovieID FROM Movies WHERE Title = '{MovieName}'), '{PublicDate}', (SELECT UserID FROM users WHERE Username = '{Username}'))"
            # cursor.execute(sql)
            # conn.commit()
            # st.success("插入成功")
            cursor.execute("SELECT MovieID FROM Movies WHERE Title = %s", (MovieName,))
            movie_result = cursor.fetchone()
            cursor.execute("SELECT UserID FROM Users WHERE Username = %s", (Username,))
            user_result = cursor.fetchone()

            # 检查是否找到了MovieID和UserID
            if movie_result is None:
                st.error("找不到电影ID。")
                st.stop()  # 提前返回，不执行插入操作
            if user_result is None:
                st.error("找不到用户ID。")
                st.stop()  # 提前返回，不执行插入操作

            # 执行插入操作
            sql = """
            INSERT INTO `Reviews` (`Content`, `Rating`, `MovieID`, `PublicationDate`, `UserID`) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (Content, Rating, movie_result[0], PublicDate, user_result[0]))
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()
    
