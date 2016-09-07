CREATE DATABASE asoiaf;

USE asoiaf;
--Drop Existing Tables
/*
DROP TABLE Locale;
DROP TABLE Death;
DROP TABLE Character;
DROP TABLE Houses;
DROP TABLE Book;
*/
--Create Tables
CREATE TABLE Houses (
  HouseName	VARCHAR(20)	PRIMARY KEY NOT NULL,
  HouseWords	VARCHAR(30)
);

CREATE TABLE Character (
  charID	CHAR(5)	PRIMARY KEY NOT NULL,
  fName		VARCHAR(25)	NOT NULL,
  lName		VARCHAR(25),
  House		VARCHAR(20)	FOREIGN KEY REFERENCES Houses(HouseName),
  title		VARCHAR(20),
  Sex		CHAR(1)	NOT NULL,
  Father	CHAR(5),
  Mother	CHAR(5),
  Liege		CHAR(5),
  KilledBy	CHAR(5),
);

CREATE TABLE Locale (
  localeName	VARCHAR(25)	PRIMARY KEY NOT NULL,
  House	VARCHAR(20)	FOREIGN KEY REFERENCES Houses(HouseName),
  Type	VARCHAR(20)	NOT NULL,
  Owner CHAR(5)	FOREIGN KEY REFERENCES Character(charID),
  Region VARCHAR(25)
);

CREATE TABLE Book (
  bookTitle VARCHAR(30) PRIMARY KEY NOT NULL,
  bookOrder TINYINT UNIQUE NOT NULL,
  release INT
);

CREATE TABLE Death(
  charID  CHAR(5) PRIMARY KEY FOREIGN KEY REFERENCES Character(charID),
  bookTitle VARCHAR(30) NOT NULL FOREIGN KEY REFERENCES Book(bookTitle)
);

--INSERT Book
INSERT INTO Book VALUES('Pre-Game', 0, 0);
INSERT INTO Book VALUES('A Game of Thrones', 1, 1996);
INSERT INTO Book VALUES('A Clash of Kings', 2, 1998);
INSERT INTO Book VALUES('A Storm of Swords', 3, 2000);
INSERT INTO Book VALUES('A Feast for Crows', 4, 2005);
INSERT INTO Book VALUES('A Dance with Dragons', 5, 2011);
INSERT INTO Book VALUES('The Winds of Winter', 6, null);
INSERT INTO Book VALUES('A Dream of Spring', 7, null);
INSERT INTO Book VALUES('The Hedge Knight', 12, 1998);
INSERT INTO Book VALUES('The Sworn Sword', 13, 2003);
INSERT INTO Book VALUES('The Mystery Knight', 14, 2010);
INSERT INTO Book VALUES('The Princess and the Queen', 15, 2013);
INSERT INTO Book VALUES('The Rogue Prince', 16, 2014);

--INSERT HOUSES
INSERT INTO Houses VALUES('Targaryen', 'Fire And Blood');
INSERT INTO Houses VALUES('Baratheon', 'Ours Is The Fury');
INSERT INTO Houses VALUES('Stark', 'Winter Is Coming');
INSERT INTO Houses VALUES('Lannister', 'Hear Me Roar');
INSERT INTO Houses VALUES('Tully', 'Family, Duty, Honor');
INSERT INTO Houses VALUES('Martell', 'Unbowed, Unbent, Unbroken');
INSERT INTO Houses VALUES('Greyjoy', 'We Do Not Sow');
INSERT INTO Houses VALUES('Arryn', 'High As Honor');
INSERT INTO Houses VALUES('Tyrell', 'Growing Strong');
INSERT INTO Houses VALUES('Bolton', 'Our Blades Are Sharp');
INSERT INTO Houses VALUES('Frey', '');
INSERT INTO Houses VALUES('Tarly', 'First In Battle');

