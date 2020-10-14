try:
    import oci
    import json
    from os import environ
except ImportError as e:
    print("ERROR: Python package '" + e.name + "' is required. Your can install this using 'pip install " + e.name + "'.")
    exit()

# plugin properties
# required
try:
    compartment_id = environ['RD_CONFIG_COMPARTMENT']
except KeyError as e:
    print('ERROR: compartment plugin property not specified') 
    exit()

# optional
config_file = environ.get('RD_CONFIG_OCI_CONFIG', None)
node_user = environ.get('RD_CONFIG_NODE_USER', 'opc')

# use oci config file, if provided
if config_file:
    try:
        config = oci.config.from_file(config_file)
    except:
        print('Could not open OCI Config File')
        exit()
    compute = oci.core.ComputeClient(config)
    network = oci.core.VirtualNetworkClient(config)
# assume InstancePrincipal, if oci config not provided
else:
    signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    compute = oci.core.ComputeClient({}, signer=signer)
    network = oci.core.VirtualNetworkClient({},signer=signer)

# process nodes
instances = compute.list_instances(compartment_id).data
nodes = {}
for instance in instances:
    node = {}
    node["nodename"] = instance.display_name
    node["username"] = node_user
    vnic_attachments = compute.list_vnic_attachments(
        compartment_id=compartment_id, 
        instance_id=instance.id
    ).data
    
    for vnic_attachment in vnic_attachments:
        vnic = network.get_vnic(vnic_attachment.vnic_id).data
        if vnic.is_primary:
            node["hostname"] = vnic.private_ip

    nodes[instance.display_name] = node

# print nodes
print(json.dumps(nodes))

