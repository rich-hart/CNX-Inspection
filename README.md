# CNX-Inspection

```
psql -U postgres -d postgres -c "CREATE USER qa WITH SUPERUSER PASSWORD 'qa';"
createdb -U postgres -O qa training-data
psql -d training-data -U qa -f initdb.sql 
```
