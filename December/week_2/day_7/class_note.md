# 12월 29일
## DDL
### AUTO_INCREMENT
- MySQL, Maria DB에서 `일련 번호`를 생성하는 기능
- 테이블을 만들 때, `초기값을 설정`하는 것이 가능하다.
- 적용은 COLUMN에 하는데, COLUMN의 자료형 뒤에 `AUTO_INCREMENT`를 추가하면 되고, `적용된 COLUMN은 Unique나 PK 제약조건이 설정`되어야 합니다.
- 하나의 테이블에 1개의 컬럼에만 적용 가능하다.
- ALTER TABLE 명령을 이용해서 `초기값을 수정`할 수 있다.
    - 시작하는 초기값 말하는 것
- 일련번호는 직접 입력해도 되고, 자동으로 입력하도록 생략해도 된다.
    - 자동 입력(AUTO)은 내가 마지막으로 직접 입력한 숫자의 다음부터 시작한다.
        - EX
            ```sql
            insert into tSale(sale_no,customer,product) values (3,'A',"a"); -- 3시작
            insert into tSale(customer,product) values ('A',"a"); -- 자동 -> 4
            insert into tSale(customer,product) values ('B',"b"); -- 자동 -> 5

            insert into tSale(sale_no,customer,product) values (8,'r',"r"); -- 직접 8
            insert into tSale(customer,product) values ('h',"h"); -- 자동 -> 9

            delete from tSale where product='h'; -- 9삭제 
            insert into tSale(customer,product) values ('h',"h"); -- 자동 -> 10 (삭제와 상관없이 이어서 진행)
            ```
- 일련 번호가 적용된 테이블 생성 예시 (고객-구매 테이블)
    ```sql
    -- 2가지 방식으로 PK 선언 가능
    CREATE TABLE tSale(
        sale_no INT AUTO_INCREMENT PRIMARYKEY,
        customer VARCHAR(10),
        product VARCHAR(30),
    );
    ---
    CREATE TABLE tSale(
        sale_no INT AUTO_INCREMENT,
        customer VARCHAR(10),
        product VARCHAR(30),
        CONSTARINT pk_tSale PRIMARY KEY(sale_no)
    );
    ```
    - 고객과 제품은 중복될 수 있는 정보다.
        - 이 두 정보는 중복될 수 있기 때문에 PK로 쓰기 애매함
        - 이때 쓸 수 있는 PK가 2개 존재
            1. TIMESTMP : 현재 시간
                - 이것 자체로 의미를 가지기 떄문에 TIMESTAMP가 더 유리하다.
                    - ex, traffic이 몰리는 시간대 파악 가능
            2. id : 일련 번호
                - static으로 생성되기 떄문에 증가만 한다.
                    - 중간에 하나를 삭제해도 그냥 계속 이어 증가함.
                        - ex, 1,2,3,4,5 -> 5삭제 -> 1,2,3,4,6(6 시작)
                    - 이러한 이유로 직접 생성기를 만들기도 한다.

#### 일련 번호 시작 지점 변경
```sql
ALTER TABLE 테이블이름 AUTO_INCREMENT = 바꿀 값;
```
- 예시,
    ```sql
    ALTER TABLE tSale AUTO_INCREMENT = 100;
    ```

#### 마지막에 삽입된 일련 번호 
```sql
select LAST_INSERT_ID(); -- 이 문구를 실행하면 마지막에 삽입된 일련번호가 출력된다.
```

### SET OPERATOR
- 2개 이상의 테이블에서 데이터를 추출하는 방법 중 하나
- 여러 개의 SELECT 문장을 결합해서 결과를 얻어내는 연산
#### 기본 형식
```sql
SELECT 문

SET operater

SELECT 문
```
#### 가이드라인
1. `첫 번째 SELECT 구문`과 `두 번째 SELECT구문의 열`은 앞에서부터 `순서대로 매칭`이 되므로, `열의 개수`와 `자료형이 일치`해야 한다.
2. 테이블은 동일할 수도 있는데, 대부분 동일하지 않음
3. 출력되는 COLUMN의 이름은 첫 번째 SELECT 구문의 것
4. ORDER BY는 마지막에 1번만 기술 가능
5. BLOB, CLOB, BFILE, LONG형 컬럼에는 사용 불가
    - 파일의 내용을 저장하는 Column들임
    - 파일 내용을 하나하나 비교하는 작업은 EVA
