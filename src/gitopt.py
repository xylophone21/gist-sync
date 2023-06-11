import git
import os

class GistGit:
    def __init__(self, workpath, user, token, gistID,proxy=None):
        self.url = f'https://{user}:{token}@gist.github.com/' + gistID + '.git'
        config = "http.proxy="+proxy if proxy != None else None
        self.workpath = os.path.join(workpath, gistID)
        self.repo = git.Repo.clone_from(self.url, to_path=self.workpath,config=config)
        self.repo.config_writer().set_value("user", "name", user).release()
        self.repo.config_writer().set_value("user", "email", user+"@unkonw").release()
        self.repo.git.checkout()

    def commitAndPush(self, message="update"):
        if self.repo.is_dirty(untracked_files=True):
            self.repo.git.add('-A')
            self.repo.git.commit(m=message)
            self.repo.git.push()
