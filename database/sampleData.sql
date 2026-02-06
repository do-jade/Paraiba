INSERT INTO subreddits (name, created_time) VALUES
('travel', CURRENT_TIMESTAMP),
('solotravel', CURRENT_TIMESTAMP),
('barcelona', CURRENT_TIMESTAMP),
('tokyo', CURRENT_TIMESTAMP);

INSERT INTO posts (post_id, subreddit_id, title, body, author, upvotes, comment_count, post_link, created_time) VALUES
('abc123', 1, 'Hidden gems in Barcelona?', 'Looking for authentic local spots that tourists dont know about. Any recommendations?', 'traveler42', 150, 12, 'https://reddit.com/r/travel/abc123', CURRENT_TIMESTAMP - INTERVAL '2 days'),
('def456', 3, 'Best tapas bars locals actually go to?', 'Tired of tourist traps. Where do YOU eat?', 'foodlover88', 89, 8, 'https://reddit.com/r/barcelona/def456', CURRENT_TIMESTAMP - INTERVAL '5 days'),
('ghi789', 2, 'Quiet neighborhoods in Tokyo', 'I want to experience real Tokyo, not Shibuya crowds', 'solotraveler', 234, 45, 'https://reddit.com/r/solotravel/ghi789', CURRENT_TIMESTAMP - INTERVAL '1 day');

INSERT INTO comments (comment_id, post_id, body, author, upvotes, created_time) VALUES
('com001', 'abc123', 'You HAVE to try Can Culleretes - oldest restaurant in Barcelona. Locals love it, barely any tourists!', 'barcelonalocal', 200, CURRENT_TIMESTAMP - INTERVAL '2 days'),
('com002', 'abc123', 'Parc de la Ciutadella early morning. Absolutely peaceful and beautiful.', 'parkfan23', 85, CURRENT_TIMESTAMP - INTERVAL '1 day'),
('com003', 'def456', 'Bar del Pla in El Born. Small, authentic, amazing wines. Never crowded.', 'winelover', 42, CURRENT_TIMESTAMP - INTERVAL '4 days'),
('com004', 'ghi789', 'Shimokitazawa neighborhood. Vintage shops, indie cafes, local vibe. Its perfect.', 'tokyoresident', 156, CURRENT_TIMESTAMP - INTERVAL '1 day'),
('com005', 'ghi789', 'Yanaka district. Old Tokyo feel, temples, small streets. Tourists skip it.', 'japanexpert', 178, CURRENT_TIMESTAMP - INTERVAL '12 hours');

SELECT 'Subreddits:' as table_name, COUNT(*) as count FROM subreddits
UNION ALL
SELECT 'Posts:', COUNT(*) FROM posts
UNION ALL
SELECT 'Comments:', COUNT(*) FROM comments;