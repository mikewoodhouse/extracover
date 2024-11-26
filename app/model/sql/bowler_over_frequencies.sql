WITH
  match_history AS (
    SELECT DISTINCT
      m.ROWID AS match_id
    FROM
      matches m
      JOIN selections s ON s.match_id = m.rowid
      JOIN tm.players b ON b.player_id = s.player_id
    WHERE
      m.start_date < '2023-08-01'
  )
, overs_by_bowler AS (
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
, total_bowled AS (
    SELECT
      player_id
    , COUNT(*)  AS total_overs_bowled
    FROM
      overs_by_bowler
    GROUP BY
      player_id
  )
, over_freqs AS (
    SELECT
      a.over
    , a.player_id
    , a.name
    , CAST(count(*) AS FLOAT) / total_overs_bowled AS frequency
    FROM
      overs_by_bowler a
      JOIN total_bowled t ON a.player_id = t.player_id
    GROUP BY
      a.over
    , a.player_id
  )
SELECT
  *
FROM
  over_freqs