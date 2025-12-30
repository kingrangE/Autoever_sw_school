## VIEW
> 물리적인 테이블을 근거한 `논리적 가상 테이블`
- SELECT 구문을 `메모리에 저장`해두고 `사용`하는 것
- SELECT 구문의 `결과가 TABLE`이므로, 이 `테이블에 이름을 붙여 사용`하는 것
---
### VIEW 기본 형식
```sql
CREATE OR REPLACE VIEW 뷰이름 [(Column 별명 나열)] AS
SELECT문
[WITH CHECK OPTION]
[WITH READ ONLY];
```
- 예시1, VIEW 생성 과정에서 별명을 설정
    ```sql
    -- 성별이 남자인 데이터 정보를 가져와 별명으로 표기
    CREATE VIEW VIEW_TEST (이름,급여,점수) AS
    SELECT NAME,SALARY,SCORE
    FROM tStaff
    WHERE GENDER = '남';
    ```
- 예시2, SELECT 구문에서 별명 설정
    ```sql
    -- 예시1 과 같은 코드임
    CREATE VIEW VIEW_TEST AS
    SELECT NAME 이름, SALARY 급여, SCORE 점수
    FROM tStaff
    WHERE GENDER = '남';
    ```
#### OR REPLACE
> `CREATE OR REPLACE VIEW`는 없으면 새로 만들고, 있으면 덮어씌우라는 의미
- VIEW를 수정할 때, 삭제(DROP)후 다시 만들어야 하는 번거로움을 없애줌

- 예시, 위에서 만든 VIEW_TEST에서 SCORE를 없앤 VIEW로 만들고 싶다.
    ```sql
    CREATE OR REPLACE VIEW VIEW_TEST AS
    SELECT NAME 이름, SALARY 급여
    FROM tStaff
    WHERE GENDER = '남';
    ```
#### WITH CHECK OPTION
> View의 조건에 맞지 않는 데이터는 `삽입`이나 `수정`을 할 수 없게 해주는 조건
- 사용하는 상황 예시
    1. tStaff의 Salary는 INT면 입력 가능
    2. tStaff Salary가 300 이상인 직원만 확인하는 VIEW 생성
    3. VIEW로 Salary 100인 직원 추가
    4. tStaff 테이블엔 100인 직원이 추가가 되었지만, VIEW에서는 조건에 맞지 않아 확인되지 않음
    5. 이러한 문제를 막기 위해 `CHECK OPTION 사용`
        - CHECK OPTION이 VIEW의 WHERE절 조건에 맞지 않는 데이터 `삽입`,`수정`을 막아줌
- 예시, 
    ```sql
    CREATE OR REPLACE VIEW 300StaffView AS
    SELECT NAME,SALARY,SCORE
    FROM tStaff
    WHERE SALARY >= 300
    WITH CHECK OPTION

    UPDATE 300StaffView SET SALARY=100 WHERE NAME="강감찬" 
    -- SQL Error [1369] [44000]: (conn=5) CHECK OPTION failed 

    UPDATE 300StaffView SET SALARY=500 WHERE NAME="강감찬" 
    -- SUCCESS
    ```

#### WITH READ ONLY (Oracle 전용)
> 이 옵션으로 생성된 View는 오직 `읽기`만 가능하다는 의미

- VIEW는 `가상의 테이블`이지만, `동적`으로 `물리적 테이블`을 참조해서 생성한다.
    - 따라서, 옵션 없이 VIEW를 만들면, 데이터의 삽입, 삭제, 갱신이 가능할 수도 있다.
    - 이를 방지하고자 할 때, `READ ONLY 옵션을 이용`한다.
- 예시
    ```sql
    -- Oracle
    CREATE OR REPLACE VIEW READVIEW AS
    SELECT NAME,SALARY,SCORE
    FROM tStaff
    WHERE SALARY >= 300
    WITH READ ONLY;
    ```
