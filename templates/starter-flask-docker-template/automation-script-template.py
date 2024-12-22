import os
import argparse

def main():
    # Your automation logic goes here
    print("Automation Script Running...")
    # Example: list files in a directory
    files = os.listdir('.')
    print("Files in current directory:", files)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Your script description here")
    parser.add_argument("--path", type=str, default=".", help="Path to scan")
    args = parser.parse_args()

    main()
