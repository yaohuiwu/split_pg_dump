import sys
import re
import os
import argparse

parser = argparse.ArgumentParser(description='Split output from pg_dump into seperate files. See https://github.com/ajgreyling/split_pg_dump')
parser.add_argument('sourcefile',help='SQL input file. Typically from pg_dump')
parser.add_argument('-of','-outputdir',dest='outputdir',help='Optional alternative destination / output directory for SQL output files')
parser.add_argument('-ns','-nosequence', dest='nosequence',action='store_true',help='Omit the sequence number prefix for resulting filenames. Handy for comparing schemas between databases')
parser.add_argument('-nt','-notype', dest='notype',action='store_true',help='Ommit the type prefix in resulting filenames' )
parser.add_argument('-nc','-noclean', dest='noclean',action='store_true',help='Skip the step of cleaning the target directory of *.sql' )
parser.add_argument('-xn','-exludenames', dest='excludenames',nargs='+', help='Exclude objects these strings in their names')
parser.add_argument('-xt','-exludetypes', dest='exludetypes',nargs='+', help='Exclude objects these types')
args = parser.parse_args()

def should_be_skipped(object_name,object_type):
    for exclude_name in args.excludenames:
        if exclude_name in object_name:
            print "skipping due to name: " + object_name + " type: " + object_type
            return True
    for exclude_type in args.exludetypes:
        if exclude_type == object_type:
            print "skipping due to type: " + object_type + " name: " + object_name
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
    'SCHEMA' : 'sc_'
}

inputfile = ''
inputfile=args.sourcefile

output_dir = ''
if args.outputdir is None:
    output_dir = os.path.dirname(os.path.realpath(__file__))
else:
    output_dir = args.outputdir

if not args.noclean:
    files = os.listdir(output_dir)
    for filename in files:
        if filename.endswith(".sql"):
            os.remove(os.path.join(output_dir,filename))

with open(inputfile) as fo:
        skip = True
        newfile = True
        cntr = 1
        filename = ''
        object_type_set = set()
        for line in fo.readlines():
            match_result = re.search('-- Name: (?P<object_name>\w+)\(?\)?; Type: (?P<object_type>\w+ ?\w+);', line)
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

                        print filename
                        with open (filename,'w') as opf:
                            if object_type == 'VIEW' or object_type == 'MATERIALIZED VIEW':
                                opf.write('\nDO $$ BEGIN\n')
                                opf.write('PERFORM __he_delete_table_or_view__(\'' + object_name + '\');\n')
                                opf.write('END $$;\n\n')    
                            opf.write(line)
                            opf.close
                            cntr+=1
                        newfile = False
                    else:
                        opf.write(line)
            else:
                if skip == False:
                    with open (filename,'a') as opf:
                        opf.write(line)       
                        opf.close
fo.close()


    