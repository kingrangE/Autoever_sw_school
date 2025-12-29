# 12월 29일

## SET OPERATOR
- `2개 이상의 테이블`에서 `데이터를 추출하는 방법` 중 하나
- 여러 개의 `SELECT 문장을 결합`해서 결과를 얻어내는 연산
### 기본 형식
```sql
SELECT 문

SET Operator

SELECT 문
```

### 가이드라인
1. `SELECT 구문`들은 앞에서부터 `순서대로 매칭`되므로, `열의 개수`와 `자료형`이 일치해야 한다.
2. 테이블은 동일할 수도 있으나, 대부분 동일하지 않다.
3. 출력되는 COLUMN의 첫 번째 이름은 첫 번째 SELECT 구문의 것
4. ORDER BY는 마지막에 1번만 기술 가능
5. BLOB,CLOB,BFILE,LONG형 컬럼에는 사용 불가
    - 위 4개의 COLUMN은 `파일 내용을 저장`하는 컬럼
    - 파일 내용을 하나하나 비교하여 검사하는 것은 EVA다.

### 연산자
1. `UNION` : `합집합` - 중복 X
2. `UNION ALL` : `합집합` - 중복 O
3. `INTERSECT` : `교집합` 
4. `EXCEPT` : `차집합`(앞 테이블-뒷 테이블)

### 실습
- EMP 테이블, DEPT 테이블의 DEPTNO 확인
    ```sql
    SELECT DEPTNO
    FROM EMP;

    SELECT DEPTNO
    FROM DEPT;
    ```
    - 합집합 (중복 X)
        ```sql
        SELECT DEPTNO
        FROM EMP
        UNION
        SELECT DEPTNO
        FROM DEPT;
        ```
    - 합집합 (중복 O)
        ```sql
        SELECT DEPTNO
        FROM EMP
        
        UNION ALL

        SELECT DEPTNO
        FROM DEPT;
        ```
    - 교집합
        ```sql
        SELECT DEPTNO
        FROM EMP
        INTERSECT
        SELECT DEPTNO
        FROM DEPT;
        ```
    - 차집합 (EMP-DEPT)
        ```sql
        SELECT DEPTNO
        FROM EMP
        EXCEPT
        SELECT DEPTNO
        FROM DEPT;
        ```

### 사용 상항
- 테이블의 성격 상의 이유로 나누어져 있을 때, 확인하기 위함.
    - EX, 대출과 저축 테이블 구분되어 있을 때, 아래를 확인
        1. 대출과 저축을 같이 한 사람(INTERSECT)
        2. 대출만 한 사람 (EXCEPT)
        3. 우리 은행 고객 (UNION)

## Sub Query
- 하나의 Query 내에 존재하는 Query
- 포함하는 쿼리 : `Main Query` / 포함된 쿼리 : `Sub Query`
- `INSERT`,`DELETE`,`UPDATE` 구문에 사용 가능
    - `SELECT` 구문에서도 사용 가능한데, 이때는 아래의 절에서 주로 사용
        1. `WHERE`
        2. `HAVING`
        3. `FROM`
- `SubQuery`는 
    - `연산자의 오른쪽`에 기술하고, **`괄호`로 감싸야 한다.**
    - `MainQuery`가 수행되기 전, 한 번만 실행된다.
### 분류
#### INLINE VIEW
> FROM 절에 사용되는 `Sub Query`
#### 단일행 서브 쿼리
> `Sub Query`의 `결과 행이 하나`인 경우
- `SELECT 구문`의 `WHERE절에 사용`된다.
- 예시, tCity 테이블에서 `popu가 최대`인 `name을 조회`
    ```sql
    SELECT name
    FROM tCity
    WHERE popu = (SELECT max(popu) FROM tCity);
    -- tCity에서 최대 popu를 찾고(subquery)
    -- popu 최대값과 같은 popu를 갖는 지역의 name을 리턴(main query)
    ```
- 예시 2, EMP 테이블에 `SAL`이 평균이상인 데이터의 `SAL`과 `ENAME` 조회
    ```sql
    SELECT ENAME,SAL
    FROM EMP
    WHERE SAL >= (SELECT AVG(SAL) FROM EMP);
    ```

