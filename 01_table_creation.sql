--. creating staging table

DROP TABLE IF EXISTS author_stage;
CREATE TABLE author_stage (
     name 		    VARCHAR(75) 		    NOT NULL
   , born 	        VARCHAR(500)   			NOT NULL
   , description    VARCHAR(9000000)  	  	NOT NULL
);


DROP TABLE IF EXISTS quote_stage;
CREATE TABLE quote_stage (
     quote 	         VARCHAR(9000000)    NOT NULL
   , author 	     VARCHAR(75) 	     NOT NULL
);

DROP TABLE IF EXISTS tag_stage;
CREATE TABLE tag_stage (
	tag_list          VARCHAR(75)         NOT NULL
  , quote             VARCHAR(9000000)    NOT NULL
);


--.table creation 
DROP TABLE IF EXISTS author;
	CREATE TABLE author (
	  author_id       SERIAL 				PRIMARY KEY
	, name 			  VARCHAR(75) 	      	NOT NULL 
	, born 	          VARCHAR(500) 			NOT NULL 
	, description 	  VARCHAR(9000000)    	NOT NULL 
);


DROP TABLE IF EXISTS quote;
	CREATE TABLE quote (
	  quote_id		SERIAL 				    PRIMARY KEY
	, quote 		VARCHAR(9000000) 		NOT NULL 
	, author_id     INTEGER           		NOT NULL, FOREIGN KEY (author_id) REFERENCES	author (author_id)
);


DROP TABLE IF EXISTS tag;
	CREATE TABLE tag (
	  tag  		    VARCHAR(75) 	    NOT NULL 
	, quote_id      INTEGER 			NOT	NULL, FOREIGN KEY (quote_id) REFERENCES quote (quote_id) 
		
	, PRIMARY KEY(tag, quote_id) 
);



