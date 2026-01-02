# 12월 26일

## Oracle, MySQL/MariaDB/MongoDB
- Oracle : User > Database
    - User가 더 큼 
    - 따라서, 로그인을 하면 Database를 사용할 준비 끝
- MySQL/MariaDB/MongoDB : Database > User
    - Database가 더 큼
    - 따라서, 사용 전 `use 데이터베이스`로 데이터베이스 어떤 것을 사용하겠다를 알려주어야 함.

## GROUPING
### GROUP BY

- SQL구문 구조
```sql
SELECT 열 이름 / 연산식 나열
FROM 테이블 이름 / SELECT 구문  
[WHERE 조건절]
[GROUP BY 그룹화할 열 이름이나 연산식을 나열]
[ORDER BY 정렬한 열 이름이나 연산식을 나열]
```

- 예시, tStaff 테이블에서 각 depart 별로 salary의 평균을 조회
```sql
SELECT depart, avg(salary)
FROM tStaff
GROUP BY depart
--- GROUP BY 없이 하면
/*
결과가 depart 1개에 대해서만 나옴 (avg(salary)는 값의 평균- 즉 1개)
GROUP BY를 사용하지 않으면, 전체를 하나의 덩어리로 보기 떄문
-> 이때 "어떤 depart를 보여줄까"는 DB마다 다름
- MySQL, MariaDB -> 가장 처음 값
- Oracle, MS-SQL -> Error 
*/
```

- 두 개 이상의 Column이나 연산식으로 그룹화
    - 예시, depart와 gender로 그룹화해서 데이터의 개수를 조회
        ```sql
        SELECT depart, gender, COUNT(*)
        FROM tStaff
        GROUP BY depart, gender;
        --- 만약 salary값이 NULL이 아닌 데이터의 개수를 조회하고 싶다면
        SELECT depart, gender, COUNT(salary)
        FROM tStaff
        GROUP BY depart, gender;
        ``` 

- GROUP BY 절이 작성되면, `SELECT 절`에는 `GROUP BY 절에 사용된 Column이름`이나 `연산식` 그리고 `집계 함수`만 나와야 한다.
    - ORACLE에서는 이 규칙을 어기면 Error가 발생 (ORACLE은 표준 SQL)
        - 예시, 묶어서 하나로 보여줄 수 없는 경우 
            - 잘못된 예시, tStaff에서 gender와 depart로 그룹화해서 depart,name,salary 합계 출력하기
                ```sql
                SELECT depart, gender, name, sum(salary) -- name은 묶어서 1개로 보여줄 수 없음(연산할 수 없으니까)
                FROM tStaff
                GROUP BY depart,gender;
                ```
            - 잘 된 예시 ,
                ```sql
                SELECT depart, gender, sum(salary) -- sum(salary)은 그룹별로 합치면 되기 때문에 상관없다.
                FROM tStaff
                GROUP BY depart,gender;
                ```
    - MariaDB나 MySQL은 첫 번쨰 데이터가 조회된다.
    - `ORM`으로 구현할 때, DB가 바뀌면서 Error가 날 수 있으므로, 꼭 유의하기
- GROUP BY 절을 사용했는데,GROUP화 한 `Column`이나 `연산식을 조회하지 않는 것`도 `바람직하지 않음`.
    - 그룹화한 Column을 조회하지 않음
        - 이건, 뭐로 그룹화했는지 알 수 없으므로 바람직하지 않음
        - 예시,
            ```sql
            SELECT sum(salary)
            FROM tStaff
            GROUP BY depart;
            ```
    - 연산식을 조회하지 않음
        - 이건 그룹화한 이유가 딱히 없는 것으로 보이므로 바람직하지 않음.
        - 그룹화를 했다는건 묶어서 무언가 하려는 것이므로, 그것을 보여야 함.
            ```sql
            SELECT depart
            FROM tStaff
            GROUP BY depart;
            ```