#### 다중행 서브 쿼리
> `Sub Query`의 `결과 행이 2개 이상`인 경우
- 단일행 연산자 대신에 다중행 연산자를 사용한다.
    - 단일행 연산자 : >,>=,<,<=,=,!= 등
    - 다중행 연산자 
        - IN : `Sub Query` 결과 중 `하나와 일치`
        - ANY,SOME : `Sub Query` 결과 중 `하나만 조건 만족`해도 리턴
        - ALL : `Sub Query` 결과 `모두가 조건을 만족`해야 리턴
        - EXIST : `Sub Query의 결과` 데이터가 존재하면 True, 없으면 False리턴
            - `특정 쿼리의 수행 여부를 결정`할 때 주로 사용

- 예시, EMP 테이블에서 DEPTNO 별로 그룹화한 후, 각 그룹의 SAL의 최대값과 일치하는 SAL을 가진 EMPNO, ENAME,SAL,DEPTNO 조회
    ```sql
    SELECT EMPNO,ENAME,SAL,DEPTNO
    FROM EMP
    WHERE SAL IN (SELECT MAX(SAL) FROM EMP GROUP BY DEPTNO);
    -- 결과 중 하나와 일치이므로 IN
    -- 만약 =을 쓰면 subquery returns more than 1 rows 뭐 이런 메시지가 나온다. =은 단일 행 비교만 가능하다는 것이다.
    ```
- 예시2, EMP 테이블에서 DEPTNO가 30인 부서의 모든 사원보다 SAL이 더 큰 데이터의 ENAME과 SAL을 조회
    ```sql
    -- 단일행으로 해결하는 경우 (최대값 사용)
    SELECT ENAME, SAL
    FROM EMP
    WHERE SAL > (SELECT MAX(SAL) FROM EMP WHERE DEPTNO = 30);
    -- 다중행으로 해결하는 경우
    SELECT ENAME,SAL
    FROM EMP
    WHERE SAL > ALL(SELECT SAL FROM EMP WHERE DEPTNO = 30);
    ```

- 예시3, EMP 테이블에서 DEPTNO가 30인 부서의 최소 1명의 사원보다 SAL이 더 큰 데이터의 ENAME과 SAL을 조회
    ```sql
    -- 단일행으로 해결하는 경우 (최소값 사용)
    SELECT ENAME,SAL
    FROM EMP
    WHERE SAL > (SELECT MIN(SAL) FROM EMP WHERE DEPTNO = 30);
    -- 다중행으로 해결하는 경우 
    SELECT ENAME,SAL
    FROM EMP
    WHERE SAL > ANY(SELECT SAL FROM EMP WHERE DEPTNO = 30);
    ```
- 예시4, EMP 테이블에서 SAL이 3000이 넘는 데이터가 있으면 EMP테이블 전체 데이터의 ENAME과 SAL을 조회
    ```sql
    SELECT ENAME, SAL
    FROM EMP
    WHERE EXISTS(SELECT SAL FROM EMP WHERE SAL > 3000);
    ```
- 예시5, EMP테이블에서 MGR의 ENAME이 KING인 사원의 ENAME과 SAL을 조회
    ```sql
    SELECT ENAME,SAL
    FROM EMP
    WHERE MGR = (SELECT EMPNO FROM EMP WHERE ENAME ='KING');
    ```

- 예시 5, EMP 테이블에서 MGR의 ENAME이 KING인 사원의 ENAME과 SAL을 조회 (MGR - 관리자의 EMPNO)


#### 다중열 서브 쿼리
> `Sub Query`의 `결과가 2개 이상`의 `열`인 경우
- 예시, tStaff 테이블에서 NAME이 안중근인 데이터와 동일한 DEPART와 GENDER를 갖는 데이터의 모든 열을 조회
    ```sql
    SELECT *
    FROM tStaff
    WHERE DEPART = (SELECT DEPART FROM tStaff WHERE NAME='안중근');
    ```

## JOIN
### 종류
#### CROSS JOIN
> ANSI 표기법 : `A CROSS JOIN B`
- Cetasian Product 라고도 불린다.
- 2개 테이블의 모든 조합을 의미한다.
- 방식
    > FROM 절에 `테이블 이름 나열`
