# 12월 31일 (BYE 2025)

## Mongo DB
1. 설치
- Mongo DB Server 설치
    - Window의 경우 설치 시, GUI 도구(Compass)가 같이 설치되며, 서버는 `서비스`로 생성
    - Mongo로 만들어져있던 shell이 같이 설치되지 않는다. Shell을 사용하고자 하는 경우 mongosh를 다운로드 받아 직접 설치
    - 외부 파일을 import 하거나 export 할 수 있는 도구들도 설치가 되지 않기 때문에 사용하고자 하면, mongodb database tools를 다운로드 받아서 사용

    - MAC,LINUX는 GUI도구가 포함되어 있지 않으므로 GUI도구를 사용하고자 하는 경우 직접 다운로드 받아서 설치

2. 이용
    1. Add new connection
        - URL 확인하고 `Save & Connect`
3. 동적 DB
    - 필드가 없으면 새로 만들어서 값을 넣는다.
4. 데이터 저장의 최상위 단위
    - Key:Value로 이루어진 `중괄호({})`
        - 그래서 아래의 경우 이상함
            ```sql
            db.user.insert([1,2]) -- [1,2] 가 저장되는게 아니라 빈 item 2개가 나온다.
            db.user.insert([{1},{2}]) -- Key:Value 안 맞아서 Error
            db.user.insert([{num:1},{num:2}]) -- num:1 / num:2 로 각각 생성 (배열로 생성되는 것이 아님)
            ```

### 작업 단위
#### 1. Database
- 가장 큰 작업 단위
- 동시 처리 성능과 연관됨
- Collection이나 Index를 추가하거나 변경하는 경우 Lock이 적용된다.
- 관련 명령
    - Database 목록 확인
        - `show dbs;`
        - admin : 관리자 DB (User 정보 등)
        - config : 설정 DB (정보가 어떻게 분산되었는지 등을 적어둠)
        - local : 테이블을 복사하여 작업하는 공간
    - Database 생성 명령
        - `create database 이름;`
    - Database 사용 설정
        - `use 이름`
        - 없는 DB면 생성해줌
    - 사용중인 Database 삭제
        - db.dropDatabase();
- 예시
    1. adam이라는 데이터베이스를 사용
        ```sql
        use adam
        ```
    2. 데이터를 1개 추가하고 목록 확인
        ```sql
        db.mycollection.insertOne({name:1})
        show dbs; -- 위에서처럼 추가하고 나야 목록에 DB가 나타난다.
        ```
#### 2. Collections
- 문서의 모임
- 관련 명령
    1. 생성 : 데이터 삽입 시, 없으면 생성
        ```sql
        db.createCollection(이름)
        ```
    2. 조회 : DB에 속한 Collection 확인
        ```sql
        show collections
        ```
    3. 삭제 : 컬렉션 제거
        ```sql
        db.컬렉션이름.drop()
        ```
    4. 이름 변경
        ```sql
        db.이름.renameCollection('수정할 이름')
        db.old_name.renameCollection('new_name')
        ```

- 샤딩과 클러스터링
    - 샤딩 : 조각, 수평 분할
    - 클러스터링 : 묶는 것

- Capped Collection
    - 크기가 정해진 컬렉션
        - 크기를 초과하면 자동으로 `가장 오래된 데이터를 삭제`하는 Collection
    - 사용처 : 메모리 크기가 정해진 환경 / 오래된 데이터가 필요없는 환경
        - 메모리 크기가 정해진 환경 
            - 하드웨어를 업그레이드 못하는 환경 (임베디드 환경(블랙박스))
            - 오래된 데이터가 필요없는 환경 (로그 데이터)
    - 생성 방법
        ```sql
        db.createCollection(컬렉션 이름, {capped:true, size: 크기})
        ```
    - 예시, 10000바이트 크기의 Collection 생성 후, 데이터 삽입 후 데이터 확인
        ```sql
        db.createCollection('cappedCollection',{capped:true,size:10000}) -- 생성
        db.cappedCollection.insertOne({x:1}) -- x=1 값 삽입
        db.cappedCollection.find() -- cappedCollection 데이터 앞에서부터 확인 
        db.cappedCollection.stats() -- 상태 조회
        /*
        상태 조회 결과
        ...
        sharded: false,
        size: 29, # size
        count: 1, # 값의 개수
        ...
        */
        -- 데이터 1000개 삽입하기
        for(i = 0; i<1000;i++){
            db.cappedCollection.insertOne({x:i})
        }
        db.cappedCollection.find() -- cappedCollection 데이터 앞에서부터 확인 (600번대부터 출력됨)
        db.cappedCollection.stats() -- 상태 조회
        /*
        상태 조회 결과
         sharded: false,
        size: 9976, # 꽉차서 예전 것이 지워진거
        count: 344, # 1~655까지 삭제(오래된 데이터)
        */
        ```
