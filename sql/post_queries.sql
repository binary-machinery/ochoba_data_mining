-- Total post count
select count(*) from posts;

-- Total post count by type
select generate_series as post_type, count(id)
from generate_series((select min(type) from posts), (select max(type) from posts))
    left join posts
        on posts.type = generate_series
group by post_type
order by post_type;

-- Sort by repost count
select author_id, author_name, count(*) as cnt from posts
where type = 5
group by author_id, author_name
order by cnt desc;
