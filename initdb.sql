CREATE TABLE zips ( id serial UNIQUE PRIMARY KEY,
                    zip bytea);

CREATE TABLE pdfs ( id serial UNIQUE PRIMARY KEY,
                    pdf bytea); 

CREATE TABLE collections_info ( id serial UNIQUE PRIMARY KEY,
                                title text,
                                file_name text,
                                version text,
                                style text,
                                zip_id serial REFERENCES zips(id),
                                pdf_id serial REFERENCES pdfs(id),
                                git_commit char(40) UNIQUE);

CREATE TABLE pngs_a ( page_number int UNIQUE PRIMARY KEY,
                      png bytea,
                      collection_id serial UNIQUE REFERENCES collections_info(id));

CREATE TABLE pngs_b ( page_number int UNIQUE PRIMARY KEY,
                      png bytea,
                      collection_id serial UNIQUE REFERENCES collections_info(id));
