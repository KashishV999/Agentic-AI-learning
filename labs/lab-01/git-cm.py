
import os
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime



def printHeader():
    now = datetime.now()
    print ("--------------------------------------------------------------")
    print("git-cm: Developed by Kashish Verma - 151579232")
    print("Run Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))
    print ("--------------------------------------------------------------")



def main():
    # Print the header information
    printHeader()

    # Locate the .env file by searching up the directory tree
    load_dotenv(find_dotenv())
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)

    else:
        print("OPENROUTER_API_KEY found successfully!!")


if __name__ == "__main__":
    main()
    