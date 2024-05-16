WITH
  over_runs AS (
    SELECT
      over
    , CAST(
        SUM(batter_runs) + SUM(extra_runs) AS FLOAT
      ) AS runs
    FROM
      balls
    WHERE
      innings = 0
    GROUP BY
      match_id
    , over
    HAVING
      MAX(ball) = 5
  )
SELECT
  r.over
, SUM(r.runs) / COUNT(*) AS avg_runs
FROM
  over_runs r
GROUP BY
  r.over
ORDER BY
  r.over