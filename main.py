import argparse
import json
import requests
import yaml
import logging
import coloredlogs
import os
from pathlib import Path

# setup logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', milliseconds=False, logger=logger)
logger.info("Start cloud benchmark")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--provider', type=str, required=False)
parser.add_argument('--id', type=str, required=False)
parser.add_argument('--poweroff', dest='poweroff', action='store_true')
parser.set_defaults(poweroff=False)
args = parser.parse_args()

# read configuration file
with open("config_benchmark_tools.yml", 'r') as file:
    data = file.read()
    config = yaml.load(data, Loader=yaml.FullLoader)

# read bin id from file if not provided as an argument
if args.provider and args.id:
    provider = args.provider
    id = args.provider
else:
    f = open("instance_metadata.txt", "r")
    provider = (f.readline())
    id = (f.readline())
sending_bin = config["bin_database_url"] + "/" + str(provider).strip() + "_" + str(id).strip()
logger.info("Sendind data to: " + sending_bin)

# read benchmark file
with open(str(Path.home()) + "/" + config["benchmark_file"]) as json_file:
    payload = json.load(json_file)

# send data
logger.info("Sending payload: " + json.dumps(payload, indent=2) + " to " + sending_bin)
response = requests.post(sending_bin, json.dumps(payload), headers={'content-type': 'application/json'})
logger.info(response.text)

# poweroff
if args.poweroff:
    logger.info("Powering off...")
    if provider == "AWS":
        os.system('sudo shutdown now')
    elif provider == "AZURE":
        response = requests.post(config["az_deallocate_vm_http"].format(config["az_subscription_id"],
                                                                        config["az_resource_group_name"],
                                                                        id))
        logger.info(response.text)
