import argparse
parser = argparse.ArgumentParser(prog=__file__.split(".")[0], description="Testing argparse")
parser.add_argument('-c', "--client", metavar='', type=str, help='the elasticsearch client')
parser.add_argument('-q', "--query", metavar='', type=str, help='the query to execute')
args = parser.parse_args()

client = args.client
query = args.query

if client:
  print(args.client)

if query:
  print(args.query)





# import sys

# args = sys.argv

# for arg in args:
#   print(f"{arg} [{type(arg)}]")