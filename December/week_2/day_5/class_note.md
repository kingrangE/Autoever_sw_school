# 12월 24일

## 데이터 베이스

### 데이터와 정보
1. 데이터 : 어떤 필요에 의해 수집했지만, `특정 목적을 위해 평가하거나 정제하지 않은 값`이나 `사실 또는 자료` 
2. 정보 : `수집한 데이터`를 `어떠한 목적을 위해 분석`하거나 `가공`하여 `가치를 추가`하거나, `새로운 의미`를 이끌어 낼 수 있는 결과
3. 지식 : 상호 연결된 `정보 패턴을 이해`하여 `이를 토대로 예측한 결과물`로 `정보에 기반한 규칙`, 획득한 `다양한 정보를 구조화`하여 `유의미한 정보로 분류`하고 `일반화 시킨 결과물`
4. 지혜 : 근본 원리에 대한 깊은 이해를 바탕으로 도출되는 `창의적 아이디어`


### 효율적 데이터 관리를 위한 조건
1. `데이터 통합`하여 관리
2. `일관된 방법`으로 관리
3. 데이터 `누락 및 중복 제거`
4. 여러 사용자가 `공동으로 실시간 사용 가능`
- 상황에 따라 다름 4번 정도가 중요

### 데이터 베이스
- 컴퓨터의 `기억 능력`을 활용하여 `자료를 가공, 저장, 활용하는 일체의 기술`
- 용어 의미
    - Data : 자료를 의미하는 datum의 복수형
    - Base : 집합
    - 즉, 자료 여러개의 집합
- 특징
    1. 운영상 필요한 데이터를 `중복을 최소화`해서 컴퓨터 기억 장치 내에 모아놓은 집합체
        - 사용하기 편리하도록 만들어 놓은 데이터의 집합
    2. 데이터의 중복 없이 `서로 관련`되어 있어, `관련된 모든 환경에서 사용`될 수 있는 `데이터들의 집합`
    3. 자료를 획득하여 `체계적으로 분류`,`정리`한 다음 컴퓨터에서 처리가 가능하도록 `전자적 형태로 저장`한 것
    4. 하나의 주제와 관련된 Data들의 모음
    5. 통합, 저장, 운영 가능한 `공동 데이터`


- 종속 : 어느 하나가 변경되었을 때, 다른 요소에 영향을 주는 것
    - 이를 방지하기 위해 Controller-Service-Repository, MVC(최근엔 서버에선 View를 안하는 추세로 가기에 트렌드에서 사라지는 중)
        - 그래서 Template Engine 쓰지 마라
            - View와 Model이 혼재해 있기 때문
- 파일의 중복(종속)을 없애자 -> 데이터베이스


- 현대적인 데이터베이스가 갖추어야 할 조건

- DBMS
    - 데이터 베이스와 다름
        - 데이터 베이스 : 데이터를 저장하고 있는 자체
        - DBMS : DB를 다루는 프로그램
    - CRUD : 조작기능
        - select, insert, update, delete
            - 최근엔 select와 그 외로 구분함
                - select : 동시에 가능
                - insert, update, delete : 동시 불가
            - 이것이 CQRS
                - CQRS가 머노 -> 설명 검색해보고 적기
                - 그래도 포폴에 이런거 해서 뭐 하면 좋을듯
    -  Control : 제어기능
        - grant, revoke, commit, rollback
            - 요즘엔 전자 2개는 DC, 후자 2개는 TC(Transaction Control로 본다.)
- 네트워크의 역사
    - 파일 시스템, Flat-File, ISAM
    - Network DB(그래프, 노드)(SNS에서 주로 사용), HierarchicalDB
    - 관계형 DBMS
    - 관계형 DBMS,객체지향형, 객체 관계형
    - 분산 파일 시스템, NoSQL

