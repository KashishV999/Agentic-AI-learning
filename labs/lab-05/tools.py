# This file contains utility functions for reading files from GitHub repositories.


from urllib import response

import requests
from typing import List
from github_file_object import GithubFile

def read_github_files(files: List[GithubFile]):
    contents =[]
    for file in files:
        url = f"https://raw.githubusercontent.com/{file.owner}/{file.repo}/{file.ref}/{file.path}"
        try:
            response = requests.get(url)
            response.raise_for_status()

            content = response.text

            # If the file is too long, truncate it and add a note about truncation
            lines = response.text.splitlines()  #converts to list of lines
            if len(lines) > file.truncateValue:
                content = "\n".join(lines[:file.truncateValue]) + f"\n... [File truncated : showing first {file.truncateValue} of {len(lines)} lines]"   # joins turns back list to string

            contents.append(f"\n<file name='{file.path}'>\n{content}\n</file>\n")

            print(f"✓ Loaded GitHub file: {file.path} from {file.owner}/{file.repo}")
            
        except Exception as e:
            print(f"❌ Error loading GitHub file: {file.path} from {file.owner}/{file.repo}")
            contents.append(f"\n<file name='{file.path}'>\n... [Error loading file: {e}] ...\n</file>\n")
            print(f"   {e}")

    return contents