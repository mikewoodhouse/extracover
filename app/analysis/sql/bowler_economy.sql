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
      balls b
      JOIN included_matches m ON m.rowid = b.match_id
    WHERE
      b.innings < 2
      AND b.extra_type = ''
      AND NOT b.wicket_fell
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
      COUNT(*) >= :min_balls_bowled
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
      COUNT(*) >= :min_balls_bowled_in_over
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