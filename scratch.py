
# import requests
# from bs4 import BeautifulSoup

# response = requests.get("https://www.stackoverflow.com/questions")
# soup = BeautifulSoup(response.text, "html.parser")

# questions = soup.select(".question-summary")

# for question in questions:
#     print(question.select_one(".question-hyperlink").getText())
#     print(question.select_one(".vote-count-post ").getText())

# class myClass:
#     def __init__():
#         pass

#     def name():
#         print("My name is slim shady")

#     def place():
#         print("Welcome to my house, play that music too loud")



# test = globals()["myClass"]
# test.name()


# dictTest = {"LIST.SCRIPTS": "mystuff", "Jomama.SCRIPTS": "AnotherOne"}

# if "LIST.SCRIPTS" in dictTest:
#     print("oh my god!")
from webHttp.UrlHandler import UrlHandler

def testCreate(classToCreate):
    obj = classToCreate()
    obj.handleUrl()

testCreate(UrlHandler)