- `GROUP BY`를 이용하면 `DISTINCT와 유사한 결과`(중복 제거)를 만들 수 있다.
    - 예시, tStaff 테이블에서 depart의 종류를 조회
        ```sql
        -- GROUP BY 사용 X
        SELECT DISTINCT depart
        FROM tStaff;
        -- GROUP BY 사용 O
        SELECT depart
        FROM tStaff
        GROUP BY depart;
        ```

### Having 절
- GROUP BY 이후에 적용되는 조건절
- 기본 형식
```sql
SELECT 열 이름 / 연산식 나열
FROM 테이블 이름 / SELECT 구문  
[WHERE 조건절]
[GROUP BY 그룹화할 열 이름이나 연산식을 나열]
`[HAVING 그룹화 이후의 조건]`
[ORDER BY 정렬한 열 이름이나 연산식을 나열]
```

- 예시, buytbl 테이블에서 총 구매액(price * amount)이 1000보다 큰 userID와 총 구매액을 조회
    ```sql
    --- 잘못한 예시
    SELECT userID, SUM(amount*price)
    FROM buytbl
    WHERE SUM(price*amount) > 1000 -- WHERE는 GROUP 이전에 실행되므로 에러 발생(집계함수 사용 불가)
    GROUP BY userID;

    --- 아래는 잘한 예시
    SELECT userID, SUM(amount*price)
    FROM buytble
    GROUP BY userID
    HAVING SUM(amount*price) > 1000;
    ```

- 예시 2, tStaff 테이블에서 depart별로 그룹화한 후, salary의 평균이 340 이상인 데이터의 depart와 평균 값을 오름차순으로 정렬하여 조회
    ```sql
    SELECT depart AS "부서", AVG(salary) AS "평균 급여"
    FROM tStaff
    GROUP BY depart
    HAVING AVG(salary) >= 340
    ORDER BY "평균 급여" ASC;
    ```
- 예시 3, tStaff 테이블에서 depart가 인사과와 영업부인 데이터의 depart와 salary의 최대값을 조회
    - WHERE와 HAVING에서 같은 일을 할 수 있다면 `WHERE`절에 작성하는 것이 낫다.
        - WHERE가 ORDER, HAVING보다 먼저 실행되므로, 더 많은 것을 FILTERING하여 효율을 올릴 수 있음.
        - Map-Reduce가 이와 유사함. (분산하여 `처리`하고 결과만 모아서 `Reduce`)
            - 이를 잘 활용한게 `Cloud` (`비싸고 좋은거 1개`가 아니라 `싼거 작은거 여러 개`로 효율을 높이기)
    ```sql
    SELECT depart, MAX(salary)
    FROM tStaff
    WHERE depart IN ('인사과','영업부')
    GROUP BY depart;
    ```
    ```sql
    SELECT depart, MAX(salary)
    FROM tStaff
    GROUP BY depart
    HAVING depart IN ('인사과','영업부');
    ```
## WINDOW 함수
- SQLD,SQLP를 준비할거면 이거 잘해야함.
- 행과 행 사이의 관계를 정의하기 위해 제공되는 함수
    - OVER 절이 들어간 함수다.
### 순위 함수
- RANK, NTILE, DENSE_RANK, ROW_NUMBER, PERCENT_RANK
    - `RANK`, `DENSE_RANK` : 동점이 나왔을 때 어떻게 처리할지에 따라 차이
        - `RANK` : 동점이 발생하면 그 다음 숫자는 + 동점자 수 더해서 진행
            - ex 2명이 공동 1등이면, 2등 없고, 다음 3등
        - `DENSE_RANK` : 동점이 발생해도, 그 다음 숫자는 이어서 감
            - ex 500명이 공동 1등이어도, 다음은 2등

    - `PERCENT_RANK` : 백분률
        - 0~1 중 순위로 몇 %인지 확인할 수 있음

    - `NTILE` : 그룹화에 관한 것, N 등분
        - NTILE(`정수`)를 입력하면, 순위별로 `정수` 등분하여 보여줌

    - `ROW_NUMBER` : 순서 매겨주는 것 
        - ROW_NUMBER는 동점자가 발생해도 그냥 순서를ㅇ등,c=3등 이렇게 처리함
