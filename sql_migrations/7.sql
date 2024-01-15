CREATE TABLE "ArticleSimilarity" (
	id INTEGER NOT NULL, 
	"p_articleID" INTEGER NOT NULL, 
	"f_articleID" INTEGER NOT NULL, 
	similarity FLOAT NOT NULL, 
	method VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("p_articleID") REFERENCES "Article" (id), 
	FOREIGN KEY("f_articleID") REFERENCES "Article" (id)
)