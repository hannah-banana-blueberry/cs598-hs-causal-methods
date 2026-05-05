DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS pre_survey;
DROP TABLE IF EXISTS post_survey;
DROP TABLE IF EXISTS demographics;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_type TEXT,
  consent INTEGER DEFAULT 0,
  completed INTEGER DEFAULT 0,
  recruitment_location TEXT,
  window_width INTEGER,
  user_agent TEXT,
  prolific_pid TEXT,
  study_id TEXT,
  session_id TEXT,
  time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pre_survey (
  user_id INTEGER NOT NULL,
  q1 INTEGER,
  q2 INTEGER,
  q3 INTEGER,
  q4 INTEGER,
  q5 INTEGER,
  q6 INTEGER,
  time_submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE post_survey (
  user_id INTEGER NOT NULL,
  q1 INTEGER,
  q2 INTEGER,
  q3 INTEGER,
  q4 INTEGER,
  q5 INTEGER,
  q6 INTEGER,
  time_submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE demographics (
  user_id INTEGER NOT NULL,
  q1 TEXT,
  q2 TEXT,
  q2text TEXT,
  q3 TEXT,
  q3text TEXT,
  q4 TEXT,
  q4text TEXT,
  q5 TEXT,
  q6 TEXT,
  q6text TEXT,
  q7 TEXT,
  q8 TEXT,
  email TEXT,
  time_submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);
