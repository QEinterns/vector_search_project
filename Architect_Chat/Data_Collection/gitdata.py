import config
import requests

def get_repository_files_recursively(owner, repo, path='', branch='master', token=None):
    """
    Retrieve all file names recursively in a directory of a repository from GitHub.

    Args:
    - owner (str): Username or organization name which owns the repository.
    - repo (str): Name of the repository.
    - path (str, optional): Path within the repository. Default is root directory.
    - branch (str, optional): Branch name. Default is 'master'.
    - token (str, optional): GitHub personal access token for authentication.

    Returns:
    - list: List of all file names in the specified directory and its subdirectories.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    contents = response.json()
    files = []
    for content in contents:
        if content['type'] == 'file':
            files.append(content['name'])
        elif content['type'] == 'dir':
            files.extend(get_repository_files_recursively(owner, repo, content['path'], branch, token))
    return files

# Example usage
owner = 'couchbase'
repo = 'magma'
path = ''  # Optional: specify the directory path within the repository
branch = 'master'  # Specify the branch name
token = config.github_passkey
file_names = get_repository_files_recursively(owner, repo, path, branch, token)
for i in file_names:
    print(i)