--INSERT Characters (charID, fName, lName, House, Sex)
--
--INSERT INTO Character VALUES('charID', 'fName',	'lName',	'House',		'Title',   'Sex', 'Father',		'Mother',	'Liege', 	'KilledBy');
--House Baratheon
INSERT INTO Character VALUES('S1002', 'Robert',		'Baratheon', 'Baratheon',	'Lord',  	'M', 	null, 		null,		'S102',		'W1005')
INSERT INTO Character VALUES('S1003', 'Stannis',	'Baratheon', 'Baratheon',	'Lord',  	'M', 	null, 		null,		null,		null)
INSERT INTO Character VALUES ('S1004', 'Renly',		'Baratheon', 'Baratheon',	'Lord',  	'M', 	null, 		null,		null,		'S1003');
INSERT INTO Character VALUES ('S1005', 'Joffrey',	'Baratheon', 'Baratheon',	'Prince',	'M', 	null, 		null,		null,	  	null);
--House Stark
INSERT INTO Character VALUES ('N1002', 'Eddard',	'Stark',	'Stark',		'Lord',  	'M', 	null,		null,		'S1002',	'S1005');
INSERT INTO Character VALUES ('N1003', 'Catelyn',	'Stark',	'Tully',		null , 		'F', 	null,		null,		null,		'R2001');
INSERT INTO Character VALUES ('N1004', 'Robb',		'Stark',	'Stark',		null,  		'M', 	'N1002', 	'N1003',	null,		'N2001');
INSERT INTO Character VALUES ('N1005', 'Sansa',		'Stark',	'Stark',		null,  		'M', 	'N1002', 	'N1003',	null,		null);
INSERT INTO Character VALUES ('N1006', 'Bran',		'Stark',	'Stark',		null,  		'M', 	'N1002', 	'N1003',	null,		null);
INSERT INTO Character VALUES ('N1007', 'Arya',		'Stark',	'Stark',		null,  		'F', 	'N1002', 	'N1003',	null,		null);
INSERT INTO Character VALUES ('N1008', 'Rickon',	'Stark',	'Stark',		null,  		'M', 	'N1002', 	'N1003',	null,		null);
INSERT INTO Character VALUES ('N1009', 'Jon',		 'Snow',	'Stark',		null,  		'M', 	'N1002', 	null,		null,		null);
INSERT INTO Character VALUES ('N1010', 'Theon',		'Greyjoy',	'Stark',		null,  		'M', 	null,  		null,		null,		null);
--House Lannister
INSERT INTO Character VALUES ('W1001', 'Tywin',		'Lannister', 'Lannister',	'Lord',  	'M', 	null, 		null,		'S1002',	null);
INSERT INTO Character VALUES ('W1002', 'Joanna',	'Lannister', 'Lannister',	 null,   	'F', 	null, 		null,		null,		null);
INSERT INTO Character VALUES ('W1004', 'Jamie',		'Lannister', 'Lannister',	 null,   	'M', 	'W1001', 	null,		null,		null);
INSERT INTO Character VALUES ('W1005', 'Cersie',	'Lannister', 'Lannister',	 null,   	'F', 	'W1001', 	null,		null,		null);
INSERT INTO Character VALUES ('W1006', 'Tyrion',	'Lannister', 'Lannister',	'Lord',  	'M', 	'W1001', 	null,		null,		null);
--Bolton
INSERT INTO Character VALUES ('N2000', 'Roose SR',	'Bolton', 'Bolton',			null,  		'M', 	null, 		null,		null,		null);
INSERT INTO Character VALUES ('N2001', 'Roose',		'Bolton', 'Bolton',			'Lord',  	'M', 	'N2000', 	null,		'N1002',	null);
INSERT INTO Character VALUES ('N2001', 'Ramsay',	'Snow', 'Bolton',			null,  		'M', 	'N2001', 	null,		null,		null);
--Frey
INSERT INTO Character VALUES ('R2001', 'Walder',	'Frey', 'Frey',				'Lord', 	'M', 	null, 		null,		null,		null);