#### 연산자
- `UNION` : `합집합` - 중복 제거
- `UNION ALL` : `합집합` - 중복 제거 X
- `INTERSECT` : `교집합` 
- `EXCEPT` : `UNION - INTERSECT` (`앞쪽에 존재하는 것만 조회`)

#### 실습
- EMP 테이블과 DEPT 테이블의 DEPTNO 확인
    ```sql
    SELECT DEPTNO
    FROM EMP;

    SELECT DEPTNO
    FROM DEPT;
    ```
    - 둘의 합집합 (중복 제거)
        ```sql
        SELECT DEPTNO
        FROM EMP
        UNION
        SELECT DEPTNO
        FROM DEPT;
        ```
    - 둘의 합집합 (중복 O)
        ```sql
        SELECT DEPTNO
        FROM EMP
        UNION ALL
        SELECT DEPTNO
        FROM DEPT;
        ```
    - 둘의 교집합
        ```sql
        SELECT DEPTNO
        FROM EMP
        INTERSECT
        SELECT DEPTNO
        FROM DEPT;
        ```
    - 둘의 차집합 (EMP-DEPT)
        ```sql
        SELECT DEPTNO
        FROM EMP
        EXCEPT
        SELECT DEPTNO
        FROM DEPT;
        ```
#### 사용 상항
- 테이블의 성격 상의 이유로 나누어져 있을 때, 확인하기 위함.
    - EX, 대출과 저축 테이블 구분되어 있을 때, 아래를 확인
        1. 대출과 저축을 같이 한 사람(INTERSECT)
        2. 대출만 한 사람 (EXCEPT)
        3. 우리 은행 고객 (UNION)

### Sub Query
- 하나의 Query안에 존재하는 Query
- 포함하고 있는 쿼리를 `Main QUery`, 포함된 쿼리를 `Sub Query`
- `INSERT`, `DELETE`, `UPDATE` 구문에 사용할 수 있고, `SELECT`구문에서도 사용 가능한데, `WHERE`,`HAVING`,`FROM`절에서 주로 사용한다.
- `SubQuery`는 `연산자의 오른쪽에 기술`해야 하고, `괄호`로 감싸야 합니다.
- Main Query가 수행되기 전, `한 번만 실행`된다.

