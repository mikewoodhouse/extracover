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
, first_ball_in_match AS (
    SELECT
      h.match_id
    , b.innings
    , b.batter                    AS player_id
    , p.name
    , MIN(b.over * 1000 + b.ball) AS first_ball_seq
    FROM
      balls b
      JOIN match_history h ON h.match_id = b.match_id
      JOIN tm.players p ON b.batter = p.player_id
    GROUP BY
      b.batter
    , h.match_id
  )
, positions_batted AS (
    SELECT
      player_id
    , name
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
, name
, position
, COUNT(*)  AS freq
FROM
  positions_batted
GROUP BY
  player_id
, position
ORDER BY
  player_id
, position