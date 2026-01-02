# 12월 26일

## Grouping

### GROUP BY
- 실행 순서
    1. FROM
    2. WHERE
    3. `GROUP BY`
    4. HAVING
    5. SELECT
    6. ORDER BY
    7. OFFSET
    8. LIMIT
    - 실행 순서상 GROUP BY가 WHERE 다음이므로, WHERE에서는 `집계함수`를 사용할 수 없다.
- 예시, tStaff 테이블에서 각 depart 별로 salary의 평균을 조회
    ```sql
    SELECT depart, AVG(salary)
    FROM tStaff 
    GROUP BY depart;
    ```
    - 만약 여기서 GROUP BY를 하지 않으면 Oracle(표준SQL)에서는 오류가 난다.
        - GROUP BY를 하지 않고, AVG를 사용하면 모든 tuple에 대한 평균이 나온다. 이때, depart(평균을 대표하는 부서이름)을 무엇으로 보여주어야 하는지 모르기 때문에 오류 발생함.
        - MySQL, MariaDB에서는 오류가 나지 않지만, 이는 에러 사항이므로 조심하기

- 두 개 이상의 Attribute 또는 연산식으로 그룹화
    - 예시 1, tStaff테이블에서 depart와 gender로 그룹화해서 데이터의 개수를 조회
        - 만약, salary가 NULL인 값을 제외하고 보고 싶다면
            ```sql
            SELECT depart,gender,COUNT(salary)
            FROM tStaff
            GROUP BY depart, gender;
            ```
        - 만약 NULL을 포함한 전체 행의 개수를 보고 싶다면
            ```sql
            SELECT depart,gender,COUNT(*)
            FROM tStaff
            GROUP BY depart, gender;
            ```
- GROUP BY 절이 작성되면, SELECT 절에는 `GROUP BY 절에서 사용된 Column 이름`이나 `연산식` 그리고 `집계 함수`만 나와야 한다.
    - Oracle에서는 이 규칙을 어기면 Error 발생
        ```sql
        -- 이렇게 하면 안된다는 예시
        -- tStaff 테이블에서 depart로 그룹화하고 name을 보여줌 
        SELECT depart, name
        FROM tStaff
        GROUP BY depart;
        ```
        - name은 3개에 해당하지 않으므로 안된다. 정확히는 name은 묶어서 1개로 보여줄 수 없으니까 에러(연산할 수 없으니까)
    - MariaDB, MySQL은 규칙을 어기면 첫 번쨰 데이터를 반환한다.
    - ORM으로 구현할 때, DB를 바꾸게 될 수 있음. 이때, 우리가 이런 실수를 하면, 에러가 발생하면서 위험해짐. 따라서, 유의해서 잘 만들자

- GROUP BY 절을 사용했는데, GROUP화한 `Column`이나 `연산식을 조회하지 않는 것`도 바람직하지 않다.
    - 내가 무엇을 GROUP화 했는지 나타내어야 하므로 GROUP화한 Column을 나타내줘야 한다.
        - 잘못된 예시
            ```sql
            SELECT sum(salary)
            FROM tStaff
            GROUP BY depart;
            ```
    - 내가 GROUP화해서 무엇을 진행할 목적이 있으므로, 그것을 보이기 위해 `연산식`을 같이 조회해줘야 한다.
        - 잘못된 예시
            ```sql
            SELECT depart
            FROM tStaff
            GROUP BY depart;
            ```

- `GROUP BY`를 사용하면, `DISTINCT`와 유사한 결과를 만들어낼 수 있다.
    - 예시, tStaff 테이블에서 `depart의 종류를 조회`
        ```sql
        -- DISTINCT 사용
        SELECT DISTINCT depart
        FROM tStaff;
        ```
        ```sql
        -- GROUP BY 사용
        SELECT depart
        FROM tStaff;
        GROUP BY depart;
        ```
### HAVING 절
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

- 예시 1, buytbl 테이블에서 총 구매액(price*amount)이 1000보다 큰 userID와 총 구매액을 조회
    ```sql
    SELECT userID, SUM(price*amount)
    FROM buytbl
    GROUP BY userID
    HAVING SUM(price*amount) > 1000
    ```
    - 이 경우엔 WHERE를 사용할 수 없다. 
        - 만약 WHERE를 쓴다면 아래와 같은 형태
            ```sql
            SELECT userID, SUM(price*amount)
            FROM buytbl
            WHERE SUM(price*amount) >1000 -- -> GROUP BY 이전에 실행되는 절이므로, 집계함수(SUM)을 사용할 수 없다.
            GROUP BY userID
            ```