- MariaDB는 이를 지원하지 않는다.
    - Maria에서 유사하게 하고싶다면, 아래처럼 할 수 있다.

        ```text
        해당 User에게 특정 View 권한을 읽기만 주면된다.
        ```
---
### VIEW의 사용 목적
#### `실행 속도 향상`
- SELECT 문 : `보조 기억 장치`에 존재하는 것을 조회
- VIEW 문 : `메모리`에 존재하는 것을 조회
#### `쿼리 길이 단축`
- `테이블처럼 사용 가능`하기 때문
- `SUB QUERY`대신 `VIEW`로 사용하면, `VIEW`이름만으로 `SUBQUERY`를 `대신할 수 있다.`
#### `보안에 유리하다.`
- 실제 테이블 구조를 알려줄 필요 없어짐.
- 보안에서 가장 중요한 것 => `최소화`
    - `필요한 Column만 보여주는 것`이 `가장 안전`하다.
    - 이를 위해 `View를 사용`한다.
---
### VIEW의 생명주기
- VIEW는 생성 시, 현재 DB 전체에서 사용 가능한 테이블이 된다.
    - 다른 임시테이블과 다르게 `일반적으로 소멸하지 않는다`.

#### VIEW의 소멸
1. 직접 삭제 (DROP VIEW)
    - 다음과 같은 명령어로 직접 삭제하는 경우 사라진다.
        ```sql
        DROP VIEW view이름;
        ```
2. 간접 삭제 (DROP TABLE)
    - VIEW가 참조하는 테이블이 삭제된 경우 사라지거나(CASCADE)/작동불능된다.
        ```sql
        DROP TABLE viewMother;
        ```
        - DROP VIEW 뒤에 `CASCADE`를 붙이면, `삭제하는 VIEW를 참조`하는 `다른 VIEW`나 `제약 조건`까지 `함께 삭제`
        - 뒤에 `RESTRICT`를 붙이면, `다른 곳에서 이 VIEW를 참조`하고 있다면, `삭제를 거부`한다.

3. 임시 뷰인 경우 (TEMPORARY VIEW)
    - 특정 세션이나 작업중에 잠깐 생성한 Temporary View는 소멸 시기가 정해져 있음
        1. 세션 종료
        2. 인라인 뷰 -> 쿼리 실행이 종료되면 삭제






## 기타 임시 테이블
### TEMPORARY TABLE
- 테이블을 만들 때, `CREATE TEMPORARY TABLE`로 만들면, `임시 테이블`이 된다.

#### 생명주기
- 현재 세션(연결)에서만 `접근 가능`
- 세면 만료 시, `테이블 소멸`
---
### CTE
> `Query`실행 중에만 잠깐 살아있는 `임시 결과 집합`
- 복잡한 쿼리 작성 시, `임시 테이블`을 만들지 않고도 코드 정리를 깔끔하게 할 수 있게 돕는다.
#### 기본 형식
```sql
WITH CTE_이름 AS (
    서브 쿼리(SELECT 문)
)
```
#### VIEW와의 차이
1. 휘발성 
    - VIEW는 한 번 만들면, 삭제하기 전까지는 DB에 저장
    - CTE는 SQL 쿼리가 끝나면 삭제
2. 가독성
    - 복잡한 JOIN이나 SubQuery를 위로 빼서 이름을 붙이므로, 가독성이 좋다.
3. 재사용성 
    - 하나의 쿼리 안에서 `여러번 재사용`할 수 있다.


---
### INLINE VIEW
> FROM 절에 사용된 `SUB QUERY`, 모든 DB에서 다 사용할 수 있는 구문이다.
```sql
SELECT *
FROM (SELECT * FROM tCity) T; -- 이렇게 ()안에 SELECT문을 넣고, 별명을 넣어서 INLINE VIEW로 사용 가능
```
- SELECT의 결과는 항상 임시 `TABLE`이다.
    - Q) 임시테이블? / A) 결과가 나온 당시에만 존재하는 테이블
    - 파이썬에서 `인스턴스`는 `클래스()`로 생성한다. 하지만 이를 `참조하는 변수가 없으면 GC가 삭제`하기 때문에, 우리는 `변수가 해당 인스턴스를 참조`하도록 한다.
        - 이처럼 SQL에서도 `SELECT로 생성된 임시테이블`에 `별명`을 만들어서 `삭제되지 않도록 하여 사용`한다.
        - 이것이 `INLINE VIEW`다.
