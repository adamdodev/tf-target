#!/usr/bin/env python3

import hcl
import pprint
import argparse
import os
import sys


def log(msg, type="print"):
    """
    Output logs to stderr instead of stdout
    This allows us to do something like `terraform plan $(target file.tf)`
    """
    if type == "pprint":
        msg = pprint.pformat(msg)
    print(msg, file=sys.stderr)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate Terraform targets from specific files.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                        help='files to parse to targets')

    args = vars(parser.parse_args())
    # log(args)
    
    for file in args['files']:

        parts = os.path.split(os.getcwd())

        current_module = parts[-1]

        with open(file, 'r') as fp:

            obj = hcl.load(fp)
            # log(obj)

            log("\nFound the following targets:\n")

            target_string = ''

            if 'module' in obj:
                for module_name in obj['module']:
                    resource_id = "module.{}.module.{}".format(current_module, module_name)
                    log(resource_id)
                    target_string += "-target={} ".format(resource_id)
            
            if 'resource' in obj:
                for resource_type in obj['resource']:
                    for resource_name in obj['resource'][resource_type]:
                        resource_id = "module.{}.{}.{}".format(current_module, resource_type, resource_name)
                        log(resource_id)
                        target_string += "-target={} ".format(resource_id)
            


            log("\n------------------------------------------------------------------------\n")

            # Output the final string of targets
            print(target_string)
