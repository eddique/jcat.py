import argparse
from app import api

def main():
    try:
        api.run()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()