- RDBMS
    - 데이터 베이스를 테이블의 집합으로 설명하는 DB 시스템
    - Codd에 의해 개발
    - 상용 RDBMS Oracle, MySQL, IBM DB2, MS-SQL Server, Sybase를 포함한 SAP의 HANA DB, TeraData Database, Tibero 등이 있음
        - 추가로 배울만한 DB -> SAP (HANA DB), T-MAX(Tibero)
    - 오픈 소스 DBMS는 MySQL, PostgreSQL, SQLite 등이 있고, MySQL이 Oracle에 인수된 이후 가장 많이 사용되는 MySQL의 fork로 MariaDB등이 있음
    - 각 DB를 잘 이해하고, 목적에 맞는 DB를 잘 선택해서 쓰는게 좋음
    
- RDBMS 개체
    1. Table : 데이터를 저장하는 개체
    2. View : 자주 사용하는 SELECT 구문을 저장해서 테이블처럼 사용하는 개체
    3. Index : 데이터를 빠르게 찾게 해줌
    4. Synonim : 별명 설정
    5. PPT 보면서 정리  
    10. Trigger
        - 작업 전 : 유효성 검사를 주로 함
        - 작업후 : 로깅(작업이 성공했으면 성공했다. 언제 했다. 상태는 어떻다 이런거 알려줌)

- NoSQL
    1. 융통성 이쓴ㄴ 데이터 모델
    2. 응답 속도, 처리 효율에서 매우 뛰어난 성능
    
    - DynamoDB : KeyValue 형태
    - Document DB -> 몽고 DB
    - Wide Columnar Store
        - Big Table DB, Column Family DB라고도 함.
        - 단점 : 할줄 아는 사람이 많이 없음 -> 배울거면 Cassandra 배워보쇼
    - Graph DB : 그래프 형태의 DB
    - Column Oriented DB
        - Column 기반 장점 : 압축률 높음, 데이터 분석에 좋음
- 참고
1. 메모리 공부는 같이 (관계형 DB, NoSQL, 메모리)하자.
    - 하나만 하는 것보다 다같이하는게 좋음
    - 프로젝트할 때, 관계형 DB와 NoSQL을 같이 써보자.
        - 읽기 : NoSQL
        - 쓰기 : 관계형 DB b


## Maria DB

### 개요
> SQL에 기반을 둔 관계형 DBMS -> Open-Source(막 고쳐서 막 써도 됨)

### 작업 단위
- `테이블`
    - Oracle에서는 User가 작업 단위 (User > Database > Table)
    - MySQL, MariaDB는 Table이 작업 단위 (즉, 테이블 이름이 같은 것을 만들지 못함, Oracle은 User가 다르면 이름이 같아도 ㄱㅊ)
    - 테이블 이름은 원래 `DB이름.테이블이름` 이렇게 불러야 하지만, 현재 데이터베이스의 경우 DB이름을 생략할 수 있다.

### 설치
1. root는 local만 가능하도록 해야한다.  
    - 다른데서 하고 싶으면, 계정을 새로 파는게 좋음
2. port 번호 : 기본 3306
3. Buffer pool size :  
    - 일반적으로 DB는 별도의 컴퓨터에 두기 떄문에 이 값을 크게 설정하는 경우가 있다. 
    - 이게 크면 여러 명이 동시에 작업해도 렉이 안 걸린다.

### 접속 도구
> dbeaver

### 명령어
- `show databases` : 데이터 베이스 확인
- `select database()` : 현재 사용 중인 데이터베이스 확인
- `create database 이름` : 데이터 베이스 생성
- `use 이름` : 데이터 베이스 변경
- `show tables` : 데이터 베이스에 속한 테이블 확인
- `drop database 이름` : 데이터베이스 삭제
```sql
# 아래는 script로 한 줄씩 실행해야 한다.
show databases; --데이터베이스들 확인

select database(); --현재 사용 중인 데이터 베이스 확인

create database adam; --adam이란이름의 데이터베이스 생성(이미 있는 경우 씹힙)

use adam; -- adam으로 DB변경

select database() -- 현재 사용 중인 DB확인 -> adam

drop database adam -- 데이터 베이스 삭제
-- 주석
/* 여러 줄 주석 */
```

