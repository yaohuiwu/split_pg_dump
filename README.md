# split_pg_dump
Split / parse pg_dump output to individual files per object

Tested on PostrgeSQL 9.6 and Ubuntu

The following python script will take the output of pg_dump above as parameter and generate multiple .sql files in the current directory. Each filename is prefixed with a sequence number so that they can be run in the correct order (for depandancies)

To make the resulting files portable (to allow you applying the changes to another database or schema) perform pg_dump with the following parameters: -s -x -O

<pre>
Output Files (from Python)
00001_ty_some_type.sql
00002_fn_some_function.sql
00003_vw_some_view.sql
00004_mv_some_materialised_view.sql
00005_sq_some_sequence.sql
00006_ix_some_index.sql
</pre>


bulkpsql.sh will allow you to apply the whole folder of files to the server by only specifying your password and schema once.