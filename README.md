# OCI Instance Resource Model Source Plugin
A Resource Model Source plugin that provides OCI Instances as nodes for Rundeck

# Assumptions
* Script interpreter will be `python3`
* Script uses python package `oci` 
* Will not traverse sub compartments
* Will not handle duplicate display names
* Hostname will be the private IP address from the primary VNIC
    * Unless an `Override VNIC Tag` is specified
* Username will be the same for all nodes

# Setup
* Download a release zip file from GitHub and place in `$RD_BASE/libext`
   * Default: `RD_BASE=/var/lib/rundeck`
   * Alternative: Clone repo and run `deploy.sh` as user `rundeck`
* Setup Rundeck server with OCI Access using Instance Principal or OCI Config File
* Logout and back in of Rundeck
* Select Project, Project Settings, Edit Nodes
* Add a new Node Source
* Enter properties, Save, Save

## Instance Principal
If Rundeck is running on an OCI Instance, then you can setup Instance Principal security for Node lookups.

* Create a Dynamic Group
    * Identity > Dynamic Group > rundeck
* Add Matching Rule to include Rundeck instance
    * Example: `Any {instance.id = 'ocid1.instance.oc1.iad.RUNDECK_ID_HERE'}`
* Add a Policy to allow the Dynamic Group read access to instances
    * Identity > Policies
    * Example" `allow dynamic-group rundeck to read instance-family in tenancy`
