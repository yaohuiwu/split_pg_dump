import sys
import re
import os
import argparse

parser = argparse.ArgumentParser(description='Split output from pg_dump into seperate files. See https://github.com/ajgreyling/split_pg_dump')
parser.add_argument('sourcefile',help='SQL input file. Typically from pg_dump')
parser.add_argument('-ns','-nosequence', dest='nosequence',action='store_true',help='Omit the sequence number prefix for resulting filenames. Handy for comparing schemas between databases')
parser.add_argument('-nt','-notype', dest='notype',action='store_true',help='Ommit the type prefix in resulting filenames' )
args = parser.parse_args()

type_prefix = {
    'MATERIALIZED VIEW' : 'mv_',
    'SEQUENCE' : 'sq_',
    'INDEX' : 'ix_',
    'TABLE' : 'tb_',
    'TYPE' : 'ty_',
    'VIEW' : 'vw_',
    'FUNCTION' : 'fn_'
}
#print "input file:", args.sourcefile
print args.nosequence
inputfile = ''
inputfile=args.sourcefile
# delete contents of 00000_pre_execute.sql. If it does not exist, create it
#open('00000_pre_execute.sql', 'w').close()

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
                skip = (object_type == 'SCHEMA' or object_type == 'TABLE' or '__idx_he_' in object_name or '__he_' in object_name or object_name in '__change_')
                if not skip :
                    object_type_set.add(object_type)

                    if (newfile):
                        filename = ''
                        if not args.nosequence:
                            filename = '{0:05d}'.format(cntr) + '_'
                        if not args.notype:
                            filename += type_prefix[object_type]
                        filename += object_name + '.sql'

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

#def write_pre_excute(object_name)
#    with open ('00000_pre_execute.sql','a') as opf:
#        opf.write('\nDO $$ BEGIN\n')
#        opf.write('PERFORM __he_delete_table_or_view__(\'' + object_name + '\');\n')
#        opf.write('END $$;\n\n')   