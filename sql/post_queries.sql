-- Total post count
select count(*) from posts;

-- Total post count by type
select generate_series as post_type, count(id)
from generate_series((select min(type) from posts), (select max(type) from posts))
    left join posts
        on posts.type = generate_series
group by post_type
order by post_type;

-- Biggest subsites
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type
    from posts
    where type = 1
)
select subsite_name, count(id) as cnt
from data
group by subsite_id, subsite_name
order by cnt desc;

-- Biggest subsites in June 2020
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type
    from posts
    where type = 1 and created between '2020-06-01 00:00:00.000000' and '2020-07-01 00:00:00.000000'
)
select subsite_name, count(id) as cnt
from data
group by subsite_id, subsite_name
order by cnt desc;

-- Sort by repost count
select author_id, author_name, count(*) as cnt from posts
where type = 5
group by author_id, author_name
order by cnt desc;