- CROSS JOIN은 따로 조건이 없기 때문에 모든 조합이 나열된다. 
    - 즉 테이블들의 모든 행이 결합되어 결과가 다음과 같다.
        - n x m 테이블과 N x M 테이블 CROSS JOIN => `행의 개수 n*N / 열의 개수 m + M`
- 예시, EMP 테이블(14 x 8)/DEPT 테이블 (4x3) CROSS JOIN
    ```sql
    SELECT *
    FROM EMP,DEPT
    -- 결과 56 X 11
    SELECT *
    FROM EMP CROSS JOIN DEPT
    ```
- 동일한 열도 다른 열로 취급하기 때문에 효율이 좋지 못하다. (사이즈가 조금만 커져도 죽어버릴 가능성이 높음)
#### EQUI JOIN
> ANSI 표기법 : `A JOIN B ON`
- `CROSS JOIN` + `= 연산`
- 양쪽 테이블에 `동일한 의미를 갖는 Column을 기준으로 일치하는 데이터만 JOIN`에 참여
- Column의 이름은 일치하지 않아도 된다.
- `양쪽 테이블의 Column이름이 동일`하다면, `테이블 이름까지 추가`해서 기재하기 
    - `테이블 이름.Column이름`
- 예시, EMP 테이블과 DEPT 테이블을 EQUI JOIN(DEPT NUM이 같은 행끼리)
    ```sql
    SELECT *
    FROM EMP,DEPT
    WHERE EMP.DEPTNO=DEPT.DEPTNO;
    -- ANSI
    SELECT *
    FROM EMP JOIN DEPT
    ON EMP.DEPTNO=DEPT.DEPTNO;
    ```

- 예시2, EMP 테이블의 ENAME이 'MILLER'인 사원의 DNAME 구하기
    ```sql
    --- EQUI JOIN으로 해결하는 예시
    SELECT ENAME,DNAME
    FROM EMP,DEPT
    WHERE EMP.DEPTNO = DEPT.DEPTNO AND ENAME = 'MILLER'
    --- Sub Query로 해결하는 예시
    SELECT DNAME AS "Miller씨의 부서"
    FROM DEPT
    WHERE DEPTNO = (SELECT DEPTNO FROM EMP WHERE ENAME = 'MILLER')
    -- ANSI
    SELECT ENAME,DNAME
    FROM EMP JOIN DEPT
    ON EMP.DEPTNO = DEPT.DEPTNO AND ENAME = 'MILLER'
    ```
- 예시 3, LOC(DEPT)가 DALLAS인 사원의 ENAME(EMP) 조회
    ```sql
    --- EQUI JOIN으로 해결하는 예시
    SELECT ENAME
    FROM EMP,DEPT
    WHERE EMP.DEPTNO = DEPT.DEPTNO AND LOC = 'DALLAS'
    --- Sub Query로 해결하는 예시
    SELECT ENAME
    FROM EMP
    WHERE DEPTNO = (SELECT DEPTNO FROM DEPT WHERE LOC='DALLAS')
    ```

#### NON EQUI JOIN
- CROSS JOIN + `= 이외의 연산`
- 사용하는 상황
    - EX, EMP 테이블의 SAL을 기반으로 SALGRADE를 조회하라
        ```sql
        SELECT ENAME,SAL,GRADE
        FROM EMP,SALGRADE
        WHERE EMP.SAL BETWEEN LOSAL AND HISAL;
        --- ANSI
        SELECT ENAME,SAL,GRADE
        FROM EMP join SALGRADE
        on EMP.SAL BETWEEN LOSAL AND HISAL;
        ```
#### SELF JOIN
- 동일한 테이블을 갖고 JOIN할 때 사용
- 사용하는 상황
    - 하나의 테이블에 `동일한 의미`를 갖는 Column이 2개 이상 존재
    - ex, 직원과 그를 관리하는 관리자 이름을 같이 조회하라.
        ```sql
        SELECT e1.ENAME e2.ENAME
        FROM EMP e1, EMP e2
        WHERE e1.MGR = e2.EMPNO; 
        ```
    - ex2, KING이 매니저인 사람의 ENAME과 JOB을 조회하라.
        ```sql
        -- SELF JOIN 사용
        SELECT e1.ENAME,e1.JOB
        FROM EMP e1, EMP e2
        WHERE e1.MGR = e2.EMPNO AND e2.ENAME = "KING";
        -- SELF JOIN 사용 X
        SELECT ENAME,JOB
        FROM EMP
        WHERE EMP.MGR = (SELECT EMPNO FROM EMP WHERE ENAME='KING')
        ```
