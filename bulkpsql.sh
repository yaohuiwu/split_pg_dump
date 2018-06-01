#set the password for the session using PGPASSWORD=<your password here>
#replace {your_schema_name_name} below with your target schema name
export PGOPTIONS="-c search_path={your_schema_name_name}"
find -type f -name "*.sql" | sort > sql_files 
while read p; do
  #replace {user} with your PostgreSQL username and {database} with the target database name
  psql -U {user} -d {database} -w -f "$p" >>output
done < sql_files
