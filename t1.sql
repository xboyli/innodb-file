CREATE TABLE `t1` (

`id` int(10) unsigned NOT NULL AUTO_INCREMENT,

`name` varchar(32) DEFAULT NULL,

`size` int(11) DEFAULT NULL,

PRIMARY KEY (`id`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `test`.`t1` (`name`, `size`) VALUES ('aaa', '1');

INSERT INTO `test`.`t1` (`name`, `size`) VALUES ('bbb', '2');

INSERT INTO `test`.`t1` (`name`, `size`) VALUES ('ccc', '3');