- 예시 2, tStaff 테이블에서 depart별로 그룹화한 후, salary의 평균이 340 이상인 데이터의 depart와 평균값을 오름차순으로 정렬하라.
    ```sql
    SELECT depart, AVG(salary) as "평균 임금"
    FROM tStaff
    GROUP BY depart
    HAVING AVG(salary) >= 340
    ORDER BY "평균 임금" ASC;
    ```
- 예시 3, tStaff 테이블에서 depart가 인사과와 영업부인 데이터의 depart와 salary의 최대값을 조회
    - `HAVING 없이`
        ```sql
        SELECT depart, MAX(salary)
        FROM tStaff
        WHERE depart IN ('인사과','영업부') 
        GROUP BY depart
        ```
    - `HAVING 있이`
        ```sql
        SELECT depart, MAX(salary)
        FROM tStaff
        GROUP BY depart
        HAVING depart IN ('인사과','영업부')
        ```
    - HAVING 대신 WHERE를 사용할 수 있으면 `WHERE`를 사용하는 것이 `더 효율적`이다.
        - 실행 순서상 WHERE가 더 앞에 있다.
            - 따라서 WHERE에서 필터링을 하면, 남은 적은 데이터로 GROUP BY를 하는 것이므로 `효율적이다`
    
## WINDOW 함수
- 행과 행 사이의 관계를 정의하기 위해 제공되는 함수
    - `OVER 절`이 들어간 함수다.

### WINDOW 사용하는 2가지 함수
1. 순위 함수
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
        - ROW_NUMBER는 동점자가 발생해도 그냥 순서를 1등,2등,3등 이렇게 처리함
2. 분석 함수
- CUME_DIST,LEAD,FIRST_VALUE,LAG,LAST_VALUE,PERCENT_RANK(얘는 둘 다 가능)
    - `CUME_DIST` : 누적 백분률
    - `LEAD` / `LAG` : 현재 행 기준으로 (다음 행 / 이전 행)
    - `FIRST_VALUE`/`LAST_VALUE` : 첫 행의 값 / 마지막 행의 값
    - `PERCENT_RANK` : 

### WINDOW 사용 예시
#### 순위함수
1. usertbl 테이블의 나이가 많은 순(birthyear)으로 순위를 매겨서 조회
    ```sql
    SELECT name, birthyear, RANK() OVER(ORDER BY birthyear)
    FROM usertbl;
    ```
2. usertbl 테이블을 addr 별로 그룹화해서 그룹 내 나이가 많은 순으로 조회
    ```sql
    SELECT name,birthyear, RANK() OVER(PARTITION BY addr ORDER BY birthyear)
    FROM usertbl;
    ```
3. usertbl 테이블의 나이를 백분률로 표기
    ```sql
    SELECT name, birthyear, PERCENT_RANK() OVER(ORDER BY birthyear)
    FROM usertbl;
    ```
4. tStaff 테이블에서 여자의 비율을 표기
    ```sql
    SELECT distinct gender,PERCENT_RANK() OVER(ORDER BY gender)
    FROM tStaff;
    ```
5. tStaff 테이블의 성별 그룹에서 입사일 순위를 입사 빠른 순->느린순으로 정렬
    ```sql
    SELECT name,gender,joindate,RANK() OVER(PARTITION BY gender ORDER BY joindate ASC)
    FROM tStaff; 
    ```
6. tStaff 테이블의 입사일을 기준으로 7개의 그룹으로 분할
    ```sql
    SELECT name, joindate, NTILE(7) OVER(ORDER BY joindate)
    FROM tStaff;
    ```
#### 분석 함수
1. usertbl에서 다음 행과의 birthyear 차이
    ```sql
    SELECT name, birthyear, birthyear-LEAD(birthyear,1) OVER(ORDER BY birthyear)
    FROM usertbl;
    ```
2. usertbl에서 % 누적합 나타내기 (다시 한 번 알아보기)
    ```sql
    SELECT name, birthyear, CUME_DIST() OVER(ORDER BY birthyear DESC)
    FROM usertbl;
    ```
