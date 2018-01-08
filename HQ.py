import requests
import time
from bs4 import BeautifulSoup as bs

def search(question, choice1, choice2, choice3):
    global session
    qurl = "https://www.google.com/search?q=" + question + " -youtube"
    print(qurl)
    searchpage = bs(requests.get(qurl).text, 'html.parser')
    findlink1 = searchpage.find_all('a', limit =20)
    print(findlink1)



if __name__ == "__main__":

    question = "how to eat?"
    choice1 = "boogers"
    choice2 = "lard"
    choice3 = "pizza"
    search(question, choice1, choice2, choice3)