#### 분류
1. FROM 절에 사용되면 `INLINE VIEW`
2. FROM 외의 경우, 두 가지로 나뉜다.
    1. `단일행 서브 쿼리`
        - 결과가 `하나의 값`인 `서브쿼리`
        - SELECT 구문의 `WHERE절에 사용`된다.
        - 예시, tCity 테이블에서 `popu가 최대`인 `name을 조회`
            ```sql
            SELECT MAX(popu),name
            FROM tCity;
            -- 원래 에러임 (표준 SQL)
            -- 근데 MySQL과 MariaDB는 첫 번쩨 값을 리턴하므로 에러가 안 뜨지만, 이상한 값임.
            ```
        - 예시를 서브쿼리로 해결
            ```sql
            SELECT name
            FROM city
            WHERE popu = (SELECT MAX(popu) FROM tCity);
            -- tCity에서 최대 popu를 찾고(subquery)
            -- popu 최대값과 같은 popu를 갖는 지역의 name을 리턴(main query)
            ```
        - 예시 2, EMP 테이블에서 SAL이 평균 이상인 데이터의 ENAME과 SAL을 조회
            ```sql
            SELECT ENAME,SAL
            FROM EMP
            WHERE SAL >= (SELECT AVG(SAL) FROM EMP);
            ```

    2. `다중 열 서브 쿼리`
        - `Sub Query`의 결과가 2개 이상의 `열`인 경우
        - 예시, tStaff 테이블에서 NAME이 안중근인 데이터와 동일한 DEPART와 GENDER를 갖는 데이터의 모든 열을 조회
            ```sql
            SELECT *
            FROM tStaff
            WHERE DEPART = (SELECT DEPART FROM tStaff WHERE NAME='안중근') AND GENDER = (SELECT GENDER FROM tStaff WHERE NAME = '안중근');
            ```
            ```sql
            SELECT *
            FROM tStaff
            WHERE (DEPART,GENDER) = (SELECT DEPART,GENDER FROM tStaff WHERE NAME='안중근');
            ```
    3. `다중 행 서브 쿼리`
        - 서브 쿼리의 결과 행이 2개 이상인 경우
        - 단일행 연산자 대신에 다중행 연산자를 사용
            - 단일행 연산자 : >,>=,<,<=,=,!=
            - 다중행 연산자 
                - `IN` : 포함, 목록 중 `하나와 일치`
                - `ANY`,`SOME` : 목록 중 `하나만 조건을 만족`해도 리턴
                    - 단일행 연산자와 함께 사용
                - `ALL` : 목록 `모두가 조건을 만족`해야 리턴
                    - 단일행 연산자와 함께 사용
                - `EXISTS` : `메인 쿼리의 비교 조건`이 `Sub Query의 결과 중에서 만족하는 값이 하나 이상`이면 True 리턴
                    - `데이터가 존재`하면 `TRUE`, `데이터가 존재하지 않으면` `FALSE` 반환
                    - `특정 쿼리의 수행 여부를 결정`할 때 사용
        - 예시) EMP 테이블에서 DEPTNO 별로 그룹화 한 후, 각 그룹의 SAL의 최대값과 일치하는 SAL을 가진 EMPNO,ENAME,SAL,DEPTNO를 조회
            ```sql
            SELECT EMPNO,ENAME,SAL,DEPTNO
            FROM EMP
            WHERE SAL IN (SELECT MAX(SAL) FROM EMP GROUP BY DEPTNO); --일치이므로 `IN`
            ```
        - 예시2, EMP 테이블에서 DEPTNO가 30인 부서의 모든 사원보다 SAL이 더 큰 데이터의 ENAME과 SAL을 조회
            ```sql  
            SELECT ENAME,SAL
            FROM EMP
            WHERE SAL > ALL(SELECT SAL FROM EMP WHERE DEPTNO = 30)
            -- 최대값을 사용하는 것으로 하면 ALL을 쓸 필요 없음
            SELECT ENAME,SAL
            FROM EMP
            WHERE SAL > (SELECT MAX(SAL) FROM EMP WHERE DEPTNO = 30)
            ```
        - 예시3, EMP 테이블에서 DEPTNO가 30인 부서의 최소 1명의 사원보다 SAL이 더 큰 데이터의 ENAME과 SAL을 조회
            ```sql
            SELECT ENAME, SAL
            FROM EMP
            WHERE SAL > ANY(SELECT SAL FROM EMP WHERE DEPTNO=30)
            -- 최소값을 사용하는 것으로 하면 ANY를 쓸 필요가 없음
            -- 최소값보다 크면 최소 1명의 사원보다 큰거
            SELECT ENAME,SAL
            FROM EMP
            WHERE SAL > (SELECT MIN(SAL) FROM EMP WHERE DEPTNO=30)
            ```
        - 예시4, EMP 테이블에서 SAL이 3000이 넘는 데이터가 있으면 EMP테이블 전체 데이터의 ENAME과 SAL을 조회
            ```sql
            SELECT ENAME,SAL
            FROM EMP
            WHERE EXISTS(SELECT SAL FROM EMP WHERE SAL > 3000)
            ```
        - 예시 5, EMP 테이블에서 MGR의 ENAME이 KING인 사원의 ENAME과 SAL을 조회 (MGR - 관리자의 EMPNO)
            ```sql
            SELECT ENAME,SAL
            FROM EMP
            WHERE MGR = (SELECT EMPNO FROM EMP WHERE ENAME='KING' )
            ```
