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
, first_ball_in_match AS (
    SELECT
      h.match_id
    , b.innings
    , b.batter                    AS player_id
    , MIN(b.over * 1000 + b.ball) AS first_ball_seq
    FROM
      balls b
      JOIN match_history h ON h.match_id = b.match_id
    GROUP BY
      b.batter
    , h.match_id
  )
, positions_batted AS (
    SELECT
      player_id
    , match_id
    , innings
    , RANK() OVER (
        PARTITION BY
          match_id
        , innings
        ORDER BY
          first_ball_seq
      ) AS position
    FROM
      first_ball_in_match
  )
SELECT
  player_id
, position
, COUNT(*)  AS freq
FROM
  positions_batted
GROUP BY
  player_id
, position