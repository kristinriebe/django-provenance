-- use:  `cat data/delete_data_tap.sql | sqlite3 db.sqlite3`
DELETE FROM tap_schema_tables;
DELETE FROM tap_schema_columns;
DELETE FROM tap_schema_schemas;
