import argparse

parser = argparse.ArgumentParser()  # setting up arguments


parser.add_argument("-ss", "--stepstyle")
args = parser.parse_args()


print(args.stepstyle)
