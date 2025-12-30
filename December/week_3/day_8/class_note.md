# 12월 30일
## VIEW
> 물리적인 테이블을 근거한 `논리적 가상 테이블`
- SELECT 구문을 메모리에 저장해두고 사용하는 것
- SELECT 구문의 결과가 TABLE이므로, 이 테이블에 이름을 붙여 사용하는 것
```sql
--기본 형식
CREATE [OR REPLACE] VIEW 뷰이름 [별명 나열]
AS
SELECT 구문
[WITH CHECK OPTION]
[WITH READ ONLY];
```
- REPLACE : ALTER를 쓸 수 없기에 사용하는것
    - 가상의 테이블이기에 ALTER를 사용할 수 없다.
- WITH CHECK OPTION : SELECT 구문에 WHERE절이 있는 경우, WHERE 조건에 맞지 않는 데이터를 삽입하거나 수정할 수 없도록 한다.
- WITH READ ONLY : 읽기 전용 설정

- 위코드 실행 시, `VIEW이름`으로 `SELECT 구문`이 `메모리에 저장`

- 예시, EMP_COPY 테이블에서 DEPTNO가 30인 데이터의 EMPNO, ENAME,DEPTNO를 조회하는 작업을 자주 수행 -> 이런 경우, 자주 사용하는 SELECT 구문을 메모리에 저장하고, 빠르게 수행할 목적으로 VIEW를 생성할 수 있다.
    ```sql
    CREATE OR REPLACE VIEW EMP_VIEW30
    AS
    SELECT EMPNO,ENAME,DEPTNO
    FROM EMP_COPY;
    WHERE DEPTNO=30;
    ```

### VIEW의 사용 목적
1. 실행 속도 향상
    - SELECT 구문 : 보조 기억 장치에 존재하는 것을 조회
    - VIEW 구문 : 메모리에 존재하는 것을 조회

2. 쿼리 길이 단축
    - `테이블처럼 사용 가능`하기 때문
    - SUB QUERY 대신에 VIEW로 만들어놓으면, VIEW이름만으로 SUB QUERY를 대신 할 수 있기 때문에 짧아짐 

3. 보안에 유리하다.
    - 실제 테이블 구조를 알려줄 필요가 없기 때문
    - 보안에서 가장 중요한 것은 `최소화`
        - 두 번째 컬럼만 필요하면, 두 번째 컬럼만 제공하는 것이 가장 좋음
        - 그래서 옛날엔 `VIEW`나 `PROCEDURE`로 제공했음.

### READ ONLY 옵션
- VIEW는 `가상의 테이블`이지만, `동적`으로 `물리적인 테이블`을 `참조해서 생성`된다.
- 옵션 없이 VIEW를 만들면 데이터의 삽입,삭제,갱신이 가능할 수도 있다.
- 이를 방지하고자 할 때, READ ONLY 옵션을 이용

#### 예시
```sql
-- 노 옵션
CREATE VIEW DEPT_VIEW1
AS
SELECT *
FROM DEPT_COPY;
-- 읽기 전용
CREATE VIEW DEPT_VIEW2
AS
SELECT *
FROM DEPT_COPY
WITH READONLY;
```
- 쓰기
```sql
-- READONLY 설정을 하지 않은 VIEW에 쓰기작업
INSERT INTO DEPT_VIEW1 VALUES(50,'비서','서울');
-- 원본 테이블 확인 (위의 변경 사항이 반영되었음) -> 즉, 원본에 영향이 감.
SELECT * FROM DEPT_VIEW1 
```
    - 이러한 이유로 VIEW를 사용할 때는 읽기 전용 계정을 만들어서, 계정에서 뷰를 읽기만 할 수 있도록 한다.



---
### 임시 테이블
- 테이블을 만들 때, `CREATE TEMPORARY TABLE`로 만들면 `임시 테이블`이 된다.
    - 현재 세션(연결)에서만 `접근 가능`하고, `세션이 만료`되면 테이블은 사라진다.