3. tStaff 테이블의 연봉을 이전사람과 비교하여 얼마나 차이나는지 확인하고, 최저 급여, 최고 급여, 누적 분포, 백분위 순위를 나타내기
    ```sql
    SELECT name, 
    ```

### WITH ROLLUP 기능
- `GROUP BY`와 같이 사용해서 `그룹 합계`, `총 합계`를 만들어주는 기능
- 예시, order_d 테이블에서 goodscd별로 그룹화해서 qty의 합계를 조회
    ```sql
    SELECT goodscd,SUM(qty)
    FROM order_d
    GROUP BY goodscd;
    ```
    - 만약 여기서 총합계를 알고싶다면
        ```sql
        SELECT goodscd, SUM(qty)
        FROM order_d
        GROUP BY goodscd WITH ROLLUP;
        ```
### PIVOT 기능
- 한 열에 포함된 `여러 값을 출력`하고, 이를 `여러 열로 변환`해서 `테이블 반환식`을 만들어 내는 것
- 예시1, uName과 season으로 `피봇 테이블` 생성
    ```sql
    SELECT uName,SUM(IF(season="봄",amount,0)) AS "봄",SUM(IF(season="여름",amount,0)) AS "여름",SUM(IF(season="가을",amount,0)) AS "가을",SUM(IF(season="겨울",amount,0)) AS "겨울",SUM(amount) AS "총 합계",
    FROM pivot
    GROUP BY uName;
    ```
## DDL
### 테이블 생성
#### 기본 형식
```sql
CREATE [TEMPORARAY] TABLE [IF NOT EXIST] 테이블명(
    컬럼명1 타입,[CONSTARAINT 제약 조건 이름] 컬럼 제약 조건,
    컬럼명2 타입,
    컬럼명3 타입,
    ...,
    [CONSTARAINT 제약 조건 이름] 테이블 제약 조건)ENGINE = 엔진명;
```
#### 데이터 타입
- `숫자` : BIT, INT, FLOAT, DOUBLE, DECIMAL(전체자리수, 소수 자리수)
- `문자` 
    - CHAR(바이트 수 - 255까지) 
        - ex, `CHAR(10)`
    - VARCHAR(바이트 수 - 65535까지)
        - ex, `VARCHAR(10)`
    - TEXT : 65535자까지
    - LONGTEXT : 43억자까지
    - BLOB(Binary Large OBject) : 65535자까지
        - 텍스트가 아닌 2진 데이터를 저장한다.
        - 이미지, 동영상, 사운드 등 
    - LONGBLOB : 43억자까지
        - 최근에는 `LONGBLOB을 이용해서 대용량 이미지, 동영상, 사운드를 저장하는 것`보단 `S3`같은 `저장소를 이용하여 저장`하고 `S3의 url을 VARCHAR로 저장`하는 방식을 주로 사용한다.
- `날짜`
    - DATE
    - DATETIME
    - TIMESTAMP
- `BOOL`
- `JSON`
- `GEOMETRY`
- `ENGINE`
    - MyISAM 
        - 구조
            > 테이블 하나 생성시 하드디스크에 아래의 3개 파일이 생성된다.
            > - `.frm` : 테이블의 `구조`가 저장된 파일
            > - `.MYD` : 실제 `데이터(행)`이 저장된 파일
            > - `.MYI` : 해당 테이블의 `인덱스` 정보가 저장된 파일
        - 특징
            1. 데이터와 인덱스가 분리되어 있다.
                - 인덱스를 찾고 실제 데이터를 가져올 때, 파일 2개를 이동해야 하지만, 구조가 단순하여 파일 단위 복사(백업)하기가 편하다.
        - `구조가 단순`하여 `전체 텍스트 검색`이나 `단순 읽기` 작업이 많은 경우 `속도가 매우 빠르다.`
        - Transaction 미지원
    - InnoDB : 
- `AUTO_INCREMENT`
    - AUTO_INCREMENT를 사용하는 경우 옵션을 통해 sequence의 시작 번호를 설정할 수 있다.
        ```sql
        AUTO_INCREMENT = 초기값
        ```
