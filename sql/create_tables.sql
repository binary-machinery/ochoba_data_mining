create table users (
    id int primary key,
    json varchar not null
);

alter table users
    add column created timestamp,
    add column name varchar,
    add column type int,
    add column karma int,
    add column is_plus bool,
    add column is_verified bool,
    add column is_available_for_messenger bool,
    add column entries_count int,
    add column comments_count int,
    add column favorites_count int,
    add column subscribers_count int;

create table user_errors (
    id serial primary key,
    user_id int not null,
    status_code int not null,
    response varchar not null
);

create table posts (
    id int primary key,
    json varchar not null
);

alter table posts
    add column entry_id int,
    add column commentsCount int,
    add column favoritesCount int,
    add column hitsCount int,
    add column likesCount int,
    add column subsite_id int,
    add column is_show_thanks bool,
    add column is_filled_by_editors bool,
    add column iseditorial bool,
    add column date_created timestamp;


create table post_errors (
    id serial primary key,
    post_id int not null,
    status_code int not null,
    response varchar not null
);