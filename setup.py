# setup.py for hashlib standalone for Python versions < 2.5
#

__version__ = "20081119"

import sys, os, re

from distutils.core import setup, Extension
from distutils.ccompiler import new_compiler


# additional paths to check, set from the command line
SSL_INCDIR=''   # --openssl-incdir=
SSL_LIBDIR=''   # --openssl-libdir=
SSL_DIR=''      # --openssl-prefix=


def add_dir_to_list(dirlist, dir):
    """Add the directory 'dir' to the list 'dirlist' (at the front) if
    'dir' actually exists and is a directory.  If 'dir' is already in
    'dirlist' it is moved to the front."""
    if dir is not None and os.path.isdir(dir) and dir not in dirlist:
        if dir in dirlist:
            dirlist.remove(dir)
        dirlist.insert(0, dir)


def prepare_hashlib_Extensions():
    """Decide which C extensions to build and create the appropriate
    Extension objects to build them.  Returns a list of Extensions."""

    exts = []

    exts.append( Extension('_sha', ['shamodule.c']) )
    exts.append( Extension('_md5',
                    sources = ['md5module.c', 'md5.c'],
                    depends = ['md5.h']) )

    # OpenSSL doesn't do these until 0.9.8 so we'll bring our own
    exts.append( Extension('_sha256', ['sha256module.c']) )
    exts.append( Extension('_sha512', ['sha512module.c']) )

    def prependModules(filename):
        return os.path.join('Modules', filename)

    # all the C code is in the Modules subdirectory, prepend the path
    for ext in exts:
        ext.sources = [ prependModules(fn) for fn in ext.sources ]
        if hasattr(ext, 'depends') and ext.depends is not None:
            ext.depends = [ prependModules(fn) for fn in ext.depends ]

    return exts


# do the actual build, install, whatever...
def main():
    # parse command line for --openssl=path
    global SSL_INCDIR, SSL_LIBDIR, SSL_DIR
    for arg in sys.argv[:]:
        if arg.startswith('--openssl-incdir='):
            SSL_INCDIR = arg.split('=')[1]
            sys.argv.remove(arg)
        if arg.startswith('--openssl-libdir='):
            SSL_LIBDIR = arg.split('=')[1]
            sys.argv.remove(arg)
        if arg.startswith('--openssl-prefix='):
            SSL_DIR = arg.split('=')[1]
            sys.argv.remove(arg)

    setup(
      name =        'resumablehashlib',
      version =     __version__,
      description = 'Secure hash and message digest algorithm library',
      long_description = """\
This is a fork of the backported
hashlib from python 2.5, originally written by
Gregory P. Smith, which aims to open the internal
state of the sha256 library to make it resumable.
It will make no attempt to defer to a local openssl
version like the original.""",
      license = "PSF license",

      maintainer = "Jake Moshenko",
      maintainer_email = "jake.moshenko@coreos.com",
      url = 'https://github.com/coreos/resumablehashlib',

      ext_modules = prepare_hashlib_Extensions(),

      py_modules = [ 'resumablehashlib' ],
    )

if __name__ == '__main__':
    main()
