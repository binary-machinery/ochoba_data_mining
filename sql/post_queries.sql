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
select subsite_id, subsite_name, count(id) as cnt
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

-- Sort by text length
with length_data as (
    select
           posts.id as post_id,
           sum(coalesce(blocks.text_length, 0)) as text_length
    from posts
    left join post_blocks blocks
        on posts.id = blocks.post_id
            and posts.type = 1
    group by posts.id
)
select posts.id, posts.title, posts.author_name, posts.subsite_name, text_length
from length_data
left join posts
    on posts.id = length_data.post_id
order by text_length desc;

-- Text length percentiles
with length_data as (
    select
           posts.id as post_id,
           sum(coalesce(blocks.text_length, 0)) as text_length
    from posts
    join post_blocks blocks
        on posts.id = blocks.post_id
            and posts.type = 1
    group by posts.id
), percentiles as (
    select generate_series as value
    from generate_series(0, 1, 0.01)
)
select percentiles.value * 100 as probability,
       percentile_disc(percentiles.value) within group (order by text_length) as percentile
from percentiles cross join length_data
where text_length < 341961
group by percentiles.value;

-- Text length percentiles for long posts
with long_posts as (
    select distinct posts.id
    from posts
    join post_tags
        on posts.id = post_tags.post_id
            and posts.type = 1
            and post_tags.value in ('#лонг', '#лонгрид', '#longread')
), length_data as (
    select long_posts.id, sum(blocks.text_length) as text_length
    from long_posts
    join post_blocks blocks
        on long_posts.id = blocks.post_id
    group by long_posts.id
), percentiles as (
    select generate_series as value
    from generate_series(0, 1, 0.05)
)
select
    percentile_disc(percentiles.value) within group (order by text_length) as percentile,
    percentiles.value * 100 as probability
from percentiles cross join length_data
group by percentiles.value;

-- Long posts count
select count(distinct post_id)
from post_tags
where value in ('#лонг', '#лонгрид', '#long', '#longread');

select count(distinct post_id)
from post_tags
where value in ('#лонг', '#лонгрид', '#longread');

-- Sort subsites by amount of long posts
select subsite_id, subsite_name, count(distinct posts.id) as cnt
from posts
join post_tags tags
    on posts.id = tags.post_id
        and posts.type = 1
        and (tags.value in ('#лонг', '#лонгрид', '#long', '#longread'))
group by subsite_id, subsite_name
order by cnt desc;

-- Sort subsites by amount of editorial long posts
select subsite_id, subsite_name, count(distinct posts.id) as cnt
from posts
join post_tags tags
    on posts.id = tags.post_id
        and posts.type = 1
        and posts.is_editorial = true
        and (tags.value = '#лонг' or tags.value = '#лонгрид')
group by subsite_id, subsite_name
order by cnt desc;

-- Sort subsites by amount of UGC long posts
select subsite_id, subsite_name, count(distinct posts.id) as cnt
from posts
join post_tags tags
    on posts.id = tags.post_id
        and posts.type = 1
        and posts.is_editorial = false
        and (tags.value = '#лонг' or tags.value = '#лонгрид')
group by subsite_id, subsite_name
order by cnt desc;

-- Sort authors by amount of long posts
select author_id, author_name, count(distinct posts.id) as cnt
from posts
join post_tags tags
    on posts.id = tags.post_id
        and posts.type = 1
        and (tags.value = '#лонг' or tags.value = '#лонгрид')
group by author_id, author_name
order by cnt desc;

-- Sort authors by sum text length of their long posts
with length_data as (
    select posts.id as post_id, sum(blocks.text_length) as text_length
    from posts
    join post_tags tags
        on posts.id = tags.post_id
            and posts.type = 1
            and (tags.value = '#лонг' or tags.value = '#лонгрид')
    join post_blocks blocks
        on posts.id = blocks.post_id
    group by posts.id
)
select author_id, author_name, sum(text_length) as text_length
from length_data
join posts
    on posts.id = length_data.post_id
group by author_id, author_name
order by text_length desc;

-- Sort authors by sum rating of their long posts
with length_data as (
    select posts.id as post_id, sum(posts.likes_sum) as total_rating
    from posts
    join post_tags tags
        on posts.id = tags.post_id
            and posts.type = 1
            and (tags.value = '#лонг' or tags.value = '#лонгрид')
    group by posts.id
)
select author_id, author_name, sum(total_rating) as total_rating
from length_data
join posts
    on posts.id = length_data.post_id
group by author_id, author_name
order by total_rating desc;

-- Sort authors by sum hits of their long posts
with length_data as (
    select posts.id as post_id, sum(posts.likes_sum) as total_rating
    from posts
    join post_tags tags
        on posts.id = tags.post_id
            and posts.type = 1
            and (tags.value = '#лонг' or tags.value = '#лонгрид')
    group by posts.id
)
select author_id, author_name, sum(hits_count) as hits_count
from length_data
join posts
    on posts.id = length_data.post_id
group by author_id, author_name
order by hits_count desc;

-- Sort by co-author posts
select co_author_id, co_author_name, count(*) as co_author_cnt
from posts
where co_author_id is not null
group by co_author_id, co_author_name
order by co_author_cnt desc;

-- Sort by filled by editors count
select author_id, author_name, count(*) as filled_by_editors_cnt
from posts
where is_filled_by_editors
group by author_id, author_name
order by filled_by_editors_cnt desc;

-- Delete duplicate tags
delete from post_tags
where id in (
        select distinct pt1.id
        from post_tags pt1
        join post_tags pt2
            on pt1.post_id = pt2.post_id
                and pt1.value = pt2.value
        where pt1.id > pt2.id
        group by pt1.id
    );

-- Sort by tags count
select value, count(distinct id) as tag_count
from post_tags
group by value
order by tag_count desc;

-- Most popular tags per month
with data as (
    select date_trunc('month', created)::date as time_window, post_tags.value as tag, count(distinct posts.id) as cnt
    from posts
    join post_tags
        on posts.id = post_tags.post_id
            and posts.created > '2017-01-01'
            and post_tags.value not in ('#long', '#лонг', '#новости', '#кино', '#фан', '#мнения', '#обзоры', '#разбор', '#опыт', '#игры', '#видео', '#сериалы', '#деньги', '#топы', '#истории', '#мобайл', '#киберспорт')
    group by time_window, post_tags.value
    order by time_window, cnt desc
)
select distinct time_window,
    nth_value(tag, 1) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _1,
    nth_value(tag, 2) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _2,
    nth_value(tag, 3) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _3,
    nth_value(tag, 4) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _4,
    nth_value(tag, 5) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _5,
    nth_value(tag, 6) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _6,
    nth_value(tag, 7) over (partition by time_window order by cnt desc range between unbounded preceding and unbounded following) as _7
from data
order by time_window;