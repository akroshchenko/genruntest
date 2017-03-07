#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import shutil
import sys
import tarfile
import tempfile
import urllib

import jinja2
import pkg_mastertool as pkglib

# TODO add function to check arguments
# TODO add function to test creates test
# TODO always switch "with_python3 0" on "with_python3 1" before parsing spec file

#def find_control_spec_file():
#    file = {'rpm':[],'deb':[]}
#    for root, dirname, filename in os.walk(os.getcwd()):
#        for item in filename:
#            if item.endwith('.spec'):
#                file['rpm'].append(os.path.join(root,filename))
#            if item == "control":
#                file['deb'].append(os.path.join(root, filename))
#    return file


def process_control_file(path):
    pass


def process_spec_file(path):
    if path is None:
        return
#        path = find_control_spec_file()['rpm']
    rpm_src = pkglib.RPMSrc(path)
    packages = rpm_src.get_packs()
    py2_packages = packages[:]
    py3_packages = []
    for pac in packages:
        if 'doc' in pac:
            py2_packages.remove(pac)
        if 'python3' in pac:
            py2_packages.remove(pac)
            py3_packages.append(pac)
    return {'py2':py2_packages, 'py3':py3_packages}


def choose_module_name(url):
    tempdir = tempfile.mkdtemp(suffix="-FORTEST", prefix="TEMPDIR-")
    downloaded_tar = urllib.urlretrieve(url, os.path.join(tempdir, 'targetpackage.tar.gz'))[0]
    extract_tar = tarfile.open(downloaded_tar, "r:gz")
    extract_tar.extractall(path=tempdir)
    extract_tar.close()
    for root, dirname, filename in os.walk(tempdir):
        if '__init__.py' in filename:
            dir_with_init = os.path.basename(root)
            break
    shutil.rmtree(tempdir)
    return dir_with_init



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--specfile', dest='specfile', help='path to the specfile (is a must option if control file is not set)')
    parser.add_argument(
        '-cl', '--control', dest='control', help='path to the control file (is a must option if spec file is not set)')
#    parser.add_argument(
#        '-m', '--module_name', dest='module_name', help='name of python module')
# TODO(akroshchenko) Add function 
#    parser.add_argument(
#        '-p', "--py-package", dest='py_package', help='name of PyPackage')
    parser.add_argument(
        '-u', '--url', dest='url', help='URL for downloading target PyPackage (is a must option)')
    args = parser.parse_args()

#    # Test
#    args.url='https://pypi.python.org/packages/00/dd/dc22f8d06ee1f16788131954fc69bc4438f8d0125dd62419a43b86383458/wrapt-1.10.8.tar.gz'


    if args.specfile is not None:
        packages=process_spec_file(args.specfile)
    else:
        print("Path to spec file is not set")
        sys.exit()

    if args.control is not None:
        packages=process_control_file(args.control)
    else:
        print("Path to control file is not set")


    TemplateLoader = jinja2.FileSystemLoader(os.getcwd())
    Env = jinja2.Environment(loader=TemplateLoader)
    template = Env.get_template('runtest_template.j2')

    print template.render(module_name=choose_module_name(args.url),
                          py2_packages=packages['py2'], py3_packages=packages['py3'])


if __name__ == '__main__':
    main()
