WITH
  bowlers AS (
    SELECT
      p.name
    , p.rowid AS player_id
    FROM
      players p
    WHERE
      p.rowid IN (2702, 2717, 374, 1753, 485, 509)
  )
, over_allocs AS (
    SELECT DISTINCT
      b.over
    , b.match_id
    , b.bowled_by
    FROM
      balls b
      JOIN bowlers p ON b.bowled_by = p.player_id
  )
, totals AS (
    SELECT
      p.player_id
    , p.name
    , CAST(Count(*) AS FLOAT) AS overs
    FROM
      bowlers p
      LEFT JOIN over_allocs a
    WHERE
      a.bowled_by = p.player_id
    GROUP BY
      p.player_id
  )
, alloc_counts AS (
    SELECT
      a.over
    , t.name
    , a.bowled_by
    , count(*) / t.overs AS frequency
    FROM
      over_allocs a
      JOIN totals t ON t.player_id = a.bowled_by
    GROUP BY
      a.over
    , a.bowled_by
    , t.name
  )
SELECT
  *
FROM
  alloc_counts