import argparse
import os
import shutil
import tarfile
import tempfile
import urllib

import jinja2
import pkg_mastertool as pkglib


# def check_arguments(args):
#     if args.py_package is None:
#         if args.specfile is None:
#             if
#         elif args.control is None:
#             raise AttributeError('Need specify either flag -p or (-s or -cl)')


def find_control_spec_file():
    file = {'rpm':[],'deb':[]}
    for root, dirname, filename in os.walk(os.getcwd()):
        for item in filename:
            if item.endwith('.spec'):
                file['rpm'].append(os.path.join(root,filename))
            if item == "control":
                file['deb'].append(os.path.join(root, filename))
    return file


def process_control_file(path=None):
    pass


def process_spec_file(path=None):
    if path is None:
        path = find_control_spec_file()['rpm']
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


# TODO add function to check arguments
# TODO add function to test creates test
def choose_module_name(url):
    tempdir = tempfile.mkdtemp(suffix="-FORTEST", prefix="TEMPDIR-")
    downloaded_tar = urllib.urlretrieve(url, os.path.join(tempdir, 'targetpackage.tar.gz'))[0]
    extract_tar = tarfile.open(downloaded_tar, "r:gz")
    extract_tar.extractall(path=tempdir)
    extract_tar.close()
    for root, dirname, filename in os.walk(tempdir):
        if '__init__.py' in filename:
            init_file = os.path.join(root, "__init__.py")
    dir_with_init = os.path.basename(os.path.split(init_file)[0])
    shutil.rmtree(tempdir)
    if len(dir_with_init) > 1:
        return "Cannot chose the directory in 'def choose_module_name(url)' "
    return dir_with_init



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--specfile', dest='specfile', help='path to the specfile')
    parser.add_argument(
        '-c', '--control', dest='control', help='path to the control file')
    parser.add_argument(
        '-m', '--module_name', dest='module_name', help='name of python module')
    #To use this parametr need to find out hot to receive URL for downloading (from PyPy)
    parser.add_argument(
        '-p', "--py-package", dest='py_package', help='name of PyPackage')
    parser.add_argument(
        '-u', '--url', dest='url', help='URL for downloading target PyPackage')
    args = parser.parse_args()


    args.url='https://pypi.python.org/packages/00/dd/dc22f8d06ee1f16788131954fc69bc4438f8d0125dd62419a43b86383458/wrapt-1.10.8.tar.gz'
    args.specfile = 'test_spec.spec'

    process_spec_file(args.specfile)

    TemplateLoader = jinja2.FileSystemLoader(os.getcwd())
    Env = jinja2.Environment(loader=TemplateLoader)
    template = Env.get_template('runtest_template.j2')

    packages = process_spec_file()
    print template.render(module_name=choose_module_name(args.url),
                          py2_packages=packages['py2'], py3_packages=packages['py3'])


if __name__ == '__main__':
    main()

# #!/usr/bin/python3
# #import jinja2
# import os
#
# # import rpmfile
# import pkg_mastertool as pkglib
# import traceback
# import unittest
# # import reqcontrol
# import argparse
#
#
# ### Parsing
# parser = argparse.ArgumentParser()
# parser.add_argument(
#   '-s', '--specfile', dest='specfile', help='Path to tht specfile')
# parser.add_argument(
#   '-cl', '--control', dest='control', help='Path to control file')
# parser.add_argument(
#   '-m', '--module_name', dest='module_name', help='Name of python module')
# args = parser.parse_args()
#
# ###
#
# # env = jinja2.Environment()
# # def RenderTemplate(path, *args):
# #
# #
# #    loader = jinja2.FileSystemLoader(os.getcwd())
# #    env = jinja2.Environment(loader=loader)
# # repo_conf1 = {"repoid":"test1",
# #               "name":"Test1",
# #               "baseurl":"http://172.18.162.63/" \
# #               "mos-repos/centos/mos9.0-centos7/proposed/x86_64/",
# #               "gpgcheck":"0"}
# #
# # repo_conf2 = {"repoid":"test2",
# #               "name":"Test2",
# #               "baseurl":"http://172.18.162.63/" \
# #               "mos-repos/centos/mos-master-centos7/os/x86_64/",
# #               "gpgcheck":"0"}
#
#
#
# def main():
#     rpm_src = pkglib.RPMSrc(path='test_spec.spec')
#     #print rpm_src.get_packs()
#     #print rpm_src["Source"]
#     packages = rpm_src.get_packs()
#     py2_package = packages[:]
#     py3_package = []
#     for pac in packages:
#         if 'python3' in pac:
#             py2_package.remove(pac)
#             py3_package.append(pac)
#
#     # print 'py2_package', py2_package
#     # print 'py3_package', py3_package
#     #py_package_src = 'wrapt - 1.10.8'
#     #py_package = pkglib.PyPackage(py_package_src)
#     py_package_src = 'https://pypi.python.org/packages/00/dd/dc22f8d06ee1f16788131954fc69bc4438f8d0125dd62419a43b86383458/wrapt-1.10.8.tar.gz'
#     py_package = pkglib.PyPackage(py_package_src)
#     print py_package
#
#
#     # py_package = pkglib.PyPackage('https://pypi.python.org/pypi/wrapt')
#     # print py_package
#     # source = if rpm_src["Source"] is None
#     # local_source = "local"
#     # py_package_src = local_source if local_source else rpm_src["Source0"]
#     # py_package = pkglib.PyPackage(py_package_src)
#
#
#
#
# if __name__ == "__main__":
#     main()
