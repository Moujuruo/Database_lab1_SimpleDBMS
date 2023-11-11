import streamlit as st
import pymysql
import time
import pandas as pd

st.set_page_config(
    page_title="常用查询",
    page_icon="🎬",
    layout="wide"
)

select_query = st.selectbox(
    "请选择查询内容",
    ("查询获奖最多的电影", "查询票房最高的电影", "查询拍摄电影最多的导演", "超过N条影评的电影数量"))
st.session_state['select_query'] = select_query

if select_query == "查询票房最高的电影":
    # sql = f"SELECT Title, BoxOffice FROM Movies ORDER BY BoxOffice DESC LIMIT 10"
    # 这里用视图 topmovies
    Number = st.number_input("输入电影数目", min_value=1, max_value=100, value=1)

    if st.button("创建视图"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            sql = f"""
                CREATE VIEW TopMovies AS
                SELECT MovieID, Title, BoxOffice
                FROM Movies
                ORDER BY BoxOffice DESC
                LIMIT {Number};
            """
            cursor.execute(sql)
            conn.commit()
            st.success('创建成功！')
        except Exception as e:
            st.error('创建失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
    if st.button("删除视图"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            sql = f"DROP VIEW topmovies"
            cursor.execute(sql)
            conn.commit()
            st.success('删除成功！')
        except Exception as e:
            st.error('删除失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
    if st.button("使用视图查询"):
        sql = f"SELECT * FROM topmovies"
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            # 记录一下查询花费的时间
            start_time = time.time()
            cursor.execute(sql)
            results = cursor.fetchall()
            end_time = time.time()
            if results:
                # sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = 'Movies'"
                # cursor.execute(sql_column)
                # query_columns = [item[0] for item in cursor.fetchall()]
                query_columns = ['MovieID', 'Title', 'BoxOffice']
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
                st.session_state['query_time_view'] = end_time - start_time
                st.success(f'查询成功！查询时间：{end_time - start_time}秒')
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()

    if st.button("不使用视图查询"):
        sql = f"SELECT MovieID, Title, BoxOffice FROM Movies ORDER BY BoxOffice DESC LIMIT {Number}"
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            # 记录一下查询花费的时间
            start_time = time.time()
            cursor.execute(sql)
            results = cursor.fetchall()
            end_time = time.time()
            if results:
                # sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = 'Movies'"
                # cursor.execute(sql_column)
                # query_columns = [item[0] for item in cursor.fetchall()]
                query_columns = ['MovieID', 'Title', 'BoxOffice']
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
                st.session_state['query_time_no_view'] = end_time - start_time
                st.success(f'查询成功！查询时间：{end_time - start_time}秒')
                if 'query_time_view' in st.session_state:
                    st.success(f'对比使用视图查询的时间为：{st.session_state["query_time_view"]}秒')
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()

if select_query == "查询获奖最多的电影":
    Number = st.number_input("输入电影数目", min_value=1, max_value=100, value=1)
    if st.button("创建视图"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            sql = f"""
                CREATE VIEW mostawardedmovie AS
                SELECT m.MovieID, m.Title, COUNT(*) AS AwardCount, GROUP_CONCAT(a.Name) AS AwardNames
                FROM Movies m
                JOIN MovieAwards ma ON m.MovieID = ma.MovieID
                JOIN Awards a ON ma.AwardID = a.AwardID
                GROUP BY m.MovieID, m.Title
                ORDER BY AwardCount DESC
                LIMIT {Number};
            """
            cursor.execute(sql)
            conn.commit()
            st.success('创建成功！')
        except Exception as e:
            st.error('创建失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
    if st.button("删除视图"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            sql = f"DROP VIEW mostawardedmovie"
            cursor.execute(sql)
            conn.commit()
            st.success('删除成功！')
        except Exception as e:
            st.error('删除失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
    if st.button("使用视图查询"):
        sql = f"SELECT * FROM mostawardedmovie"
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            # 记录一下查询花费的时间
            start_time = time.time()
            cursor.execute(sql)
            results = cursor.fetchall()
            end_time = time.time()
            if results:
                # sql_column = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{st.session_state['db']}' AND TABLE_NAME = 'Movies'"
                # cursor.execute(sql_column)
                # query_columns = [item[0] for item in cursor.fetchall()]
                query_columns = ['MovieID', 'Title', 'AwardCount', 'AwardNames']
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
                st.session_state['query_time_view'] = end_time - start_time
                st.success(f'查询成功！查询时间：{end_time - start_time}秒')
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
    
    # if st.button("不使用视图查询"):
    sql = f"""
            SELECT m.MovieID, m.Title, COUNT(*) AS AwardCount, GROUP_CONCAT(a.Name) AS AwardNames
            FROM Movies m
            JOIN MovieAwards ma ON m.MovieID = ma.MovieID
            JOIN Awards a ON ma.AwardID = a.AwardID
            GROUP BY m.MovieID, m.Title
            ORDER BY AwardCount DESC
            LIMIT {Number};
        """
    if st.button("不使用视图查询"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            # 记录一下查询花费的时间
            start_time = time.time()
            cursor.execute(sql)
            results = cursor.fetchall()
            end_time = time.time()
            if results:
                # query_columns = [item[0] for item in cursor.fetchall()]
                query_columns = ['MovieID', 'Title', 'AwardCount', 'AwardNames']
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
                st.session_state['query_time_no_view'] = end_time - start_time
                st.success(f'查询成功！查询时间：{end_time - start_time}秒')
                if 'query_time_view' in st.session_state:
                    st.success(f'对比使用视图查询的时间为：{st.session_state["query_time_view"]}秒')
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()

if select_query == "查询拍摄电影最多的导演":
    Number = st.number_input("输入导演数目", min_value=1, max_value=100, value=1)
    sql = f'''
        SELECT d.DirectorID, d.Name,  MovieCount
        FROM Directors d
        JOIN (
            SELECT DirectorID, COUNT(*) AS MovieCount
            FROM Movies
            GROUP BY DirectorID
            ORDER BY MovieCount DESC
            LIMIT {Number}
        ) AS top_directors ON d.DirectorID = top_directors.DirectorID
        GROUP BY d.DirectorID, d.Name
        ORDER BY MovieCount DESC;
        '''
    if st.button("确认查询"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                query_columns = ["DirectorID", "Name", "MovieCount"]
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()

if select_query == "超过N条影评的电影数量":
    Number = st.number_input("输入影评数目", min_value=1, max_value=100, value=1)
    sql = f'''
        SELECT m.Title, COUNT(r.ReviewID) AS ReviewCount
        FROM Movies m
        LEFT JOIN Reviews r ON m.MovieID = r.MovieID
        GROUP BY m.MovieID
        HAVING ReviewCount > {Number}
        ORDER BY ReviewCount DESC;
        '''
    if st.button("确认查询"):
        try:
            # 使用共享变量
            conn = st.session_state['conn']
            cursor = st.session_state['cursor']
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                query_columns = ["Title", "ReviewCount"]
                df = pd.DataFrame(results, columns=query_columns)
                st.write(df)
        except Exception as e:
            st.error('查询失败！')
            st.error(e)
            conn.rollback()
        finally:
            cursor.close()
            # st.session_state['conn'].close()
            st.session_state['cursor'] = st.session_state['conn'].cursor()
