/*
	For balls where no wicket fell and no extra was conceded, return the
	frequency for each batsman score for each over
	This is the "baseline" for batters
*/
WITH 
  included_matches AS (
    SELECT
      rowid
    FROM
      matches
    WHERE
      start_date <= :max_match_date
  )
, non_extra_balls AS (
    SELECT
      b.*
    FROM
      all_balls b
      JOIN included_matches m ON m.rowid = b.match_id
    WHERE
      b.innings < 2
      AND b.extra_type = ''
      AND NOT b.wicket_fell
  )
, 
SELECT
	over
,	wickets_down
,	(SUM(CASE WHEN batter_runs = 0 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "0"
,	(SUM(CASE WHEN batter_runs = 1 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "1"
,	(SUM(CASE WHEN batter_runs = 2 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "2"
,	(SUM(CASE WHEN batter_runs = 3 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "3"
,	(SUM(CASE WHEN batter_runs = 4 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "4"
,	(SUM(CASE WHEN batter_runs = 5 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "5"
,	(SUM(CASE WHEN batter_runs = 6 THEN 1.0 END)) / SUM(Count(*)) OVER (PARTITION BY over, wickets_down) AS "6"
FROM
	non_extra_balls
GROUP BY over, wickets_down
ORDER BY over, wickets_down