---


### CTE
- 중간 결과를 저장하기 위한 임시테이블
- `INLINE VIEW`와 유사한 역할
#### 기본 형식
```sql
WITH 테이블이름(컬럼이름) AS (서브 쿼리) 형식
```
- 위와 같이 생성하여 `현재 SQL`에서만 사용한다.
- VIEW와 별 차이가 없지만, `생명 주기`에서 차이가 존재한다.
    - VIEW : `DB가 존재하는 한` 계속 존재
    - CTE : `한 Transaction 내에서만` 존재

#### 예시, tStaff 테이블에서 DEPART가 영업부고, GENDER가 남자인 사원의 NAME,SALARY,SCORE를 가지는 CTE 생성
```sql
WITH TEMP(이름,급여,성취도) AS (
    SELECT NAME,SALARY,SCORE FROM tStaff WHERE DEPART = '영업부' AND GENDER = '남'
)
-- 서브 쿼리처럼 작성하면 된다.
```
- 이용, 평균 급여 이상인 사람을 구하기
    ```sql
    WITH TEMP(이름,급여,성취도) AS (
    SELECT NAME,SALARY,SCORE FROM tStaff WHERE DEPART = '영업부' AND GENDER = '남')
    SELECT * FROM TEMP WHERE 급여 >= (SELECT AVG(급여) FROM TEMP);
    ```
    ```sql
    -- CTE를 안 쓴다면?
    SELECT NAME 이름, SALARY 급여, SCORE 성취도
    FROM tStaff
    WHERE DEPART='영업부' AND GENDER = '남' AND SALARY >= (SELECT AVG(SALARY) FROM tStaff WHERE DEPART='영업부' AND GENDER = '남');
    -- WHERE DEPART='영업부' AND GENDER = '남' 이 조건을 두 번 쓰니까 이를 함수처럼 빼주는게 CTE다.
    -- CTE는 오로지 이것을 위함이므로, 한 트랜잭션 내에서 1번 사용하는 것이다.
    -- 즉, 자주 사용하는 데이터를 하나의 이름으로 만들어놓는 것
    -- INLINE VIEW를 쓴다면?
    SELECT NAME 이름, SALARY 급여, SCORE 성취도
    FROM (SELECT NAME,SALARY,SCORE FROM tStaff WHERE GENDER='남' AND DEPART= '영업부') t
    WHERE SALARY > (SELECT AVG(SALARY) FROM tStaff);
    ```


---
### INLINE VIEW
> FROM 절에 사용된 `SUB QUERY`, 모든 DB에서 다 사용할 수 있는 구문이다.
```sql
SELECT *
FROM (SELECT * FROM tCity) T; -- 이렇게 ()안에 SELECT문을 넣고, 별명을 넣어서 INLINE VIEW로 사용 가능
```
- SELECT의 결과는 항상 임시 `TABLE`(결과가 나온 당시에만 존재하는 테이블)
    - 파이썬에서 참조 변수 - 인스턴스간의 관계처럼 여기서도 SELECT로 생성된 임시테이블에 별명을 만들어서 사용이 가능하다.(이것이 INLINE VIEW)
- INLINE VIEW를 사용하면 성능이 좋아지는 경우가 많다.
    - DB = 디스크(보조기억 장치), TABLE = 메모리 -> 즉 메모리에 있는 것을 불러오는게 빠르므로, 테이블을 이용하는 VIEW가 빠르다.
#### 예시 : tStaff에서 Grade가 `과장`, `부장`인 사원중에 score가 70이상인 데이터 조회
```sql
-- NO INLINE VIEW
SELECT *
FROM tStaff
WHERE grade IN ('과장','부장') AND score>=70;
-- INLINE VIEW
SELECT *
FROM (SELECT * FROM tStaff WHERE grade IN ('과장','부장'))GBStaff
WHERE score>=70;
```

