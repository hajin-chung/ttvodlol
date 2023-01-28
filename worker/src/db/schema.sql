DROP TABLE IF EXISTS queue;
CREATE TABLE queue (
  id TEXT,
  url TEXT,
  created_at TEXT,
  flag INTEGER DEFAULT 0,
  PRIMARY KEY (`id`)
);