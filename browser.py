
# write your code here

import os
import sys
import requests

from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()


def main():

# ..............Sec1: Create Directory from Command Line....................

    # block creates a new directory if argument supplied on command line
    #block also saves the abspath of the new directory
    global save_path
    if len(sys.argv)==2:
        print(sys.argv[1])
        if os.path.isdir(sys.argv[1]):
                    save_path = os.path.abspath(sys.argv[1])
        else:
            os.mkdir(sys.argv[1])
            save_path = os.path.abspath(sys.argv[1])

#..............END Sec1................................................

    masterList = [] #  Keeping track of shortcut commands
    global pages
    pages = [] #  Keeping track of pages for Stack

#.............................Sec2: Main loop.......................

    x = 1
    while x:

        userIn = input("> " )


        if CheckDot(userIn) is True:
            r = requests.get(doPrefix(userIn))
            if r: #all good, save and load webpage

                print(Style.RESET_ALL)
                parsedPage = TextOnly(r)
                print(Style.RESET_ALL)

                masterList.append(RemoveDot(userIn))
                pages.append(parsedPage)
                SaveFile(RemoveDot(userIn), doPrefix(userIn), save_path)
                print(parsedPage)
                print(Style.RESET_ALL)

            else:
                print('no good webpage')

        # elif userIn == 'bloomberg.com':
        #     masterList.append(RemoveDot(userIn))
        #     pages.append(bloomberg_com) # save this page in stack
        #     SaveFile(RemoveDot(userIn),userIn, save_path)
        #     print(bloomberg_com)
        #
        # elif userIn == 'nytimes.com':
        #     masterList.append(RemoveDot(userIn))
        #     pages.append(nytimes_com) #save this page in stack
        #     SaveFile(RemoveDot(userIn),userIn, save_path)
        #     print(nytimes_com)

        elif userIn in masterList: #this is for the back function
            OpenFile(userIn, save_path)

        elif userIn == ('back'):
            Back()

        elif userIn == 'exit':
            x = 0

        else:
            print("error , url must have dot or entry must be in saved tab")



#.......................END Sec2..........................................

#......................Sec3: Methods.....................................

def TextOnly(r):
    #  Parses a website returning only text. 'r' is a requests object
    soup = BeautifulSoup(r.text,'html.parser')

    allText = soup.findAll(text=True)
    wanted = ['p','h1','h2','h3','h4','h5','h6','a','ul','ol','li','title']
    output=''
    for t in allText:
        if t.parent.name in wanted:

            output += f'{t}'
    return output





def RemoveDot(s):
        if '.' in s:

            new = s.rsplit('.',1)
            return new[0]
        else:
             print('error')
             return False

def CheckDot(s):
    if '.' in s:
        return True
    else:
        return False

def SaveFile(title, website, save_path = os.getcwd()):
    complete_path = os.path.join(save_path,title +'.txt')
    r = requests.get(website)
    parsed = TextOnly(r)
    with open(complete_path,'w', encoding='utf8') as f:
        f.write(parsed)


def OpenFile(file_name, save_path):
        complete_path = os.path.join(save_path,file_name +'.txt')
        with open(complete_path,'r', encoding='utf8') as f:
            print(f.read())

def Back():
    if pages: # if the stack at second last entry exists
        pages.pop()# pop the last entry
        if pages: # check to see if there are still entries after popping
            print(pages[-1]) # show the new last entry
    else:
        return None


#......................PREFIX Fixing Section..................

def doPrefix(initInput):
    if checkPrefix(initInput) == False:
        return appendPrefix(initInput)
    else:
        return initInput

def appendPrefix(url):
    newUrl = 'https://' + url
    return newUrl

def checkPrefix(url):
    #  Returns true if valid https:// prefix, else false
    if url.find('https://') != 0:
        return False
    else:
        return True






if __name__ == '__main__':
    main()



