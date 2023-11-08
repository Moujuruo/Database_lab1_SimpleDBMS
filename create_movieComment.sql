-- 创建用户表
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    Email VARCHAR(100),
    RegistrationDate DATETIME NOT NULL
);

-- 创建电影表
CREATE TABLE Movies (
    MovieID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    DirectorID INT,  -- 外键，需要在创建导演表后设置
    ReleaseYear YEAR,
    Genre VARCHAR(50),
    Duration INT,
    Language VARCHAR(50),
    Budget DECIMAL(19, 2),
    BoxOffice DECIMAL(19, 2)
);

-- 创建影评表
CREATE TABLE Reviews (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    Content TEXT NOT NULL,
    Rating DECIMAL(3, 2) NOT NULL,
    PublicationDate DATETIME NOT NULL,
    UserID INT,
    MovieID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);

-- 创建导演表
CREATE TABLE Directors (
    DirectorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Birthday DATE,
    Nationality VARCHAR(50)
);

-- 更新Movies表，添加外键约束
ALTER TABLE Movies
ADD FOREIGN KEY (DirectorID) REFERENCES Directors(DirectorID);

-- 创建演员表
CREATE TABLE Actors (
    ActorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Birthday DATE,
    Nationality VARCHAR(50)
);

-- 创建角色表
CREATE TABLE Characters (
    CharacterID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    ActorID INT,
    MovieID INT,
    FOREIGN KEY (ActorID) REFERENCES Actors(ActorID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);

-- 创建电影公司表
CREATE TABLE ProductionCompanies (
    CompanyID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    FoundationDate DATE,
    Headquarters VARCHAR(100)
);

-- 更新Movies表，添加电影公司外键
ALTER TABLE Movies
ADD COLUMN CompanyID INT,
ADD FOREIGN KEY (CompanyID) REFERENCES ProductionCompanies(CompanyID);

-- 创建奖项表
CREATE TABLE Awards (
    AwardID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    AwardingOrganization VARCHAR(100),
    AwardingDate DATE
);

-- 创建影片与奖项的关联表（多对多关系）
CREATE TABLE MovieAwards (
    MovieID INT,
    AwardID INT,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (AwardID) REFERENCES Awards(AwardID),
    PRIMARY KEY (MovieID, AwardID)
);



-- 添加一个trigger
DELIMITER //
CREATE TRIGGER before_user_delete
BEFORE DELETE ON Users FOR EACH ROW
BEGIN
    DELETE FROM Reviews WHERE UserID = OLD.UserID;
END; //
DELIMITER ;


-- SHOW TRIGGERS

-- DROP TRIGGER before_user_delete;

-- 创建视图
CREATE VIEW TopMovies AS
SELECT MovieID, Title, BoxOffice
FROM Movies
ORDER BY BoxOffice DESC
LIMIT 10;


-- 创建索引
CREATE INDEX idx_BoxOffice ON Movies (BoxOffice);
