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
  players (name TEXT, reg TEXT, UNIQUE (name, reg));

CREATE TABLE IF NOT EXISTS
  selections (
    match_id  INTEGER
  , team_id   INTEGER
  , player_id INTEGER
  );

CREATE TABLE IF NOT EXISTS
  balls (
    match_id INTEGER
  , innings INTEGER
  , over INTEGER
  , ball_seq INTEGER /* includes wides/noballs */
  , ball INTEGER /* of match.balls_per_over */
  , bowled_by INTEGER
  , batter INTEGER
  , non_striker INTEGER
  , batter_runs INTEGER
  , extra_runs INTEGER
  , extra_type TEXT
  );