- `CHARSET`
    - `utf8`,`utf8mb4`와 같은 문자 집합을 말한다.
    - `DEFAULT CHARSET=인코딩 방식` 이렇게 설정할 수 있다.
    - 대소문자 구분 여부에 따라 Collation 변경까지 잘 생각하기
        - 대소문자 구분 X (Default) : utf8mb4_ci (`_ci`로 설정하여 구분하지 않게 함. (CHARSET을 따로 설정하지 않으면 기본적으로 _ci다.))
        - 대소문자 구분 O : utf8mb4_bin (`_bin`을 설정하여 `구분`하게 한다.)
#### 예시
- 조건
    1. 테이블명 : contact
    2. 기본키 이름 : num 
        - 기본키는 1부터 시작 (일련번호)
    3. 이름, 주소, 전화번호, 이메일, 생일을 저장하는 테이블
        - 이름은 `거의 변경하지 않는 20자`
        - 주소는 `자주 변경`되는 데이터 ``100자``
        - 전화번호는 `자주 변경`되지만, `자리수는 변경되지 않는 20자`
        - 이메일은 `자주 변경`되는 `100자` `(대소문자 구분)`
        - 생일은 `날짜 타입`
    4. 읽기 위주의 테이블 (InnoDB보다 `MyISAM이 더 유리`하다.)
    5. 문자열에 이모티콘을 저장하고 싶다. (CHARSET을 utf8로 하면 이모지를 저장하지 못함. 즉, utf8mb4로 변경해주어야 함.)
- 코드
    ```sql
    CREATE TABLE contact(
        num INT AUTO_INCREMENT PRIMARY_KEY,
        name VARCHAR(20),
        addr char(100),
        phone_number VARCHAR(20),
        email char(100) COLLATE utf8mb4_bin,
        birthday DATE
    )ENGINE = MyISAM AUTO_INCREMENT = 1 DEFAULT CHARSET=utf8mb4
    ```

### 테이블 수정

#### COLUMN 추가
```sql
ALTER TABLE 테이블이름 ADD 컬럼이름 자료형 [first / after 컬럼이름];
```

- EX, contact 테이블 num 다음에 added_column 정수 열 추가
    ```sql
    ALTER TABLE contact ADD added_column INT after num;
    ```
    
#### COLUMN 삭제
```sql
ALTER TABLE 테이블 이름 DROP 컬럼 이름;
```

- 예시, 아까 생성한 added_column 삭제
    ```sql
    ALTER TABLE contact DROP added_columnt;
    ```

#### COLUMN 변경
1. COLUMN의 `자료형`이나 `크기`, `이름`을 변경
    ```sql
    ALTER TABLE 테이블명 CHANGE 기존컬럼이름 새로운컬럼이름 자료형;
    ```
    - 예시, contact 테이블의 phone_number 컬럼을 pn으로 변경
        ```sql
        ALTER TABLE contact CHANGE phone_number pn INT;
        ```
2. COLUMN의 자료형 변경, `NOT NULL`,`NULL 허용`도 이 방식으로 변경한다.
    ```sql
    ALTER TABLE 테이블이름 MODIFY 컬럼이름 자료형;
    ```
    - Q) `NOT NULL`, `NULL 허용`만 변경하는건데 왜 자료형 변경을 사용?
    - A) `NOT NULL`과 `NULL 허용`은 차지하는 메모리의 크기가 다르다. 
#### Column의 순서 조정
```sql
ALTER TABLE 테이블이름 MODIFY 컬럼명 데이터타입 [FIRST/AFTER 컬럼명]
-- ALTER TABLE dept MODIFY deptno INT AFTER dname;
```
- 기능은 있긴한데, Column의 순서는 큰 의미가 없다. 
    - Y? SELECT 조회에서 내가 보고 싶은 COlumn 순서대로 지정하면 되기 때문.

#### 테이블 이름 변경
```sql
ALTER TABLE 이전테이블이름 RENAME 새로운테이블이름;
-- ALTER TABLE old_name RENAME new_name;
```
#### 테이블 삭제
```sql
DROP TABLE 테이블이름;
--DROP TABLE table_name;
```

#### 테이블의 데이터만 삭제 (구조 남김)
```sql
TRUNCATE TABLE 테이블이름;
```

#### 테이블 압축
- 테이블 생성 과정에서 `압축 테이블로 생성`
    ```sql
    -- CREATE TABLE ROW_FORMAT=COMPRESSED
    CREATE TABLE user_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        log_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) 
    ENGINE=InnoDB 
    ROW_FORMAT=COMPRESSED 
    KEY_BLOCK_SIZE=8; -- 압축된 페이지의 타겟 사이즈 (기본 16KB를 8KB로 줄이겠다는 의미 (1,2,4,8,16 선택))
    ```
