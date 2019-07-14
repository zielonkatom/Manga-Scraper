from bs4 import BeautifulSoup
import urllib.request
import urllib.request
import os
from introLogo import logo
from math import ceil
import sys
import time

'''
Before downloading check if anime and url are correct.
Change which episode should be downloaded.
This one takes links form a file, if they are not there they will be
added to database after giving valid link.
'''


logo()
'''
Get all the links from the file, check the input, if it's not there adds the new link with a title
for further use.
'''
with open("links.txt", "r+") as file:
    links = {}
    print("""You can choose one from the database below or add
a new title to the collection.""")
    print("".center(60, "."))
    for s in file:
        title, address = s.strip().split(" - ")
        try:
            files = os.listdir("D://Manga/{}".format(title))
            maxEp = []
            for folder in files:
                if folder.split(".")[-1] == "mobi" or folder.split(".")[-1] == "py":
                    continue
                maxEp.append(int(folder.split(" ")[-1]))
                epNumber = max(maxEp)
        except FileNotFoundError:
            epNumber = 0
        print("-".rjust(5),title, "(",epNumber,")")
        links[title] = address
    print("".center(60, "."))
    anime = input("\nWhich manga would you like to download?\n")    
    if anime in links:
        link = links[anime]
    else:
        link = input("\nPlease provide a valid link.\n")
        links[anime] = link

        file.write("\n"+anime +" - "+ link)

start = int(input("\nInput first episode you wish to download: \n"))

end = int(input("\nInput the last episode you wish to download: \n")) + 1


def urlPage(link, ep):
    '''
    Proper reading the given url. Last part of the link is the most important.
    it always is like _someNumber of the episode.
    '''
    if len(link.split("_")[-1]) == 3:
        link = link[:-3]+"{}"
    elif len(link.split("_")[-1]) == 2:
        link = link[:-2]+"{}"
    elif len(link.split("_")[-1]) == 1:
        link = link[:-1]+"{}"
    else:
        print("Something went wrong with the link.")
        quit()
    url = link.format(ep)
    return url

def reqPage(url):
    '''
    Permission problems, need to change agent. Python's default agent is easily detectable. 
    '''
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req

def progressBar(i, N, size):
    '''Defining progress bar, just fancy stuff to watch.'''
    percent = float(i) / float(N)
    time.sleep(0.1)
    print('\r' + str(i).rjust(3,'0')+"/"+str(N).rjust(3,'0')+ " ["+str("#"*ceil(percent*size)).ljust(size)+"] " + str(int(percent*100)) +"%", end="")

   
for ep in range(start, end):
    #counter for progress bar
    counter = 1
    # define the name of the directory to be created, at least everything is sorted this way
    path = "/Manga/{}/{} {}".format(anime, anime, ep)

    try:  
        os.makedirs(path)
    except OSError:  
        print ("\nCreation of the directory %s failed" % path)
        if os.listdir(path):
            print("Already downloaded, check files.")
            continue
    else:  
        print ("\nSuccessfully created the directory D:/%s " % path)

    url = reqPage(urlPage(link, ep))
    
    pytanie = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(pytanie, features="lxml")
    #Soup doing its stuff and searching for all img on the website
    searchdiv = soup.select("#vungdoc img")
    print("Downloading..")
    for pages in searchdiv:
        pageLink = reqPage(pages['src'])
        try:
            f = urllib.request.urlopen(pageLink)
        except urllib.error.HTTPError:
            print('Something went wrong')
            continue
        filename, ext = (pages['src'].split('/')[-1].split('.'))
        output = open("D:\\Manga\{}\{} {}\{}.jpg".format(anime, anime, ep,str(filename).zfill(2)),"wb")
        
        output.write(f.read())
        output.close()
        progressBar(counter,len(searchdiv),50)
        counter = counter + 1
    print('\nDownloaded episode {}.'.format(ep))
print("\n\n")
print("".center(60, "."))
print("Done!".center(60, "."))
print("".center(60, "."))
print("\n\n")
input()