### 기본 형식
```sql
순위함수 이름() OVER([PARTITION BY 파티션 목록] ORDER BY 정렬조건) 
-- PARTITION BY -> 그룹 별로 나눠서 볼거냐 묻는거 
    -- EX, 1반 성적 순위, 2반 성적 순위 이런식으로 볼거냐, 전교 성적 순위를 볼거냐
-- ORDER BY -> 뭐가지고 순위 정할거냐
    -- 점수로 순위를 정할건지, 이름으로 순위를 정할건지 등
```

- 예시, usertbl 테이블의 나이가 많은 순(birthyear로 비교)으로 순위를 매겨서 조회
    ```sql
    SELECT name, birthyear, RANK() OVER(ORDER BY birthyear)
    FROM usertbl;
    ```

- 예시2, usertbl 테이블을 addr별로 그룹화해서 나이가 많은 순으로 순위를 매겨서 조회
    - 그룹 내에서 몇 등인지
    ```sql
    SELECT name, birthyear,addr, RANK() OVER(PARTITION BY addr ORDER BY birthyear)
    FROM usertbl;
    ```

### 분석 함수
- CUST_DIST,LEAD,FIRST_VALUE,LAG,LAST_VALUE,PERCENT_RANK(얘는 둘 다 가능)
    - `CUST_DIST` : 누적백분률
    - `LEAD` / `LAG` : 다음 행 / 이전 행
    - `FIRST_VALUE`/`LAST_VALUE` : 첫 행의 값 / 마지막 행의 값
    - `PERCENT_RANK` : 

- `다음 행과의 차이를 구하는데 사용`한다.
    - 예시, usertbl에서 다음 행과의 birthyear 차이
        ```sql
        SELECT name, birthyear, birthyear-LEAD(birthyear,1) OVER(ORDER BY birthyear) -- 1이면 바로 다음, 2면 다다음, 3이면 다다다음
        FROM usertbl;
        ```
    - 예시2, usertbl에서 % 누적합 나타내기 (다시 한 번 알아보기)
    
        ```sql
        SELECT name, birthyear, CUME_DIST() OVER(ORDER BY birthyear DESC)
        FROM usertbl;
        ```

## WITH ROLLUP 기능
- GROUP BY와 같이 사용해서 `그룹 합계`와 `총 합계`를 만들어주는 기능

- 예시, `order_d테이블`에서 `goodscd별로 그룹화`해서 `qty의 합계를 조회`
    ```sql
    SELECT goodscd,SUM(qty)
    FROM order_d
    GROUP BY goodscd;
    ```
    - 만약 추가로 총합계를 알고 싶다면?
        - 여기서 goodscd부분이 NULL로 나오는데 바꾸는 방법은 없나?(검색하기)
        ```sql
        SELECT goodscd,SUM(qty)
        FROM order_d
        GROUP BY goodscd WITH ROLLUP;
        ```

## PIVOT 기능
- 한 열에 포함된 `여러 값을 출력`하고, 이를 `여러 열로 변환`해서 `테이블 반환식`을 만들어 내는 것

- 예시1, uName과 season으로 `피봇 테이블` 생성
    - 오른쪽으로 펼쳐지는 열 합계 테이블 확인 가능
    ```sql
    SELECT uName, SUM(IF(season="봄",amount,0)) AS "봄 합계",SUM(IF(season="여름",amount,0)) AS "여름 합계",SUM(IF(season="가을",amount,0)) AS "가을 합계",SUM(IF(season="겨울",amount,0)) AS "겨울 합계" ,SUM(amount) AS "총 합계"
    FROM pivotTest
    GROUP BY uName;
    ```

## DDL
### 테이블 생성
#### 기본 형식
CREATE [TEMPORARAY] TABLE [IF NOT EXIST] 테이블명(
    컬럼명1 타입,[CONSTARAINT 제약 조건 이름] 컬럼 제약 조건,
    컬럼명2 타입,
    컬럼명3 타입,
    ...,
    [CONSTARAINT 제약 조건 이름] 테이블 제약 조건)ENGINE = 엔진명;

