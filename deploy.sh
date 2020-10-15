# run as rundeck user to deploy plugin
base=${RDECK_BASE:-/var/lib/rundeck}
zip -r $base/libext/rundeck-oci-nodes-plugin.zip rundeck-oci-nodes-plugin/
