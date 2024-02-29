import config
import requests
import os

# def get_repository_files_recursively(owner, repo, path='', branch='master', token=None):
#     """
#     Retrieve all file names recursively in a directory of a repository from GitHub.

#     Args:
#     - owner (str): Username or organization name which owns the repository.
#     - repo (str): Name of the repository.
#     - path (str, optional): Path within the repository. Default is root directory.
#     - branch (str, optional): Branch name. Default is 'master'.
#     - token (str, optional): GitHub personal access token for authentication.

#     Returns:
#     - list: List of all file names in the specified directory and its subdirectories.
#     """
#     headers = {}
#     if token:
#         headers['Authorization'] = f'token {token}'
#     url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     contents = response.json()
#     files = []
#     for content in contents:
#         if content['type'] == 'file':
#             files.append(content['name'])
#         elif content['type'] == 'dir':
#             files.extend(get_repository_files_recursively(owner, repo, content['path'], branch, token))
#     return files

def download_file(url, file_path):
    """
    Download a file from the specified URL to the specified file path.

    Args:
    - url (str): URL of the file to download.
    - file_path (str): Local file path where the downloaded file will be saved.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    with open(file_path, 'wb') as f:
        f.write(response.content)

def download_repository_files(owner, repo, path='', branch='master', token=None, download_dir='downloaded_files'):
    """
    Download all PDF files in a directory of a repository from GitHub, including subdirectories.

    Args:
    - owner (str): Username or organization name which owns the repository.
    - repo (str): Name of the repository.
    - path (str, optional): Path within the repository. Default is root directory.
    - branch (str, optional): Branch name. Default is 'master'.
    - token (str, optional): GitHub personal access token for authentication.
    - download_dir (str, optional): Local directory where the downloaded files will be saved.

    Returns:
    - list: List of PDF file names downloaded.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    contents = response.json()
    downloaded_files = []
    for content in contents:
        if content['type'] == 'file' and content['name'].endswith('.pdf'):
            file_name = os.path.join(download_dir, content['name'])
            download_url = content['download_url']
            download_file(download_url, file_name)
            downloaded_files.append(file_name)
        elif content['type'] == 'dir':
            downloaded_files.extend(download_repository_files(owner, repo, content['path'], branch, token, download_dir))
    return downloaded_files

# Example usage
owner = 'couchbase'
repo = 'magma'
path = ''  # Optional: specify the directory path within the repository
branch = 'master'  # Specify the branch name
token = config.github_passkey
download_dir = '/Users/spatra/Desktop/Movie/Architect_Chat/Data_Collection/data'  # Specify the directory where files will be downloaded
downloaded_files = download_repository_files(owner, repo, path, branch, token, download_dir)
print("Downloaded files:", downloaded_files)
