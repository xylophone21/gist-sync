import re
import os
import shutil
import urllib.parse
from zlib import compress
import base64
import string

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))

class MarkdownResult:
    def __init__(self):
        self.title = ""
        self.files = []

class MarkdownParser:
    def __init__(self,parent,filename,token,user):
        self.user = user
        self.token = token
        self.parent = parent
        self.filename = filename
        self.url = None
        self.gistId = None

    def deflate_and_encode(plantuml_text):
        """zlib compress the plantuml text and encode it for the plantuml server.
        """
        zlibbed_str = compress(plantuml_text.encode('utf-8'))
        compressed_string = zlibbed_str[2:-4]
        return base64.b64encode(compressed_string).translate(b64_to_plantuml).decode('utf-8')
    
    def parse(self):
        reUrl = re.compile(r'\[gist-sync-url\]:(.*)',re.I)

        file_path = os.path.join(self.parent, self.filename)
        with open(file_path, 'r') as f:
            for line in f:
                urlMatch = reUrl.match(line)
                if urlMatch:
                    self.url = urlMatch.group(1)
                    urlret = urllib.parse.urlparse(self.url)
                    path = urlret.path
                    if path[-1] == '/':
                        path = path[:-1]
                    self.gistId = path.split('/')[-1]
                    # self.user = path.split('/')[-2]
                    break

        return self.gistId != None and self.user != None

    def syncTo(self, path):
        if not self.gistId or not self.user:
            return None

        reTitle = re.compile(r'\s?#\s+(.*)')
        reImg = re.compile(r'.*!\[.*\]\((.*)\)')
        reCode = re.compile(r'(\s*)```(\w*)')

        retObj = MarkdownResult()
        retObj.files.append("index.md")

        mdPath = os.path.join(path, "index.md")
        inCode = False
        preSpace = ""
        codeTxt = ""
        with open(mdPath, 'w') as mdf:
            file_path = os.path.join(self.parent, self.filename)
            with open(file_path, 'r') as f:
                for line in f:
                    codeMatch = reCode.match(line)
                    if codeMatch:
                        info = codeMatch.group(2)
                        if not inCode and (info == "puml" or info == "plantuml"):
                            inCode = True
                            codeTxt = ""
                            preSpace = codeMatch.group(1)
                            line = ""
                        elif inCode:
                            inCode = False
                            pumlCode = MarkdownParser.deflate_and_encode(codeTxt)
                            codeTxt = ""
                            line = f'\n{preSpace}![plantuml](https://plantuml.io/plantuml/png/{pumlCode})\n'
                            
                    if inCode:
                        codeTxt += line
                        continue

                    titleMatch = reTitle.match(line)
                    if titleMatch:
                        retObj.title = titleMatch.group(1)

                    imgMatch = reImg.match(line)
                    if imgMatch:
                        imgStr = imgMatch.group(1)
                        imgPath = imgStr.split()[0]
                        newFilename = self._convertImgFileName(imgPath)
                        print("find img:", imgStr)
                        if newFilename is not None:
                            oldFile = os.path.join(self.parent, imgPath)
                            newFile = os.path.join(path, newFilename)
                            shutil.copyfile(oldFile, newFile)
                            retObj.files.append(newFilename)
                            # The path ref https://gist.github.com/cben/46d9536baacb7c5d196c/
                            newPath = os.path.join(self.gistId, "raw" , newFilename)
                            line = line.replace(imgPath, newPath)

                    mdf.write(line)

        for parent,dirnames,filenames in os.walk(path):
            if ".git" in parent:
                continue

            for filename in filenames:
                if filename not in retObj.files:
                    # print("remove file:" + filename)
                    os.remove(os.path.join(parent, filename))

        return retObj

    def _convertImgFileName(self, path):
        if path.startswith("http"):
            return None

        newFilename = "z"+path.replace("/", "_").replace("..", "_")
        return newFilename

        