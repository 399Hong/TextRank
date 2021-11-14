from pathlib import Path
from os import listdir
import re
def get_project_root() -> Path:
    return Path(__file__).parent

def outputEvaluation():
    pass

def getArticle() -> tuple:

    path = get_project_root()/"BBC News Summary"/"News Articles"
    dir_s = listdir(path)
    if ".DS_Store" in dir_s:
        dir_s.remove(".DS_Store")
    for dir in dir_s:
        # looping through folder
        files = listdir(path/dir)
        for file in files:
            yield (file,dir)# file name, dir name


def getSummary() -> tuple :
    path = get_project_root()/"BBC News Summary"/"Summaries"
    dir_s = listdir(path)
    if ".DS_Store" in dir_s:
        dir_s.remove(".DS_Store")
    for dir in dir_s:
        # looping through folder
        files = listdir(path/dir)
        for file in files:
            yield (file,dir)# file name, dir name

def processExpectedSummaries(filename: str) -> list:
    with open(filename,'r',encoding= 'unicode_escape') as f:
        text = f.read()
    pattern = re.compile(r'.*?[a-z][.]')
    sentences = re.findall(pattern, text)
    return [i.strip() for i in sentences]

def tokenizeSentences(text: str) -> list:
    pattern = re.compile(r'.*?[a-z][.]')
    return re.findall(pattern, text)

def compare(li1:list, li2:list):
    match = 0
    for i in li1:
        for j in li2:
            if(i == j):
                match += 1
    return match