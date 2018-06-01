import sys
import re
import os

type_prefix = {
    'MATERIALIZED VIEW' : '_mv_',
    'SEQUENCE' : '_sq_',
    'INDEX' : '_ix_',
    'TABLE' : '_tb_',
    'TYPE' : '_ty_',
    'VIEW' : '_vw_',
    'FUNCTION' : '_fn_'
}

print "input file:", sys.argv[1]
inputfile=sys.argv[1]
with open(inputfile) as fo:
        skip = True
        newfile = True
        cntr = 1
        filename = ''
        object_type_set = set()
        for line in fo.readlines():
            match_result = re.search('-- Name: (?P<object_name>\w+\(?\)?); Type: (?P<object_type>\w+ ?\w+);', line)
            if not (match_result is None):
                newfile = True
                object_name = match_result.group('object_name')
                object_type = match_result.group('object_type')
                if object_name == 'FUNCTION':
                    print object_name
                skip = (object_type == 'SCHEMA' or object_type == 'TABLE' or '__idx_he_' in object_name or '__he_' in object_name)
                if not skip :
                    object_type_set.add(object_type)

                    if (newfile):
                        filename = '{0:05d}'.format(cntr) + type_prefix[object_type] + object_name + '.sql'
                        print filename
                        with open (filename,'w') as opf:
                            if object_type == 'VIEW':
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