- `INLINE VIEW를 사용`하면 `조회 성능이 좋아지는 경우가 많다.`
    - Y? 
       - `DB = 디스크`(보조기억 장치), `TABLE = 메모리`
        - 즉 메모리에 있는 것을 불러오는게 빠르므로, `테이블을 이용하는 VIEW가 빠르다.`

---
### 임시 테이블들의 차이
> `INLINE VIEW`가 가장 작음, `VIEW`가 가장 큼.
> - 작은 것에서 해결되면, 큰 것에선 당연히 해결할 수 있다.
> - 큰 것에서 해결된다해서, 작은 것에서 해결된다는 보장은 없다.

#### INCLINE VIEW : 자신이 속한 `SELECT` 구문에서만 사용
#### CTE : 하나의 `Transaction`내에서만 동작
#### TEMPORARY TABLE : `현재 세션`에서만 `사용 가능`한 테이블
#### VIEW : `현재 DB 전체`에서 사용 가능한 테이블

---
## 파이썬 연동
### 1. Programming 언어와 DB 연동
#### 필요한 정보
1. `DB 서버 위치`(IP, Domain) / `포트번호`(컴퓨터에서 외부 접속 가능한 Application을 구분하기 위한 번호) / `접속할 DB 이름` / `User ID와 PW`
    - 경우에 따라서는 `IP`와 `Port번호`만으로도 `접속 가능`한 경우가 있다.
    - 현재 컴퓨터는 IP를 `localhost` / `127.0.0.1`로 설정한다.
#### 프로그래밍 언어와 DB 사이에서 Interface 역할을 해 줄 드라이버 

### 2. 연동 방식
1. Driver 만으로 연동 : `SQL 필수`
2. ORM과 Framework를 이용 : `SQL 사용 X`, `Programming 언어의 함수 or 클래스를 이용`해서 작업 수행

### 3. MariaDB연동
#### 필요한 정보
1. IP : localhost (자신의 PC)
2. 포트번호 : 3306 (DB port)
3. DB name : adam
4. User ID : root
5. 비밀번호 : 비밀 ㅎ

#### B. 드라이버
- Python이므로 pymysql 패키지 설치하기 
    - `pip install pymysql`
---
### 드라이버를 이용한 접속 및 연동
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
        - 다만 이때, `SQL Injection`같은 문제를 막기 위해 `execute 전, 유효성 검사`를 잘 해야 한다. (불용어 검사 등)
    3. Python에서 `실행한 결과를 DB에 반영`하고자 하는 경우에는 `cursor().commit()`을 실행하여 반영해주어야 한다.
        - 만약, 취소하고자 하는 경우엔 `cursor().rollback()`을 실행해주면 된다.
        - 이 과정을 거치지 않으면, 아무리해도 DB에 반영되지 않는다.

#### DQL 수행 : SELECT
- SQL 실행과 동일함.
- DB에 영향을 주는 것이 아니기에 `COMMIT`과 `ROLLBACK`할 필요가 없다.
- `SQL실행객체로 실행`한 뒤
    1. `실행객체.fetchone()` -> 검색된 결과를 `iterator로 1개씩`
        ```python
        #한 개씩 출력
        while True: 
            result =sql_execution_object.fetchone()
            if not result :
                break
        print(result)
        ```
    2. `실행객체.fetchall()` -> 검색된 결과 전체를 `(tuple,tuple,tuple,...)`로 반환
        ```python
        sql_execution_object.execute("SELECT * FROM usertbl")
        result = sql_execution_object.fetchall()
        ```
