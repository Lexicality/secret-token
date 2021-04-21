import argparse
import sys

from secret_token import decode, encode, validate


def main():
    parser = argparse.ArgumentParser(description="Secret token helper")
    parser.add_argument("action", choices=["encode", "decode", "validate"])
    parser.add_argument("secrets", metavar="SECRET", nargs="+")

    args = parser.parse_args()

    if args.action == "encode":
        for raw_secret in args.secrets:
            print(encode(raw_secret))
    elif args.action == "decode":
        for raw_secret in args.secrets:
            print(decode(raw_secret))
    else:
        for raw_secret in args.secrets:
            if not validate(raw_secret):
                print(f"Secret '{raw_secret}' is not valid!")
                sys.exit(1)


main()