- sql파일 한 번에 실행 : `source 파일명`


- 샘플데이터 요약
    1. EMP 테이블 - 사원 테이블
        - EMPNO: 사원 번호 - 정수 4자리, 기본키
        - ENAME: 사원 이름 - 문자
        - JOB: 직무 - 문자
        - MGR: 관리자 사원 번호 - 정수 4자리
        - HIREDATE: 입사일 - DATE
        - SAL: 급여 - 실수 7자리이고 소수 2자리
        - COMM: 상여금 - 실수 7자리이고 소수 2자리(NULL 포함)
        - DEPTNO: 부서 번호 - 정수 2자리 이고 DEPT 테이블의 DEPTNO를 참조
    2. DEPT 테이블 - 부서 테이블
        - DEPTNO: 부서 번호 - 정수 2자리 이고 기본키
        - DNAME: 부서 이름 - 문자
        - LOC: 위치 - 문자
    3. ... (PPT보고 추가)

- 유용한 명령어


---
- 일반적으로 DB는 프로젝트당 하나 만듦
- 참고의 DEPT,EMP,SALGRADE -> SQLD 시험 대비로 좋음 (그대로 나옴)
- 예약어(SELECT 같은거 대소문자 구분안함)
    - MySQL, MariaDB -> 컬럼이나 테이블 명도 대소문자 구분안함
- SQL은 비 절차적 언어 (순서대로 실행되지 않음)
- DB,네트워크 명령어는 메모장에 적고 시뮬레이터 같은걸로 검증한 후, 옮기기
    - 데이터는 소중하니까

### SELECT 기본 형식
- SELECT FROM [WHERE][GROUP BY][HAVING][ORDER BY]
    - [] 선택적으로 입력
