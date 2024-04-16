CREATE TABLE IF NOT EXISTS
  matches (
    match_id INTEGER NOT NULL PRIMARY KEY
  , start_date DATE
  , match_type TEXT
  , gender TEXT
  , venue TEXT
  , event TEXT
  , city TEXT
  , overs INTEGER /* because the Hundred */
  , balls_per_over INTEGER /* because the Hundred */
  );

CREATE TABLE IF NOT EXISTS
  teams (
    team_id INTEGER NOT NULL PRIMARY KEY
  , name TEXT
  );

CREATE TABLE IF NOT EXISTS
  participation (
    match_id INTEGER
  , team_id INTEGER
  , innings INTEGER
  );

CREATE TABLE IF NOT EXISTS
  players (
    player_id INTEGER NOT NULL PRIMARY KEY
  , name TEXT
  , reg TEXT
  );

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