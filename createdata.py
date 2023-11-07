import pymysql
from faker import Faker
import random

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password" : "root",
    "db" : "moviecomment"
}


fake = Faker()

try:
    # 建立数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 插入导演数据
    for _ in range(100):  # 增加导演数量
        name = fake.name()
        birthday = fake.date_of_birth().strftime('%Y-%m-%d')
        nationality = fake.country()
        cursor.execute('INSERT INTO Directors (Name, Birthday, Nationality) VALUES (%s, %s, %s)', (name, birthday, nationality))
    conn.commit()

    # 插入电影公司数据
    for _ in range(50):  # 增加电影公司数量
        name = fake.company()
        foundation_date = fake.date_between(start_date='-50y', end_date='today').strftime('%Y-%m-%d')
        headquarters = fake.city()
        cursor.execute('INSERT INTO ProductionCompanies (Name, FoundationDate, Headquarters) VALUES (%s, %s, %s)', (name, foundation_date, headquarters))
    conn.commit()

    # 插入电影数据
    cursor.execute('SELECT DirectorID FROM Directors')
    director_ids = [item[0] for item in cursor.fetchall()]
    cursor.execute('SELECT CompanyID FROM ProductionCompanies')
    company_ids = [item[0] for item in cursor.fetchall()]

    for _ in range(2000):  # 增加电影数量
        title = fake.sentence(nb_words=5)  # 电影名使用更多单词
        director_id = random.choice(director_ids)
        company_id = random.choice(company_ids)
        release_year = random.randint(1980, 2023)
        genre = random.choice(['Drama', 'Comedy', 'Action', 'Horror', 'Sci-Fi'])
        duration = random.randint(80, 180)
        language = random.choice(['English', 'Spanish', 'French', 'German', 'Chinese'])
        budget = round(random.uniform(1e6, 1e8), 2)
        box_office = round(budget * random.uniform(1.0, 3.0), 2)
        cursor.execute('INSERT INTO Movies (Title, DirectorID, ReleaseYear, Genre, Duration, Language, Budget, BoxOffice, CompanyID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (title, director_id, release_year, genre, duration, language, budget, box_office, company_id))
    conn.commit()

    # 插入奖项数据
    for _ in range(50):  # 插入更多奖项
        name = fake.catch_phrase()
        awarding_organization = random.choice(['Academy Awards', 'Golden Globes', 'BAFTA', 'Cannes Film Festival', 'Venice Film Festival', "Jinji Award", "Hong Kong film Award"])
        awarding_date = fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d')
        cursor.execute('INSERT INTO Awards (Name, AwardingOrganization, AwardingDate) VALUES (%s, %s, %s)', (name, awarding_organization, awarding_date))
    conn.commit()

    # 插入演员数据
    for _ in range(700):  # 增加演员数量
        name = fake.name()
        birthday = fake.date_of_birth().strftime('%Y-%m-%d')
        nationality = fake.country()
        cursor.execute('INSERT INTO Actors (Name, Birthday, Nationality) VALUES (%s, %s, %s)', (name, birthday, nationality))
    conn.commit()

    # 插入用户数据
    for _ in range(200):  # 增加用户数量
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        registration_date = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO Users (Username, Password, Email, RegistrationDate) VALUES (%s, %s, %s, %s)', (username, password, email, registration_date))
    conn.commit()

    # 插入角色数据
    cursor.execute('SELECT MovieID FROM Movies')
    movie_ids = [item[0] for item in cursor.fetchall()]
    cursor.execute('SELECT ActorID FROM Actors')
    actor_ids = [item[0] for item in cursor.fetchall()]

    for _ in range(4000):  # 增加角色数量
        name = fake.name()
        actor_id = random.choice(actor_ids)
        movie_id = random.choice(movie_ids)
        cursor.execute('INSERT INTO Characters (Name, ActorID, MovieID) VALUES (%s, %s, %s)', (name, actor_id, movie_id))
    conn.commit()

    # 插入影评数据
    cursor.execute('SELECT UserID FROM Users')
    user_ids = [item[0] for item in cursor.fetchall()]

    for _ in range(50000):  # 增加影评数量
        content = fake.text(max_nb_chars=500)  # 使用更长的评论
        rating = round(random.uniform(1, 10), 1)
        publication_date = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        user_id = random.choice(user_ids)
        movie_id = random.choice(movie_ids)
        cursor.execute('INSERT INTO Reviews (Content, Rating, PublicationDate, UserID, MovieID) VALUES (%s, %s, %s, %s, %s)', (content, rating, publication_date, user_id, movie_id))
    conn.commit()

    # 插入影片与奖项的关联数据
    cursor.execute('SELECT AwardID FROM Awards')
    award_ids = [item[0] for item in cursor.fetchall()]

    for _ in range(200):  # 创建更多影片与奖项的关联
        movie_id = random.choice(movie_ids)
        award_id = random.choice(award_ids)
        # 为了避免重复，我们检查是否已存在该组合
        cursor.execute('SELECT COUNT(*) FROM MovieAwards WHERE MovieID = %s AND AwardID = %s', (movie_id, award_id))
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO MovieAwards (MovieID, AwardID) VALUES (%s, %s)', (movie_id, award_id))
    conn.commit()

    print("Data insertion complete.")

except pymysql.MySQLError as e:
    print("MySQL Error: ", e)
except Exception as e:
    print("General Error: ", e)
finally:
    if conn.open:
        cursor.close()
        conn.close()