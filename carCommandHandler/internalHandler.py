import json
#import queue

def toJSON(message):
    if type(message) is bytes:
        message = message.decode("utf-8")
    return json.dumps(message)

def fromJSON(message):
    if type(message) is bytes:
        message = message.decode("utf-8")
    return json.loads(message)

#def commandQueueExe()
#cmd_queue = queue.Queue()
#for command in fileRead.read().split():
#    cmd_queue.put(command)

#while cmd_queue.empty() == False:
#    value = cmd_queue.get()
#    print(value)
#    if value == "END":
#        break

#print("End of program")