- 데이터 타입
    - 숫자 : BIT, INT, FLOAT DOUBLE, DECIMAL(전체자리수, 소수 자리수)
    - 문자 
        - CHAR (바이트 수- 255까지)
        - VARCHAR(바이트 수 - 65535까지)
        - TEXT : 65535자까지
        - LONGTEXT : 43억자까지
        - BLOB : 65536
        - LONGBLOB : 43억정도까지
            -  BLOB, LONGBLOB 파일의 경로와 내용을 함께 나타낼 떄,
    - 날짜 
        - DATE
        - DATETIME
        - TIMESTAMP
    - BOOL
    - JSON
    - GEOMETRY
    - ENGINE
        - MyISAM : 인덱스를 지원하는 구조 -> 조회에 유리하나, 변경 작업을 수행할 때 시간이 많이 걸림
        - InnoDB : 조회는 불리, 변경 작업을 빠르게 수행
    - AUTO_INCREMENT
        - 시퀀스의 시작 번호를 설정할 수 있다
            ```sql
            AUTO_INCREMENT = 초기값
            ```
    - CHARTACTER SET 설정
        - utf8,utf8mb4 이런거
        - `DEFAULT CHARSET=인코딩 방식` 이렇게 설정
        - 대소문자 구분에 따라 콜레이션 변경까지 잘 생각하기
            - 대소문자 구분 : utf8mb4_bin (binary로 설정하여 구분하게 함)
            - 대소문자 구분 X (DEFAULT) : utf8mb4_ci (이게 기본 값, 따로 기재하지 않으면 이렇게 됨)
- 테이블 생성 예시 
    - 조건
        1. contact 테이블 
        2. 기본키 이름 num(1부터 시작하는 일련 번호)
        3. 이름을 저장할 것, 이름은 거의 변경이 없는 20자
        4. 주소는 자주 변경되는 데이터 100자
        5. 전화번호는 자주 변경이 되지만, 자릿수는 변경이 안되는 20자 정도
        6. 이메일은 자주 변경이 되는 데이터로 100자 대소문자 구분한다.
        7. 생일은 날짜 타입으로 생성
        8. 이 테이블은 읽기를 주로할 예정
        9. 문자열에 이모티콘을 저장하고 싶고, 
    - 코드
        ```sql
        CREATE TABLE contact(
            num INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(20), -- 거의 변경하지 않으므로 VARCHAR로 메모리 절약
            addr CHAR(100), -- 자주 변경은 migration을 막기 위해 CHAR로
            phone_number VARCHAR(20), -- 자리수 변경이 거의 없으므로 메모리 절약을 위해 VARCHAR
            email CHAR(100) COLLATE utf8mb4_bin, -- 이메일은 자주 변경되고, 길이도 변하므로 CHAR
            birthday date 
        )ENGINE = MyISAM AUTO_INCREMENT = 1 DEFAULT CHARSET=utf8mb4; -- AUTO_INCREMENT =1로 시작지점 설정(1이 디폴트값이라 안해도 됨)
        ```
- 내가 만든 예시
    - 조건 
        1. 

### 테이블 수정
#### Column추가
```sql
ALTER TABLE 테이블이름 ADD 컬럼이름 자료형 [first / after 컬럼이름] 
-- 만약 first 또는 after 컬럼이름 으로 위치를 설정하지 않으면 가장 마지막 위치에 생성된다.
```
- 예시, contact 테이블에 정수형 age 컬럼 PK 다음 자리에 추가
    ```sql
    ALTER TABLE contact ADD age INT after num
    ```
#### Column 삭제
```sql
ALTER TABLE 테이블 이름 DROP 컬럼 이름;
```
- 예시, 아까 생성한 age 컬럼 제거
    ```sql
    ALTER TABLE contact DROP age;
    ```
#### Column 변경
- 기존 테이블의 `자료형`이나 `크기`또는 `이름`을 변경
    ```sql
    ALTER TABLE 테이블이름 CHANGE 이전컬럼이름 새로운컬럼이름 자료형
    ```
    - 예시, contact 테이블의 phone_number이라는 컬럼을 tel 이름의 column으로 변경
        ```sql
        ALTER TABLE contact CHANGE phone_number tel INT;
        ```
