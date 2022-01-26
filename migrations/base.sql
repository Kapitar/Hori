create table users
(
    id int auto_increment
		primary key,
	osu_id int,
	nickname varchar(128) charset utf8 not null
);