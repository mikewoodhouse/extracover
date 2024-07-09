/*
Base probability per ball that a wicket fell in each over
e.g. in 89963 over-0 balls, 3512 wickets fell
, hence wicket prob per over-0 ball = 3.9038%
 */
SELECT
  over
, SUM(wicket_fell)                    AS wickets
, Count(*)                            AS balls
, (SUM(wicket_fell) + 0.0) / COUNT(*) as pct
FROM
  balls
WHERE
  LENGTH(extra_type) = 0
GROUP BY
  over