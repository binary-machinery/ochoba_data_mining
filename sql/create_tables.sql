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
    add column created timestamp,
    add column type int,
    add column subsite_id int,
    add column subsite_name varchar,
    add column subsite_type int,
    add column author_id int,
    add column author_name varchar,
    add column title varchar,
    add column is_enabled_comments bool,
    add column is_enabled_likes bool,
    add column is_repost bool,
    add column is_show_thanks bool,
    add column is_filled_by_editors bool,
    add column is_editorial bool,
    add column hotness int,
    add column comments_count int,
    add column favorites_count int,
    add column hits_count int,
    add column likes_count int,
    add column likes_sum int;

create table post_errors (
    id serial primary key,
    post_id int not null,
    status_code int not null,
    response varchar not null
);

create table post_tags (
    id serial primary key,
    post_id int,
    value varchar,
    source varchar
);

create table post_blocks (
    id serial primary key,
    post_id int,
    type varchar,
    data varchar,
    text_length int
);

create table subsites (
    id int primary key,
    json varchar,
    has_restricted_access bool not null default false
);

create table subsite_errors (
    id serial primary key,
    subsite_id int not null,
    status_code int not null,
    response varchar not null
);