- SELECT [DISTINCT]* 또는 {컬럼명[별명]}
    - 조회할 컬럼이나 연산식을 작성
    - 테이블의 모든 컬럼을 조회 -> `SELECT 절에 *을 사용`
        - 예시, tCity 테이블의 모든 데이터를 조회
            ```sql
            SELECT *
            FROM tCity
            ```
    - 특정 컬럼을 조회 -> `컬럼 이름 나열`
        - 예시, tCity 테이블에서 name과 popu 컬럼 조회
            ```sql
            SELECT name,popu
            FROM tCity;
            ```
        - tStaff 테이블에서 name, depart, grade 컬럼 조회
            ```sql
            SELECT name,depart,grade
            FROM tStaff;
            ```
    - SELECT 별명
        - 별명은 실행 순서상 SELECT 뒤에 있는 곳에서만 사용할 수 있다.
        - 형식 : 컬럼 이름/연산식 AS "별명"
            - 별명에 공백이 있거나 대문자 등의 `특수문자`가 있는 경우 " "로 묶지 않으면 ERROR가 발생
        - 예시, tCity 테이블에서 `name 컬럼을 조회`하는데 `도시명`이라는 별명으로 조회 
            ```sql
            SELECT name AS "도시명"
            FROM tCity;
            ```
    - 연산식 출력
        - SELECT 절에 COLUMN 이름 대신에 연산식(+-*/%)을 이용하는 것이 가능하다.
        - 보통 연산식을 출력할 때 `별명을 많이 사용`한다.
        - 예시, tCity 테이블에서 name과 popu에 10000을 곱한 결과를 출력
            ```sql
            SELECT name, popu * 10000 AS "인구"
            FROM tCity;
            ```
    - 단순 계산식(테이블에 저장된 데이터가 아닌) 출력하는 경우, FROM 생략 가능
        - ORACLE이라면, dual을 사용해야 한다고 함.
        - 예시, 1년 시간
            ```sql
            SELECT 24*365 as total_hour_per_year
            ```
    - 컬럼을 연결해서 조회
        - 보고서 만들 때 주로 사용
            - 아래처럼 조회 결과와 문장을 조합해서 나타낼 수 있어서 보고서에 주로 이용
        - `CONCAT(컬럼 이름이나 연산식 나열)`
        - 예시, EMP테이블에서 ENAME과 JOB연결
            ```sql
            SELECT CONCAT(ENAME,"님의 직무는 ",JOB,"입니다.")
            FROM EMP;
            ```
    - 증복 제거
        - `DISTINCT`
        - 중복값을 제거하는 명령어, SELECT 절에 한 번만 사용 가능
            - 하나의 컬럼이 오면, 그 컬럼의 중복을 제거
            - 여러 개의 컬럼이 오면, 전달받은 모든 컬럼 값이 일치해야 중복으로 인식
                - ex, (1,2,3) - (1,2,2) -> 다름 / (10,20,30)-(10,20,30) -> 같음(중복)
        - 예시, tCity 테이블에서 region의 중복을 제거하고 조회
            ```sql
            SELECT DISTINCT region
            FROM tCity

            -- 위와 아래는 결과가 같음 (묶는다는 것은 중복을 제거한다는거니까)
            SELECT region
            FROM tCity
            GROUP BY region;
            ```
    - 정렬
        - `ORDER BY`절에서 수행
        - `ORDER BY`절이 없으면, MariaDB는 `PK를 가지고 정렬`해서 `데이터를 조회`한다.
        - `ORDER BY`절의 형식
            - COLUMN이름 또는 연산식[ASC/DESC]형태를 나열 (ASC(default) : 오름차순, DESC : 내림차순)
            - COLUMN이름 대신에 SELECT에서 설정한 별명을 사용할 수 있고, SELECT 절에 나열한 COLUMN의 INDEX(순서)사용 가능
            - 여러 개 작성하면, `앞의 값이 동일`할 때, `뒤의 식이 수행`된다.
        - 예시, `tCity` 테이블의 모든 컬럼을 `popu의 오름차순으로 정렬`해서 `조회`
            ```sql
            SELECT *
            FROM tCity
            ORDER BY popu ASC;
            ```
        - 정렬은 SELECT 다음에 수행되기 때문에 별명을 사용해도 된다.
            ```sql
            SELECT name as "도시명", area as "도시크기"
            FROM tCity
            ORDER BY 도시크기 DESC;
            ```
        - 인덱스(순서 정보)를 사용하여 정렬할 수도 있다.
            ```sql
            SELECT name as "도시명", area as "도시크기"
            FROM tCity
            ORDER BY 2 DESC; -- 두번째(area)기준 정렬
            ```
        - 정렬한 기준을 조회하지 않고도 정렬할 수 있기는 함
            - 근데 권장 X -> 무슨 기준으로 정렬됐는지 잘 알 수 없기 때문이다.

### WHERE 기본형식
- WHERE CONDITION(조건)
    - 조건

- WHERE :  읽을 `레코드`의 조건을 지정
    - 이 절이 생략되면, 테이블의 모든 데이터를 조회한다.
    - 조회뿐 아니라, insert, delete, update할 때 조건 지정이 필요한 경우에 사용 가능
- WHERE의 연산자
    1. `=` : 같다.
    2. `>` : 왼쪽 크다.
    3. `<` : 오른쪽 크다
    4. `>=` : 왼 같크
    5. `<=` : 오 가트
    6. `!=`,`<>`,`^=`,NOT 컬럼이름 : 다르다.
- 주의
    - literal을 기술할 때, `문자열`과 `날짜`는 `작은 따옴표(')`로 감싸야 한다.
        - BUT, `MySQL`과 `MariaDB`는 작은 따옴표 대신에 `큰 따옴표(")를 써도 동작`한다.
- 예시, tCity 테이블에서 name이 서울인 데이터의 모
    ```sql
    SELECT *
    FROM tCity
    WHERE name="서울" -- Maria DB니까 " 되는데 다른거에서는 '이거 써야함
    ```
