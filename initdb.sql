CREATE TABLE collections ( id serial PRIMARY KEY,
                           title text,
                           name text NOT NULL,
                           version text NOT NULL,
                           zip bytea,
                           UNIQUE (name, version));

CREATE TABLE pdfs ( id serial PRIMARY KEY,
                    git_commit char(40) NOT NULL,
                    style text NOT NULL,
                    pdf bytea);

CREATE TABLE collections_pdfs (collection serial REFERENCES collections(id),
                               pdf serial REFERENCES pdfs(id));
                    

CREATE TABLE pngs_a ( page_number serial PRIMARY KEY,
                       png bytea NOT NULL,
                       pdf_id serial REFERENCES pdfs(id));

CREATE TABLE pngs_b ( page_number serial PRIMARY KEY,
                       png bytea NOT NULL,
                       pdf_id serial REFERENCES pdfs(id));