- 기존 자료형 변경, `NOT NULL`이나 `NULL 허용`도 이 방식으로 변경
    ```sql
    ALTER TABLE 테이블이름 MODIFY 컬럼이름 자료형
    ```
    - NOT NULL, NULL 허용은 제약 조건 변경이 아니라, 데이터 사이즈 자체가 변경되어야 함.
        - 그래서 `자료형 변경과 같은 취급인 것`이다.
        - EX, char(5)일 때
            - NOT NULL => 정확히 5바이트 할당
            - NULL => NULL 표기 바이트까지 1개 추가 할당
            - 따라서 `NOT NULL <=> NULL 변경`은 `사이즈 자체가 변경`되는 것이므로 `자료형 변경`

#### Column의 순서 조정 
- 기능은 있긴한데 사실 0순서는 의미가 없음, SELECT로 순서를 내가 보고싶은대로 지정하면 되니까
```sql
ALTER TABLE 테이블이름 MODIRY COLUMN 컬럼이름 자료형 FIRST/AFTER 컬럼이름;
```
#### 테이블 이름 변경
```sql
ALTER TABLE 이전테이블이름 RENAME 새로운테이블이름;
```

#### 테이블 삭제
```sql
DROP TABLE 테이블이름;
```
#### 테이블의 모든 데이터 삭제 (테이블 구조는 남는다.)

```sql
TRUNCATE TABLE 테이블이름;
```

#### 테이블 압축
```sql
CREATE TABLE ROW_FORMAT=COMPRESSED
```

#### 주석을 설정
```sql
COMMENT ON TABLE 테이블이름 IS 주석;
```

## 무결성 제약 조건
### Intergrity(무결성)
- 데이터의 `정확성`과 `일관성`을 `유지`하고 `보증`하는 것
- 적용 범위
    1. Entity Integrity (개체 무결성) : PRIMARY KEY 값은 NULL이거나 중복될 수 없다.
    2. Referential Intergrity(참조 무결성) : FOREIGN KEY의 값은 참조할 수 있는 값이거나 NULL이어야 한다.
    3. Domain Intergrity(도메인 무결성) : Column에 저장되는 값은 원자값이어야 하고, Type지정, NULL 여부 체크, 기본값 등의 규칙을 지켜야 한다.

### NOT NULL
- 필수 입력
- 컬럼의 크기와 연관이 있다.(NULL이면 바이트 1개 추가)때문에 컬럼을 만들 때, 설정하고, 수정을 할 때도 MODIFY(자료형 수정)으로 한다.
- 예시
    ```sql
    CREATE TABLE tNullable(
        name CHAR(10) NOT NULL,
        age INT
    );

    INSERT INTO tNullable(name,age) VALUES("아담",55);
    INSERT INTO tNullable(name) VALUES("이브");
    INSERT INTO tNullable(age) VALUES(14); -- ERROR : name은 NOT NULL이므로
    ```
### CHECK
- `값의 종류나 범위를 설정`하는 `제약 조건`
    ```sql
    CHECK(컬럼이름 가질 수 있는 값의 종류나 범위 설정)
    ```
- 예시
    - 조건
        1. tCheckTest 테이블을 생성
        2. gender : 3글자 까지만 가능하고, 남/여 둘 중 한 값만 가져야 함.
        3. origin : 3글자이고, 동/서/남/북 하나만 가져야 함
        4. grade : 정수, 1~5사이
        5. name : 10자, 박으로 시작
    ```sql
    CREATE TABLE tCheckTest(
        gender CHAR(3) CHECK(gender='남' OR gender='여'),
        -- origin CHAR(3) CHECK(origin = '동' OR origin = '서' OR origin = '남' OR origin = '북'), 
        origin CHAR(3) CHECK(origin IN ('동','서','남','북')), -- 둘 다 가능(OR/IN)
        -- grade INT CHECK(grade <= 5 AND grade >= 1),
        grade INT CHECK(grade BETWEEN 1 AND 5),
        name CHAR(10) CHECK(name LIKE '박%') -- ~로 시작한다 ->LIKE
    );
    ```