### JOIN
- 2개 이상의 테이블을 합쳐서 하나의 테이블을 만드는 작업
    - 여기서 2개 이상의 테이블 -> 동일한 테이블 2개도 가능

- SUBQUERY와 JOIN 사용 상황 구별
    - SUBQUERY는 여러 테이블에 대해서 조회 불가
        - 하나에서 여러 개 할 때 사용하는 것
    - JOIN 은 여러 테이블에 대해 사용할 때 사용
    - SUBQUERY로 할 수 있는 경우 SUBQUERY로 
        - 정규화의 단점 : 너무 쪼개서 빈번한 JOIN으로 인한 성능 하락
#### 종류
1. CROSS JOIN : 2개 테이블의 `모든 조합`, Catesian Product라고도 함.
    - JOIN이 아니라고 하기도 함.
    - 양쪽 테이블의 모든 조합을 만들어 내는 것
    - 방식
        1. FROM 절에 `테이블 이름을 나열`
        2. JOIN 조건이 없기
    - 그래서 양쪽 테이블의 모든 컬럼이 다 나옴.
        - 모든 행이 다른 테이블의 모든 행과 결합
        - 이렇기에, `Column의 개수는 합계`가 되고, `행의 개수는 곱하기`가 된다.
    - 예시, EMP = 8 X 14 / DEPT = 3 X 4 
        ```sql
        SELECT *
        FROM EMP,DEPT
        -- CROSS JOIN(EMP,DEPT) = 11 X 56
        ```
        - 동일한 열도 다른 열로 취급하기 때문에 크게 좋지 못하다.
        - 사이즈가 좀만 커져도 죽어버릴 가능성이 존재함.
2. EQUI JOIN : JOIN을 할 때, = 연산자를 사용함.
    - 양쪽 테이블에 `동일한 의미를 갖는 컬럼을 기준으로 일치하는 데이터만 JOIN`에 참여
    - COLUMN의 이름은 일치하지 않아도 된다.
    - `양쪽 테이블의 Column이름이 동일`하다면, `테이블 이름까지 추가`해서 기재
    - EMP 테이블과 DEPT 테이블을 EQUI JOIN
        - CROSS JOIN에서 WHERE를 추가하는 것
        ```sql
        SELECT *
        FROM EMP,DEPT
        WHERE EMP.DEPTNO = DEPT.DEPTNO; 
        -- 열 이름이 같기 때문에 테이블.열로 표기하여 구분해준다. 
        -- 열 이름이 다르다면, 그냥 열 이름만 적어도 된다.
        ```
    - 사용하는 경우
        - 예시, EMP 테이블의 ENMAE이 `MILLER`인 사원의 ENAME과 DEPT 테이블의 DNMAE을 조회
            ```sql
            SELECT ENAME,DNAME
            FROM EMP,DEPT
            WHERE EMP.DEPTNO = DEPT.DEPTNO AND EMP.ENAME = 'MILLER';
            -- MILLER의 DEPT가 궁금하다 가정하에 Subquery
            SELECT DNAME
            FROM DEPT
            WHERE DEPTNO = (SELECT DEPTNO FROM EMP WHERE ENAME='MILLER')
            ```
        - 예시2, DEPT 테이블의 LOC가 DALLAS인 사원의 EMP 테이블의 ENAME을 조회
            ```sql
            -- JOIN
            SELECT ENAME
            FROM DEPT,EMP
            WHERE EMP.DEPTNO=DEPT.DEPTNO AND DEPT.LOC='DALLAS';
            -- SUB QUERY -> 이렇게 SUB QUERY 가 가능하면 SUBQUERY하기
            SELECT ENAME
            FROM EMP
            WHERE DEPTNO = (SELECT DEPTNO FROM DEPT WHERE DEPT.LOC = 'DALLAS')
            ```