---
### 임시 테이블들의 차이
> INLINE VIEW가 제일 작고 VIEW가 가장 크다. 즉, 작은 것에서 해결되면 큰 것에선 당연히 해결할 수 있는 문제다.
#### INLINE VIEW : 자신이 속한 `SELECT` 구문에서만 사용 
#### CTE : 하나의 트랜잭션 내에서만 동작
#### TEMPORARY TABLE : 현재 세션에서만 사용 가능한 테이블
#### VIEW : 현재 데이터베이스 전체에서 사용 가능한 테이블
---

## 프로시저
- 만들면, 메모리에 상주함 (속도 향상)
- ㅎㅁ수처럼 동작하기 때문에, 변수를 주면, SQL 문장을 시작함
    - 외부에서 알 수 없음 -> 보안 향상
### 사용 목적


## TRIGGER

## OPTIMIZING

### INDEX
- 빠르게 조회하고 싶으 ㄹ때 사용하는 것
- 근데, 삽입, 삭제, 갱신에서는 안 좋아짐
    - INDEX를 같이 업데이트 해줘야 해서
- 장점
    1. 검색 속도가 빨라짐
    2. 시스템에 걸리는 부하를 줄여 시스템 전체 선응을 향상 시킴
- 단점
    - B트리 
        - 1/2 이상 채우는 트리
    - 조회할 때 2~4%로 조회하는 경우 IDX로 해두면 좋다.
        - 그러나, 대규모로 조화하ㅏ는 경우, 안하는 게 낫다.
- 종류
    - 클러스티 기반
    - 트리 기반
    - 넌 클러스터 기반
- 자동으로 생성되는 인덱스
- 인덱스를 사용해야 하는 경우, 사용하지 말아야 하는 경우

## 백업 및 복원
### 데이터베이스 백업
```sql 
-- 전체 데이터베이스백업
```
### 데이터 베이스 복원
```sql
-- 전체 데이터베이스 복원
mysql -u [아이디] -p[패스워드] < >
```
- 나중에 리눅스에서 크론잡으로 해보기

## 파이썬 연동
### 1. Programming 언어와 DB 연동
#### A. 필요한 정보
1. `DB 서버 위치`(IP, Domain) / `포트번호`(컴퓨터에서 외부 접속 가능한 Application을 구분하기 위한 번호) / `접속할 DB 이름` / `User ID와 PW`
    - 경우에 따라서는 `IP`와 `Port번호`만으로도 `접속 가능`한 경우가 있다.
    - 현재 컴퓨터는 IP를 `localhost` / `127.0.0.1`로 설정한다.
#### B. 프로그래밍 언어와 DB 사이에서 Interface 역할을 해 줄 드라이버 
---
### 2. 연동 방식
1. Driver 만으로 연동 : `SQL 필수`
2. ORM과 Framework를 이용 : `SQL 사용 X`, `Programming 언어의 함수 or 클래스를 이용`해서 작업 수행
---
### 3. MariaDB연동 실습
#### A. 필요한 정보
1. IP : localhost (자신의 PC)
2. 포트번호 : 3306 (DB port)
3. DB name : adam
4. User ID : root
5. 비밀번호 : 비밀 ㅎ
#### B. 드라이버
- Python이므로 pymysql 패키지 설치하기 
    - `pip install pymysql`
---
### 4. 접속 및 연동
#### 접속
```python
import pymysql

tmp = pymysql.connect(host='DB위치',port='포트번호(정수)',user='계정',password='비밀번호',database='데이터베이스이름',charset='인코딩방식')
```
#### 접속 해제
```python
tmp.close()
```
---
### 드라이버를 이용한 조작 실습
#### DML 수행
- `연결 객체` -> `cursor 호출` -> `SQL 실행 객체 생성`

    ```sql
    sql_execution_object = tmp.cursor()
    ```
