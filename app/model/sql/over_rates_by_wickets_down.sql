WITH
  wickets_in_over AS (
    SELECT DISTINCT
      match_id
    , innings
    , 0 AS over
    , 0 AS wickets
    FROM
      balls
    UNION
    SELECT
      b.match_id
    , b.innings
    , b.over
    , SUM(b.wicket_fell) AS wickets
    FROM
      balls b
    GROUP BY
      b.match_id
    , b.innings
    , b.over
  )
, overs AS (
    SELECT
      b.match_id
    , b.innings
    , b.over
    , CAST(
        SUM(b.batter_runs + b.extra_runs) AS FLOAT
      ) * 6 / COUNT(*) AS run_rate
    FROM
      balls b
    GROUP BY
      b.match_id
    , b.innings
    , b.over
  )
, over_numbers AS (
    WITH RECURSIVE
      generate_series (value) AS (
        SELECT
          0
        UNION ALL
        SELECT
          value + 1
        FROM
          generate_series
        WHERE
          value + 1 <= 19
      )
    SELECT
      value AS over
    FROM
      generate_series
  )
SELECT
  w.match_id
, w.innings
, w.over
, SUM(w.wickets)
FROM
  over_numbers n
  LEFT JOIN wickets_in_over w ON n.over > w.over
where
  w.match_id = 1
GROUP BY
  w.match_id
, w.innings
, w.over