
--.insert into author 
INSERT INTO author(name, born, description)
SELECT name, born, description
FROM author_stage
WHERE NOT EXISTS (
	SELECT 1
	FROM author_stage AS t
	INNER JOIN author AS a ON a.name = t.name 
)


--.insert into quote 
INSERT INTO quote (quote, author_id)
SELECT quote, author_id
FROM author
INNER JOIN quote_stage ON quote_stage.author = author.name 
WHERE NOT EXISTS (
	SELECT 1
	FROM quote_stage AS t
	INNER JOIN quote AS q ON q.quote = t.quote 
)


--.insert into tag 
INSERT INTO tag(tag, quote_id)
SELECT tag_list, quote_id
FROM quote
INNER JOIN tag_stage ON tag_stage.quote = quote.quote


--*******--.top 10.--********--
DROP TABLE IF EXISTS top_tags;
	CREATE TABLE top_tags (
		  tag    VARCHAR(100) NOT NULL
		, count  INTEGER      NOT NULL
	);
INSERT INTO top_tags (tag, count)
SELECT tag, COUNT(*) AS ct
FROM tag
GROUP BY tag
ORDER BY ct DESC LIMIT 10;

--.-----Truncate staging tables --.----
TRUNCATE author_stage;
TRUNCATE quote_stage;
TRUNCATE tag_stage;