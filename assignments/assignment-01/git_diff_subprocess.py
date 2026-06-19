import subprocess
import sys


def get_staged_diff():
    try:
        # Run git diff --staged
        result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True, check=True)
        diff = result.stdout.strip()
        if not diff:
            print("❌ No staged changes found for review")
            sys.exit(1)
        return diff
    except subprocess.CalledProcessError:
        print("❌ Not a git repo.")
        sys.exit(1)