--locale
INSERT INTO Locale VALUES('Kings Landing',	'Baratheon', 'City',	'S1002', 'The Crownlands');
INSERT INTO Locale VALUES('Winterfell',		'Stark',	'Castle',	'N1002', 'The North');
INSERT INTO Locale VALUES('The Dreadfort',	'Bolton',	'Castle',	'N2001', 'The North');
INSERT INTO Locale VALUES('Casterly Rock',	'Lannister','Castle',	'W1001', 'The Westerlands');
INSERT INTO Locale VALUES('The Twins',		'Frey',		'Castle',	'R2001', 'The Riverlands');
INSERT INTO Locale VALUES('Storms End',		'Baratheon', 'Castle',	'S1003', 'The Stormlands');
INSERT INTO Locale VALUES('The Twins',		'Frey',		'Castle',	'R2001', 'The Riverlands');
INSERT INTO Locale VALUES('The Twins',		'Frey',		'Castle',	'R2001', 'The Riverlands');
INSERT INTO Locale VALUES('The Twins',		'Frey',		'Castle',	'R2001', 'The Riverlands');
INSERT INTO Locale VALUES('The Twins',		'Frey',		'Castle',	'R2001', 'The Riverlands');

--Death
INSERT INTO Death VALUES('S1002', 'A Game of Thrones');
INSERT INTO Death VALUES('S1005', 'A Storm of Swords');
INSERT INTO Death VALUES('N1002', 'A Game of Thrones');
INSERT INTO Death VALUES('N1003', 'A Storm of Swords');
INSERT INTO Death VALUES('N1004', 'A Storm of Swords');
INSERT INTO Death VALUES('S1004', 'A Clash of Kings');
INSERT INTO Death VALUES('W1002', 'Pre-Game');


ALTER TABLE Character
ADD FOREIGN KEY (father) REFERENCES Character(charID);
ALTER TABLE Character
ADD FOREIGN KEY (mother) REFERENCES Character(charID);
ALTER TABLE Character
ADD FOREIGN KEY (Liege) REFERENCES Character(charID);
ALTER TABLE Character
ADD FOREIGN KEY (killedBy) REFERENCES Character(charID);

GO
CREATE VIEW CharacterByHouseSpoilerFree
AS SELECT TOP (100) PERCENT fName, lName, Sex, House
  FROM Character
  ORDER BY House;

GO
CREATE VIEW LordsOfTheRealm
AS SELECT TOP (100) PERCENT l.Region, l.localeName, c.fName, c.lName
  FROM Character c, Locale l
  WHERE c.title = 'Lord' and l.Owner = c.charID
  ORDER BY Region;

GO
CREATE VIEW NedsLiegeLords
AS SELECT TOP (100) PERCENT c.fName, c.lName, l.localeName, l.Region
    FROM Character c, Locale l
    WHERE c.title = 'Lord' and l.Owner = c.charID and c.Liege = 'N1002' and c.Father != 'N1002'
    ORDER BY c.lname;

GO
CREATE VIEW TrueBornStarkChildren
AS SELECT TOP (100) PERCENT fName, lName
  FROM Character
  WHERE Father = 'N1002' and Mother = 'N1003'
  ORDER BY charID;

GO
CREATE VIEW BastardsOfTheRealm
AS SELECT TOP (100) PERCENT fName, lName
  FROM Character
  WHERE lName = 'Snow'
	or lName = 'Sand'
	or lName = 'Rivers'
	or lName = 'Stone'
	or lName = 'Waters'
	or lName = 'Hill'
	or lName = 'Flowers'
  ORDER BY lName;

GO
CREATE VIEW DeathsAsOf2016
As SELECT TOP (100) PERCENT c.fName, c.lName, d.bookTitle
  FROM Character c, Death d, Book b
  WHERE d.charID = c.charID and d.bookTitle = b.bookTitle and b.release < 2015
  ORDER BY b.bookOrder;
