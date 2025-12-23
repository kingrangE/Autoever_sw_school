# 과제 1 log.txt에 나타난 IP 개수 세기
from collections import Counter
try : 
    # 내용 읽기
    file = open("log.txt")
    msg = file.read()

    # 줄바꿈을 기준으로 분할 -> 접속 정보들이 줄마다 구분됨.
    # 공백을 기준으로 분할 -> 접속 정보 요소들이 구분됨 (0번째 : ip) 
    # ip 정보를 모아 list로 반환
    splitted_msg = list(map(lambda x : x.split(" ")[0],msg.split("\n")))

    # ip 정보들의 출현횟수를 Counter를 통해 세봄
    count_msg = Counter(splitted_msg)

    # 결과 출력
    print(count_msg)
except Exception as e: 
    print("[Error] : File 처리 중 문제 발생\na   Detail :",e)