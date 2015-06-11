-- Table definitions for the tournament project.

-- drop database if it already exists
drop database if exists tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players(
	P_Id SERIAL,
	Name varchar(255) NOT NULL,
	PRIMARY KEY(P_Id)
);

--Unused in tournament.py, used to keep track of multiple tournaments
CREATE TABLE Tournaments(
	T_Id SERIAL,
	T_Name varchar(255),
	PRIMARY KEY(T_Id)
);

CREATE TABLE Matches(
	P_Id_1 int NOT NULL,
	P_Id_2 int NOT NULL,
	WonGame bit, -- 1: player_id1 won; 0: player_id1 did not win
	Draw bit, -- 1: draw; 0: not draw
	PRIMARY KEY(P_Id_1, P_Id_2),
	FOREIGN KEY(P_Id_1) REFERENCES Players,
	FOREIGN KEY(P_Id_2) REFERENCES Players
);

--Unused in tournament.py, used to keep track of multiple tournaments
CREATE TABLE Matches_Multi_Tournament(
	P_Id_1 int NOT NULL,
	P_Id_2 int NOT NULL,
	T_Id int NOT NULL,
	WonGame bit, -- 1: player_id1 won; 0: player_id1 did not win
	Draw bit, -- 1: draw; 0: not draw
	PRIMARY KEY(P_Id_1, P_Id_2, T_Id),
	FOREIGN KEY(P_Id_1) REFERENCES Players,
	FOREIGN KEY(P_Id_2) REFERENCES Players,
	FOREIGN KEY(T_Id) REFERENCES Tournaments
);

CREATE VIEW PlayerCount AS 
	SELECT COUNT(Players.P_Id) 
	FROM Players;
