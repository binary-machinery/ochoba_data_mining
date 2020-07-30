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
select
       stats.subsite_id as id,
       coalesce(subsites.name, 'Блоги') as name,
       subsites.created as created,
       stats.cnt as cnt
from (
    select subsite_id, count(data.id) as cnt
    from data
    group by subsite_id
    ) as stats
left join subsites
    on stats.subsite_id = subsites.id
order by stats.cnt desc;

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

-- Calculate estimated time for failed post queries
update post_errors
    set estimated_creation_time = (
        with data as (
            (select * from posts where id > post_errors.post_id order by id asc limit 10)
            union
            (select * from posts where id < post_errors.post_id order by id desc limit 10)
        )
        select to_timestamp(avg(cast(extract(epoch from created) as integer))) as created
        from data
    );

-- Sort posts by hits
select id, title, author_name, subsite_name, hits_count, likes_sum from posts
where type = 1
order by hits_count desc;

-- Sort subsites by hits
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type,
           hits_count
    from posts
    where type = 1
)
select subsite_id, subsite_name, sum(hits_count) as hits from data
group by subsite_id, subsite_name
order by hits desc;

-- Sort subsites by hits in June 2020 and show their hits ratio
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type,
           hits_count
    from posts
    where type = 1
)
select subsite_id, subsite_name, sum(hits_count) as hits,
       concat(round(sum(hits_count)::decimal / (select sum(hits_count) from posts where created between '2020-06-01' and '2020-07-01') * 100, 2), '%') as ratio
from data
where created between '2020-06-01' and '2020-07-01'
group by subsite_id, subsite_name
order by hits desc;

-- Sort posts by rating
select id, title, author_name, subsite_name, hits_count, likes_sum from posts
where type = 1
order by likes_sum desc;

-- Sort subsites by rating
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type,
           likes_sum
    from posts
    where type = 1
)
select subsite_id, subsite_name, sum(likes_sum) as rating from data
group by subsite_id, subsite_name
order by rating desc;

-- Sort posts by negative rating
select id, title, author_name, subsite_name, hits_count, likes_sum from posts
where type = 1
order by likes_sum;

-- Sort posts by comments
select id, title, author_name, subsite_name, hits_count, likes_sum, comments_count from posts
where type = 1
order by comments_count desc;

-- Sort subsites by rating
with data as (
    select id,
           created,
           case when subsite_type = 1 then 0 else subsite_id end         as subsite_id,
           case when subsite_type = 1 then 'Блоги' else subsite_name end as subsite_name,
           subsite_type,
           comments_count
    from posts
    where type = 1
)
select subsite_id, subsite_name, sum(comments_count) as comments from data
group by subsite_id, subsite_name
order by comments desc;

-- Percentiles
with length_data as (
    select
           posts.id as post_id,
           sum(coalesce(blocks.text_length, 0)) as text_length
    from posts
    left join post_blocks blocks
        on posts.id = blocks.post_id
            and posts.type = 1
    group by posts.id
), percentiles as (
    select generate_series as value
    from generate_series(0, 1, 0.05)
)
select percentiles.value, percentile_disc(percentiles.value) within group (order by text_length)
from percentiles cross join length_data
group by percentiles.value;

-- Long posts percentiles
with length_data as (
    select posts.id, sum(blocks.text_length) as text_length
    from posts
    join post_tags tags
        on posts.id = tags.post_id
            and posts.type = 1
            and (value = '#лонг' or value = '#лонгрид')
    join post_blocks blocks
        on posts.id = blocks.post_id
    group by posts.id
), percentiles as (
    select generate_series as value
    from generate_series(0, 1, 0.05)
)
select percentiles.value, percentile_disc(percentiles.value) within group (order by text_length)
from percentiles cross join length_data
group by percentiles.value;