3. NON EQUI JOIN : JOIN을 할 때, = 이외의 연산자를 사용한다.
    - 사용하는 상황
        - 같은게 아니라 어떤 범위안에 오는 데이터를 찾아야 하는 경우
            - ex, LOSAL과 HISAL,GRADE를 가지는 salgrade로 EMP 테이블 사람들의 GRADE를 확인하기
                ```sql
                SELECT ENAME, SAL, GRADE
                FROM EMP, SALGRADE
                WHERE SAL BETWEEN LOSAL AND HISAL;
                ```
4. OUTER JOIN : 한쪽에만 존재하는 데이터도 JOIN에 참여
- 한쪽 테이블에만 존재하는 데이터도 JOIN에 참여하는 것
- 종류
    1. LEFT OUTER JOIN
    2. RIGHT OUTER JOIN
    3. FULL OUTER JOIN (MariaDB에서 지원 X)
- 예시, EMP 테이블에서 DEPTNO와 DEPT 테이블에서 DEPTNO 조회
    - 일반적, EQUI JOIN
        ```sql
        SELECT *
        FROM EMP,DEPT
        WHERE EMP.DEPTNO = DEPT.DEPTNO;
        -- 이렇게 하면, EMP 에는 DEPTNO 40이 없으므로, DEPT 테이블의 DEPT 40 값은 빠지게 된다.
        ```
    - OUTTER JOIN
        - 왼쪽 테이블 데이터 전체를 JOIN에 참여시키기
            ```sql
            SELECT *
            FROM EMP LEFT OUTER JOIN DEPT
            ON EMP.DEPTNO = DEPT.DEPTNO;
            ```
        - 오른쪽 테이블 데이터 전체를 JOIN에 참여시키기
            ```sql
            SELECT *
            FROM EMP RIGHT OUTER JOIN DEPT
            ON EMP.DEPTNO = DEPT.DEPTNO;
            ```
        - 양쪽 테이블 데이터 전체를 JOIN에 참여시키기 (FULL OUTER JOIN)
            ```sql
            SELECT *
            FROM EMP LEFT OUTER JOIN DEPT
            ON EMP.DEPTNO = DEPT.DEPTNO
            UNION
            SELECT *
            FROM EMP RIGHT OUTER JOIN DEPT
            ON EMP.DEPTNO = DEPT.DEPTNO;
            ```
5. SELF JOIN : 동일한 테이블을 갖고 JOIN
    - 사용하는 상황
        - 하나의 테이블에 동일한 의미를 갖는 컬럼이 2개 이상 존재할 때 가능한 JOIN
            - ex, EMP 테이블에는 EMPNO와 MGR 컬럼 존재, EMPNO(사원 번호), MGR(관리자 번호), 이때 사원 이름과 관리자 사원 이름을 같이 조회하고자 하는 경우, 이 테이블을 2번 참조해야 한다.
                - 사원 이름 -> 관리자 번호 -> 관리자 번호와 같은 사원 번호의 사원 이름 => 총 2번
                ```sql
                -- 이렇게 self join을 쓰면 한 번에 확인 가능
                SELECT e1.ename, e2.ename
                FROM EMP e1, EMP e2;
                WHERE e1.mgr = d2.empno;
                ```
            - KING이 매니저인 사원의 ENAME과 JOB
                ```sql
                -- SUB QUERY
                SELECT ENAME,JOB
                FROM EMP
                WHERE MGR = (SELECT EMPNO FROM EMP WHERE ENAME = 'KING')
                -- SELF JOIN
                SELECT e1.ename,JOB
                FROM EMP e1, EMP e2
                WHERE e1.mgr = e2.empno AND e2.name = 'KING';
                ```
