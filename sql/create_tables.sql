create table users (
    id int primary key,
    json varchar not null
);

create table user_errors (
    id serial primary key,
    user_id int not null,
    status_code int not null,
    response varchar not null
);

create table posts (
    id int primary key,
    json varchar not null,
    text_length int not null default 0,
    media_count int not null default 0
);

create table post_errors (
    id serial primary key,
    post_id int not null,
    status_code int not null,
    response varchar not null
);