- `sql 실행 객체.execute(실행할 SQL 문장[, 마운트될 데이터를 튜플로 설정])`
    1. `실행할 SQL 문장`에서 `직접 값 설정 가능`
        ```python
        sql_execution_object.execute(f"INSERT INTO usertbl VALUES(6,'개떵개','2025-12-30')")
        ```

    2. `실행할 SQL 문장`에 %로 표시한 후, `튜플로 값 대입` 가능
    
        ```python
        sql_execution_object.execute(f"INSERT INTO usertbl VALUES(%s,%s,%s)",(7,'ㄸㄱㄸ','2025-10-14'))
        sql_execution_object.execute(f"UPDATE usertbl SET name=%s WHERE name=%s",("개개개",'개떵개'))
        ```
        - 다만 이때, `SQL Injection`같은 문제를 막기 위해 execute 전, 유효성 검사를 잘 해야 한다. (불용어 검사 등)
    3. Python에서 `실행한 결과를 DB에 반영`하고자 하는 경우에는 `cursor().commit()`을 실행하여 반영해주어야 한다.
        - 만약, 취소하고자 하는 경우엔 `cursor().rollback()`을 실행해주면 된다.
        - 이 과정을 거치지 않으면, 아무리해도 DB에 반영되지 않는다.

#### DQL 수행
- SQL과 실행 방법 동일
- DB에 영향을 주는 것이 아니므로 `COMMIT`이나 `ROLLBACK`할 필요가 없다.
- SQL을 실행하고, SQL 실행 객체가 fetchone이나 fetchall 메서드를 호출하면 검색된 결과 데이터 1개 또는 여러 개를 tuple이나 tuple의 tuple로 리턴합니다.
    ```python
    # 한번에전체 출력
    sql_execution_object.execute("SELECT * FROM usertbl")
    result = sql_execution_object.fetchall()
    ```
    ```python
    # 한 개씩 출력
    while True: 
        result =sql_execution_object.fetchone()
        if not result :
            break
        print(result)
    ```
#### 프로시저 실행
- `cursor 객체`를 가지고 `callproc`라는 `메서드를 호출`하면 되는데, 첫 번째 매개변수는 `프로시저 이름`, `args`라는 매개변수에 입력 매개변수를 튜플로 대입해서 실행

- 프로시저가 `DML` 문장을 실행하는 경우라면, `commit` 과`rollback`을 호출해서 Transaction을 적용합니다.

- DB 접속 도구(DBeaver)에서 프로시저를 생성
    ```sql
    DELIMITER //
    CREATE PROCEDURE myproc(IN _userid INT,IN _name CHAR(3),IN _date date) -- IN은 안 써도 된다고 한다.

    BEGIN
    INSERT INTO usertbl VALUES(_userid,_name,_date); 

    END //
    DELIMITER ;
    ```
    - 프로시저를 쓰니까 TABLE 구조에 대해 몰라도 작업을 할 수 있다.

- 프로시저 실행 (`CALL`을 이용하여 `함수처럼 사용`)
    ```sql
    CALL myproc(10,'테스트','2026-01-01');
    ```
- 파이썬에서 procedure
    ```python
    cursor.callproc('프로시저이름',args=(프로시저 매개변수들))
    sql_execution_object.callproc('myproc',('11','파테스','2025-01-01'))
    ```

#### BLOB 연동
- `BLOB (Binary Large Object)`
    - 데이터베이스에서 비정형 데이터를 저장할 때 사용하는   데이터타입
    - 비정형 데이터는 `이미지`,`오디오`,`비디오`,`실행 파일` 등 `바이너리(이진)`형태의 데이터