#### 프로시저 실행
- 방법 : `cursor` 객체를 통해 `callproc` 메서드 호출
    ```python
    cursor.callproc('프로시저이름',args=(프로시저 매개변수들))
    ```
- 예시, 
    - 다음과 같은 프로시저가 있을 때, 드라이버를 이용한 프로시저 실행
        ```sql
        DELIMITER //
        CREATE PROCEDURE myproc(IN _userid INT,IN _name CHAR(3),IN _date date) -- IN은 안 써도 된다고 한다.

        BEGIN
        INSERT INTO usertbl VALUES(_userid,_name,_date); 

        END //
        DELIMITER ;
        ```
    ```python
    sql_execution_object.callproc('myproc',args=(11,'파테스','2025-01-01'))
    ```

#### BLOB 연동
- `BLOB(Binary Large Object)`
    - DB에서 `비정형 데이터를 저장`할 때 사용하는 `데이터 타입`
        - `비정형 데이터` : `이미지`,`오디오`,`비디오`,`실행 파일` 등 `바이너리(이진)`형태의 데이터
- 예시, kingrangE 이미지를 BLOB로 저장
    1. BLOB를 담을 예시 테이블 생성
        ```sql
        CREATE TABLE blobTest(
            id INT PRIMARY KEY,
            file_name CHAR(30),
            content LONGBLOB
        );
        ```
    2. python 프로그램을 통해 파일을 읽고, 테이블에 저장
        ```python
        FILE_PATH = 'kingrangE.png'
        with open(FILE_PATH,"rb") as f:
            content = f.read()
        sql_execution_object.execute("INSERT INTO blobTest VALUES(%s,%s,%s)",(1,"kingrangE",content))
        con.commit()
        ```
    3. python 프로그램을 통해 테이블을 읽어 파일 저장
        ```python
        NEW_FILE_PATH = "newrangE.png"
        sql_execution_object.execute("SELECT * FROM blobTest")
        with open(NEW_FILE_PATH,"wb") as f:
            f.write(sql_execution_object.fetchone()[2])
        ```
---

### ORM을 이용한 조작 실습
#### ORM이란
- `Object Relational Mapping`
    - `객체 지향 패러다임`을 `관계형 데이터베이스`에 `보존하는 기술`
    - `객체`와 `RDB 테이블`을 `매핑`해서 사용하는 방법
        - 클래스 = 테이블
        - 인스턴스 = 행(row)
        - 속성(Field) = 열(column)
#### ORM 장점
1. `DB 독립성` 
    - 코드가 특정 DB에 종속되지 않아 나중에 DB를 바꾸는데 수월하다.
2. `가독성 향상`
    - 프로그래밍 언어 문법으로 되어 있어 가독성이 높다.
3. `생산성 향상`
    - 비즈니스 로직에 집중할 수 있다.
4. `유지보수 용이`
    - DB 구조가 변경되어도 코드 수정을 최소화할 수 있다.
#### ORM 단점
1. `성능 이슈` 
    - 복잡한 쿼리, 대량의 데이터를 처리할 땐, SQL보다 느릴 수 있다.
2. `쿼리 복잡`
    - 쿼리 처리가 복잡하다.

#### 파이썬에서 많이 사용되는 ORM
> `SQLAlchemy`
- 설치
    ```bash
    pip install sqlalchemy
    ```
#### import 및 연결 URL 설정
- 연결 URL 형식
    ```python
    "DB종류[+DB드라이버]://username:password@host:port/database[?charset]"
    ```
- 만약, password에 `/`,`:`,`@` 이런 것들이 포함된다면, URL 형식이 망가질 수 있음
    - 따라서 아래와 같이 `인코딩을 하여 사용`해야 한다.

        ```python
        from urllib.parse import quote_plus
        from sqlalchemy import create_engine
        # 인코딩하여 적용
        encoded_password = quote_plus(password)
        DB_URL = f"mysql+pymysql://user:{encoded_password}@host/dbname" 
        # 연결 URL 구성
        engine = create_engine(DB_URL)
        ```