6. ANSI JOIN : 미국 표준 협회에서 제안한 JOIN 방식
    - 기존의 JOIN을 다른 문법으로 지원
    - COLUMN이름이 같은 경우 JOIN ON 대신, JOIN USING(컬럼이름)으로 대체 가능하다.
    1. ANSI CROSS JOIN
        - 기존의 Cartesian Product를 CROSS JOIN 예약어로 수행
            - 기존 :EMP 테이블과 DEPT 테이블의 CROSS JOIN
                ```sql
                SELECT *
                FROM EMP,DEPT
                ```
            - ANSI 방식 : 먕ㅅ;힘
                ```sql
                SELECT *
                FROM EMP CROSS JOIN DEPT;
                ```
    2. ANSI INNER JOIN
        - EQUI JOIN을 ANSI로 사용하는 문법
        - 기존 : 
            ```sql
            SELECT *
            FROM EMP,DEPT
            WHERE EMP.DEPTNO = DEPT.DEPTNO;
            ```
        - ANSI : 
            ```sql
            SELECT *
            FROM EMP INNER JOIN DEPT 
            ON EMP.DEPTNO = DEPT.DEPTNO;
            --- 컬럼 이름이 같으므로 아래도 가능하다.
            SELECT *
            FROM EMP INNER JOIN DEPT 
            USING (DEPTNO);
            --- JOIN 마저 쓰기 귀찮다면
            SELECT *
            FROM EMP NATURAL JOIN DEPT;
            ```

7. 다중 조인 : JOIN을 두 번 이상 수행
    - JOIN의 결과도 하나의 테이블이므로 연속해서 JOIN가능    
    - 예시
        ```sql
        SELECT * FROM CCAR C INNER JOIN TMARKER M ON C.MAKER = M.MAKER IINNER JOIN tCity T ON M.factory = T.name;
        ```
8. SEMI JOIN : 서브 쿼리를 이용해서 JOIN
#### 테이블에 다른 이름 부여
- FROM 에서 테이블 이름 뒤에 별명을 표기할 수 있따.
    - 다만, 이때 별명을 설정한 경우, 별명대신 테이블 이름으로 호출하면 Error가 난다.
- SELF JOIN에서 필수인 기능이다.
    - 같은 테이블은 구분하려면 무조건 필요하니까
```sql
SELECT ENAME,DNAME
FROM EMP e, DEPT d
WHERE e.DEPTNO = d.DEPTNO AND ENAME='MILLER';
```
## DML
> 데이터 조작 언어
### 종류
1. SELECT - 최근엔 DML 대신 DQL로 분리하는 경우도 존재
2. INSERT
3. DELETE
4. UPDATE
- 2~4는 TRANSACTION과 연관있음
### 데이터 삽입
```sql
-- 기본
INSERT INTO 테이블이름(삽입할 필드 목록) VALUES (값 나열);
-- 삽입할 필드가 전체인 경우
INSERT INTO 테이블이름 VALUES (값 나열);
-- 여러개 입력
INSERT INTO 테이블이름(삽입할 필드 목록) VALUES (값 나열),(값 나열),(값 나열),(값 나열),...,(값 나열);
```
- 필드 목록을 생략하면 모든 값을 순서대로 대입
- AUTO_INCREMENT가 설정된 컬럼
    - 값을 생략하면 일련 번호
- DEFAULT가 설정된 컬럼
    - 값을 생략하면 기본값
- 그 외의 컬럼
    - 값을 생략하면 NULL
- 예시, tCity 테이블은 name, area, popu, metro, region으로 구성된 테이블
    ```sql
    INSERT INTO tCity(name,area,popu,metro,region) VALUES('길원',1,1,'지하철','인천')
    -- 모든 값을 다 넣는 것이므로 아래처럼 표현 가능
    INSERT INTO tCity VALUES('원길',2,2,'하철지','천인')
    --- 여러 개를 한
    ```
#### SELECT 구문의 결과를 가지고 삽입
- VALUES 대신에 SELECT 구문을 사용하면 된다.
    ```sql
    INSERT INTO 테이블이름(삽입할 필드 목록) SELECT (삽입할 값 나열) FROM 테이블이름;
    ```