- SQL 예약어는 대소문자 구분을 하지 않지만, Column안에 저장된 문자열은 `대소문자 구분`을 한다.
- 테이블 이름이나 컬럼 이름은 사용하는 데이터베이스에 따라 다르다.
    - MySQL과 MariaDB에서는 `테이블을 만들 때` 별 다른 옵션을 지정하지 않으면, 저장할 때는 대소문자를 구분, `조회할 때는 구분하지 않음.`
    - `대소문자를 구분`하도록 조회
        - Column이름 앞에 `BINARY`를 추가하기
        - 예시2, tCity 테이블에서 metro column의 값이 y인 데이터 조회 (대소문자 구분 X)
            ```sql
            SELECT *
            FROM tCity
            WHERE metro ='y' -- (이게 'Y'든 'y'든 상관 없다.)

            ---
            SELECT *
            FROM tCity
            WHERE BINARY metro = 'Y' -- (이러면 'Y'인 애들만 조회가 된다.(대소문자 구분))
            ```
    - 콜레이션을 변경하여 대소문자를 구분하도록 할 수도 있다. (콜레이션이 뭐지?)
        - MySQL이나 MariaDB의 경우 `문자 집합`이 `utf-8`이나 `utf-8-mb4`로 저장함. 이 두 개의 경우 __ci(Case Insensitive)가 붙는 콜레이션으로 만든다.
            - Case Insensitive : 대소문자 무시
                - 이 콜레이션 덕분에 조건절에서 대소문자를 구분하지 않는거
                - 이 콜레이션을 변경해야 대소문자를 구분하기 때문에 __bin,__cs로 바꿔줘야 구분한다.
                - 즉, 테이블을 만들 때 다음과 같이 설정하면 구분하도록 바뀐다.
                    ```sql
                    CREATE TABLE 테이블이름(
                        컬럼이름 자료형 COLLATE utf8mb4__bin,
                    );
                    ```
                - 기존 테이블을 변경하고 싶다면?
                    ```sql
                    ALTER TABLE 테이블이름 MODIFY 컬럼이름 자료형 COLLATE utf8mb4__bin,
                    ```
                    - 예시, tCity 테이블의 metro 컬럼의 자료형은 VARCHAR(50) 이 컬럼이 대소문자 구분되도록 해보기
                        ```sql
                        ALTER TABLE tCity MODIFY metro VARCHAR(50) COLLATE utf8mb4__bin
                        ```
            - 영어 -> ASCII 코드로 그대로 표현한다.
                - A:65(0100 0001), a:97(0110 0001), 표현 비트 수가 늘어나도 이 앞에 0으로 채워진 비트를 붙이는 방식이기에 어떤 표현 방식에서도 변하지 않는다.(글이 안 깨짐)
            - 그 외 언어 -> 지네 마음대로 코드를 표현함
                - 한글 MS949(cp949):WINDOW 인코딩, EUC-KR : 웹
                - 전세계 문자 사용 인코딩
                    - utf-8(3byte) : 이모지를 사용 못함
                    - utf-8-mb4(4byte) : 이모지도 사용 가능



- FROM 테이블 이름[새로운 이름] 또는 SELECT 구문
    - 조희할 테이블 이름

- GROUP BY 그룹핑할 컬럼 이름이나 연산식
    - 그룹핑할 때
- HAVING 그룹핑 한 후의 CONDITION
    - 그룹화된 것들로 조건 거르기
- ORDERBY 정렬한 컬럼 이름 또는 연산식
- LIMIT 행 개수 [OFFSET offset]
- NULL
    - 가리키는 데이터가 없다라는 뜻
    - 파이썬에서는 None, 데이터 분석-결측치(NAN), 데이터베이스에서 NULL은 아직 알려지지 않은 값
        - 최근의 프로그래밍 언어 - NULL을 DB처럼 다룸
        - 그래서 NULL이 가능하면 Optional이라고 한다.
    - Kotlin,Swift
        - 일반 값 -> 8자리만 할당
        - NULL가능(Optional) -> NULL을 표시하는 1자리 추가 -> 총 9자리 할당
        - 장점
            - NULL을 검사할 때, 기존엔 8자리 모두 확인 
                - OPtional 방식 => 맨앞자리만 검사
