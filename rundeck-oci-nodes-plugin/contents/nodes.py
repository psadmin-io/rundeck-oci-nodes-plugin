try:
    import oci
    import json
    from os import environ
except ImportError as e:
    print("ERROR: Python package '" + e.name + "' is required. Your can install this using 'pip install " + e.name + "'.")
    exit()

# plugin properties

## required
try:
    compartment_id = environ['RD_CONFIG_COMPARTMENT']
except KeyError as e:
    print('ERROR: compartment plugin property not specified') 
    exit()

## optional
config_file = environ.get('RD_CONFIG_OCI_CONFIG', None)
node_user = environ.get('RD_CONFIG_NODE_USER', 'opc')
vnic_tag = environ.get('RD_CONFIG_VNIC_TAG', None)
defined_list = environ.get('RD_CONFIG_DEFINED_TAGS', None)
freeform_enabled = environ.get('RD_CONFIG_FREEFORM_TAGS', None)

# oci config

## use oci config file, if provided
if config_file:
    try:
        config = oci.config.from_file(config_file)
    except:
        print('Could not open OCI Config File')
        exit()
    compute = oci.core.ComputeClient(config)
    network = oci.core.VirtualNetworkClient(config)
## assume InstancePrincipal, if oci config not provided
else:
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    compute = oci.core.ComputeClient({}, signer=signer)
    network = oci.core.VirtualNetworkClient({},signer=signer)

# process nodes
instances = compute.list_instances(compartment_id).data
nodes = {}
for instance in instances:
    if instance.lifecycle_state == 'TERMINATED':
        # skip terminated instances
        continue

    node = {}
    node["nodename"] = instance.display_name
    node["username"] = node_user

    # hostname
    vnic_attachments = compute.list_vnic_attachments(
        compartment_id=compartment_id, 
        instance_id=instance.id
    ).data    
    for vnic_attachment in vnic_attachments:
        vnic = network.get_vnic(vnic_attachment.vnic_id).data
        
        if vnic.is_primary:
            # use primary vnic ip
            node["hostname"] = vnic.private_ip
        
        if vnic_tag in vnic.freeform_tags or vnic_tag in vnic.defined_tags:
            # use vnic tag override ip
            node["hostname"] = vnic.private_ip
            break

    # tags
    if freeform_enabled == "true":
        # convert all freeform tag values to comma seperated string
        node["tags"] = ', '.join(filter(None, instance.freeform_tags))

    if defined_list:
        for namespace in defined_list.split(','):
            namespace_tags = instance.defined_tags.get(namespace)
            if namespace_tags:
                # convert all defined tag values to comma seperated string
                if node["tags"]:
                    node["tags"] = node["tags"] + ", " + ', '.join(filter(None, namespace_tags.values()))
                else:
                    node["tags"] = ', '.join(filter(None, namespace_tags.values()))

    nodes[instance.display_name] = node

# print nodes
print(json.dumps(nodes))

