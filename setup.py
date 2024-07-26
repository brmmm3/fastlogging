"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/brmmm3/fastlogging
"""

import os
import sys
# To use a consistent encoding
from codecs import open
import shutil
try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

BASEDIR = os.path.dirname(__file__)
PKGNAME = 'fastlogging'
PKGDIR = os.path.join(BASEDIR, PKGNAME)
VERSION = "1.2.0"

if os.path.exists("build"):
    shutil.rmtree("build")
for filename in os.listdir(PKGDIR):
    if filename.endswith(".cpp") or filename.endswith(".c") or filename.endswith(".pyx") or filename.endswith(".html"):
        os.remove(os.path.join(PKGDIR, filename))

annotate = "annotate" in sys.argv
debug = "debug" in sys.argv
if debug:
    del sys.argv[sys.argv.index("debug")]
nocython = "nocython" in sys.argv

if nocython:
    del sys.argv[sys.argv.index("nocython")]
else:
    # noinspection PyUnresolvedReferences
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
        import Cython.Compiler.Version
    except ImportError:
        print("Warning: cython package not installed! Creating fastlogging package in pure python mode.")
        nocython = True

if nocython:
    install_requires = []
    cmdclass = {}
    packages = [PKGNAME]
    ext_modules = None
else:
    from pyorcy import extract_cython

    extract_cython(os.path.join(PKGDIR, 'fastlogging.py'))
    extract_cython(os.path.join(PKGDIR, 'network.py'))

    # noinspection PyUnboundLocalVariable
    print("building with Cython " + Cython.Compiler.Version.version)

    # noinspection PyPep8Naming
    class build_ext_subclass(build_ext):

        def run(self):
            build_ext.run(self)
            shutil.copyfile(PKGNAME + "/__init__.py", self.build_lib + "/" + PKGNAME + "/__init__.py")
            shutil.copyfile(PKGNAME + "/console.py", self.build_lib + "/" + PKGNAME + "/console.py")
            shutil.copyfile(PKGNAME + "/optimize.py", self.build_lib + "/" + PKGNAME + "/optimize.py")

        def build_extensions(self):
            if self.compiler.compiler_type == "msvc":
                for extension in self.extensions:
                    if debug:
                        extension.extra_compile_args = ["/Od", "/EHsc", "-Zi", "/D__PYX_FORCE_INIT_THREADS=1"]
                        extension.extra_link_args = ["-debug"]
                    else:
                        extension.extra_compile_args = ["/O2", "/EHsc", "/D__PYX_FORCE_INIT_THREADS=1"]
            else:
                for extension in self.extensions:
                    if debug:
                        extension.extra_compile_args = ["-O0", "-g", "-ggdb", "-D__PYX_FORCE_INIT_THREADS=1"]
                        extension.extra_link_args = ["-g"]
                    else:
                        extension.extra_compile_args = ["-O2", "-D__PYX_FORCE_INIT_THREADS=1"]
            build_ext.build_extensions(self)

    cythonize("fastlogging/*.pyx", language_level=3, annotate=annotate,
              exclude=["setup.py"])
    cmdclass = {'build_ext': build_ext_subclass}

    MODULES = [filename[:-4] for filename in os.listdir(PKGDIR)
               if filename.endswith(".pyx")]
    packages = None
    ext_modules = [
        Extension(PKGNAME + "." + module_name, sources=[PKGNAME + "/" + module_name + ".pyx"])
        for module_name in MODULES]


# Get the long description from the README file
with open(os.path.join(BASEDIR, 'README.rst'), encoding='utf-8') as F:
    long_description = F.read()

if annotate:
    sys.exit(0)

setup(
    name='fastlogging',
    version=VERSION,
    description='A faster replacement of the standard logging module.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://github.com/brmmm3/fastlogging',
    download_url='https://github.com/brmmm3/fastlogging/releases/download/%s/fastlogging-%s.tar.gz' % (VERSION, VERSION),

    author='Martin Bammer',
    author_email='mrbm74@gmail.com',
    license="MIT",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],

    keywords='fast logging',
    include_package_data=True,
    cmdclass=cmdclass,
    packages=packages,
    ext_modules=ext_modules
)
