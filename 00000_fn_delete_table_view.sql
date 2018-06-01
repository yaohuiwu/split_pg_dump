
create
	or replace function __he_delete_table_or_view__(
		objectname character varying
	) returns void language plpgsql as 
$function$ 
declare isTable integer;

isView integer;

isMatView integer;

begin select
	into
		isTable count(*)
	from
		pg_tables
	where
		tablename = objectName
		and schemaname = current_schema;

select
	into
		isView count(*)
	from
		pg_views
	where
		viewname = objectName
		and schemaname = current_schema;

select
	into
		isMatView count(*)
	from
		pg_matviews
	where
		matviewname = objectName
		and schemaname = current_schema;

if isTable = 1 then execute 'DROP TABLE IF EXISTS ' || objectName;

return;
end if;

if isView = 1 then execute 'DROP VIEW IF EXISTS ' || objectName;

return;
end if;

if isMatView = 1 then execute 'DROP MATERIALIZED VIEW IF EXISTS ' || objectName;

return;
end if;

return;
end;

$function$;
