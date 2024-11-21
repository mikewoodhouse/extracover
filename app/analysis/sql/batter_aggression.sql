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
, batters AS (
    SELECT
      batter
    FROM
      non_extra_balls
    GROUP BY
      batter
    HAVING
      COUNT(*) >= :min_balls_faced
  )
, batter_by_over_avgs AS (
    SELECT
      b.batter
    , x.over
    , COUNT(*)
    , SUM(CAST(x.batter_runs AS FLOAT)) / COUNT(*) AS batter_avg_runs
    FROM
      non_extra_balls x
      JOIN batters b ON x.batter = b.batter
    GROUP BY
      b.batter
    , x.over
    HAVING
      COUNT(*) >= :min_balls_faced_in_over
  )
, batter_by_over_diffs AS (
    SELECT
      b.batter
    , b.over
    , b.batter_avg_runs - a.avg_runs AS over_agg
    FROM
      all_by_over_avgs a
      JOIN batter_by_over_avgs b ON a.over = b.over
  )
SELECT
  batter
, AVG(over_agg) AS aggression
FROM
  batter_by_over_diffs
GROUP BY
  batter