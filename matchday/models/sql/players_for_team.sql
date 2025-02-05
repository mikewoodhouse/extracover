WITH
    last_match AS (
        SELECT
            p.name
          , p.rowid           AS player_id
          , m.start_date      AS last_match
          , s.match_id        AS last_match_id
          , ROW_NUMBER() OVER (
                PARTITION BY
                    p.rowid
                  , p.name
                ORDER BY
                    m.start_date DESC
            ) AS row_num
        FROM
            players p
            JOIN selections s ON s.player_id = p.rowid
            JOIN teams t ON t.rowid = s.team_id
            JOIN matches m ON m.rowid = s.match_id
        WHERE
            t.name = '{{team_name}}'
    )
SELECT
    lm.name
  , lm.player_id
  , lm.last_match
  , IFNULL (MIN(b.over * 6 + b.ball_seq), 60) AS first_ball_recd
  , IFNULL (MIN(b.over * 6 + w.ball_seq), 60) AS first_ball_bowled
FROM
    last_match lm
    LEFT JOIN balls b ON b.match_id = lm.last_match_id
    AND b.batter = lm.player_id
    LEFT JOIN balls w ON w.match_id = lm.last_match_id
    AND w.bowled_by = lm.player_id
WHERE
    row_num = 1
GROUP BY
    lm.name
  , lm.player_id
  , lm.last_match
ORDER BY
    lm.last_match DESC
  , lm.name;