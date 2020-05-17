CREATE TABLE `ohlcv_daily` (
  `ticker` varchar(5) NOT NULL,
  `date` int(11) NOT NULL,
  `open` float NOT NULL,
  `high` float NOT NULL,
  `low` float NOT NULL,
  `close` float NOT NULL,
  `volume` float NOT NULL,
  `adj_close` float NOT NULL,
  `return` float DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ticker`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;