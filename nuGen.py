try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper

import os
import sys
import yaml
import argparse
import collections

def read_drv_yaml_file(file_path):
    # open yaml file and read it
    if not os.path.exists(file_path):
        sys.exit('File not found: {}'.format(file_path))
    with open(file_path) as _file:
        data = yaml.load(_file, Loader=Loader)
        return dict({k.replace("-", "_"): v for k, v in data.items()})

def create_compList(_dict, odir):
    # open file
    with open(os.path.join(odir, 'compList.txt'), 'w') as f:
        # loop through components and create use statements
        od = collections.OrderedDict(_dict['components'].items())
        comp_str = [comp for comp in od.keys()]
        f.write('set(COMPS {})\n\n'.format(' '.join(comp_str)))
        for k1, v1 in od.items():
            f.write('# - auto-generated section for component: {}\n'.format(k1))
            if v1['shared']:
              f.write('set(BUILD_SHARED_LIBS true)\n')
            else:
              f.write('set(BUILD_SHARED_LIBS false)\n')
            _str = []
            _str.append('add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../')
            _str.append('{} '.format(v1['source_dir']))
            _str.append('${CMAKE_CURRENT_BINARY_DIR}/')
            _str.append('{})\n'.format(v1['source_dir']))
            f.write(''.join(_str))
            _str = []
            _str.append('target_include_directories({} INTERFACE '.format(k1))
            _str.append('${CMAKE_CURRENT_BINARY_DIR}/')
            _str.append('{})\n'.format(v1['source_dir']))
            f.write(''.join(_str))
            if 'fort_module' in v1:
              f.write('target_link_libraries(numet.exe {})\n'.format(k1))
            elif not v1['shared']:
              sys.exit('Static option selected but no fort_module for component: {}'.format(k1))
            f.write('install(TARGETS {})\n\n'.format(k1))

def create_compUse(_dict, odir):
    # open file
    with open(os.path.join(odir, 'compUse.inc'), 'w') as f:
        # loop through components and create use statements
        od = collections.OrderedDict(_dict['components'].items())
        for k1, v1 in od.items():
          if 'fort_module' in v1:
            f.write('use {}, only: {}SS => SetServices, {}SV => SetVM\n'.format(v1['fort_module'], k1, k1))

def create_compDef(_dict, odir):
    # open file
    with open(os.path.join(odir, 'compDef.inc'), 'w') as f:
        # loop through components and create use statements
        i = 1
        od = collections.OrderedDict(_dict['components'].items())
        for k1, v1 in od.items():
          if 'fort_module' in v1:
            f.write('CompDef({})%ssPtr => {}SS\n'.format(i, k1))
            f.write('CompDef({})%svPtr => {}SV\n'.format(i, k1))
            f.write('CompDef({})%name = "{}"\n'.format(i, k1))
            i = i+1

def main(argv):

    # default value
    odir = '.'

    # read input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--ifile' , help='Input driver yaml file', required=True)
    parser.add_argument('--odir'  , help='Output directory for generated code')
    args = parser.parse_args()

    if args.ifile:
        ifile = args.ifile
    if args.odir:
        odir = args.odir

    # read driver configuration yaml file
    dict_drv = read_drv_yaml_file(ifile)

    # create compList.txt for CMake
    create_compList(dict_drv, odir)

    # create compUse.inc
    create_compUse(dict_drv, odir)

    # create compDef.inc
    create_compDef(dict_drv, odir)

if __name__== "__main__":
	main(sys.argv[1:])
