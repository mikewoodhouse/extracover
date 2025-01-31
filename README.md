# extracover

## IMPORTANT

Check that the UI runs - at present `fastapi 0.115.7` causes a problem, so downgrade using `uv pip install "fastapi==0.115.6"`

## Purpose

(if anyone happens upon this...)

To investigate the evolution of cricket innings in (initially) T20 matches and to explore the extent to which predictions may be made by applying relevant factors as a series of "overlay" factors based on historic data before the start of the game abd whether in-game factors such as pitch conditions, weather etc can be derived and applied to increase accuracy as the innings develops.

## Data

https://cricsheet.org/
https://cricsheet.org/register/people.csv
https://cricsheet.org/register/names.csv


## Data TODOs

* Classify players:
  * bowl style
  * handedness
* Classify events
  * Domestic
  * International & "level"
* Rule variations
  * noballs - when is the deduction one and when two? Is it possible to identify as a match condition or do we need to look into competition? `info.match_type_number`, perhaps? When there are batter runs then the size of the penalty is obvious, it's otherwise that might be a problem...

## Model Ideas

### Machine Learning?

Inputs might include:

* Batter
  * "Aggression"
  * Balls faced (or first 10/thereafter?)
  * Wicket likelihood
* Bowler
  * "Costliness"
  * Wicket prob
  * Wide/Noball frequency
* Match
  * Innings
  * Current RR
  * Target (if 2nd inns) RR
  * Stage of innings (balls remaining/balls in innings?)
* Venue
  * Typical score stats

Train on ball outcomes (one hot?):

* batter runs: 0-6
* wicket
* wide/noball
* bye/legbye

# Notes

Wides & noballs by phase:

| phase | wides | noballs |   total | total (legit) | wide % |   no % |
| :---: | ----: | ------: | ------: | ------------: | -----: | -----: |
|   0   | 19997 |    2319 |  563215 |        540899 |  3.70% | 0.439% |
|   1   | 29972 |    3852 | 1051477 |       1017653 |  2.95% | 0.379% |
|   2   |  5426 |    1285 |  134451 |        127740 |  4.25% |  1.01% |