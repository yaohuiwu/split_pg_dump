import sys
import re
import os
import argparse

parser = argparse.ArgumentParser(description='Split output from pg_dump into seperate files. See https://github.com/ajgreyling/split_pg_dump')
parser.add_argument('sourcefile',help='SQL input file. Typically from pg_dump')
parser.add_argument('-of','-outputdir',dest='outputdir',help='Optional alternative destination / output directory for SQL output files')
parser.add_argument('-ns','-nosequence', dest='nosequence',action='store_true',help='Omit the sequence number prefix for resulting filenames. Handy for comparing schemas between databases')
parser.add_argument('-nt','-notype', dest='notype',action='store_true',help='Ommit the type prefix in resulting filenames' )
#parser.add_argument('-nc','-noclean', dest='noclean',action='store_true',help='Skip the step of cleaning the target directory of *.sql' )
parser.add_argument('-xn','-exludenames', dest='excludenames',nargs='+', help='Exclude objects these strings in their names')
parser.add_argument('-xt','-exludetypes', dest='exludetypes',nargs='+', help='Exclude objects these types. Options are MATERIALIZED VIEW,SEQUENCE,INDEX,TABLE,TYPE,VIEW,FUNCTION,SCHEMA,CONSTRAINT,TRIGGER,FK CONSTRAINT')
args = parser.parse_args()

rule_tables_set = set()

def should_be_skipped(object_name,object_type):

    if args.excludenames is None:
        return False
    else: 
        for exclude_name in args.excludenames:
            if exclude_name in object_name:
                print ("skipping due to name: " + object_name + " type: " + object_type)
                return True
        if args.exludetypes is None:
            return False
        else:
            for exclude_type in args.exludetypes:
                if exclude_type == object_type:
                    if exclude_type == 'TABLE' and object_name in rule_tables_set:
                        #this is a special case. This table is for a view which pg_dump exported as a table and a rule so don't skip it
                        return False
                    print ("skipping due to type: " + object_type + " name: " + object_name)
                    return True
        return False

type_prefix = {
    'MATERIALIZED VIEW' : 'mv_',
    'SEQUENCE' : 'sq_',
    'INDEX' : 'ix_',
    'TABLE' : 'tb_',
    'TYPE' : 'ty_',
    'VIEW' : 'vw_',
    'FUNCTION' : 'fn_',
    'SCHEMA' : 'sc_',
    'RULE' : 'rl_',
    'CONSTRAINT' : 'cs_',
    'TRIGGER' : 'tr_',
    'FK CONSTRAINT' : 'fk_',
    'COMMENT': 'ct_',
    'TABLE DATA': 'tb_dt_'
}

inputfile = ''
inputfile=args.sourcefile

output_dir = ''
if args.outputdir is None:
    output_dir = os.path.dirname(os.path.realpath(__file__))
else:
    output_dir = args.outputdir

#if not args.noclean:
#    files = os.listdir(output_dir)
#    for filename in files:
#        if filename.endswith(".sql"):
#            os.remove(os.path.join(output_dir,filename))

text_file = open(inputfile, 'r')
all_lines = text_file.read()
text_file.close()
rule_matches = re.findall(r'CREATE RULE "_RETURN" AS\s*ON SELECT TO (?P<table_name>\w+)\s*DO INSTEAD',all_lines,re.MULTILINE)
if not (rule_matches is None):
#    rule_tables_set.add(rule_matches.group('table_name'))
    for rule_table in rule_matches:
        rule_tables_set.add(rule_table)
        print(rule_table)

#quit()

with open(inputfile) as fo:
    skip = True
    newfile = True
    cntr = 1
    filename = ''
    object_type_set = set()
    for line in fo.readlines():
#           use https://pythex.org/ to test the regular expression            
        match_result = re.search(r'-- Name: (?P<object_name>\w+)\(?\)?.*?Type: (?P<object_type>\w+ ?\w+);', line)
        data_match_result = re.search(r'-- Data for Name: (?P<object_name>\w+); Type: (?P<object_type>\w+ ?\w+); Schema: (?P<schema>\w+); Owner: (?P<owner>\w+)', line)
        if not (match_result is None):
            newfile = True
            object_name = match_result.group('object_name')
            object_type = match_result.group('object_type')
            skip = should_be_skipped(object_name,object_type)
            if not skip :
                object_type_set.add(object_type)

                if (newfile):
                    filename = ''
                    if not args.nosequence:
                        filename = '{0:05d}'.format(cntr) + '_'
                    if not args.notype:
                        filename += type_prefix[object_type]
                    filename += object_name + '.sql'
                    filename = os.path.join(output_dir,filename)

                    print(filename)
                    with open (filename,'w') as opf:
                        if object_type == 'VIEW' or object_type == 'MATERIALIZED VIEW':
                            opf.write('\nDO $$ BEGIN\n')
                            opf.write('PERFORM __he_delete_table_or_view__(\'' + object_name + '\');\n')
                            opf.write('END $$;\n\n')    
                        # remove schema from comment line with name and type of object
                        line = re.sub(r'Schema: \w+;','',line)
                        opf.write(line)
                        opf.close
                        cntr+=1
                    newfile = False
                else:
                    opf.write(line)
        elif not (data_match_result is None):
            newfile = True
            object_name = data_match_result.group('object_name')
            object_type = data_match_result.group('object_type')
            skip = should_be_skipped(object_name,object_type)
            if not skip :
                object_type_set.add(object_type)

                if (newfile):
                    filename = ''
                    if not args.nosequence:
                        filename = '{0:05d}'.format(cntr) + '_'
                    if not args.notype:
                        filename += type_prefix[object_type]
                    filename += object_name + '.sql'
                    filename = os.path.join(output_dir,filename)

                    print(filename)
                    with open (filename,'w') as opf:
                        opf.write(line)
                        opf.close
                        cntr+=1
                    newfile = False
                else:
                    opf.write(line)
        else:
            if skip == False:
                with open (filename,'a') as opf:
                    create_function_const = 'CREATE FUNCTION '
                    if create_function_const in line:
                        line = line.replace(create_function_const,'CREATE OR REPLACE FUNCTION ')
                    opf.write(line)       
                    opf.close
    if cntr == 1 :
        print ("No files created. Ensure that pg_dump was run with -v (verbose mode)!")
fo.close()




    