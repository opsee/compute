# In Ansible lots of things take lists (or comma seperated
# strings), however lots of things return dicts. One
# example of this is the hostvars and groups variable.
#
# groups returns a list of machines in a group, and
# hostvars is a dict containing all the hosts. So if you
# need a list of ip addresses of those hosts for the
# route53 module you cant. This filter makes this possible.

def dict_values(d):
    return d.values()

def dict_keys(d):
    return d.keys()

class FilterModule(object):
    def filters(self):
        return {
            'dict_values': dict_values,
            'dict_keys': dict_keys
        }
