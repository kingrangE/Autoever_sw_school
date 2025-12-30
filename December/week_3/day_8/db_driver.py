# 강사님 따라하기
import sys

import pymysql
import time

try :
    tmp = pymysql.connect(host='localhost',port=3306,user='root',password='6764',database='adam')
    
    #SQL 실행 객체 생성
    sql_execution_object = tmp.cursor()
    """DML 실행
    sql_execution_object.execute(f"INSERT INTO usertbl VALUES(6,'개떵개','2025-12-30')")
    sql_execution_object.execute("UPDATE usertbl SET name=%s WHERE name=%s",('개개개','개떵개'))
    tmp.commit() #commit으로 작업 사항 반영 필요
    """
    
    """procedure 실행
    sql_execution_object.callproc('myproc',('11','파테스','2025-01-01'))
    """

    """DB 읽어와서 출력
    sql_execution_object.execute("SELECT * FROM usertbl")
    result = sql_execution_object.fetchall() # 한 번에 전체 출력
    while True:
        result =sql_execution_object.fetchone() # 한개씩 반복 출력
        if not result :
            break
        print(result)
    """

    """ 파일 읽고 저장
    FILE_PATH = 'kingrangE.png'
    with open(FILE_PATH,"rb") as f :
        image = f.read()
    sql_execution_object.execute("INSERT INTO blobTest VALUES(%s,%s,%s)",(1,'kingrangE',image))
    tmp.commit()
    """

    """저장된 파일 불러와 로컬 저장
    FILE_PATH = "new.png"
    sql_execution_object.execute("SELECT * FROM blobTest")
    with open(FILE_PATH,"wb") as f:
        f.write(sql_execution_object.fetchone()[2])
    """
    

except Exception as e :
    print("작업 실패",sys.exc_info())
    print("Error :",e)