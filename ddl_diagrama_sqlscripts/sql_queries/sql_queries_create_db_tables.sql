IF DB_ID('platforms_database') IS NULL
   CREATE DATABASE platforms_database;
go
USE platforms_database;
go
if OBJECT_ID('paises') IS NULL
	CREATE TABLE paises(
			id INTEGER IDENTITY,
			alpha2_iso_code VARCHAR(2) NOT NULL UNIQUE,
			PRIMARY KEY (id)
			)
go
if OBJECT_ID('plataformas') IS NULL
	CREATE TABLE plataformas(
			id INTEGER IDENTITY,
			nombre VARCHAR(40) NOT NULL,
			PRIMARY KEY (id)
			)
go
CREATE NONCLUSTERED INDEX I_plataformas_id ON plataformas(id);
go
if OBJECT_ID('contenidos') IS NULL
	CREATE TABLE contenidos(
			content_id VARCHAR(50) NOT NULL,
			platform_id INTEGER FOREIGN KEY REFERENCES plataformas(id),
			title VARCHAR(250) NOT NULL,
			"type" VARCHAR(5),
			director VARCHAR(50),
			"cast" TEXT,
			country_id INTEGER FOREIGN KEY REFERENCES paises(id),
			date_added DATE,
			"year" INTEGER,
			rating VARCHAR(20),
			duration INTEGER,
			genres VARCHAR(250),
			"description" TEXT,
			seasons INTEGER);
go
CREATE INDEX I_content_content_platform_ids ON contenidos(content_id, platform_id);
go
ALTER TABLE contenidos ADD CONSTRAINT CK_contenido_year CHECK ("year" <= YEAR(getdate()) and "year" >= 1800);
ALTER TABLE contenidos ADD CONSTRAINT CK_date_added CHECK (date_added <= FORMAT(getdate(), 'yyyy-MM-dd'));
ALTER TABLE contenidos ADD CONSTRAINT CK_duration CHECK (duration > 0);
ALTER TABLE contenidos ADD CONSTRAINT CK_seasons CHECK (seasons > 0);
ALTER TABLE contenidos ADD CONSTRAINT CK_tipos CHECK ("type" IN('movie', 'serie'));
