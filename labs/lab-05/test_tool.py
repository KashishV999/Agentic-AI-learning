# test_tool.py
from tools import read_github_files
from github_file_object import GithubFile
def test():
    print("Testing read_github_files...\n")

    content = read_github_files([
        GithubFile(
            owner="microsoft",
            repo="vscode",
            path="package.json",
            ref="main"
        ),
        GithubFile(
            owner="kubernetes",
            repo="website",
            path="README.md",
            ref="main"
        ),
    ])

    print(content)

if __name__ == "__main__":
    test()