import config

from github import Github

# Authentication is defined via github.Auth
from github import Auth

# using an access token
auth = Auth.Token(config.github_passkey)

# Public Web Github
g = Github(auth=auth)

for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    print(dir(repo))

g.close()