---
### CRUD
#### 0) JOSN 표기
1. 객체 : \{키:값,키:값\}
2. 배열 : [데이터 나열]
3. MongoDB에서는 배열이 최상위일 수는 없다.

#### 1) 데이터 전체 조회
```sql
db.collection이름.find()
```

#### 2) 생성
- 특징
    1. 단일 Document Level에서 원자적(Atomic)으로 실행
        - 즉, 하나씩 순서대로 실행
    2. 데이터 삽입할 때, _id라는 key를 만들지 않고 삽입하면, _id라는 키가 자동으로 생성되고, 값(ObjectId)이 추가된다.
    3. insert, save, insertOne, insertMany 등의 함수를 이용하여 값을 생성(삽입)한다.
        - insert와 save의 차이는 동일한 _id를 강제로 삽입할 때, 
            - insert -> Error
            - save -> Upsert(있으면 수정, 없으면 추가) 
                - ORM도 Upsert한다.
- 예시, insert라는 함수를 사용
    ```sql
    -- 1개 삽입
    db.test.insert({name:"길원",today_expression: "Hi my name is kilwon",})

    --객체 안에 다른 객체나 배열을 포함해서 삽입
    db.test2.insert({
        item:"ABC1",
        details:{
            model:"14QS",
            manufacturer:"kingrangE"
        },
        stock : [{size:"S",qty:25},{size:"L",qty:50}],
        category : "clothing"
    })
    -- 배열의 데이터를 분할하여 삽입
    db.test.insert([{name:"matt"},{name:"lora"}])
    /*
    Why did it happend?
    nosql에서는 {}를 기준으로 key를 생성함
    즉 [{},{}] -> {}, {}로 보는 것이다. 따라소 key를 두 개 생성하게 된다.
    
    */
    ```
    - 변수를 사용하여 저장
    ```sql
    var mydocs = [
        {
            item:"ABC2",category:"etc1"
        },
        {
            item:"ABC3",category:"etc2"
        }
        ,{
            item:"ABC4",category:"etc3"
        },
        {
            item:"ABC5",category:"etc4"
        }
    ]

    db.inventory.insert(mydocs)
    ```
- insert함수의 두 번째 매개변수는 ordered
    - 이 매개변수는 삽입할 데이터가 `배열`일 때, `싱글 스레드`를 사용할지 `멀티 스레드`를 사용할 지 여부를 설정하는 것
    - 기본값은 true인데, 이경우 `싱글 스레드` 
        - false로 바꾸면, `멀티 스레드`
    - 싱글 스레드 : 중간에 에러가 발생하면, 이후 데이터를 삽입하지 않음 ( IGNORE 안 쓴 MariaDB )
        - 순차적으로 넣어야 하면 싱글 스레드 굳
    - 멀티 스레드 : 내 CPU의 코어 개수만큼 동시에 수행함. 즉, 중간에 에러가 발생해도 다른 작업을 계속 수행함. ()
        - 순차적으로 들어갈 필요 없으면 멀티 스레드 굳
- 샘플 Collection을 생성 : `index`를 설정해서 `중복 값`을 저장하지 못하도록 생성
    ```sql
    db.sample.createIndex({name:1},{unique:true})
    --데이터 1개 삽입
    db.sample.insert({name:"park"})
    -- 싱글 스레드 -> park이 중복되어서 튕김 (MongoBulkWriteError: E11000 duplicate)
    db.sample.insert([{name:"kim"},{name:"park"},{name:"lee"}]) 
    -- 현재 데이터 park kim만 존재
    db.sample.find()
    -- 멀티 스레드 삽입 (ordered : false)
    -- Error가 나지만 정상 완료
    db.sample.insert([{name:"kim"},{name:"park"},{name:"lee"},{name:"choi"},{name:"jeon"}],{ordered:false})
    -- 확인 park~jeon 모두 존재
    db.sample.find()
    ```
