import re
import urllib.parse

class MarkdownParser:
    def __init__(self,file_path,token,user):
        self.user = user
        self.token = token
        self.file_path = file_path
        self.url = None
        self.gistId = None
    
    def parse(self):
        reUrl = re.compile(r'\[gist-sync-url\]:(.*)',re.I)

        with open(self.file_path, 'r') as f:
            for line in f:
                urlMatch = reUrl.match(line)
                if urlMatch:
                    self.url = urlMatch.group(1)
                    urlret = urllib.parse.urlparse(self.url)
                    path = urlret.path
                    if path[-1] == '/':
                        path = path[:-1]
                    self.gistId = path.split('/')[-1]
                    self.user = path.split('/')[-2]
                    break

        return self.gistId != None and self.user != None

    def syncTo(self, path):
        if not self.gistId or not self.user:
            return False

        
        
        reTitle = re.compile(r'\s?#\s+(.*)')
        reImg = re.compile(r'!\[.*\]\((.*)\)')

        with open(self.file_path, 'r') as f:
            for line in f:
                titleMatch = reTitle.match(line)
                if titleMatch:
                    self.title = titleMatch.group(1)

                imgMatch = reImg.match(line)
                if imgMatch:
                    imgStr = imgMatch.group(1)
                    imgPath = imgStr.split()[0]
                    # if not imgPath.startswith("http"):
                    #     self.imgs.append(imgPath)

        