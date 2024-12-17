import subprocess

def get_commit_hashes():
    # Get the latest commit hash
    result = subprocess.run(['git', 'log', '--pretty=format:%H', '-n', '2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print("Error running git log:", result.stderr)
        return None, None

    # Get the latest two commit hashes
    commits = result.stdout.splitlines()
    if len(commits) < 2:
        print("Not enough commits in the repository.")
        return None, None

    return commits[1], commits[0]  # Previous commit and latest commit

def get_diff_files(previous_commit, latest_commit):
    # Get the diff between two commits to see what files have been added, modified, or removed
    result = subprocess.run(['git', 'diff', '--name-status', previous_commit, latest_commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("Error running git diff:", result.stderr)
        return [], [], []

    # Initialize lists to store file names
    added_files = []
    updated_files = []
    removed_files = []

    # Process the diff output
    lines = result.stdout.splitlines()
    for line in lines:
        status, file_path = line.split("\t")
        if status == 'A':
            added_files.append(file_path)   # A for Added
        elif status == 'M':
            updated_files.append(file_path)  # M for Modified
        elif status == 'D':
            removed_files.append(file_path)  # D for Deleted

    return added_files, updated_files, removed_files

def main():
    previous_commit, latest_commit = get_commit_hashes()
    
    if previous_commit is None or latest_commit is None:
        return
    
    added_files, updated_files, removed_files = get_diff_files(previous_commit, latest_commit)
    
    # Print results
    print("Newly Added Files:")
    for file in added_files:
        print(f"  {file}")
    
    print("\nUpdated Files:")
    for file in updated_files:
        print(f"  {file}")
    
    print("\nRemoved Files:")
    for file in removed_files:
        print(f"  {file}")

if __name__ == "__main__":
    main()

