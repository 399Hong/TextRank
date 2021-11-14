from textRank import textRank
import util
import re
import time



if __name__ == "__main__":
    mode = int(input("Enter 1 for demo, 2 for testing on dataset\n"))

    if mode == 1:
        fileName= "inp.txt"
        tr = textRank.textRank()
        tr.readText(fileName)
        tr.lazySetup()
        tr.lazyLoad()
        tr.displaySents()

    if mode == 2:
        # set up text Rank
        tr = textRank.textRank()

        tr.lazySetup()
        
        '''
        fileName = "glove.6B.200d.txt"
        tr.installStopWords()
        tr.glove(fileName)
        '''

        # getting all files
        articles = util.getArticle()
        summaries = util.getSummary()

        path = util.get_project_root()/"BBC News Summary"

        matches = 0
        total = 0
       
        target = ""
        cur = 0
        liMax = []
        liNoFound = []
        while (a := next(articles, None)) is not None: 
            total +=1
            s = next(summaries)
            # read article and get top 7 
            print()
            print("Processing ",end = "")
            print(path/"News Articles"/a[1]/a[0])
            print()
            tr.reset()
            tr.readText(path/"News Articles"/a[1]/a[0])
            tr.lazyLoad()
            modelOutput = tr.getSents()

            # read sumamries 
            expectedOutput = util.processExpectedSummaries(path/"Summaries"/a[1]/a[0])
            newMatches = util.compare(modelOutput,expectedOutput)
            if newMatches > cur:
                cur = newMatches
                liMax.append(a[1]+"/"+a[0])
            if newMatches == 0:
                liNoFound.append(a[1]+"/"+a[0])


            matches += newMatches
            print(f"processed {total} articles(s), found {matches} matches.")
        print(f"Maximum: {cur} matches found in {liMax}")
        print(f"Zero: {0} matches found in {liNoFound}")

end = time.time()
print(end - start)
        #2225
           
           
        