- 예시, 이미지를 하나 BLOB로 저장
    1. BLOB를 담을 예시 테이블 생성
        ```sql
        CREATE TABLE blobTest(
            id INT PRIMARY KEY,
            filename VARCHAR(100),
            filecontent LONGBLOB
        );
        ```
    2. 파일을 읽고, DB에 저장
        ```python
        FILE_PATH = 'kingrangE.png'
        with open(FILE_PATH,"rb") as f :
            image = f.read()
        sql_execution_object.execute("INSERT INTO blobTest VALUES(%s,%s,%s)",(1,'kingrangE',image))
        con.commit()
        ```
    3. DB를 읽어 파일 저장
        ```python
        FILE_PATH = "new.png"
        sql_execution_object.execute("SELECT * FROM blobTest")
        with open(FILE_PATH,"wb") as f:
            f.write(sql_execution_object.fetchone()[2])
        ```

### ORM을 이용한 파이썬 조작
- `ORM` : Object Relational Mapping
    - `객체 지향 패러다임`을 `관계형 데이터베이스`에 `보존하는 기술`
    - `객체`와 `RDB의 테이블`을 매핑해서 사용하는 방법
    - `RDB의 테이블` = `객체 지향 언어의 Class`와 유사
        - `Class`와 `테이블`의 `불일치`를 `ORM이 해결`한다.

- 장점
    1. 특정 DB에 종속되지 않는다.
    2. 객체 지향적 프로그래밍 가능
    3. 생산성이 향상된다.
- 단점
    1. 쿼리 처리가 복잡하다.
    2. 설계를 잘못하면 성능이 떨어진다.
    3. ~~학습 시간~~
- 파이썬에서 많이 사용되는 ORM 
    - `SQLAlchemy`
    - 설치
        ```bash
        pip install sqlalchemy
        ```

#### import 및 연결 URL 설정
```python
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker

DB_URL = "mysql+pymysql://root:6764@localhost:3306/adam?charset=utf8mb4"
# MySQL DB : mysql+pymysql://사용자ID:사용자PW@IP:PORT/DATABASE?charset=
# Oracle DB : mysql+pymysql://사용자ID:사용자PW@IP:PORT/DATABASE?charset=

#데이터베이스 연결 통로생성
engine = create_engine(DB_URL,echo=True)
#echo가 True면 실제 수행되는 SQL을 확인할 수 있다.

#세션 설정 (통신할 수 있는 통로)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#모델 생성할 기본 클래스 생성
Base = declarative_base()
# 테이블 모델 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100),unique=True)

#테이블 자동 생성
Base.metadata.create_all(bind=engine)
```
#### 데이터 삽입
```python
db = SessionLoacl()
try :
    new_user = User(name="졸려요",email="iwanna")
    db.add(new_user)
    db.commit()

except Except as e:
    print("Error :",e)
finally:
    db.close()
```

### 데이터 조회
```python
db = SessionLoacl()
try :
    user = db.query(User).filter(User.name=="졸려요").first()
    print(user)
    print(user.name)

except Except as e:
    print("Error :",e)
finally:
    db.close()
```

#### 데이터 갱신
```python
db = SessionLoacl()
try :
    user = db.query(User).filter(User.name=="졸려요").first()
    print(user)
    print(user,name)

except Except as e:
    print("Error :",e)
finally:
    db.close()
```
## 참고
1. 자료구조 잘 공부해야 함
    - 그래야 알고리즘을 구현할 때, 자료구조를 적절하게 선택할 수 있다.
    - 알고리즘 문제를 풀 때도, 자료구조 안 보이는걸로 풀어서, 자료구조를 언제 어떻게 적절하게 쓰는지 알아라
    - 자료구조가 어디에 어떻게 이용되는지 공부하라.
2. Private Cloud에서 가장 구현하기 쉬운 것이 `DBMS`와 `File Server` 나중에 해볼거임
3. fflush() 
    - Computer는 OS와 통신하던 다른 Computer와 통신하던, 항상 전달하고 싶은 메시지를 Buffer에 넣고 Buffer를 전달하는 방식으로 한다.
    - 그래서 다른 것과 통신하는데 `마지막 메시지가 안 가는 경우는 버퍼에 있는 채로 종료`되기 때문, 따라서 `fflush를 추가해주면 해결`된다.