- NULL을 확인할 때는 = 나 <>를 사용하지 않고 IS NULL과 IS NOT NULL을 사용한다.
    - `= NULL`로 데이터를 조회하면 조회되지 않음
    - 구조 자체가 다르기 떄문 (8자리 vs 9자리)
    - 예시, `tStaff테이블`에서 `score가 NULL인 데이터의 모든 컬럼` 조회
        ```sql
        SELECT *
        FROM tStaff
        WHERE score = NULL;
        /*위에는 값이 하나도 조회가 안됨*/
        SELECT *
        FROM tStaff
        WHERE score IS NULL;
        -- 이렇게 하면 2개 값이 조회된다.
        ```

- AND, OR, NOT
    - AND : 모두 참 = 참
    - OR : 모두 거짓 = 거짓
    - NOT : 반대
    - 우선 순위 : `NOT > AND > OR`
        - 1주차 2번쨰 시간에 배운 효율적 조회를 잘 사용하는 것이 매우 중요
            - 앞 조건에서 더 많이 거를 수록 효율이 올라간다.
    - 예시, tCity 테이블에서 popu가 100이상이고, area가 700이상인 데이터의 모든 컬럼 조회
        ```sql
        SELECT *
        FROM tCity
        WHERE area >= 700 AND popu >= 100 
        ```

- LIKE
    - 패턴으로 부분 문자열을 검색
    - LIKE에서는 `와일드카드` 사용 가능
    - 와일드 카드
        - `%` :글자 수 상관 없음
            - ~로 시작하는 / 끝나는 / 포함됨을 검색할 때 사용한다.
            - 예시, tCity테이블에서 name에 천이 포함된 데이터를 조회
                ```sql
                select *
                FROM tCity
                WHERE name LIKE '%천%'; -- 앞 뒤로 %로 감쌈
                ```
            - 예시2, tCity테이블에서 name이 천으로 시작하는 데이터 조회
                ```sql
                select *
                FROM tCity
                WHERE name LIKE '천%';

                -- 끝나는건 '%천'
                ```
            - 예시3, EMP테이블에서 입사연도가 1981인 데이터의 이름을 조회하기
                ```sql
                select ENAME
                FROM emp
                WHERE HIREDATE LIKE '1981%'
                ```
                
        - `_` : 한 글자라는 표기
            - 예시, tstaff 테이블에서 name의 세번째 글자가 "신"인 데이터를 조회
                - `앞의 자리 수만큼 _를 사용`함. (신이 3번쨰니까 _ 2개)
                ```sql
                SELECT *
                FROM tStaff
                WHERE name LIKE "__신%";
                ```
            - 예시 2, tstaff테이블에서 이름의 길이가 정확히 4자인사람 조회
                - 자릿수만큼 _를 사용 (4글자 -> _ 4개)
                ```sql
                SELECT *
                FROM tstaff
                WHERE name LIKE "____";
                ```
        - `[문자 나열]` : 나열된 문자 중 하나
        - `[^문자 나열]` : 나열된 문자를 제외하고
    - 와일드 카드 문자를 검색하고자 하는 경우 -> `ESCAPE` 구문 사용
        - ESCAPE는 와일드 카드 문자가 와일드 카드가 아닌 일반 문자로 인식되도록해줌
        - 예시, `30%`인 데이터를 조회하고 싶으면 어떻게 해야할까
            ```sql
            select *
            from x
            WHERE scale = '30#%' escape '#' -- 이렇게하면 # 다음의 문자 1개는 일반 문자로 취급하게 함
            ```
- BETWEEN
    - `BETWEEN A AND B` : A부터 B까지 (조건 : A <= B 여야함)
        - `문자열`이나 `날짜`도 `크기 비교가 가능`하다.
    - BETWEEN이 그냥 AND로 비교하는 것보다 빠르다.
        - x>=A AND x<=B; -> x를 2번 조회
        - A BETWEEN B -> A로 먼저 오름차순 정렬, A 이상을 기준으로 B 까지 정렬 후 반환 -> x를 1번 조회

    - 예시, tCity테이블에서 area가 700 이상 1000이하인 것
        ```sql
        select *
        from tCity
        WHERE area BETWEEN 700 AND 1000
        ```
    - 예시2, emp테이블에서 hiredate가 1981년인 데이터를 조회
        ```sql
        SELECT *
        FROM emp
        WHERE hiredate BETWEEN '1981-01-01' AND '1981-12-31';
        ```
