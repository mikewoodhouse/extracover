/*
	Scoring shot frequencies by batsman & over, for players having faced  
	enough deliveries to get usual distributions (first attempt: 1000 balls faced)
*/

WITH 
in_batsmen AS (
	SELECT
	  seq
	, batter AS batter_id
	, striker_name AS batter_name
	FROM all_balls
-- if non-striker balls also contribute to qualification
--	UNION ALL
--	SELECT
--	  seq
--	, non_striker AS batter_id
--	, non_striker_name AS batter_name
--	FROM all_balls
)
, qualifying_batters AS (
	SELECT
		batter_id
	,	batter_name
	FROM
		in_batsmen
	GROUP BY batter_id, batter_name
	HAVING Count(*) > 1000
)
, legit_balls AS (
	SELECT
	  over
	, striker_name
	, batter_id
	, batter_runs AS runs
	FROM all_balls
	JOIN qualifying_batters ON batter_id = batter
	WHERE LENGTH(extra_type) = 0
)
SELECT
	striker_name
,	batter_id
, 	over
,	(SUM(CASE WHEN runs = 0 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "0"
,	(SUM(CASE WHEN runs = 1 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "1"
,	(SUM(CASE WHEN runs = 2 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "2"
,	(SUM(CASE WHEN runs = 3 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "3"
,	(SUM(CASE WHEN runs = 4 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "4"
,	(SUM(CASE WHEN runs = 5 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "5"
,	(SUM(CASE WHEN runs = 6 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY striker_name, over) AS "6"
FROM
	legit_balls
GROUP BY striker_name, over, batter_id
ORDER BY striker_name, batter_id, over