### UNIQUE
- 필드의 중복값을 배제
- NULL을 허용
- 2개 이상의 컬럼에도 적용 가능하지만, 2개 이상의 컬럼에 적용할 때는 `테이블 제약 조건`으로 설정해야 한다.
- 예시
    ```sql
    CREATE TABLE tUniqueTest(
        name CHAR(10),
        area INT UNIQUE,
        popu INT UNIQUE
    );-- area도 중복값이 없어야 하고, popu도 중복값이 없어야 한다.(개별 적용)
    CREATE TABLE tUniqueTest(
        name CHAR(10),
        area INT,
        popu INT,
        CONSTRAINT UK_area_popu UNIQUE(area,popu)
    ); -- area, popu 각각은 중복값이 있을 수 있지만, area와 popu를 합쳐서는 중복이 있으면 안된다.
    ```

### PRIMARY KEY
- `기본키` 설정
- `테이블에 하나만 설정` 가능
- `2개 이상의 컬럼으로 구성`하는 경우 `테이블 제약 조건으로 설정`
- 예시
    ```sql
    CREATE TABLE tPKTest(
        num INT PRIMARY_KEY,
        name CHAR(10),
    );
    CREATE TABLE tPKTest(
        name CHAR(10),
        area INT,
        popu INT,
        CONSTRAINT PK_area_popu UNIQUE(area,popu)
    ); -- area, popu 각각은 중복값이 있을 수 있지만, area와 popu를 합쳐서는 중복이 있으면 안된다.
    ```

### 참조 무결성 - FOREIGN KEY
- 실습을 위한 테이블 생성
    ```sql
    CREATE TABLE tEmp(
        name CHAR(10) PRIMARY KEY,
        salary INT NOT NULL,
        addr VARCHAR(30) NOT NULL
    );
    CREATE TABLE tProject(
        projectID INT PRIMARY KEY,
        name CHAR(10),
        project VARCHAR(30) NOT NULL,
        cost INT
    );
    ```
    - 샘플 데이터 삽입
        ```sql
        INSERT INTO tEmp(name,salary,addr) VALUES("길원",1000,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길투",1100,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길삼",2000,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길사",1300,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길오",1600,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길육",2030,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길칠",1010,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길팔",1200,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길구",4310,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길십",6010,"서울");
        ```
        ```sql
        INSERT INTO tProject(projectID,name,project,cost) VALUES(1,"길원","A프",30);
        INSERT INTO tProject(projectID,name,project,cost) VALUES(2,"길투","B프",40);
        INSERT INTO tProject(projectID,name,project,cost) VALUES(3,"길심","C프",50);
        -- 길심이란 사람은 없으므로 에러가 나와야 하는데 안나옴
        ```
    - 이렇게 값을 넣으면 tEmp에 없어도 tPorject에 값을 만들 수 있음 -> 이는 에러임
    - 따라서 Foriegn Key를 이용해야 한다.
