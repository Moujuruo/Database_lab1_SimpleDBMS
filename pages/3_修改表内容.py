import streamlit as st
import pymysql
import pandas as pd
import datetime

def insert_director():
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

def insert_reviews():
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

st.set_page_config(
    page_title="修改表内容",
    page_icon="🎬",
    layout="wide"
)

select = st.selectbox(
        "选择表",
        ("Reviews", "Characters", "Movies", "Directors", "ProductionCompanies", "Users", "Actors", "Awards", "movieawards")
    )
st.session_state['select'] = select


if select == "Directors":
    insert_director()

if select == "Reviews":
    insert_reviews()
    
    
if select == "Actors":
    ActorName = st.text_input("演员名字")
    Birthday = st.date_input("出生日期", datetime.date(1990, 1, 1))
    Nationality = st.text_input("国籍")

    # directorID是主键
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            sql = f"INSERT INTO `Actors` (`Name`, `Birthday`, `Nationality`) VALUES ('{ActorName}', '{Birthday}', '{Nationality}')"
            cursor.execute(sql)
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "Awards":
    # Name, AwardingOrganization, AwardingDate
    Name = st.text_input("奖项名字")
    AwardingOrganization = st.text_input("颁奖机构")
    AwardingDate = st.date_input("颁奖日期", datetime.date(2021, 1, 1))
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            sql = f"INSERT INTO `Awards` (`Name`, `AwardingOrganization`, `AwardingDate`) VALUES ('{Name}', '{AwardingOrganization}', '{AwardingDate}')"
            cursor.execute(sql)
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "Users":
    # Username, Password, Email, RegistrationDate
    Username = st.text_input("用户名")
    Password = st.text_input("密码")
    Email = st.text_input("邮箱")
    # 检查邮箱格式 xxxx@xxxx.xxx, 用正则
    import re
    if not re.match(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", Email):
        st.error("邮箱格式不正确")
        st.stop()
    
    # 这里用当前时间作为默认值
    RegistrationDate = st.date_input("注册日期", datetime.date.today())
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            sql = f"INSERT INTO `Users` (`Username`, `Password`, `Email`, `RegistrationDate`) VALUES ('{Username}', '{Password}', '{Email}', '{RegistrationDate}') "
            cursor.execute(sql)
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "Characters":
    # Name, MovieName, ActorName
    Name = st.text_input("角色名字")
    MovieName = st.text_input("电影名字")
    ActorName = st.text_input("演员名字")
    # 要用MovieName去查MovieID，要用ActorName去查ActorID
    # 并且要检查是否找到了MovieID和ActorID
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            cursor.execute("SELECT MovieID FROM Movies WHERE Title = %s", (MovieName,))
            movie_result = cursor.fetchone()
            cursor.execute("SELECT ActorID FROM Actors WHERE Name = %s", (ActorName,))
            actor_result = cursor.fetchone()

            # 检查是否找到了MovieID和ActorID
            if movie_result is None:
                st.error("找不到电影ID。")
                st.stop()  # 提前返回，不执行插入操作
            if actor_result is None:
                st.error("找不到演员ID。")
                st.stop()  # 提前返回，不执行插入操作
            # 执行插入操作
            sql = """
            INSERT INTO `Characters` (`Name`, `MovieID`, `ActorID`) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (Name, movie_result[0], actor_result[0]))
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "ProductionCompanies":
    # Name, FoundationDate, Headquarters
    Name = st.text_input("公司名字")
    FoundationDate = st.date_input("成立日期", datetime.date(1990, 1, 1))
    Headquarters = st.text_input("总部")
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            # 在数据库中插入数据
            sql = f"INSERT INTO `ProductionCompanies` (`Name`, `FoundationDate`, `Headquarters`) VALUES ('{Name}', '{FoundationDate}', '{Headquarters}')"
            cursor.execute(sql)
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "movieawards":
    # MovieName, AwardName
    MovieName = st.text_input("电影名字")
    AwardName = st.text_input("奖项名字")
    # 要用MovieName去查MovieID，要用AwardName去查AwardID
    # 并且要检查是否找到了MovieID和AwardID
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            cursor.execute("SELECT MovieID FROM Movies WHERE Title = %s", (MovieName,))
            movie_result = cursor.fetchone()
            cursor.execute("SELECT AwardID FROM Awards WHERE Name = %s", (AwardName,))
            award_result = cursor.fetchone()

            # 检查是否找到了MovieID和AwardID
            if movie_result is None:
                st.error("找不到电影ID。")
                st.stop()  # 提前返回，不执行插入操作
            if award_result is None:
                st.error("找不到奖项ID。")
                st.stop()  # 提前返回，不执行插入操作
            # 执行插入操作
            sql = """
            INSERT INTO `movieawards` (`MovieID`, `AwardID`) 
            VALUES (%s, %s)
            """
            cursor.execute(sql, (movie_result[0], award_result[0]))
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()

if select == "Movies":
    # Title DirectorName ReleaseYear Genre Duration Language Budget BoxOffice ProductionCompanyName
    Title = st.text_input("电影名字")
    DirectorName = st.text_input("导演名字")
    ReleaseYear = st.number_input("上映年份", min_value=1900, max_value=2050, value=2023)
    Genre = st.selectbox(
        "类型",
        ("Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Thriller", "War", "Western", "Other")
    )
    if Genre == "Other":
        Genre = st.text_input("请输入类型")
    Duration = st.number_input("时长", min_value=0, max_value=1000, value=100)
    Language = st.text_input("语言")
    Budget = st.number_input("预算", min_value=0, max_value=1000000000, value=1000000)
    BoxOffice = st.number_input("票房", min_value=0, max_value=1000000000, value=1000000)
    ProductionCompanyName = st.text_input("制作公司名字")
    # 要用DirectorName去查DirectorID，要用ProductionCompanyName去查CompanyID
    # 并且要检查是否找到了DirectorID和CompanyID
    try:
        conn = st.session_state['conn']
        cursor = st.session_state['cursor']
        if st.button("确认插入"):
            cursor.execute("SELECT DirectorID FROM Directors WHERE Name = %s", (DirectorName,))
            director_result = cursor.fetchone()
            cursor.execute("SELECT CompanyID FROM ProductionCompanies WHERE Name = %s", (ProductionCompanyName,))
            productioncompany_result = cursor.fetchone()

            # 检查是否找到了DirectorID和CompanyID
            if director_result is None:
                st.error("找不到导演ID。")
                # st.stop()  # 提前返回，不执行插入操作
            if productioncompany_result is None:
                st.error("找不到制作公司ID。")
                st.stop()  # 提前返回，不执行插入操作
            # 执行插入操作
            sql = """
            INSERT INTO `Movies` (`Title`, `DirectorID`, `ReleaseYear`, `Genre`, `Duration`, `Language`, `Budget`, `BoxOffice`, `CompanyID`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (Title, director_result[0], ReleaseYear, Genre, Duration, Language, Budget, BoxOffice, productioncompany_result[0]))
            conn.commit()
            st.success("插入成功")
    except Exception as e:
        st.error(e)
        conn.rollback()
    finally:
        cursor.close()
        st.session_state['cursor'] = st.session_state['conn'].cursor()