#### OUTTER JOIN
> ANSI : 
> - LEFT : `A LEFT OUTER JOIN B ON `
> - RIGHT : `A RIGHT OUTER JOIN B ON `
> - FULL : `A LEFT OUTER JOIN B ON ~~ UNION A RIGHT OUTER JOIN B ON ~~~`
- 한쪽에만 존재하는 데이터도 JOIN에 참여시킴
- 종류
    1. `LEFT OUTER JOIN` : 왼쪽 테이블에만 존재하는 데이터도 참여
        - 오른쪽에 대응되는 데이터가 없다면 오른쪽 테이블 Column NULL표시
    2. `RIGHT OUTER JOIN` : LEFT OUTER JOIN의 오른쪽 버전
    3. `FULL OUTER JOIN` : LEFT OUTER + RIGHT OUTER
        - 이 자체의 기능은 MariaDB에서 지원하지 않는다. (Union을 사용하여 구현)
- 예시, EMP 테이블과 DEPT 테이블 JOIN하는 경우
    - 기본
        ```sql
        SELECT *
        FROM EMP,DEPT
        WHERE EMP.DEPTNO = DEPT.DEPTNO;
        -- DEPT에만 있는 40값이 생략됨
        ```
    - DEPT에 있는 40값을 같이 출력하기 위해 오른쪽 테이블 전체값을 이용하도록 함.
        ```sql
        SELECT *
        FROM EMP RIGHT OUTER JOIN DEPT
        ON EMP.DEPTNO = DEPT.DEPTNO;
        ```

#### MULTIPLE JOIN
- JOIN의 결과를 이용하여 다시 JOIN하는 방식 (연속 JOIN)
- 예시
    ```sql
    SELECT s.name, c.course_name
    FROM Students s
    JOIN Enrollments e ON s.student_id = e.student_id
    JOIN Courses c ON e.course_id = c.course_id;
    ```

#### SEMI JOIN
- 일반적 JOIN이랑 다르다. `상대 테이블에 조건에 맞는 데이터가 존재하는지`만 확인 -> `한쪽 테이블`의 컬럼만 보여주는 방식
    - 즉, 저 쪽에 내 데이터와 `짝이 되는게 있는지`만 확인
        - 따라서, 대응되는 행이 여러 개라 하더라도 단 1번만 출력
- 예시, 주문 내역이 한 개라도 있는 고객 
    ```sql
    SELECT * FROM Customers c
    WHERE EXISTS (
        SELECT 1 FROM Orders o 
        WHERE o.customer_id = c.customer_id
    );
    ``` 
#### NATURAL JOIN
- 두 테이블에서 `이름`과 `자료형`이 모두 같은 컬럼을 자동적으로 찾아 `JOIN` .(자동이므로 `ON` 사용 X)
    - 원하지 않는 결과를 초래할 수 있어서 권장하지 않음


## DML
> 데이터 조작 언어
### 종류
#### SELECT
> 데이터 조회
- 최근에는 DML대신 DQL로 분리하는 경우도 존재한다.
    - Q) DQL?
    - A) Data Query Language, 데이터를 조회(검색)하는데 사용되는 명령어

- SELECT를 이용해서 테이블 생성
    ```sql
    CREATE TABLE 테이블이름 SELECT 구문
    ```
- 예시1, DEPT의 모든 데이터를 복사한 DEPT_COPY 테이블 생성
    ```sql
    CREATE TABLE DEPT_COPY 
    SELECT * 
    FROM DEPT;
    ```
- 예시2, tStaff의 salary가 340이상인 데이터를 복사한 340OVerStaff 테이블 생성
    ```sql
    CREATE TABLE 340OverStaff
    SELECT *
    FROM tStaff
    WHERE salary >= 340;
    ```
- 예시3, 테이블의 구조만 필요한 경우 
    ```sql
    CREATE TABLE staffStructure
    SELECT *
    FROM tStaff
    WHERE NULL; -- NULL을 하면 모든 데이터에 대해 항상 거짓이므로 아무런 데이터도 조회되지 않는다. 즉, 구조만 복사된다.
    ```

