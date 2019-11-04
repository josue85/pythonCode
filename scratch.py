import socket, select, queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('localhost', 12345))
server.listen(5)

inputs = [server]
outputs = []
messageQueue = {}

while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # inputs
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(False)
            inputs.append(connection)
            messageQueue[connection] = queue.Queue()

        else:
            data = s.recv(1024)
            if data:
                messageQueue[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                #readable socket with no data is a disconnect
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                del messageQueue[s]

    # outputs
    for s in writable:
        try:
            nextMessage = messageQueue[s].get_nowait()
        except:
            if s in outputs:
                outputs.remove(s)
        
        else:
            s.send(nextMessage)

    # Exceptions
    for s in exceptional:
        # be gone you 
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del messageQueue[s]





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
# from webHttp.UrlHandler import UrlHandler

# def testCreate(classToCreate):
#     obj = classToCreate()
#     obj.handleUrl()

# testCreate(UrlHandler)
