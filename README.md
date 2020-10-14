# OCI Instance Resource Model Source Plugin
A Resource Model Source plugin that provides OCI Instances as nodes for Rundeck

# Assumptions
* No sub compartments
* No duplicate display names
* Hostname will be private IP address from primary VNIC
* All nodes will connect with the same user. Default: opc

# Setup
* Place zip file in `/var/lib/rundeck/libext/`
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