#### INSERT
> 데이터 삽입
```sql
-- 기본 형태
INSERT INTO 테이블이름(삽입할 필드 나열) VALUES (삽입할 값 나열);
-- 삽입할 필드가 전체인 경우
INSERT INTO 테이블이름 VALUES (삽입할 값 나열);
-- 여러 값을 한 번에 넣는 경우
INSERT INTO 테이블이름(삽입할 필드 나열) VALUES (삽입할 값 나열),(삽입할 값 나열),(삽입할 값 나열);
-- SELECT를 이용하여 값을 삽입하는 경우
INSERT INTO 테이블이름(삽입할 필드 나열) SELECT (삽입할 값 나열) FROM 값을 가져올 테이블 [WHERE 조건];
```
- 값을 생략한 경우 처리 방식
    1. AUTO_INCREMENT가 설정된 컬럼 : `일련 번호`
    2. DEFAULT가 설정된 컬럼 : `기본 값`
    3. 그 외 : `NULL`
- 예시, tCity 테이블은 name, area, popu, metro, region으로 구성된 테이블
    ```sql
    INSERT INTO tCity(name,area,popu,metro, region) VALUES('길원',1,1,'y','NN');
    INSERT INTO tCity VALUES('원길',2,2,'n','YY');
    ```
- 예시, tCity에 있는 값을 이용하여 tStaff에 삽입
    ```sql
    INSERT INTO tStaff SELECT (name,region,metro,'20251229','신입',area,popu) FROM tCity WHERE region='경기';
    ```

- **IGNORE INSERT**
    - 여러 삽입 구문을 실행하는 경우, `IGNORE`를 사용하면 해당 구문에서 오류가 나더라도 `삽입`이 가능하다.
        - NO IGNORE
            ```sql
            INSERT INTO DEPT02 VALUES(10,'영업부','서울');
            INSERT IGNORE INTO DEPT02 VALUES(20,'에러부','인천시서구완정로11번안길111동1201호'); -- 최대 길이를 넘는 값
            INSERT INTO DEPT02 VALUES(30,'개발부','경기');
            ```
            - 기본적으로 `삽입`은 `싱글스레드 기반 작업`(순차적 처리) 이다.
                - 오류가 나면 멈춤.
        - IGNORE
            ```sql
            INSERT IGNORE INTO DEPT02 VALUES(10,'영업부','서울');
            INSERT IGNORE INTO DEPT02 VALUES(20,'에러부','인천시서구완정로11번안길111동1201호'); -- 최대 길이를 넘는 값
            INSERT IGNORE INTO DEPT02 VALUES(30,'개발부','경기');
            ```
            - 결과를 보면, 자기가 넣을 수 있는 11번안길까지만 넣고 뒤에는 잘라버림
            - `IGNORE를 사용`하면 `에러를 무시하고 실행`할 수 있지만, `예상하지 못한 결과`를 얻을 수 있어서 조심해야 한다.

#### DELETE

> 데이터 삭제 (테이블 구조는 남김)
```sql
DELETE FROM 테이블이름 [WHERE 조건];
```
- WHERE절이 없으면, `TABLE의 모든 데이터 삭제` 
- WHERE가 있으면 `해당되는 Tuple만 삭제`
- 예시, DEPT02 테이블에서 DEPTNO가 10인 데이터 삭제
    ```sql
    DELETE FROM DEPT02 WHERE DEPTNO=10;
    ```
- 예시2, DEPT02 테이블의 모든 데이터 삭제 (구조만 남김)
    ```sql
    DELETE FROM DEPT02;
    ```
#### UPDATE
```sql
UPDATE 테이블 이름
SET 수정할 내용
[WHERE 조건];
```
- WHERE절이 없으면, `TABLE의 모든 데이터 수정`
- WHERE절이 있으면, `해당되는 Tuple만 삭제`
- 예시, 300Staff에서 영업부를 영업 지원부로 이름 변경
    ```sql
    UPDATE 300Staff
    SET depart = '영업 지원부'
    WHERE depart = '영업부';
    ```
## TCL

### Transaction
> 데이터 베이스 작업의 논리적 단위
> > \*물리적 단위 : Block / Page (실제 데이터를 저장하는 부분)