- 기존 테이블을 `압축 테이블`로 변경
    - 새로 테이블을 생성하는 것과 `유사한 부하`가 발생하므로, `서비스 점검 시간`이나 `트래픽이 적은` 시간대에 하는 것이 좋다.
    ```sql
    ALTER TABLE user_logs
    ENGINE=InnoDB
    ROW_FORMAT=COMPRESSED
    KEY_BLOCK_SIZE=4;
    ```
- 압축 결과 확인 방법
    ```sql
    SELECT 
        table_name, 
        row_format, 
        data_length / 1024 / 1024 AS data_mb, -- 데이터 크기(MB)
        index_length / 1024 / 1024 AS index_mb -- 인덱스 크기(MB)
    FROM information_schema.tables 
    WHERE table_name = 'tProject';
    ```
- 압축시 `저장 공간은 절약 가능`하지만, 데이터를 읽고 쓸 때마다 압축-압축해제를 계속 해야하므로, `CPU 사용량이 증가`할 수 있다.
- INT, DATETIME 위주의 데이터보단 `TEXT`,`VARCHAR`처럼 중복된 문자열이 많은 데이터에서 압축효율이 높다.

#### 테이블 주석 설정
```sql
-- postgreSQL/Oracle 주석 방법
COMMENT ON TABLE 테이블이름 IS 주석;
    -- COMMENT ON TABLE DEPT IS '부서 정보 테이블'

-- MySQL/MariaDB 주석 방법
ALTER TABLE 테이블이름 COMMENT = 주석;
    -- ALTER TABLE DEPT COMMENT = '부서 정보 테이블'
```

- 주석 정보 확인
    ```sql
    SHOW TABLES STATUS;
    ```
- 컬럼 주석 설정 방법
    ```sql
    ALTER TABLE 테이블명 MODIFY 컬럼명 자료형 COMMENT '주석';
    -- ALTER TABLE dept MODIFY deptno int COMMENT '부서 번호';
    ```
- 컬럼 주석 정보 확인
    ```sql
    SHOW FULL COLUMNS FROM DEPT_COPY;
    ```

## 데이터 무결성 제약 조건
> DB에 저장된 데이터의 `정확성`,`일관성`,`유효성`을 보장하기 위해 정의한 `데이터가 지켜야 할 규칙`

### 주요 제약 조건의 종류
#### 개체 무결성 
- 정의 : 테이블의 각 행은 고유해야 하며, 이를 식별하기 위한 `기본키(Primary Key)`는 `중복되거나 빈 값`일 수 없다.
- 효과 : DB 내에서 특정 Record를 정확히 찾아낼 수 있음을 보장. (Record의 유일성 확보)
- 예시 : `학생 테이블`에서 `학번`이 PK라면, 학번이 없거나, 학번이 중복되는 학생이 없다.
- 참고 : PK는 꼭 단일 값만 가능한 것이 아니다.
- 예시, 단일 PK
    ```sql
    CREATE TABLE user(
        id INT PRIMARY KEY,
        name CHAR(10) NOT NULL,
    )
    CREATE TABLE user(
        id INT ,
        name CHAR(10) NOT NULL,
        CONSTRAINT PK_id PRIMARY KEY,
    )
    ```
- 예시2, 복합 PK
    ```sql
    CREATE TABLE user(
        id INT,
        name CHAR(10),
        CONSTRAINT PK_id_name PRIMARY KEY(id,name)
        -- 이게 실무적인 코드는 아님.
        -- 이렇게 되면 id와 name을 결합한 것이 PK로 이용된다. 즉, 두 항목 모두가 겹쳐야 중복
    )
    ```
- 예시3, N:M 관계에서 FK 2개로 PK를 만들기
    ```sql
    CREATE TABLE product(
        id INT PRIMARY KEY,
        name CHAR(30)
    )
    CREATE TABLE user(
        id INT PRIMARY KEY,
        name CHAR(10)
    )
    CREATE TABLE orders(
        user_id INT,
        product_id INT,
        CREATED_AT DATETIME,
        CONSTRAINT pk_user_product_created PRIMARY KEY(user_id,product_id,CREATED_AT),
        -- 3개를 묶어서 하나의 PK로 사용
        CONSTRAINT fk_to_user_id FOREIGN KEY(user_id) REFERENCES user(id),
        CONSTRAINT fk_to_product_id FOREIGN KEY(product_id) REFERENCES product(id)
    )
    ```

