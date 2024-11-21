WITH
  non_extra_balls AS (
    SELECT
      *
    FROM
      balls
    WHERE
      innings < 2
      AND extra_type = ''
  )
, all_by_over_avgs AS (
    SELECT
      over
    , COUNT(*)
    , SUM(CAST(batter_runs AS FLOAT)) / COUNT(*) AS avg_runs
    FROM
      non_extra_balls
    GROUP BY
      over
  )
, bowlers AS (
    SELECT
      bowled_by AS bowler
    FROM
      non_extra_balls
    GROUP BY
      bowled_by
    HAVING
      COUNT(*) >= 500
  )
, bowler_by_over_avgs AS (
    SELECT
      b.bowler
    , x.over
    , COUNT(*)
    , SUM(CAST(x.batter_runs AS FLOAT)) / COUNT(*) AS bowler_avg_runs
    FROM
      non_extra_balls x
      JOIN bowlers b ON x.bowled_by = b.bowler
    GROUP BY
      b.bowler
    , x.over
    HAVING
      COUNT(*) >= 10
  )
, bowler_by_over_diffs AS (
    SELECT
      b.bowler
    , b.over
    , b.bowler_avg_runs - a.avg_runs AS over_agg
    FROM
      all_by_over_avgs a
      JOIN bowler_by_over_avgs b ON a.over = b.over
  )
SELECT
  bowler
, AVG(over_agg) AS economy
FROM
  bowler_by_over_diffs
GROUP BY
  bowler