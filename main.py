import argparse
import json
import requests
import yaml
import logging
import coloredlogs
import os
from pathlib import Path
from metadata import Metadata

CONFIG_FILE = "config_benchmark_tools.yml"
INSTANCE_FILE = "instance_metadata.yml"

# setup logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', milliseconds=False, logger=logger)
logger.info("Start cloud benchmark")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--stop', dest='stop', action='store_true')
parser.set_defaults(stop=False)
args = parser.parse_args()

# read configuration file
with open(CONFIG_FILE, 'r') as file:
    data = file.read()
    config = yaml.load(data, Loader=yaml.FullLoader)

try:
    # check if instance metadata file exists
    with open(INSTANCE_FILE, 'r') as file:
        data = file.read()
        metadata = yaml.load(data, Loader=yaml.FullLoader)
except IOError:
    # build the metadata file
    print("Instance metadata file not accessible, building it")
    metadata = Metadata().metadata
    with open("instance_metadata.yml", 'w') as file:
        yaml.dump(metadata, file)

sending_bin = config["bin_database_url"] + "/" + metadata["provider"] + "_" + metadata["id"]
logger.info("Sendind data to: " + sending_bin)

# read benchmark file
try:
    bench_file = str(Path.home()) + "/" + config["benchmark_file"]
    with open(bench_file) as json_file:
        payload = json.load(json_file)

    # delete the file
    os.remove(bench_file)
    logger.info("File deleted")

    # send data
    logger.info("Sending payload: " + json.dumps(payload, indent=2) + " to " + sending_bin)
    response = requests.post(sending_bin, json.dumps(payload), headers={'content-type': 'application/json'})
    logger.info(response.text)
except Exception as e:
    logger.error(e)

# stop
if args.stop:
    logger.info("Send stop notify")
    response = requests.post(config["stop_url"], json.dumps(metadata), headers={'content-type': 'application/json'})