- IN
    - IN(목록)을 이용하면 목록 중 하나를 조회
        -  즉, 요소1 or 요소2 or 요소3 과 유사함
    - 예시, tCity테이블 region이 경상, 전라인 데이터 조회
        ```sql
        /*IN 사용*/
        SELECT *
        FROM tCity
        WHERE region IN ('경상','전라');
        ---
        /*OR 사용*/
        SELECT *
        FROM tCity
        WHERE region = '경상' OR region ='전라'; 
        ```
### LIMIT 기본 형식
- 행의 개수 제한에 사용
- SELECT 구문의 맨 마지막에 작성
    ```sql
    LIMIT [건너뛸 개수,] 조회할 개수
    LIMIT 조회할 개수 OFFSET 건너뛸 개수
    ```
- 정렬을 수행한 후 작업하기
- 예시, tCity 테이블에서 area가 가장 큰 4개의 데이터 조회
    ```sql
    SELECT *
    FROM tCity
    ORDER BY area DESC
    LIMIT 4
    ```
- 예시, tCity 테이블에서 area가 큰 순서로 4번째부터 3개
    ```sql
    SELECT *
    FROM tCity
    ORDER BY area DESC
    LIMIT 3,2 -- LIMIT 2 OFFSET 3과 같은 의미
    ```

### 검색 결과 파일로 저장
- 형식
    ```sql
    SELECT ... INTO OUTFILE '파일경로'
    [CHARACTER SET 인코딩 방식]
    [export_options]
    ```
- OUTFILE '파일경로' 대신에 변수이름을 사용하면 변수에 저장
- OUTFILE 대신에 `DUMPFILE`을 사용해야 하는 경우가 있는데 이 경우는 검색 결과에 `BLOB`(파일의 내용을 저장할 때 사용하는 타입) 타입의 데이터가 있는 경우
#### 옵션
{FIELDS|COLUMNS}
TERMINATED BY 문자열
[[OPTIONALLY] ENCLOSED BY 'char']
ESCAPE BY 'char'
LINES [STARTING BY 문자열][TERMINATED BY 문자열]
- 예시, `members 테이블`의 모든 데이터를 `파일에 저장`
    ```sql
    SELECT * 
    INTO OUTFILE 'C:\Users\USER\Desktop\members.dat'
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    FROM member;
    ```
- 집가서 해보기


#### 실행 순서 (중요!)
- FROM->WHERE->GROUP BY->HAVING->SELECT->ORDER BY->LIMIT
    - 이 순서를 역순으로 못한다. 예를 들어, 별명을 SELECT에서 만들었다면, 그 별명은 SELECT전의 부분에선 쓰지 못한다. 하지만, 뒤에선 쓸 수 있다.

### FUNCTION
> 입력 데이터를 이용해서 연산을 수행한 후, 출력 값을 만들어내는 개체
- PPT 보면서 잘 실습하고 정리하기


#### 매개변수 개수에 따른 분류
1. SCALA 함수 : 값 하나를 가지고 작업을 수행하는 함수
    - 각 함수에 대한 내용을 PPT를 참고하여 수정하기
2. GROUP 함수 : 0개 이상의 데이터를 가지고 작업을 수행하는 함수

#### 용도에 따른 분류
1. 문자 함수
2. 날짜 함수
3. 수치 함수
4. 제어 함수
5. 집계 함수
6. 정보 함수
7. 암호 함수

### 타입 변환
- 묵시적 형 변환
    - PPT 보고 정리하자!
- `TO_CHAR`