- 외래키를 잘 사용한 예시
    - 실습을 위한 테이블 생성
        ```sql
        CREATE TABLE tEmp(
            name CHAR(10) PRIMARY KEY,
            salary INT NOT NULL,
            addr VARCHAR(30) NOT NULL
        );
        CREATE TABLE tProject(
            projectID INT PRIMARY KEY,
            name CHAR(10),
            project VARCHAR(30) NOT NULL,
            cost INT,
            CONSTRAINT FK_emp FOREIGN KEY(name) REFERENCES tEmp(name)
            -- 본 테이블의 name 컬럼이 tEmp의 name을 참조하도록 설정
        );
        ```
    - 데이터 삽입
        ```sql
        INSERT INTO tEmp(name,salary,addr) VALUES("길원",1000,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길투",1100,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길삼",2000,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길사",1300,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길오",1600,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길육",2030,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길칠",1010,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길팔",1200,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길구",4310,"서울");
        INSERT INTO tEmp(name,salary,addr) VALUES("길십",6010,"서울");
        ```
        ```sql
        INSERT INTO tProject(projectID,name,project,cost) VALUES(1,"길원","A프",30);
        INSERT INTO tProject(projectID,name,project,cost) VALUES(2,"길투","B프",40);
        INSERT INTO tProject(projectID,name,project,cost) VALUES(3,"길심","C프",50);
        -- 길심이란 사람은 없으므로 에러가 나옴.
        ```
    - 데이터 삭제
        - 참조 당하는 데이터는 삭제가 되지 않는다.
            ```sql
            DELETE FROM tEmp WHERE name="길원"; -- 에러가 발생함. 길원은 참조하고 있음.
            ```
        - 외래키로 참조당하고 있는 테이블은 삭제가 불가능하다.
            ```sql
            DROP TABLE tEmp; -- tProject에서 참조하므로 에러 발생
            ```
    -  FOREIGN KEY를 설정할 때의 옵션
        ```sql
        ON DELETE [NO ACTION | CASCADE | SET NULL | SET DEFAULT]
        ON UPDATE [NO ACTION | CASCADE | SET NULL | SET DEFAULT]
        ```
        - `NO ACTION` : 아무것도 하지 않음
        - `CASCADE` : 연쇄 삭제, 참조하고 있는 데이터도 삭제
        - `SET NULL` : 참조하는 값에 NULL
        - `SET DEFAULT` : 데이터베이스 설정에 따름
        - 예시
             ```sql
            CREATE TABLE tEmp(
                name CHAR(10) PRIMARY KEY,
                salary INT NOT NULL,
                addr VARCHAR(30) NOT NULL
            );
            CREATE TABLE tProject(
                projectID INT PRIMARY KEY,
                name CHAR(10),
                project VARCHAR(30) NOT NULL,
                cost INT,
                CONSTRAINT FK_emp FOREIGN KEY(name) REFERENCES tEmp(name) ON DELETE CASCADE
                -- CASCADE를 설정하여 연쇄 삭제가 가능하도록 함. tEmp의 데이터가 삭제되면 tProject에서 참조하고 있는 tuple이 삭제됨
            );
            CREATE TABLE tProject(
                projectID INT PRIMARY KEY,
                name CHAR(10),
                project VARCHAR(30) NOT NULL,
                cost INT,
                CONSTRAINT FK_emp FOREIGN KEY(name) REFERENCES tEmp(name) ON DELETE SET NULL
                -- SET NULL로 설정하여 회언 탈퇴할 때, 기록을 남길지 말지
            );
            ```
    - 제약 조건 수정
        - 제약 조건 확인
            ```sql
            SELECT *
            FROM information_schema.table_constraints;
            ```
        - 제약 조건 수정
            ```sql
            ALTER TABLE 테이블이름 MODIFY 컬럼이름 자료형 제약조건;
            ```
        - 제약 조건 추가
            ```sql
            ALTER TABLE 테이블이름 ADD 제약조건(컬럼이름);
            ```
        - 제약 조건 삭제
            ```sql
            ALTER TABLE 테이블이름 DROP CONSTRAINT 제약조건이름;
            ```
### 기본값 설정
- 자료형 뒤에 DEFAULT와 함께 값을 설정
- 삽입할 때, 값을 설정하지 않으면 `기본값이 설정`된다.
- 예시,
    ```sql
    CREATE TABLE tEmployee(
        name CHAR(10) PRIMARY KEY,
        salary INT DEFAULT 0, -- salary를 입력하지 않으면 0값이 들어감
    )
    INSERT INTO tEmployee(name,salary) VALUES("길원",1)
    INSERT INTO tEmployee(name) VALUES("길투") -- 이렇게 salary를 전달하지 않으면 0으로 입력된다.
    ```

    
## 참고
1. Customizing, Optimizing 
    - 기본적인 이론적 배경이 중요함.
    - `SQL`튜닝이 이런 이론적 배경으로 만들어지는거 (Query 튜닝) 
2. CQRS 일관성 유지
    - Message Broker (Kafka, Rabbit MQ)
        - RDBMS와 NoSQL이 불일치 할 수 있는데, 이때, Message Broker로 해결한다.

    