DROP TABLE IF EXISTS matches;

DROP TABLE IF EXISTS teams;

DROP TABLE IF EXISTS participation;

DROP TABLE IF EXISTS players;

DROP TABLE IF EXISTS selections;

DROP TABLE IF EXISTS balls;

DROP TABLE IF EXISTS people;

CREATE TABLE IF NOT EXISTS
  matches (
    start_date DATE
  , match_type TEXT
  , gender TEXT
  , venue TEXT
  , event TEXT
  , city TEXT
  , overs INTEGER /* because the Hundred */
  , balls_per_over INTEGER /* because the Hundred */
  , file_path TEXT
  );

CREATE TABLE IF NOT EXISTS
  teams (name TEXT NOT NULL, UNIQUE (name));

CREATE TABLE IF NOT EXISTS
  participation (
    match_id INTEGER
  , team_id INTEGER
  , innings INTEGER
  );

CREATE TABLE IF NOT EXISTS
  players (
    name TEXT NOT NULL
  , reg TEXT NOT NULL
  , cricinfo INTEGER
  , cricinfo_2 INTEGER
  , dob DATE
  , role TEXT
  , bat_style TEXT
  , bowl_style TEXT
  , datetime_spidered TEXT
  , UNIQUE (name, reg)
  );

CREATE INDEX player_reg ON players (reg);

CREATE TABLE IF NOT EXISTS
  selections (
    match_id  INTEGER
  , team_id   INTEGER
  , player_id INTEGER
  );

CREATE INDEX selections_match_id ON selections (match_id);

CREATE INDEX selections_player_id ON selections (player_id);

CREATE TABLE IF NOT EXISTS
  balls (
    match_id INTEGER
  , innings INTEGER /* >1 when super over or similar */
  , over INTEGER
  , ball_seq INTEGER /* includes wides/noballs */
  , ball INTEGER /* of match.balls_per_over */
  , bowled_by TEXT
  , batter TEXT
  , non_striker TEXT
  , batter_runs INTEGER
  , extra_runs INTEGER
  , extra_type TEXT
  , wicket_fell BOOLEAN NOT NULL CHECK (wicket_fell IN (0, 1)) DEFAULT 0
  , dismissed INTEGER
  , how_out TEXT
  );

CREATE INDEX balls_match_inns_over ON balls (match_id, innings, over);

CREATE INDEX balls_bowler ON balls (bowled_by);

CREATE TABLE IF NOT EXISTS
  people (
    identifier TEXT
  , name TEXT
  , unique_name TEXT
  , key_bcci TEXT
  , key_bcci_2 TEXT
  , key_bigbash TEXT
  , key_cricbuzz TEXT
  , key_cricheroes TEXT
  , key_crichq TEXT
  , key_cricinfo TEXT
  , key_cricinfo_2 TEXT
  , key_cricingif TEXT
  , key_cricketarchive TEXT
  , key_cricketarchive_2 TEXT
  , key_nvplay TEXT
  , key_nvplay_2 TEXT
  , key_opta TEXT
  , key_opta_2 TEXT
  , key_pulse TEXT
  , key_pulse_2 TEXT
  );

CREATE INDEX people_reg ON people (identifier);

/*
all_balls:
1. build a unique sequential key across the innings (rowid might work but can't 100%
be certain of order)
2. Sum wickets that fell prior to each ball (sexy PARTITION BY)
 */
DROP VIEW IF EXISTS all_balls;

CREATE VIEW
  all_balls AS
WITH
  sequenced_balls AS (
    SELECT
      innings * 10000 + over * 100 + ball_seq AS seq
    , *
    FROM
      balls
  )
SELECT
  b.*
, strikers.name         AS striker_name
, non_strikers.name     AS non_striker_name
, bowlers.name          AS bowler_name
, SUM(wicket_fell) OVER (
    PARTITION BY
      match_id
    , innings
    ORDER BY
      seq ROWS BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) - wicket_fell AS wickets_down
FROM
  sequenced_balls b
  JOIN players strikers ON strikers.rowid = b.batter
  JOIN players non_strikers ON non_strikers.rowid = b.non_striker
  JOIN players bowlers ON bowlers.rowid = b.bowled_by;