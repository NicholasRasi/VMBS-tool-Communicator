import argparse
import json
import requests
import yaml
import logging
import coloredlogs


# setup logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', milliseconds=False, logger=logger)
logger.info("Start cloud benchmark")

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bin', type=str, required=False)
parser.add_argument('--poweroff', type=bool, required=False)
args = parser.parse_args()

# read bin id from file if not provided as an argument
if args.bin:
    bin_id = args.bin
else:
    f = open("bin_id.txt", "r")
    bin_id = (f.read())

# read configuration file
with open("config_benchmark_tools.yml", 'r') as file:
    data = file.read()
    config = yaml.load(data, Loader=yaml.FullLoader)

# setup bin url
sending_bin = config["bin_database_url"] + "/" + str(bin_id).strip()
logger.info("Sendind data to: " + sending_bin)

# read benchmark file
with open(config["benchmark_file"]) as json_file:
    payload = json.load(json_file)

# send data
logger.info("Sending payload: " + payload + " to " + sending_bin)
response = requests.post(sending_bin, payload, headers={'content-type': 'application/json'})
logger.info(response.text)

# poweroff
if args.poweroff:
    logger.info("Powering off...")