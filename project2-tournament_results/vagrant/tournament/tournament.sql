-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



CREATE DATABASE tournament;

\c tournament;

CREATE TABLE Players(
	P_Id SERIAL,
	Name varchar(255) NOT NULL,
	PRIMARY KEY(P_Id)
);

--Unused in tournament.py
CREATE TABLE Tournaments(
	T_Id SERIAL,
	T_Name varchar(255),
	PRIMARY KEY(T_Id)
);

CREATE TABLE Matches(
	P_Id_1 int NOT NULL,
	P_Id_2 int NOT NULL,
	GameResult int, -- 1= player_id1 won, 0=player_id2 or draw
	Draw int, --0 = not draw, 1 = draw
	PRIMARY KEY(P_Id_1, P_Id_2),
	FOREIGN KEY(P_Id_1) REFERENCES Players,
	FOREIGN KEY(P_Id_2) REFERENCES Players
);

--Unused in tournament.py
CREATE TABLE Matches_Multi_Tournament(
	P_Id_1 int NOT NULL,
	P_Id_2 int NOT NULL,
	T_Id int NOT NULL,
	GameResult int, -- 1= player_id1 won, 0=player_id2 or draw
	Draw int, --0 = not draw, 1 = draw
	PRIMARY KEY(P_Id_1, P_Id_2, T_Id),
	FOREIGN KEY(P_Id_1) REFERENCES Players,
	FOREIGN KEY(P_Id_2) REFERENCES Players,
	FOREIGN KEY(T_Id) REFERENCES Tournaments
);
