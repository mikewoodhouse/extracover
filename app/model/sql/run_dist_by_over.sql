/*
	For balls where no wicket fell and no extra was conceded, return the
	frequency for each batsman score for each over
*/
WITH 
	legit_balls AS (
	SELECT
	  over
	, batter_runs AS runs
	FROM balls
	WHERE LENGTH(extra_type) = 0
	AND NOT wicket_fell
)
SELECT
	over
,	(SUM(CASE WHEN runs = 0 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "0"
,	(SUM(CASE WHEN runs = 1 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "1"
,	(SUM(CASE WHEN runs = 2 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "2"
,	(SUM(CASE WHEN runs = 3 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "3"
,	(SUM(CASE WHEN runs = 4 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "4"
,	(SUM(CASE WHEN runs = 5 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "5"
,	(SUM(CASE WHEN runs = 6 THEN 1 END) + 0.0) / SUM(Count(*)) OVER (PARTITION BY over) AS "6"
FROM
	legit_balls
GROUP BY over
ORDER BY over