#### 도입 배경
> `데이터의 일관성을 유지`하기 위함
#### Transaction의 성질 (ACID)
1. Atomicity(원자성) : ALL OR NOTHING
    - 전부 되던지, 하나도 되지 말아라.
    - EX) A,B가 중고거래 함. T-1에서 A 돈 -10만원, T-2에서  B돈 +10만원 해야하는데 T-1하고 서비스가 뻗어버리면 A만 돈을 잃는다. 이를 막기 위해 원자성이 필요함. 
        - T-1, T-2 모두가 실행되지 못한다면 모두 다 하지 않은 것으로 처리하는 것이 `원자성`
2. Consistency(일관성) : Transaction이 완료된 후에도 DB는 `미리 정해진 규칙(제약 조건)`을 `반드시 만족`해야 한다.
    - 데이터 타입, PK, 체크 제약 조건 등이 작업 전 후로 모순이 생기면 안 된다.
    - EX) A 계좌에 5만원 있는데 `10만원을 출금 시도`하려하면, `계좌 잔액이 0이상`이어야 한다는 `규칙(일관성)을 지키기 위해` `해당 Transaction을 거부`함. (작업 전 후의 데이터 상태가 규칙에 어긋나기 때문)
    
3. Isolation(격리성) : `동시에 여러 Transaction이 실행`될 때, `서로의 작업에 끼어들거나, 영향을 주어서는 안 된다.`
    - 각각의 Transaction은 혼자 실행되는 것처럼 느껴져야 한다.
        - 한 Transaction이 수정 중인 데이터를 다른 Transaction에서 멋대로 읽거나 수정할 수 없다.
    - A가 B에게 10만원을 보내는 와중에 C가 A에게 5만원을 보낸다면?
        - Isolation 성질이 잆다면, 잔액이 이상하게 계산될 수 있음.
        - 하지만, Isolation을 위한 DB Lock 기술이 있기에 막을 수 있다.
4. Durability(영속성) : 성공적으로 `완료된 Transaction의 결과`는 `영원히 반영`되어야 한다.
    - `Commit`이 완료되었다면, 직후에 서버 전원이 꺼지더라도 데이터는 `디스크에 안전하게 저장`되어야 한다.
    - B의 잔액이 10만원 늘어나고 0.1초 뒤에 서버가 꺼졌다 가정
        - 서버를 다시 켰을 때, `log file`등을 이용하여 복구함으로서 Durability를 유지한다.

#### 임시 작업 영역
> Transaction이 `Atomic` 성질을 유지할 수 있게 해주는 기술
> - 원본 데이터를 바로 수정하는 것이 아닌, 임시 작업 영역을 활용하여 수정

- 임시 작업 영역 구현을 위한 요소
    1. `Undo Log`
        - Transaction 중 오류가 발생하여 `Rollback`해야할 때, 여기 `저장된 로그를 기반으로 원상 복구`
            - Q) 그냥 임시 작업 하던거 버리면 되는데 왜 Undo Log를 이용해서 복구하나요?
            - A) 여러 이유가 존재한다.
                1. Buffer Pool은 메모리 위에 있는 만큼 그 `크기가 한정적`이다. 만약, `Transaction이 매우 길어진다면, Buffer Pool이 가득` 차서 `Uncommitted Transaction Page도 기록`해버리게 된다.(`Steal`)
                2. `동시성 제어`, T1이 쓰기 작업 A를 하는데, T2가 읽기 작업 B를 요청하는 경우, 쓰기 작업 중이던 것을 보여주는 것이 아닌, 작업 이전의 값(Undo Log에 기록된 값)을 보여줘서 데이터가 꼬이지 않게 한다.
    2. `Buffer Pool`
        - 디스크에 매번 작업하면 속도가 너무 오래걸리기 때문에, `메모리에 존재`하는 `임시 캐시 영역`
        - 모든 `데이터 변경`은 일단 `Buffer Pool`에 있는 `Page`위에서 일어난다.
        - `Dirty Page` : 수정은 되었지만, 아직 디스크에 반영되지 않은 페이지를 말함. `Transaction이 Commit`되면 `이 Dirty Page들이 한 번에 Disk로` 옮겨짐