- 예시, tCity의 값을 이용하여 tStaff에 삽입
    ```sql
    INSERT INTO tStaff SELECT name,region,metro,'20251229','신입',area,popu FROM tCity WHERE region='경기';
    ```

### SELECT를 이용해서 테이블 생성
```sql
CREATE TABLE 테이블이름 AS SELECT 구문;
```
- 예시, DEPT의 모든 데이터를 공유하는 DEPT_COPY 테이블 생성
    ```sql
    CREATE TABLE DEPT_COPY 
    SELECT *
    FROM DEPT;
    ```
- 예시2, tStaff의 salary가 300이상인 데이터를 공유하는 300Staff테이블 생성
    ```sql
    CREATE TABLE 100Staff
    SELECT *
    FROM tStaff
    WHERE salary >= 300;
    ```
- 예시3, 테이블의 구조만 필요한 경우 (WHERE를 이용해 어떠한 tuple도 매칭되지 않도록 함)
    ```sql
    CREATE TABLE emptyStaff
    SELECT *
    FROM tStaff
    WHERE NULL; -- NULL은 항상 거짓
    ```

### DELETE
> 데이터 삭제
```sql
DELETE FROM 테이블이름 [WHERE 조건];
```
- WHERE절이 없으면, TABLE의 모든 데이터 삭제 
- WHERE가 있으면 해당되는 TUPLE만 삭제
- 예시, DEPT02 테이블에서 DEPTNO가 10인 데이터 삭제
    ```sql
    DELETE FROM DEPT02 WHERE DEPTNO=10;
    ```
- 예시, DEPT02 테이블의 모든 데이터 삭제
    ```sql
    DELETE FROM DEPT02
    ```

### UPDATE
```sql
UPDATE 테이블 이름
SET 수정할 내용
[WHERE 조건];
```
- WHERE절이 없으면, TABLE의 모든 데이터 수정 
- WHERE가 있으면 해당되는 TUPLE만 수정
- 예시, 300Staff에서 영업부를 영업 지원부로 이름 변경
    ```sql
    UPDATE 300Staff
    SET depart = '영업지원부'
    WHERE depart='영업부';
    ```

### IGNORE
- 여러 삽입 구문을 스크립트로 만들어서 삽입하는 경우, `IGNORE를 사용`하면, `중간에 오류가 발생`하더라도 계속 `삽입이 가능`하다.
- NO IGNORE 예시, DEPT와 동일 구조인 빈테이블 DEPT02에 데이터 3개 삽입
    ```sql
    -- 에러가 발생하여 첫 번쨰 값만 들어가는 코드
    INSERT INTO DEPT02 VALUES(10,'영업부','서울');
    INSERT INTO DEPT02 VALUES(20,'에러부','인천시서구완정로65번안길104동905호'); -- 최대 길이를 넘는 값
    INSERT INTO DEPT02 VALUES(30,'개발부','경기');
    ```
    - 기본적으로 삽입은 싱글스레드 기반 (순차적 처리) -> 오류가 나면 멈춰버림
- IGNORE 예시, DEPT와 동일 구조인 빈테이블 DEPT02에 데이터 3개 삽입
    ```sql
    -- 에러가 발생하여 첫 번쨰 값만 들어가는 코드
    INSERT IGNORE INTO DEPT02 VALUES(10,'영업부','서울');
    INSERT IGNORE INTO DEPT02 VALUES(20,'에러부','인천시서구완정로11번안길111동1201호'); -- 최대 길이를 넘는 값
    INSERT IGNORE INTO DEPT02 VALUES(30,'개발부','경기');
    ```
    - 결과를 보면, 자기가 넣을 수 있는 11번안길까지만 넣고 뒤에는 잘라버림
        - IGNORE를 사용하면 에러를 막을 수는 있지만, 예상하지 못한 결과를 얻을 수 있어서 조심해야 한다.

