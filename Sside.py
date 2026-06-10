import socket,os
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('172.29.19.197',63635))#socket.gethostname()
host = socket.gethostname()
port = 63635

commands = ["ls","create","check"]
common_key =12
# Check if there is user with its password
def check(user ,password):
    succeful_opration = False
    with open("file.txt","r") as fd:
        rd=fd.readlines()
        if rd:    
            info = []
            for obj in rd:
                info.append(obj.split(":"))
            for i in range(0,len(info)):
                if user == info[i][0]:
                    if password == info[i][1]:
                        succeful_opration = True
        fd.close()
    return succeful_opration
# cypher password
def encrption(passord ,key):
    alphabeta ={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8
                ,"j":9,"k":10,"l":11,"m":12,"n":13,"o":14,"p":15,"q":16,"r":17
                ,"s":18,"t":19,"u":20,"v":21,"w":22,"x":23,"y":24,"z":25,"@":26,"#":27,
                "1":28,"2":29,"3":30,"4":31,"5":32,"6":33,"7":34,"8":35,"9":36,"0":37}
    alphabeta_list =["a","b","c","d","e","f","g","h","i"
                ,"j","k","l","m","n","o","p","q","r"
                ,"s","t","u","v","w","x","y","z","@","#",
                "0","1","2","3","4","5","6","7","8","9"]
    passord_after = ""
    for x in passord:
        new_key = alphabeta[x] - key
        passord_after = passord_after+alphabeta_list[new_key]
    return passord_after
def Seasion_Cookie(user):
    with open("file.txt","r") as fd:
        rd=fd.readlines()
        info = []
        for obj in rd:
            info.append(obj.split(":"))
        for i in range(0,len(info)):
            if user == info[i][0]:  
                Cookie =f"{info[i][2]}++{info[i][3].replace("\n", "")}"
        fd.close()    
    return Cookie

def list_files():
    in_file = str(os.getcwd())
    files = os.listdir(in_file)
    return files

def from_list_string(files):
    files2 = files
    for file in files2:
        file = file+"++"
    server.sendto(bytes(file,"utf-8"),address)

def last_id():
    with open("file.txt","r") as fd:
        rd=fd.readlines()
        info = []
        for obj in rd:
            info.append(obj.split(":"))
        for i in range(0,len(info)):
            info[i][2] =info[i][2].replace("\n", "")
        return int(info[-1][-1])
    
def create(user,password,social):
    founded =check(user,password=password)
    New_id_is = last_id()+1
    if not founded :
        with open("file.txt","a") as fd:
            fd.writelines(f"{user}:{password}:{social}:{New_id_is}\n")
            return "done"
    else:
        return "founded"

try:
    print(f"lising on {host}")
    
    while True:
        try:
            datas, address = server.recvfrom(1024)
            print(f"client:{address}: port {str(port)}")
            msg=datas.decode("utf-8")
            
            if msg == "syn":
                msg = "syn/ack"
                server.sendto(bytes(msg,"utf-8"),address)
            elif msg in commands:
                if msg == "ls":
                    from_list_string(list_files())
                elif msg == "create":
                    data = server.recvfrom(1024)
                    data = data[0].decode("utf-8").split(":")
                    does_there =create(data[0],encrption(data[1],key=common_key),data[2])
                    S_C = last_id()
                    if does_there == "founded":
                        server.sendto(bytes("found","utf-8"),address)
                    else:
                        server.sendto(bytes("done","utf-8"),address)
                        server.sendto(bytes(str(S_C),"utf-8"),address)
                else:
                    data = server.recvfrom(1024)
                    data = data[0].decode("utf-8").split(":")
                    is_there = check(data[0],encrption(data[1],key=common_key))
                    
                    if is_there:
                        server.sendto(bytes("found","utf-8"),address)
                        S_C = Seasion_Cookie(data[0])
                        server.sendto(bytes(S_C,"utf-8"),address)
                    else:
                        server.sendto(bytes("not","utf-8"),address)

                    
        except Exception as e:
            print(f"the error :{e}")
            break
        except KeyboardInterrupt:
            break
except Exception as e:
    print(f"the error :{e}")
except KeyboardInterrupt:
    pass

