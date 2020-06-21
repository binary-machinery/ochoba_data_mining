-- user count
select count(*) from users;


-- an amount of "Дерьмак"-like names (local recurring meme)
select count(*) from users
where lower(name) like '%дерьмак%';


-- unique "Дерьмак"-like names
select distinct name from users
where lower(name) like '%дерьмак%';


-- sort by rating
select karma, name, entries_count, comments_count
from users
order by karma desc;


-- user count with negative rating
select count(*)
from users
where karma < 0;


-- sort by rating (negative)
select karma, name, entries_count, comments_count
from users
order by karma;


-- sort by subscriber count
select subscribers_count, name, karma, entries_count, comments_count from users
order by subscribers_count desc;


-- sort by entries count
select entries_count, name, karma
from users
order by entries_count desc;


-- sort by comments count
select comments_count, name, karma
from users
order by comments_count desc;


-- sort by favourites count
select favorites_count, name, karma from users
order by favorites_count desc;


-- sort by rating efficiency
select karma / (entries_count + comments_count) karma_efficiency, name, karma, entries_count, comments_count
from users
where entries_count + comments_count != 0
order by karma_efficiency desc;


-- verified accounts
select count(*) from users
where is_verified = true;

select name, created, karma, entries_count, comments_count from users
where is_verified = true
order by id;


-- error count by error code
select status_code, count(*) from user_errors
group by status_code;