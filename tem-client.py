from simple_tem import TEMClient

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("-p", "--port", default = 3535)
args = parser.parse_args()
c = TEMClient(args.host, args.port)