#### 명시적 형변환 
- MySQL에서는 VARCHAR로 형 변환이 불가하다.
    - WHY?
    - VARCHAR와 CHAR의 차이를 생각하면 알 수 있다.
        - CHAR : 길이가 고정
        - VARCHAR : 길이가 가변
    - 예시, adam을 저장
        - CHAR(10),VARCHAR(10) 각각 생성했다 가정
            1. CHAR에 adam을 저장 (10칸 중 4칸 소비) - 6칸 남음
                - 장점 : 크기를 계속 유지(변경에 유리)
                - 단점 : 메모리를 절약하지 않음
            2. VARCHAR에 adam을 저장 (10칸 중 4칸 소비) - 6칸 남음 -> 6칸 남는거 삭제
                - 장점 : 낭비되는 공간이 덜함(메모리 절약)
                - 단점 : 변경이 어려움
                    - 글자 수가 늘어나면, 길이를 늘려야 되는데, 다른 데이터도 공간을 차지하기 떄문에 그것이 안됨 -> Row Migration 발생(행이동)(이사가야함)
                        - 이로인해시간이 많이 소요됨


### GROUPING
#### 집계 함수
- `NULL이 아닌 데이터`를 그룹화해서 통계를 계산해주는 함수 (숫자나 날짜에만 사요)
- 그룹화해서 작업하기 때문에 GROUP BY절 다음에 사용해야만 한다.
- 문자열의 경우 `크기 비교`가 가능하기 때문에 `MIN`,`MAX` 사용 가능
- 종류 : `SUM`,`AVG`,`MIN`,`MAX`,`COUNT`
    - 위 5개는 모든 DB에 다있다.
        - `VAR_SAMP(분산)`, `STDEV(표준편차)` : 일부에만 있음
#### COUNT함수
- 컬럼 이름을 설정하면, COLUMN의 데이터가 NULL이 아닌 개수를 Return, *을 설정하면 모든 COLUMN이 NULL인 경우(NULL,NULL,NULL,...,NULL)를 제외한 데이터 리턴

- 예시, EMP 테이블에서 COMM이 NULL이 아닌 데이터의 개수를 조회
    ```sql
    SELECT COUNT(COMM)
    FROM EMP;
    ```
- 예시2, EMP 테이블 행의 개수 조회
    ```sql
    SELECT COUNT(*)
    FROM EMP;
    ```
- 예시3, tStaff테이블에서 depart 의 종류 개수 세기
    ```sql
    SELECT COUNT(DISTINCT depart)
    FROM tStaff;
    ```
- 예시4, tStaff에서 salary의 평균 조회
    ```sql
    SELECT AVG(salary)
    FROM tStaff;
    --- NULL 이 없으면 합/개수와 AVG의 값이 같음
    --- 하지만 아래처럼 다른 경우엔 결과가 다름 -> NULL인 개수까지 
    SELECT AVG(score)
    FROM tStaff;
    SELECT SUM(score)/COUNT(*) -- 전체 합(NULL제외) / 전체 개수 => 나누는 개수가 변경되었으므로 달라짐 따라서, COUNT(score)로 해서 score에 있는 NULL을 제외한 항목의 개수를 세도록 해야함. 아니면 IFNULL 이용하기
    FROM tStaff;
    ```
- 예시5, WHERE에 집계함수 못 쓴다. (실행시간 기준에 안 맞기 때문)
    ```sql
    /*에러 남*/
    SELECT depart
    FROM tstaff
    WHERE MAX(salary) > 100 -- WHERE는 GROUP BY 이전에 실행되기 때문에 집계함수 (MAX)를 쓰면 오류가 발생한다.
    GROUP BY depart
    ```
- 예시6, FROM으로 새로운 이름 만들기
    - 새로운 이름을 만들었으면 무조건 그 새로운 이름으로 적용해야 한다.
    ```sql
    SELECT *
    FROM emp e -- e 로 별명 줌
    WHERE e.comm > 100  -- 별명 사용 정상
    ---
    SELECT *
    FROM emp e
    WHERE emp.comm > 100 -- emp 사용 안댐 e라고 했으니까 e써야 함.
    ```