```python
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "mysql+pymysql://root:pwpw@localhost:3306/adam?charset=utf8mb4"
# if postgre, postgresql+psycopg2://user:pass@localhost:5432/mydb

# DB 연결 통로
engine = create_engine(DB_URL,echo=True)
# echo를 True로 설정하면, 실제 수행되는 SQL 구문을 확인할 수 있음

# 통신할 수 있는 세션
Session = sessionmaker(autocommit=False,autoflush=False,bind=engine)
```

#### 테이블 정의 및 생성

```python
# 모델 생성할 기본 클래스 
Base = declarative_base()

# 테이블 모델 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10),nullable=False)
    email = Column(String(30),unique = True)

# 테이블 자동 생성
Base.metadata.create_all(bind=engine)
```

#### INSERT
```python
db = Session()
try :
    new_user = User(name="김아무개",email="amugae@a.com") # 인스턴스(행) 생성
    db.add(new_user) # 인스턴스 DB에 추가
    db.commit() # DB에 반영
except Exception as e:
    print("Error 발생 :",e)
finally : 
    db.close()
```

#### SELECT
> User 테이블의 이름이 김아무개인 데이터의 첫 행을 조회
```python
db = Session()
try : 
    user = db.query(User).filter(User.name=="김아무개").first()
    print(user)
    print("유저 이름 :",user.name,"유저 메일",user.email)
except Exception as e :
    print("Error 발생 :",e)
finally :
    db.close()
```

#### UPDATE
1. 조회해서 정보를 가져온 후 수정 반영하기
    ```python
    db = Session()
    try :
        # 조회하여 User 정보를 가져옴
        user = db.query(User).filter(User.name=="김아무개").first()
        # user가 값이 존재하면 해당 값을 수정함
        if user :
            # 필드값 수정
            user.name= "김똥개"
            # 번경 반영
            db.commit()
        else :
            print("김아무개는 없는거야 병건아...")

    except Exception as e :
        print("Error 발생 :",e)

    finally :
        db.close()
    ```
2. 한 번에 수정하기
    ```python
    db = Session()
    try :
        # 조회하여 User 정보를 가져옴
        user = db.query(User).filter(User.name=="김아무개").update({"name":"김똥개"})
        db.commit()

    except Exception as e :
        print("Error 발생 :",e)

    finally :
        db.close()
    ```

#### DELETE
```python
db = Session()
try :
    # 조회하여 User 정보를 가져옴
    user = db.query(User).filter(User.name=="김아무개").first()
    # user가 값이 존재하면 해당 값을 수정함
    if user :
        # 삭제
        db.delete(user)
        db.commit() #반영
    else :
        print("김아무개는 원래 없는거야 병건아...")

except Exception as e :
    print("Error 발생 :",e)

finally :
    db.close()
```

## 참고
1. 자료구조를 잘 알아야 한다.
    - 알고리즘 구현 시, 자료구조를 적절히 선택하는 것이 중요
        - 따라서, 알고리즘 문제 풀 때도, 자료구조를 모르는 상태로 푸는 연습을 할 것
    - 자료구조가 어디에 어떻게 이용되는지 공부하라.
2. `Private Cloud`에서 가장 구현하기 쉬운 것이 `DBMS`와 `File Server`
    - 나중에 구현해볼 예정
3. fflush()
    - Computer는 다른 무언가(OS,Other Computer etc.)와 통신할 때는 `항상 Buffer`를 이용하여 통신한다.
        - Buffer에 전달하고 싶은 MSG를 넣고 Buffer 전송
    - 근데 만약 Buffer에서 안 꺼내지면, MSG를 받지 못함.
        - 이때, 버퍼를 강제로 비우는 것이 fflush()다.