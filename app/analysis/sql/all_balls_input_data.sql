WITH
  train_matches AS (
    SELECT
      rowid      AS train_match_id
    , start_date
    FROM
      matches
    WHERE
      START_DATE <= :max_match_date
  )
SELECT
  innings
, over
, CAST(bowled_by AS INTEGER) AS bowler_id
, CAST(batter AS INTEGER)    AS batter_id
, wickets_down
, wicket_fell
, CASE
    WHEN extra_type = 'wide' THEN 1
    ELSE 0
  END AS wide
, CASE
    WHEN extra_type = 'noball' THEN 1
    ELSE 0
  END AS noball
, batter_runs
FROM
  all_balls
  JOIN train_matches ON match_id = train_match_id
WHERE
  innings < 2
ORDER BY
  start_date
, innings
, over
, ball