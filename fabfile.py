from os.path import dirname
from fabric.api import local
from fabric.context_managers import lcd

ROOT = dirname(__file__)

def download_packages():
    """
    Downloads packages in requirements.txt and installs them into
    the packages folder.
    """
    from os import listdir, mkdir
    from os.path import splitext, isdir, join, exists
    from shutil import rmtree

    PKG_DIR = join(ROOT, 'packages')
    if not exists(PKG_DIR):
        mkdir(PKG_DIR)
    local("pip install --no-install -d packages -r requirements.txt")

    def extract_folders():
        with lcd(PKG_DIR):
            for f in listdir(PKG_DIR):
                f = join(PKG_DIR, f)
                func = 'tar x%%sf %s' %f
                name, ext = splitext(f)
                if ext in ('.gz','.tgz'):
                    func = func % 'z'
                elif ext in ('.bz2',):
                    func = func % 'j'
                else:
                    continue
                local(func)
                local('rm %s' % f)

    def zip_packages():
        with lcd(PKG_DIR):
            for f in listdir(PKG_DIR):
                f = join(PKG_DIR, f)
                if isdir(f):
                    with lcd(f):
                        local("zip -r -0 %s.zip . -i \*" % f)
                    rmtree(f)

    extract_folders()
    zip_packages()

def runserver():
    local("google_appengine/dev_appserver.py .")