## TCL

### Transaction
> 데이터 베이스 작업의 논리적 단위
> - 물리적 단위 : Block / Page 
- Transaction의 단위를 잘 정하는 것이 DB 잘 다루는 것
- Transaction의 도입 배경
    - 데이터의 일관성을 유지하기 위함
- Transaction의 성질 (ACID) 
    1. `Atomicity`(원자성) : ALL OR NOTHING
        - 전부 되던지, 하나도 되지 말아라.
    2. `Consistency`(일관성) : Transaction 수행 전과 수행 후가 일관성이 있어야 한다.
    3. `Isolation`(격리성) : 다른 Transaction과 격리되어야 한다.
    4. `Durability`(영속성) : 한 번 완료된 Transaction은 영원히 반영되어야 한다.

### 임시 작업 영역
- 데이터베이스에서의 작업은 `임시 작업 영역`을 통해서 이루어진다.
- `임시 작업 영역`때문에 `Transaction의 일관성`이 이루어진다.

### 관련 명령어
- `COMMIT` : 작업 완료
- `ROLLBACK` : 작업 취소
- `SAVEPOINT` : 중간 저장점

### COMMIT과 ROLLBACK되는 상황
#### COMMIT 되는 상황
- 명시적으로 COMMIT을 수행
- DDL이나 DCL 수행을 한 경우
- 접속도구가 정상적으로 종료된 경우

#### ROLLBACK된 상황
- 명시적으로 ROLLBACK을 수행
- 접속 도구의 비정상적 종료

### Trnasaction의 모드
1. 자동 : SQL 문장을 수행하면 자동으로 COMMIT되는 것
2. 수동 : 명시적으로 COMMIT을 수행해야만 COMMIT


### 적절한 COMMIT 시간
- COMMIT 너무 자주
    - 내가 작업할 시간이 너무 적다
- COMMIT 너무 뜸하게
    - ROLLBACK시, 리스크가 너무 크다.
- 즉, SAVEPOINT를 중간중간 심어서 ROLLBACK시, 어디로 갈지 내가 선택하는 것이다.

### 예시 연습
- 예시 1, ROLLBACK
    ```sql
    INSERT INTO DEPT_COPY VALUES(50,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 추가된거 확인됨.
    ROLLBACK; -- 마지막 작업 취소
    SELECT * FROM DEPT_COPY; -- 추가된게 사라짐
    ```
- 예시 2, COMMIT 을 먼저 하고 ROLLBACK
    ```sql
    INSERT INTO DEPT_COPY VALUES(50,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 추가된거 확인됨.
    COMMIT; -- 작업 저장
    ROLLBACK; -- 마지막 작업 취소
    SELECT * FROM DEPT_COPY; -- 추가된게 사라지지 않음(커밋했기 때문)
    ```
- 예시 3, 데이터 삽입 후, DDL 수행 -> ROLLBACK
    - DDL,DCL,정상 종료된 경우에는 AUTO COMMIT 된다.
        - DDL,DCL은 DBA에서 보통 진행하기 때문에 정상 커밋으로 자동 처리한다.
    ```sql
    INSERT INTO DEPT_COPY VALUES(60,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 추가된거 확인됨.
    TRUNCATE TABLE DEPT02; -- DDL 문장 실행
    ROLLBACK; -- 마지막 작업 취소
    SELECT * FROM DEPT_COPY; -- 추가된게 사라지지 않음(커밋했기 때문)
    ```
- 예시 4, SAVEPOINT 사용
    ```sql
    INSERT INTO DEPT_COPY VALUES(70,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 추가된거 확인됨.
    SAVEPOINT S1; -- S1 지점
    INSERT INTO DEPT_COPY VALUES(80,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 추가된거 확인됨.
    SAVEPOINT S2; -- S2 지점
    ROLLBACK TO S1; -- ROLLBACK , TO S1을 지우면 70,80 둘 다 안한걸로된다.
    SELECT * FROM DEPT_COPY;
    ```