- Object ID
    - MongoDB에서 사용하는 일련번호
    - 12Byte로 구성되어 있는데 _id 키에 데이터를 설정하지 않으면 자동으로 삽입된다.
        - 직접 설정하고 싶다면? new ObectId() 이용 -> 직접하는게 큰 의미는 없다. 할 수는 있다.
        ```sql
        var newId = new ObjectId()
        db.sample.insert({_id:newId,name:"직접넣음"})
        ```
- insertOne
    - `하나의 데이터만 삽입`하고자 하는 경우 사용
    - `WriteConcern`이라는 매개변수가 있는데 `이 매개변수를 이용`해서 `Lock을 설정`
    - 삽입에 성공하면, `성공한 데이터`의 `ObjectId`를 Return한다.
    - 예시
        ```sql
        db.user.insertOne({username :"an",pw:"1111"})
        ```
- insertMany
    - `여러 개의 데이터를 삽입`할 때 사용
    - 매개변수 `WriteConcern`
    - JS 할 줄 아는 사람은 JS 쓰는 것도 좋다.
        ```sql
        var num = 1
        for(num = 1; num < 3; num++){
            db.user.insertONe({username:"an"+i,pw:i})
        }
        ```
- Document 생성
    - 삽입 유효성 검사
         - 몽고 DB는 삽입된 데이터에 최소한의 검사를 수행
    - Doument의 기본 구조를 검사해 `_id`필드가 존재하지 않으면 새로 추가, 모든 Documents는 16MB보다 작아야 하므로 크기 검사
#### 3) 읽기
```sql
--기본형식
db.collection이름.find(
    query,
    projection
)
-- qeury : 조건
-- projection : 조회할 필드 이름
-- 결과 : document를 조회할 수 있는 cursor

db.collection이름.find()
-- 매개변수가 없으면, Collection의 전체 데이터 조회
```
- 예시, users 컬렉션 전체 데이터 조회
    ```sql
    db.users.find()
    ```
- 예시2, json 파일의 데이터 읽어오기(area.json,by_month.json,by_road_type.json,by_type.json)
    ```sql
    mongoimport -d 데이터베이스이름 -c 컬렉션이름 <json 파일 경로
    -- window에서 이 구문을 수행하고자 하는 경우엔 mongodb database tools를 다운로드 받아야만 수행할 수 있다.
    
    --area
    mongoimport -d adam -c area <json area.json
    mongoimport -d adam -c by_month <json by_month.json
    mongoimport -d adam -c by_road_type <json by_road_type.json
    mongoimport -d adam -c by_type <json by_type.json
    ```
- filtering
    - 속성과 값을 묶어서 `객체`로 설정
    - users 컬렉션에서 `name`이 `adam`인 데이터 조회
        ```sql
        db.users.find({name:"adam"})
        ```
    - 예시3, containerBox 컬렉션에서 category가 animal이고, name이bear인 데이터 조회
        ```sql
        db.containerBox.find({category:"animal",name:"bear"})
        -- 이렇게 ,로 구분하기만 해도 자동으로 AND 개념으로 적용된다.
        ```

- projection (필드 단위 추출)
    - 두번째 매개변수로 {필드이름:<Boolean값>, 필드이름:<Boolean>,...}를 설정
    - true면 해당 필드 조회, false면 해당 필드 조회하지 않음
    - `_id`는 명시적으로 `false를 주지 않으면 조회`된다. (다른건 안 주면 안 조회)
    - 예시, _id,name조회
        ```sql
        db.containerBox.find({},{name:true})
        ```
- 비교 연산자
    - 종류 :`$eq`(=),`$ne`(!=),`$gt`(>),`$gte`(>=),`$lt`(<),`$lte`(<=),`$in`(in),`$nin`(not in)
    - 예시, inventory collection에서 item Column의 값이 `hello`인 데이터를 조회
        ```sql
        db.inventory.find({item:{$eq:"hello"}})
        ```
    - 예시2, inventory collection에서 tags 컬럼의 값이 `blank`이거나 `blue`인 데이터 조회
        ```sql
        db.inventory.find({tags:{$in:["blank","blue"]}})
        ```
    - 예시3, users collection에서 id column의 값이 `admin`이 아닌 데이터 조회
        ```sql
        db.users.find({id:{$ne:"admin"}})
        ```
    - 예시4, null 조회
        ```sql
        -- 둘 다 된다.
        db.c.find({y:{$eq:null}})
        db.c.find({y:null})
        -- c 에는 z 속성이 없다 근데, 아래 구문을 실행하면?
        db.c.find({z:null})
        -- 모든 값이 다 나온다. -> 속성이 없는 것도 NULL로 간주하기 때문
        ```
    - 예시 5, 속성이 존재할 때만 비교하고자 하는 경우
        ```sql
        db.c.find({z:{$eq:null,$exists:true}})
        -- z속성이 없는 경우 해당하지 않는 것으로 봄
        ```
