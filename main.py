import sys, os

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)

for filename in os.listdir(package_dir_path):
    sys.path.insert(0, "%s/%s" % (package_dir_path, filename))

from web import app
