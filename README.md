# split_pg_dump
Split / parse pg_dump output to individual files per object
<p>
<pre>

positional arguments:
  sourcefile            SQL input file. Typically from pg_dump

optional arguments:
  -h, --help            show this help message and exit
  -of OUTPUTDIR, -outputdir OUTPUTDIR
                        Optional alternative destination / output directory
                        for SQL output files
  -ns, -nosequence      Omit the sequence number prefix for resulting
                        filenames. Handy for comparing schemas between
                        databases
  -nt, -notype          Ommit the type prefix in resulting filenames
  -nc, -noclean         Skip the step of cleaning the target directory of
                        *.sql
  -xn EXCLUDENAMES [EXCLUDENAMES ...], -exludenames EXCLUDENAMES [EXCLUDENAMES ...]
                        Exclude objects these strings in their names
  -xt EXLUDETYPES [EXLUDETYPES ...], -exludetypes EXLUDETYPES [EXLUDETYPES ...]
                        Exclude objects these types. Options are MATERIALIZED
                        VIEW,SEQUENCE,INDEX,TABLE,TYPE,VIEW,FUNCTION,SCHEMA,CO
                        NSTRAINT,TRIGGER,FK CONSTRAINT

Samples: To exclude schema and foreign key constraints: -xt 'SCHEMA' 'FK CONTSTAINT'
</pre>
<p>
Tested on PostrgeSQL 9.6 and Ubuntu 14.04.2 LTS
<p>
The python script <a href="https://github.com/ajgreyling/split_pg_dump/blob/master/split_pg_dump.py">split_pg_dump.py</a> will take the output of pg_dump above as parameter and generate multiple .sql files in the current directory. Each filename is prefixed with a sequence number so that they can be run in the correct order (for depandancies)
<p>
To make the resulting files portable (to allow you applying the changes to another database or schema) perform pg_dump with the following parameters: -s -x -O
<p>
<b>Output Filenames</b>
<p>
Defaults with no options
<pre>
00001_ty_some_type.sql
00002_fn_some_function.sql
00003_vw_some_view.sql
00004_mv_some_materialised_view.sql
00005_sq_some_sequence.sql
00006_ix_some_index.sql
</pre>
<p>
-ns , -nosequence
<pre>
ty_some_type.sql
fn_some_function.sql
vw_some_view.sql
mv_some_materialised_view.sql
sq_some_sequence.sql
ix_some_index.sql
</pre>
<p>
-nt , -notype
<pre>
00001_some_type.sql
00002_some_function.sql
00003_some_view.sql
00004_some_materialised_view.sql
00005_some_sequence.sql
00006_some_index.sql
</pre
<p>
<p>
<a href="https://github.com/ajgreyling/split_pg_dump/blob/master/bulkpsql.sh">bulkpsql.sh</a> will allow you to apply the whole folder of files to the server by only specifying your password and schema once.