- 정규 표현식 조희
    - `$regex를 이용`해서 `정규 표현식`을 이용해서 `조회 가능`
    - 기본 형식
        ```
        {<필드>:/pattern/}
        {<필드>:{$regex: /pattern/, $options:'옵션'}}
        {<필드>:{$regex: 'pattern', $options:'옵션'}}
        {<필드>:{$regex: /pattern/options}}
        ```
    - 옵션 종류
        1. `i` : 대소문자 무시
        2. `m` : 정규 표현식에 ^를 사용할 때 값에 \n가 있으면 무시
        3. `x` : 정규식 안에 있는 `모든 공백을 무시`
        4. `s` : .을 사용할 때 \n을 포함해서 매치
        - 예시
            1. users 컬렉션에서 a가 포함된 데이터를 조회
                ```sql
                db.users.find({name:/a/})
                ```
            2. users 컬렉션에서 pa로 시작하는 데이터를 조회
                ```sql
                db.users.find({name:/^pa/})
                ```
            3. users 컬렉션에서 ro로 끝나는 데이터를 조회
                ```sql
                db.users.find({name:/ro$/})
                ```
- 데이터 개수 제한(`limit`)
    ```sql
    db.컬렉션명.find().limit(개수)
    --db.users.find().limit(4) -- 4개만 가져오기
    -- 1개 조회
    db.users.find().limit(1)
    db.users.findOne()
    ```
- 데이터 건너뛰기(`skip`)
    ```sql
    db.컬렉션명.find().skip(개수)
    --db.users.find().skip(3) #3개 건너뛰기
    ```
- 정렬(`sort`)
    - 컬럼 이름을 설정하고, 1을 설정하면 오름차순, -1을 설정하면 내림차순
    - $natural:1 을 설정하면 입력 순서대로 오름차순 정렬, -1을 설정하면 내림차순 정렬
    - users 컬렉션의 데이터를 id를 기준으로 `오름차순 정렬`
    ```sql
    db.collections.find().sort(id:1)
    db.collections.find().sort($natural:1)
    ```
- cursor(`iterator`)
    - 데이터에 순차적으로 접근하기 위한 포인터
    - Mongo DB의 find 함수의 리턴 데이터가 cursor
    - cursor에는 hasNext()와 next()메서드가 존재
        - hasNext() -> 다음 데이터 존재 여부 확인
        - next() -> 다음 데이터 가져오기
    - 예시, users 테이블의 데이터를 cursor를 사용해서 접근
        ```sql
        var user_cursor = db.users.find()
        ```
        - 다음 데이터 여부 확인 및 가져오기
            ```sql
            user_cursor.hasNext()
            user_cursor.next()
            ```
    - 예시, 삼항연산자 이용
        ```sql
        var user_cursor = db.users.find()
        cursor.hasNext()? cursor.next():null
        ```
#### 4) 수정
- 종류
    1. update()
        - 매개변수 3가지 : 조건, 갱신내용, 옵션(upsert에 대한 부분)
        - update함수는 연산자를 이용해서 `특정 필드의 값`만 변경하는 것이 가능
        - 데이터를 삭제하고 수정
            ```sql
            db.sample.drop()
            db.sample.insert({name:"park",score:90}) -- 데이터 삽입
            db.sample.update({name:"park"},{$set:{score:100}}) -- name이 park인 데이터 score 수정
            db.sample.find()
            ```
        - 수정 연산자
            - $currentDate
            - $inc
            - $min
            - $max
            - $mul
            - $rename
            - $setOnInsert
            - $set
            - $unset
    2. updateOne()
    3. updateMany()
    4. replaceOne() : 덮어쓰기, 즉 값이 사라질 수 있음
        - 기본 형식
            ```sql
            replaceOne(
                <query>,
                <replacement>,
                {
                    upsert:<boolean>,
                    writeConcern:<document>,
                    collation:<document>
                }
            )
            ```
            - query : 필터링 조건
            - replacement : Document를 대체/수정할 내용
            - upsert : 없으면 추가 있으면 수정
            - collation : 대소문자 구분 옵션
        - 예시, name이 matt인 데이터의 username을 Karpoid /status를 sleep/points를 100/password를 2222로 수정
            ```sql
            db.users.replaceOne(
                {name:"matt"},
                {
                    name:"Karpoid",
                    status:"sleep",
                    points: 100,
                    password:2222,
                },
                {
                    upsert:true
                }
            )
            ```