#### 참조 무결성
- 정의 : `FK 값`은 참조하려는 테이블의 `기본키 값과 일치`하거나 `NULL이어야 한다.` 테이블 간의 `관계 일관성`을 유지해준다.
- 효과 : Orphan Data 발생 방지
    - Orphan Data
        - 존재하지 않는 데이터를 참조하는 데이터
- 예시 : `수강신청` 테이블에 `학번(PK)이 입력`될 때, 실제로 존재하는 학생의 `학번`이어야 한다. 또한, `참조하는 학생 데이터가 사라지는 경우`, `관련 수강 데이터도 처리`(삭제/변경) 되어야 한다.
- 참고 : 데이터 삭제 시, 참조 당하는 데이터/테이블은 삭제가 안된다.
    - EX) 위의 orders 테이블에서 참조되는 users의 1번 데이터는 삭제할 수 없다. (참조되지 않는다면 가능)
    - 이때 `삭제 규칙을 설정`하면 `업데이트/삭제 시 처리 방식을 결정`할 수 있다.
        ```sql
        -- 옵션
        ON DELETE [NO ACTION / CASCADE / SET NULL / SET DEFAULT ]
        ON UPDATE [NO ACTION / CASCADE / SET NULL / SET DEFAULT ]
        ```
        - NO ACTION : 아무것도 하지 않음 (DEFAULT)
        - CASCADE : 연쇄 삭제, 참조하는 데이터도 삭제
        - SET NULL : 참조하고 있는 데이터에 NULL
        - SET DEFAULT : 데이터 베이스 설정에 따른다.
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

#### 도메인 무결성
- 정의 : `특정 Column에 입력되는 값`은 `정의된 도메인(범위, 타입, 형식)`내에 있어야 한다.
- 효과 : 데이터 타입과 값의 유효성 보장
- 예시 : 나이 Column에 문자열 혹은 미정, 너무 크거나 0이하의 값은 입력될 수 없다. (In MariaDB, `CHECK`제약 조건이나 `데이터 타입`을 통해 `이를 구현`한다.)
- 예시 :
    ```sql
    -- 기본 형식
    -- CHECK(컬럼이름=값의 종류 or 값의 범위)
    ```
- 예시
    - 조건
        1. users 테이블
        2. 성별 = 남자 or 여자
        3. 나이 = 0이상 100이하
        4. 이름 = 전으로 시작
    ```sql
    CREATE TABLE users(
        gender CHAR(2) CHECK(gender IN ('남자','여자')),
        age INT CHECK(age BETWEEN 0 AND 100),
        name CHAR(5) CHECK(name LIKE '전%') -- ~로 시작한다 -> LIKE
    )
    ```
#### 고유 무결성
- 정의 : `특정 컬럼에 입력되는 값`들이 테이블 내에서 `서로 중복되지 않아야 한다.`
- 효과 : 기본키가 아니어도 Unique 해야 하는 속성들을 보호
- 예시 : 회원 테이블에서 id가 pk인 경우라 하더라도 email, 전화번호 등은 Unique해야 한다. 이러한 속성들을 `UNIQUE 제약 조건을 통해 관리`한다.
- 참고 : 2개 이상의 Column을 합쳐서도 적용 가능하지만, 이때는 `테이블 제약 조건`으로 설정해야 한다.
    ```sql
    CREATE TABLE user(
        name CHAR(10) UNIQUE,
        age INT ,
        email CHAR(100) UNIQUE,
        -- 이렇게하면, name과 email이 각각 UNIQUE 검사를 하는 것, 즉, name 컬럼에 동일한 이름이 2개 이상 있을 수 없고, email as well
    )
    CREATE TABLE user(
        name CHAR(10),
        age INT,
        email CHAR(100),
        CONSTRAINT UK_name_email UNIQUE(name,email)
        -- 이렇게하면, name,email 각 컬럼에서는 중복된 값이 있을 수 있지만, name-email 조합이 동일한 행이 2개 이상 있을 수 없다.
    )
    ```
