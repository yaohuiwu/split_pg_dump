# split_pg_dump
Split / parse pg_dump output to individual files per object

<pre>
usage: split_pg_dump.py [-h] [-ns] [-nt] sourcefile

Split output from pg_dump into seperate files. See
https://github.com/ajgreyling/split_pg_dump

positional arguments:
  sourcefile        SQL input file. Typically from pg_dump

optional arguments:
  -h, --help        show this help message and exit
  -ns, -nosequence  Omit the sequence number prefix for resulting filenames.
                    Handy for comparing schemas between databases
  -nt, -notype      Ommit the type prefix in resulting filenames
</pre>

Tested on PostrgeSQL 9.6 and Ubuntu 14.04.2 LTS

The python script <a href="https://github.com/ajgreyling/split_pg_dump/blob/master/split_pg_dump.py">split_pg_dump.py</a> will take the output of pg_dump above as parameter and generate multiple .sql files in the current directory. Each filename is prefixed with a sequence number so that they can be run in the correct order (for depandancies)

To make the resulting files portable (to allow you applying the changes to another database or schema) perform pg_dump with the following parameters: -s -x -O

<b>Output Filenames</b>

Default s with no options
<pre>
00001_ty_some_type.sql
00002_fn_some_function.sql
00003_vw_some_view.sql
00004_mv_some_materialised_view.sql
00005_sq_some_sequence.sql
00006_ix_some_index.sql
</pre>

-ns , -nosequence
<pre>
ty_some_type.sql
fn_some_function.sql
vw_some_view.sql
mv_some_materialised_view.sql
sq_some_sequence.sql
ix_some_index.sql
</pre>

-nt , -notype
<pre>
00001_some_type.sql
00002_some_function.sql
00003_some_view.sql
00004_some_materialised_view.sql
00005_some_sequence.sql
00006_some_index.sql
</pre

<a href="https://github.com/ajgreyling/split_pg_dump/blob/master/bulkpsql.sh">bulkpsql.sh</a> will allow you to apply the whole folder of files to the server by only specifying your password and schema once.