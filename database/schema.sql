CREATE TABLE subreddits (
    subreddit_id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    last_scraped TIMESTAMP,
    created_time TIMESTAMP
);

CREATE TABLE posts (
    post_id VARCHAR(20) PRIMARY KEY,
    subreddit_id INTEGER REFERENCES subreddits(subreddit_id),
    title TEXT NOT NULL,
    body TEXT,
    author TEXT,
    upvotes INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    post_link VARCHAR(500),
    last_scraped TIMESTAMP,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ml_processed BOOLEAN DEFAULT false
);

CREATE TABLE comments (
    comment_id VARCHAR(20) PRIMARY KEY,
    post_id VARCHAR(20) REFERENCES posts(post_id) ON DELETE CASCADE,
    parent_comment_id VARCHAR(20),
    body TEXT NOT NULL,
    author VARCHAR(100),
    upvotes INTEGER DEFAULT 0,
    last_scraped TIMESTAMP,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ml_processed BOOLEAN DEFAULT false
);

CREATE INDEX idx_subreddits_last_scraped ON subreddits(last_scraped);

CREATE INDEX idx_posts_subreddit ON posts(subreddit_id);
CREATE INDEX idx_posts_ml_processed ON posts(ml_processed) WHERE ml_processed = false;
CREATE INDEX idx_posts_created_time ON posts(created_time DESC);
CREATE INDEX idx_posts_upvotes ON posts(upvotes DESC);
CREATE INDEX idx_posts_subreddit_ml ON posts(subreddit_id, ml_processed);
CREATE INDEX idx_posts_title_search ON posts USING gin(to_tsvector('english', title));
CREATE INDEX idx_posts_body_search ON posts USING gin(to_tsvector('english', body));

CREATE INDEX idx_comments_post ON comments(post_id);
CREATE INDEX idx_comments_ml_processed ON comments(ml_processed) WHERE ml_processed = false;
CREATE INDEX idx_comments_parent ON comments(parent_comment_id);
CREATE INDEX idx_comments_created_time ON comments(created_time DESC);
CREATE INDEX idx_comments_upvotes ON comments(upvotes DESC);
CREATE INDEX idx_comments_post_ml ON comments(post_id, ml_processed);
CREATE INDEX idx_comments_body_search ON comments USING gin(to_tsvector('english', body));
