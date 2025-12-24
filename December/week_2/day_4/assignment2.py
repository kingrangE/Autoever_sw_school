from collections import Counter
try :
    file = open("log.txt")
    msg = file.read()
    splitted_msg = msg.split("\n")
    count = list(map(lambda x : len(x.split(" ")),splitted_msg))
    
    result  = {}

    for split_msg in splitted_msg :
        ip = split_msg.split(" ")[0] 
        try :
            traffic =  int(split_msg.split(" ")[9])
        except Exception as e :
            traffic = 0
        result[ip] = result.get(ip,0)+traffic
    
    for k,v in result.items():
        print(f"{k} 주소로 들어온 트래픽 : {v}")
except Exception as e:
    print("[Error] 파일 처리 중 에러 발생 \n    Detail :",e)