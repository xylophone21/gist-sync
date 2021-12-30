import git

def checkoutGist(workpath, user, token, gistID):
    g = git.cmd.Git(workpath)
    g.execute(['git', 'clone', f'https://{user}:{token}@gist.github.com/' + gistID + '.git'])