#### 5. 삭제
- remove
- deleteOne
- deleteMany

## Python과 MongoDB 연결
### 1. Driver를 이용해서 연동
- 함수 사용법이 완전히 동일하다.
### 2. ODM을 이용한 연동
#### ODM
- 객체와 문서를 매핑하는 도구
- `MongoDB와 같은 DocumentDB`는 `JSON형태의 데이터`를 다루는데 `ODM`을 쓰면 이 문서를 `Python의 Class처럼 다룰 수 있음`
    - dictionary 대신 object를 이용해서 작업하는 것이 가능
- 종류
    1. MongoEngine
        - 많이 사용한다.
        - `mongoengine`
    2. Beanie
        - FastAPI와 연동이 잘 된다.

- ODM/ORM 차이
    - ODM
        - 대상 DB  : MongoDB와 같은 문서형 DB
        - 데이터 구조 : Json / Document
        - Python Package : MongoEngine, Beanie
    - ORM
        - 대상 DB : MariaDB같은 RDBMS
        - 데이터 구조 : Table / Row
        - Python Package : SQLAlchemy, Django ORM
- Beanie 사용
    - 비동기 ODM
        - 일반적으로 속도가 더 빠름
        - 언제 끝나는지 알 수 없어서 `Callback`을 받아야한다.
        - 완료 순서가 기존 순서와 맞지 않을 수 있다.
            - 그래서 msg에 numbering을 해줘야 한다. (맨 앞-> BOF, 맨 뒤 -> EOF 이런식으로)
    - 구성
        1. `motor` : 비동기 드라이버 
        2. `pydantic` : 검증 라이브러리
        - 위 두 개를 기반으로 동작
    - 패키지 
        1. beanie
        2. motor


## 참고
1. IP
    - 127.0.0.1 -> Loopback
    - 0.0.0.0 -> 모든 커뮤터
2. DBeaver와 SQL PLUS/Command Line Tools의 차이
    - DBeaver : 접속 도구
    - SQL PLUS/Command Line Tools : DB에 직접 접속하는 관리자 도구

3. Application / Process / Thread
    - Application/Program 
        - 파일이나 파일의 집합 
    - Process
        - 실행중인 프로그램
    - Thread
        - 자원할당 역할 (격리)
        - CPU가 Memory를 분할하여 여기갔다 저기갔다 하면서 처리하는 것
        - 메모리 인터리빙
4. MessageBroker
    - Kafka, RabbitMQ
    - 결제 시스템에선 거의 다 이거만 쓴다.
    - 퍼블릭 클라우드도 다 이거 쓴다.
5. DB-> Server -> CLient
    - Client -> Server 데이터 전송 전, `유효성 검사` 진행
        - 단점 : 보안취약, 코드노출 , 따라서 암독화를 한다.
    - Server : Client로부터 데이터를 받으면 바로 `유효성 검사` 다시
        - 장점: 코드 노출 X
        - 단점: 결과 늦게 옴, 느림
        - 이유 : 네트워크를 통해 오다가 변질될 수 있기 때문
    - Server->DB : 위와 마찬가지로 유효성 검사 진행
        - 네트워크를 또 통하기 떄문
        - 크기, 인코딩 방식,자료형, 이건 몽고 디비가 알아서함. 
            - 나머지는 개발자가 해야함

6. 환경 변수 설정
    - A 경로에 a.exe 프로그램을 실행하고 싶다.
    - 그럼 항상 A경로로 가기 귀찮으니까 PATH에 등록해놓고 쓰면 된다.
    - 개녀
7. 웹은 비동기
    - Thread로 처리해버림
8. Driver는 직접 connection close를 해줘야한다. ORM/ODM은 자동으로 해준다.