#### Transaction 명령어
1. `COMMIT` : 작업 완료
    - Transaction 내에서 수행된 모든 작업을 DB(물리적 디스크)에 영구적으로 반영하는 명령 
    - `COMMIT의 결과` : Transaction이 완전히 종료
        - 다른 사용자도 결과를 볼 수 있음
        - 수정하던 Record에 대한 Lock이 해제된다.
    - `COMMIT되는 상황` 
        1. 명시적으로 `COMMIT` 수행
        2. `DDL`, `DCL` 수행
        3. 접속도구(ex, DBeaver) `정상적 종료`
2. `ROLLBACK` : 작업 취소
    - Transaction 시작 이전 형태로 되돌리는 명령
    - `ROLLBACK 실행시` Undo Log에 저장해둔 이전 데이터들을 가져와 현재의 임시 작업 영역에 덮어써버린다.
    - `ROLLBACK 결과` 
        1. 진행 중이던 모든 변경 사항이 사라진다.
        2. Transaction이 종료되고, 데이터는 이전 상태로 복구된다.
        3. 작업중이던 Record에 대한 Lock이 풀린다.
    - `ROLLBACK 되는 상황`
        1. 명시적으로 `ROLLBACK`
        2. 접속 도구의 `비정상적 종료`
3. `SAVEPOINT` : 중간 저장됨
    - 전체 취소 대신 특정 지점까지 되돌리기 위해 저장하는 명령
    - `SAVEPOINT`를 이용하여 ROLLBACK할 경우, SAVEPOINT 이전에 실행한 명령들은 취소되지 않는다.

#### TRANSCATION 연습
1. ROLLBACK 
    ```sql
    INSERT INTO DEPT_COPY VALUES(50,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 보임
    ROLLBACK;
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 사라짐 (ROLLBACK해서)
    ```
2. COMMIT 후, ROLLBACK
    ```sql
    INSERT INTO DEPT_COPY VALUES(50,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 보임
    COMMIT; -- 반영
    ROLLBACK; 
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 보임 (COMMIT 한 후의 작업만 사라짐)
    ```
3. 자동 커밋 수행
    ```sql
    INSERT INTO DEPT_COPY VALUES(50,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 보임
    TRUNCATE TABLE DEPT02; --다른 테이블에 DDL 수행
    ROLLBACK;
    SELECT * FROM DEPT_COPY; -- 50이 추가된게 그대로 있음(DDL이 COMMIT을 수행하기 때문)
    ```
    - Q) 현재 작업중인 테이블에 DDL을 수행한 것도 아닌데 왜 현재 테이블이 커밋되나요?
    - A) DB 엔진이 Transcation을 관리하는 단위가 아니라, Session(연결)전체가 Transaction을 관리하는 단위이기 때문
        - 즉, 해당 세션에서 발생한 변경 사항 전부를 Transaction에 담음 
4. SAVEPOINT 사용
    ```sql
    INSERT INTO DEPT_COPY VALUES(60,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 60이 추가된게 보임
    SAVEPOINT S1;
    INSERT INTO DEPT_COPY VALUES(70,'비서','서울');
    SELECT * FROM DEPT_COPY; -- 70이 추가된게 보임
    SAVEPOINT S2;
    ROLLBACK TO S1;
    SELECT * FROM DEPT_COPY; -- 70은 사라지고, 60만 남음 (S1 지점으로 이동했기 때문)
    ```


## 참고
1. 테이블에 다른 이름 부여
    - FROM에서 테이블 이름 뒤에 별명을 표기할 수 있다.
        - 이 방식으로 별명을 등록했다면, 그 뒤로는 별명만으로 테이블을 칭해야한다. (기존 테이블 명으로 칭할시 오류  
    - SELF JOIN에서는 이 방식이 필수다.
        - 자기 자신이면 테이블 명 구분이 안되므로
    ```sql
    SELECT *
    FROM EMP e, DEPT d
    WHERE e.DEPTNO = d.DEPTNO;
    ```
2. ON, USING
    - ANSI 표기법으로 JOIN을 사용할 때, 아래 상황에선 `ON` 대신 `USING을 사용`할 수 있다.
        - `두 테이블의 Column 명이 같을 때`
        - USING은 무조건 괄호로 묶어야 한다.
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