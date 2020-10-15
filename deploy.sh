# run as rundeck user to deploy plugin
base=${RDECK_BASE:-/var/lib/rundeck}
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $dir
zip -r $base/libext/rundeck-oci-nodes-plugin.zip rundeck-oci-nodes-plugin/
cd -
