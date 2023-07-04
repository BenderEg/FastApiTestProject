from db_code import db_close, db_connect

con, cursor = db_connect()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
(
    id serial PRIMARY KEY,
    title character varying COLLATE pg_catalog."default" NOT NULL,
    content character varying COLLATE pg_catalog."default" NOT NULL,
    published boolean NOT NULL DEFAULT true,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    user_id integer NOT NULL,
    CONSTRAINT posts_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID 
)''')

cursor.execute('''INSERT INTO posts (title, content, user_id) VALUES ('second_post', 'something new', 6);
INSERT INTO posts (title, content, user_id) VALUES ('third_one', 'breaking news', 6);
INSERT INTO posts (title, content, user_id) VALUES ('Bay', 'Universe', 6);
''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users 
(
    id serial PRIMARY KEY NOT NULL,
    email character varying COLLATE pg_catalog."default" NOT NULL UNIQUE,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now()  
)''')
               

cursor.execute('''CREATE TABLE IF NOT EXISTS public.votes
(
    post_id integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT votes_pkey PRIMARY KEY (post_id, user_id),
    CONSTRAINT votes_posts_fk FOREIGN KEY (post_id)
        REFERENCES public.posts (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT votes_users_fk FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)''')

db_close(con)