#### NULL 무결성
- 정의 : 테이블의 특정 컬럼에 `빈 값(NULL)`이 올 수 있는지 없는지를 결정한다.
- 효과 : 필요한 값의 누락을 방지
- 예시 : 주문 테이블에서 `결제 금액`은 누락되면 안된다. `NOT NULL 제약 조건을 설정`하여 `무결성을 유지`한다.
- 참고 : 
    - NOT NULL을 설정하여 NULL 무결성을 만족시킬 수 있다.
        ```sql
        CREATE TABLE user(
            email char(10) NOT NULL, -- email은 NOT NULL (필수 입력)
            password char(100)
        )
        ```
    - 다만, 테이블 생성시 NULLABLE 이었던 속성을 NOT NULL로 변경하기 위해서는 `MODIFY(자료형 수정)`으로 해야한다.
        - Why? NULL 여부는 `각 record의 Header에 속한 BITMAP에 표시`가 된다. 만약 `NOT NULL이라면 비트맵을 위한 공간 자체가 할당되지 않는다`. 따라서 변경하려면 해당 `테이블의 메타데이터 자체를 수정`해서 `모든 행의 물리적 구성을 변경`해야 하므로, `MODIFY로 진행`한다.
            - Q) NULLABLE과 NOT NULL이 섞여있으면? 
            - A) NULLABLE에 대한 부분만 비트맵이 생성된다. 
                - Q) 섞여있는데 순서를 어떻게 구분하나?
                - A) Data Dictionary (컬럼 이름과 순서, 데이터 타입, NULL허용 여부 저장)를 확인하여 어떤 컬럼이 NULL인지 골라내고 매핑하여 구분한다.

### 제약 조건 수정
#### 제약 조건 확인
```sql
SELECT *
FROM information_schema.table_constraints;
```
#### 제약 조건 수정
```sql
ALTER TABLE 테이블이름 MODIFY 컬럼이름 자료형 제약조건;
-- ALTER TABLE user MODIFY id INT CHECK(id>0);
```
#### 제약 조건 추가
```sql
ALTER TABLE 테이블이름 ADD 제약조건(컬럼이름);
-- ALTER TABLE user ADD PRIMARY KEY(name);
```
#### 제약 조건 삭제
```sql
ALTER TABLE 테이블이름 DROP CONSTRAINT 제약조건이름;
```
#### 예시
1. user table id(PK),name -> id,name(PK)로 변경하기
    ```sql
    ALTER TABLE user
    DROP CONSTRAINT pk_id
    ADD PRIMARY KEY(name);
    ```
    - 주의, PK는 not null이 보장되어야 한다. 따라서 위 코드를 실행하기 전, 아래 코드로 NULL 무결성을 먼저 확보한다.
        ```sql
        ALTER TABLE user
        MODIFY name char(10) NOT NULL;
        ```
### 기본값 설정
- 자료형 뒤, DEFAULT와 함께 값을 설정할 수 있다.
    ```sql
    CREATE TABLE user(
        id PRIMARY KEY,
        name CHAR(10) DEFAULT "성이름",
    )
    INSERT INTO user(id) VALUES(1); -- 이름이 성이름으로 설정된다.
    ```

## 참고

1. Oracle, MySQL/MariaDB/MongoDB
    - Oracle : User > Database
        - User가 더 크다.
        - 따라서, 로그인을 하면 Database를 사용할 준비가 끝난다.
    - MySQL/MariaDB/MongoDB : Database > User
        - Database가 더 크다.
        - 따라서 User가 달라도, Database이름이 같으면 안 된다.
        - 또한, 로그인을 하더라도 Database 사용(`use Database`)을 알리지 않으면 안된다.

2. Customizing, Optimizing
    - 기본적인 이론적 지식이 중요하다.
    - `~하면 ~게 된다`가 아닌 정확하게 어떠한 흐름으로 시스템이 동작하는지를 알아야 한다.
3. CQRS 일관성 유지
    - 만약 한 쪽에서 작업하다가 꺼지면, secondary 서버는 업데이트 되지 못할 수 있다.
    - 이 문제를 해결해주는 것이 `MessageBroker`다.
        - MessageBroker 종류 : RabbitMQ, Kafka
    - CQRS 환경에서 수정된 것이 READ DB에서 업데이트 되지 않을 수 있는데 이를 MessageBroker로 해결한다.
