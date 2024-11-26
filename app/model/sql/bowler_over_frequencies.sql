WITH
  match_history AS (
    SELECT DISTINCT
      m.ROWID AS match_id
    FROM
      matches m
      JOIN selections s ON s.match_id = m.rowid
      JOIN tm.players b ON b.player_id = s.player_id
    WHERE
      m.start_date < :start_date
  )
, over_allocs AS (
    SELECT DISTINCT
      b.over
    , b.bowled_by AS player_id
    , b.match_id
    , p.name
    FROM
      balls b
      JOIN match_history m ON m.match_id = b.match_id
      JOIN tm.players p ON b.bowled_by = p.player_id
  )
, over_freqs AS (
    SELECT
      a.over
    , a.player_id
    , a.name
    , count(*)    AS frequency
    FROM
      over_allocs a
    GROUP BY
      a.over
    , a.player_id
  )
SELECT
  *
FROM
  over_freqs