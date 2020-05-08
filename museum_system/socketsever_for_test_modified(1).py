import socket
import threading
import time
from time import sleep, ctime


sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(("192.168.1.102", 5438))
#sk.bind(("xxx.xxx.xx.xx",xxxx))
sk.listen(5)

print("sever listening 5438, maximum connection 5")

VISITED_TRUE = 1
VISITED_FALSE = 0

ALARM_LEVEL_FREE = 0
ALARM_LEVEL_APPROACHED = 1
ALARM_LEVEL_ALARMING = 2

BEEPER_ARMED_TRUE = 1
BEEPER_ARMED_FALSE = 0

nodeInfo = {
    # Info from node to hass
    "id": 1,
    # RFID success
    "collectionId": "9f63d0d1-eb9f-415d-8e59-77648825c609",
    # RFID fail (no card)
    # "collectionId": "None",
    "visited": 1,
    "alarmlevel": 0,
    "temperature": 21.0,
    "humidity": 45.0,
    # Info from hass to node
    "beeperarmed": 1
}

nodeList = []



def commu(conn):
    global nodeInfo
    global nodeList
    nodeList.append(nodeInfo)
    buf = conn.recv(99999)
    # Check packet head
    bs = str(buf, encoding="utf8")
    print(bs.split())
    content = bs.split()
    body = content[0]
    miss = content[1]
    temperature = content[2]
    humidity = content[3]
    idd = content[4]

    if body == 'nobody':
        nodeInfo["visited"] = 0
    elif body == 'somebody':
        nodeInfo["visited"] = 1

    if body == 'alarm':
        nodeInfo["alarmlevel"] = 1
    else:
        nodeInfo["alarmlevel"] = 0

    nodeInfo["collectionId"] = miss
    nodeInfo["temperature"] = temperature
    nodeInfo["humidity"] = humidity
    nodeInfo["id"] = idd
    nodeInfo["beeperarmed"] = 1
    #后续数据处理

    # Reply with beeperarmed
    conn.send(bytes(str(1)+'E', encoding="utf8"))

    # Log data into nodeList
    # nodeList[id].collectionId = bs[2] or so

    # Send back to hass (TODO)
    # updateData(nodeList[id])


while True:
    conn, address = sk.accept()
    thread = threading.Thread(target=commu, args=[conn])
    thread.start()