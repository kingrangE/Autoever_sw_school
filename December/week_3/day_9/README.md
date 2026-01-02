# Mongo DB
1. 설치
    - Mongo DB Server 설치
        1. Window
            - 설치 시, GUI(Compass)도구가 같이 설치
            - Shell은 따로 설치 필요 -> `mongosh`
            - 외부 파일 import/export 도구도 따로 설치 필요 -> `mongodb database tools`
        2. Mac/Linux
            - 설치 시, GUI도구도 포함되어 있지 않음 -> 따로 설치 필요
2. 특징
    - 무언가 추가를 하려하는데, 없으면 새로 만들어서 추가한다.

## 작업 단위
### 1. Database
- 가장 큰 작업 단위
- `동시 처리 성능`과 연관
- `Collection`이나 `Index`를 `추가`하거나 `변경`하는 경우 `Lock`이 적용된다.
#### 관련 명령
1. `Database 목록 확인`
    
    ```sql
    show dbs;
    ```
    - 기본 Database 목록
        1. `Admin` : 관리자 DB 
        2. `Config` : 설정 DB
        3. `Local` :

2. `Database 생성 명령`

    ```sql
    create database 이름;
    ```

3. `Database 사용 설정`

    ```sql
    use 이름
    ```
    - 이때, 없는 DB면 생성해준다.

4. `Database 삭제`
    
    ```sql
    db.dropDatabase();
    ```
#### 명령 예시
1. adam이라는 데이터베이스 사용
    
    ```sql
    use adam
    ```

2. 데이터를 1개 추가하고 목록 확인

    ```sql
    db.mycollection.insertOne({name:1})
    show dbs;
    ```

### 2. Collections
- 문서의 모임

#### 관련 명령
1. 생성
    - 데이터 삽입 시, 없으면 자동 생성되긴 한다.
    ```sql
    db.createCollection(컬렌션이름)
    -- db.createCollection(test) test 컬렉션 생성
    ```
2. 조회
    - DB에 속한 Collection 확인
    ```sql
    show collections
    ```
3. 삭제 
    - Collection 제거
    ```sql
    db.컬렉션이름.drop()
    ```
4. 이름 변경
    ```sql
    db.기존컬렉션이름.renameCollection('새로운 이름')
    -- db.old_name.renameCollection('new_name')
    ```
    
#### Capped Collection
- 크기가 정해진 컬렉션
    - `크기를 초과`하면 자동으로 `가장 오래된 데이터를 삭제`하는 Collection
- 사용 환경
    1. 메모리 크기가 정해진 환경(임베디드)
    2. 오래된 데이터가 필요없는 환경(로그 데이터)
- 생성 방법
    ```sql
    db.createCollection()
    ```
- 예시, 10000바이트 제한의 Collection 생성 후, 1000개 데이터 삽입
    ```sql
    db.createCollection('cappedCollection',{capped:true,size:10000}) -- size(바이트)
    db.cappedCollection.insertOne({idx:0}) -- idx 0을 저장
    db.cappedCollection.find() -- idx 0 확인 
    db.cappedCollection.stats() -- 상태 조회
    /*
    상태 조회 결과
    ...
    sharded: false,
    size: 29, # size
    count: 1, # 값의 개수
    ...
    */
    ```
    - 10000개 데이터 생성
    ```sql
    for(i =0;i< 1000;i++){
        db.cappedCollection.insertOne({idx:i+1})
    }
    db.cappedCollection.stats()
    /*
    상태 조회 결과
    sharded: false,
    size: 9976, # 꽉차서 예전 것이 지워진거
    count: 344, # 1~655까지 삭제(오래된 데이터)
    */
    ```

## CRUD
### 0. JSON 표기
1. 객체는 아래와 같은 형태로 나타내어야만 한다.
    ```sql
    {키:값,키:값}
    ```
2. 배열은 다음과 같은 형태로 나타낸다.
    ```sql
    [데이터 나열]
    ```
3. MongoDB에서 데이터는 JSON 형태가 최상위다.

### 1. 데이터 전체 조회
```sql
db.collection이름.find()
```

### 2. 생성
#### 특징
1. `단일 Document Level`에서 `원자적(Atomic)`으로 실행
    - 즉, `하나씩` 순서대로 실행
2. insert, save, insertOne, insertMany 등의 함수를 이용하여 값을 `삽입(생성)`할 수 있다.
    - insert와 save의 차이 (`동일한 _id를 삽입할 때`)
        - insert : `Error`
        - save : `Upsert`
            - `Update + Insert` (없으면 삽입, 있으면 Update)
3. `insert` 대신 `insertOne`, `insertMany`를 사용하는 것을 권고하는 추세다.
    - 명시적으로 몇 개의 값을 넣기를 원하는지 파악할 수 있기에 `명확성`이 올라감

#### 예시
1. insert로 값 삽입
    ```sql
    db.test.insertOne({name:"길원"})
    ```
2. 객체(`{}`)안에 다른 객체(`{}`)나 배열(`[]`)을 포함해서 삽입
    ```sql
    db.test2.insertOne({
        item:"ABC1", -- 일반 텍스트
        details:{ -- 객체 
            model:"14QS",
            manufacturer:"kingrangE"
        },
        stock : [{size:"S",qty:25},{size:"L",qty:50}], -- 객체 배열
        category : "clothing" -- 일반 텍스트
    })
    ```
3. 배열의 데이터를 분할하여 삽입
    ```sql
    db.many_test.insertMany([{name:"matt"},{name:"lora"}])
    db.one_test.insertOne([{name:"matt"},{name:"lora"}])
    ```
    - One은 무조건 1개의 Document를 넣겠다는 의미.
        - 즉, []로 여러 요소를 묶은 그 `덩어리 자체`를 `하나의 Document로 저장`한다.
        - `key` : 요소들의 순서(0:{name:"matt"},1:{name:"lora"})
        - `value` : 각 요소
    - Many는 []로 묶은 여러 요소를 넣겠다는 의미
        - 즉, `[]로 묶은 여러 요소를 전달`하면 `요소 각각을 Document로 저장`한다.
    
4. 변수를 사용하여 저장
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
    db.test.insertMany(mydocs)
    ```
#### insertMany()
- `ordered 매개변수`
    - 데이터 삽입을 `순서를 무시할지`,`순서를 지킬지` 결정하는 것
        1. `true`(default) : `순서를 지킴`(싱글 스레드)
        2. `false` : `순서를 무시`(멀티 스레드)
- `멀티 스레드`와 `싱글 스레드` 차이
    1. `싱글 스레드` : `하나의 스레드`로 `순차적 처리`
        - 중간에 에러 발생 시, 삽입이 중단된다. (에러 원인 이후부터는 삽입 안됨)
        - `순서가 중요한 데이터` 삽입 시 이용
    2. `멀티 스레드` : `여러 스레드`로 `나누어 처리`
        - 중간에 에러가 발생하더라도 건너뛰고 사용한다.
        - `순서가 중요하지 않은 데이터` 삽입 시 이용
- `sharding 환경`에서 `ordered`
    - true일때 : 라우터(mongos)가 순서를 지켜야 하기에, shard server에 `순차적 요청`
    - false일때 : 라우터가 순서를 무시해도 되므로, 여러 shard server에 `동시에 요청`을 전송 -> 작업 시간 단축 가능
- 예시
    - Index를 Unique 설정하여 중복 방지를 하고, ordered test
        ```sql
        db.col.createIndex({name:1},{unique:True})
        db.col.insertOne({name:"길1"})
        db.col.insertMany([{name:"길1"},{name:"길2"},{name:"길3"}, {name:"길4"}],{ordered:true})-- ordered 안써도 됨(기본값)
        -- 에러가 나며 아무런 값이 들어가지 않음
        db.col.insertMany([{name:"길1"},{name:"길2"},{name:"길3"}, {name:"길4"}],{ordered:false}) -- 에러는 나지만 길2~4가 다 들어감
        ```
#### **createIndex** : 필드에 Index를 생성하는 메서드
- Index : '색인'
- Mongo DB에서는 기본적으로 `B-Tree`구조로 Index를 관리
- Index Unique 설정
- 인덱스 생성 시, `unique에 true 옵션`을 주면, Mongo는 새로운 데이터를 넣을 때마다 `해당 테이블 인덱스`를 먼저 검사한다.
- 기본 형식
    ```sql
    db.컬렉션이름.createIndex({필드명:정렬방향(1/-1)},[{unique:true}])
    -- db.users.createIndex({name:1},{unique:True})
    -- users 컬렉션의 name 필드에 정방향으로 고유 인덱스 생성 (이제 이름 겹치는 객체 못 넣음)
    ```
- 여러개 생성 형식
    ```sql
    db.컬렉션이름.createIndexes([
        {key:{필드명:정렬방향}[,{name:"",unique:true}]} 
    ])
    /**
    db.users.createIndexes([
        {key:{name:1},{name:"이름 인덱스",unique:True}},
        {key:{age:1},{name:"나이 인덱스"}}
        {key:{gender:-1},{name:"성별인덱스"}}
    ])
    /
    ```
- 복합인덱스 (여러 필드를 묶어서 하나의 인덱스)
    ```sql
    db.컬렉션명.createIndex({필드:정렬방향,필드:정렬방향})
    -- 이름은 정방향, 나이는 역방향
    -- db.users.createIndex({name:1,age:-1}) 
    ```
    - 복합 인덱스로 설정하면, 주의해야 할 점
        - 앞에 오는 필드를 생략하고 뒤에 오는 필드만으로 검색할 수 없다. (앞에 것을 기준으로 뒤에 것을 정렬했기 때문)
        - ex 예시를 통해 보면, name을 기준으로 age를 정렬한 것이기에 아래와 같다.
            - name으로만 검색 -> 가능
            - name+age로 검색 -> 가능
            - age로 검색 -> 불가

### 3. 읽기
#### 기본 형식
```sql
db.collection이름.find(
    query,
    projection
)
```
- `query` : 조건
    - `속성과 값을 묶어 검색`하는 것
- `projection` : 조회할 필드 선택
    - `true/false`로 `필드 조회 여부를 선택`하는 것
    - `_id`는 false로 명시하지 않으면 자동 조회
        - 그 외의 Field는 명시하지 않으면 제외
- 결과 : document를 조회할 수 있는 cursor
    - 매개변수가 없는 경우(`db.collection.find()`) 전체 데이터를 조회한다.
#### 비교 연산자
- 종류
    - 종류 :`$eq`(=),`$ne`(!=),`$gt`(>),`$gte`(>=),`$lt`(<),`$lte`(<=),`$in`(in),`$nin`(not in)
#### 정규 표현식
- `$regex`을 이용한 `정규 표현식`으로 `조회 가능`
- 기본 형식
    ```
    {<필드>:{$regex: /pattern/, $options:'옵션'}}
    {<필드>:{$regex: 'pattern', $options:'옵션'}}
    {<필드>:{$regex: /pattern/options}}
    ```
- 옵션 종류
    1. `i` : `대소문자 무시`
    2. `m` : `정규 표현식`에 `^를 사용`할 때, 값에 \n가 있으면 `개행 문자(줄바꿈) 무시`
    3. `x` : 정규식 안에 있는 `모든 공백 무시`
        - 가독성을 높일 때 사용한다.
    4. `s` : 정규 표현식에 .을 사용할 때, `\n을 포함해서 매치`
        - `.`은 \n을 제외한 모든 문자와 매치됨.
        - `s`옵션을 사용하면 `\n`이랑도 매치된다.

#### 읽는 데이터 개수 제한하기

```sql
db.컬렉션명.find().limit(개수)
```

#### 데이터 건너뛰고 읽어오기

```sql
db.컬렉션명.find().skip(개수)
```

#### 정렬
1. 오름차순
    
    ```sql
    db.컬렉션명.find().sort(필드명:1)
    ```

2. 내림차순 
    
    ```sql
    db.컬렉션명.find().sort(필드명:-1)
    ```

3. 입력한 순서대로 출력하기
    
    ```sql
    db.컬렉션명.find().sort("_id":1)  -- id는 자동으로 생성되게 하면, 일련 번호이기 때문에 정렬시, 입력 순서와 같아진다.
    ```

    - Q) 그냥 `find()`하는거랑 뭐가 다른거죠?
    - A) 만약 index를 사용하게 되면, 우리가 만든 index에 따라 다시 정렬되기 때문에 find()하더라도 `입력 순서`대로 나오지 않는다. 하지만 `_id`를 사용하는 경우엔 그러한 문제를 방지할 수 있다.
    - 참고 : `$natural`을 사용할 수도 있으나, 이는 디스크의 물리적 공간에 입력한 순서대로 보여주는 것이므로,  `WiredTriger` 엔진 때문에 내가 입력한 순서와 디스크 공간에 입력된 순서가 다를 수 있다. (따라서 `$natural`로는 신뢰 100%의 입력 순서를 보장하지 못한다.) 

#### cursor
- `iterator`라고도 부른다.
- find() 쿼리의 결과 집합을 가리키는 `포인터`
    - 장점 : `대량의 데이터`도 `메모리 부족` 없이 효율적으로 처리할 수 있다.
- cursor 얻는 방법
    - find()를 통해 얻은 결과를 변수에 저장한다.
        ```js
        var 변수명 = db.컬렉션명.find()
        ```
- `cursor`에는 `hasNext()`와 `next()`메서드가 존재한다.
    - `hasNext()`: 다음 요소의 존재 여부 (T/F)
    - `next()` : 다음 요소 출력


#### 읽기 예시
1. users 전체 조회
    ```sql
    db.users.find()
    ```
2. json 파일 데이터 읽어오기
    ```sql
    --mongoimport -d 데이터베이스이름 -c 컬렉션이름 < json 파일 경로

    mongoimport -d adam -c area <json downloads/area.json
    ```
3. (`query`) users collection에서 name이 `adam`인 데이터 조회
    ```sql
    db.users.find({name:'adam'})
    ```
4. (`query`) containerBox 컬렉션에서 category가 animal, name이 bear인 데이터 조회
    ```sql
    db.users.find({category:'animal',name:'bear'})
    ```
5. (`projection`) users collection에서 _id,name 조회
    ```sql
    db.users.find({},{name:true}) --_id는 기재 안하면 출력
    ```
6. (`projection`) users collection에서 name만 조회
    ```sql
    db.users.find({},{_id:false,name:true}) --_id는 기재 안하면 출력
    ```
7. (`비교연산자`) users collection에서 job 값이 'student'거나 'teacher'인 데이터만 조회
    ```sql
    db.users.find({job:{$in:['student','teacher']}})
    ```
8. (`비교연산자`) users collection에서 name 값이 'sam'이 아닌 데이터만 조회
    ```sql
    db.users.find({name:{$ne:"sam"}})
    ```
9. (`비교연산자`)(`null`) null조회
    ```sql
    db.users.find({name:null})
    ```
    - name 자체가 없는 것들도 `null`로 인식해서 조회가 된다.
10. (`비교연산자`)(`null`) 속성이 존재할 때만 비교하고자 하는 경우
    - $exists 값을 true로 준다.
    ```sql
    db.users.find({name:{$eq:null,$exists:true}})
    ```
11. (`정규표현식`) users collection에서 name에 a가 포함된 테이블조회
    ```sql
    db.users.find({name:/a/})
    ```
12. (`정규표현식`) users collection에서 name이 pa로 시작하는 테이블 조회
    ```sql
    db.users.find({name:/^pa/})
    ```
13. (`정규표현식`) users collection에서 name이 ro로 끝나는 테이블 조회
    ```sql
    db.users.find({name:/ro$/})
    ```
14. (`정규표현식`)(`i 옵션 사용`)users collection에서 id 대소구분없이 HI로 시작하는 테이블 조회
    ```sql
    db.users.find({name:/^HI/i})
    ```
15. (`정규표현식`)(`옵션 사용`) users collection에서 introduce에 줄바꿈 없이 Bye로 끝나는 문장 긁어오기
    ```sql
    db.users.find({introduce:/Bye$/m})
    ```
16. (`정규표현식`)(`옵션 사용`) 상품코드 PROD-{숫자 4자리}-{영어 대문자 2자리}를 매칭하는 regex 코드 가독성 높게 쓰기
    ```sql
    db.users.find({introduce:/^PROD-\\d{4}-[A-Z]{2}/}) -- no x
    db.users.find({introduce:{
        $regex:`
        ^PROD
        -
        \\d{4}
        -
        [A-Z]{2}`,$options:"x"}}) -- with x
    ```
17. (`정렬`) User Collection에 저장된 정보 중 name을 기준으로 오름차순/내림차순 정렬
    ```sql
    db.user.find().sort(name:1) -- 오름차순
    db.user.find().sort(name:-1) -- 내림차순
    ```
18. (`정렬`) Error Log Collection에 정보를 저장한 순서대로 오래된 것부터 출력
    ```sql
    db.Error_Log.find().sort(_id : 1) 
    ```
19. (`cursor`)(`순회 메모리 절약`) 수만건의 데이터를 조회해서 `특정 로직`을 수행해야 할 때, `커서`를 순회하며 `메모리 효율적 처리`
    ```js
    var cursor = db.users.find(status : "Active")

    cursor.forEach(user=>{
        //각 document에 대해 Business Logic 수행
        process(user)
    })
    ```
20. (`cursor`)(`Manage time-out`) cursor가 timeout으로 닫히는 것을 방지시키기
    - cursor는 10분간 아무 활동 없으면, 자동으로 닫힌다. 한 document당 처리 시간이 길다면, cursor가 닫히지 않도록 조절하기
    ```js
    var cursor = db.users.find().noCursorTimeout();
    try{
        while(cursor.hasNext()){ //다음 값이 있으면
            const doc = cursor.next() //가져오기
            process(doc) // 비즈니스로직
        }
    }finally{
        //모든 작업이 끝나면 수동으로 닫아주기
        //자동으로 안 닫히게 처리해놨으므로, 수동으로 닫는 과정이 필수다.
        cursor.close();
    }
    ```
### 4. 수정
- 종류
    1. updateOne
    2. updateMany
    3. replaceOne
- 특징
    - 세 메서드 모두 최대 3개의 `매개변수`를 가짐
        1. `filter` : 조건 (대상 특정)
        2. `update` : 내용 (어떻게 바꿀 것인지)
        3. `option` : 설정 (추가 설정 옵션)
#### updateOne / updateMany
- `업데이트 연산자`를 이용하여 `조건에 맞는 Document`를 `내용`에 따라 `수정`하기
    - 형식
        ```js
        db.컬렉션명.updateOne({filter},{update},{option})
        ```
    - `업데이트 연산자`
        1. `$set` : `필드 값`을 `설정`
            
            ```js
            {$unset: {tempdata : ""}}
            ```

        2. `$unset` : `필드 자체`를 `삭제`

            ```js
            {$unset: {tempdata : ""}} // tempdata 필드 삭제
            ```

        3. `$inc` : `숫자 값`을 `지정한 만큼` `증가`/`감소`

            ```js
            {$inc: {viewCount:1}} // 조회수 증가
            ``` 
        
        4. `$mul` : `숫자 값`을 `지정한 만큼` `곱함`

            ```js
            {$mul : {price:0.9}} // 10% 할인
            ```
        
        5. `$rename` : 필드 `이름 변경`
            
            ```js
            {$rename : {"number" : "phone_number"}} // 필드명 상세하게 변경
            ```
        
        6. `$min`/`$max` : `기존 값`보다 `작거나`/`클 때`만 `업데이트` 

            ```js
            {$max : {highScore : 120}} // 저장된 highScore가 120보다 작으면 업데이트
            {$min : {high_rank : 2}} // highrank가 2보다 크면 업데이트
            ```

        7. `$push` : 배열의 끝에 요소 추가
            
            ```js
            {$push : {tags:"MongoDB"}}
            ```
        
        8. `$addToSet` : 배열에 `중복되지 않을 때`만 `요소를 추가` 
            
            ```js
            {$addToSet : {tags:"MongoDB"}} // tags 배열에 MongoDB가 없을 때 추가
            ```
        
        9. `$pop` : 배열의 첫 번째(-1) 또는 마지막 요소(1)를 제거
            
            ```js
            {$pop : {tags : 1}} // tags 배열의 마지막 요소 제거
            ```
        
        10. `$pull` : 조건에 맞는 모든 요소를 배열에서 제거

            ```js
            {$pull : {tags : "Java"}} // tags 배열에 Java인 요소를 모두 제거
            ``` 
        11. `$` : 쿼리 조건과 일치하는 `첫번째 요소`

            ```js
            db.students.updateOne(
                {_id:1,grades:80}, // id가 1이고, grade가 80점인 요소 찾기
                {$set : {"grades.$":85}} //grades 배열 중 점수가 80점인 첫 번째 요소를 찾아 85로 수정
            )
            // 배열 내 모든 요소 수정
            db.students.updateOne(
                {_id:1,grades:80}, // id가 1이고, grade가 80점인 요소 찾기
                {$set : {"grades.$[]":85}} //grades 배열 내 모든 요소 85로 수정
            )
            ```
    - `옵션`
        1. `upsert` : true로 설정하면, 문서가 없으면 새로운 `문서 생성`(`insert`), 있으면 `업데이트`(`update`)
        2. `writeConcern` : 기록됨을 보장받을 것인가 (`데이터가 잘 써졌다는 것을 응답할 때까지 얼마나 기다릴 것인가`)
            - 데이터의 무결성 V.S. 빠른 성능에 따라 이 값을 조절한다.
            - 형식
                ```js
                {w : <value>, j:<boolean>,wtimeout:<number>}
                ```
                - w : 확인할 서버 개수 (보통 서버를 다중화한다. 여기서 몇 개의 서버까지 입력되었는지를 확인할 것인지 의미한다.)
                    - Default : 1
                    - `w : 0` : 확인하지 않는다. (가장 빠름, but, 데이터 유실 위험이 크다.)
                    - `w: "majority"` : 복제 세트 내 `과반수의 서버`에 기록되어야 `성공`으로 간주
                - j : 데이터가 Disk의 Journal 로그에 실제로 기록되었는지 확인
                    - true : 하드디스크에 적혀있음을 보장 (서버가 꺼져도 데이터 복구 가능)
                    - false : 메모리에만 적혀도 성공으로 간주 
                    - Journal Log 
                        - DB가 Disk에 물리적으로 저장하기 전에, `어떤 작업을 할 것인지` 기록해두는 저장공간
                        - 저널링 
                            1. 쓰기 요청 : 사용자가 데이터를 삽입하거나 수정
                            2. 저널 기록 : 메모리에 Data를 쓰기 전 혹은 동시에 `저널 로그 파일`에 `어떤 것을 변경할 것인지 기록`
                            3. 메모리 갱신 : 메모리(RAM)에 데이터 Update
                            4. 최종 디스크 저장 : `메모리의 데이터`를 `실제 데이터 파일(.wt)`에 옮겨 적음
                        - Q) 왜 필요한가
                        - A) MongoDB는 성능을 위해 데이터를 먼저 메모리(RAM)에 쓰고, 약 60초마다 Disk에 한 번에 모아서 저장한다. 이 60초 사이에 전원이 꺼지면, 메모리에 있던 Data는 모두 사라진다. 이를 막아주는 것이 `Journal Log`다. 
                            - 전원이 꺼지더라도, `마지막 디스크 저장 시점을 확인`하고, `그 시점 이후부터의 저널 로그 기록 읽기`, `로그를 보고 못한 작업을 수행`을 통해 복구한다.
                - wtimeout : 타임아웃 시간 설정
                    -  예를 들어, `w:"majority"`로 설정하는 경우, 서버들의 응답이 늦어지면 무한정 대기하게 될 수 있다. 이를 방지하기 위한 타임아웃 시간이다.
            - 예시, 성능 최우선 (로그 수집, 단순 카운트)
                ```js
                db.logs.insertOne(
                    { event: "click", time: new Date() },
                    { writeConcern: { w: 1, j: false } } // 하나에라도 기록했는지만 확인
                )
                ```
            - 예시, 데이터 안전 최우선 (결제)
                ```js
                db.users.updateOne(
                    { _id: 1 },
                    { $set: { balance: 5000 } },
                    {
                        writeConcern: {
                            w: "majority", //과반수 반영 
                            j: true, // 하드디스크 기록 
                            wtimeout: 5000 // 5000ms 까지만 기다림
                        }
                    }
                )
                ```
        3. `collation` : 대소문자나 Accent 구분 등 `언어별 비교 규칙` 설정
            ```js
            db.users.updateOne(
                {name:"alice"},
                {$set:{status : "Active"}},
                {
                    collation : {locale:"en",strength : 2} // 2 => 대소문자 무시 , 1 = 기본 문자만 비교(base가 같으면 같은거), 3 = 대소문자 엄격히 구분
                }
            )
            ```
        4. `hint` : 특정 index를 `강제로 사용`하게 함. (성능 최적화를 위함)
            ```js
            db.users.updateMany(
                {status:"Inactive"},
                {$set:{deleteReady : true}},
                {hint : "email"} //email 인덱스를 이용하여 업데이트 대상 찾기
            )
            ```
#### replaceOne
- Update 메서드와 형식이나 사용하는 방식은 동일하다.
- Update와의 차이점
    - Update는 데이터를 `Update`하는 것 (고치기)
    - Replace는 데이터를 `overwrite`하는 것 (덮어쓰기)
        - 따라서 Replace로 수정하는 경우, 작성한 Document 그대로 변경된다.

### 5. 삭제
- 과거에는 `remove()`를 주로 사용했지만 현재는 명확성을 위해 `deleteOne()`, `deleteMany()`를 사용한다.

- 삭제 메서드의 결과
    1. acknowledge : 작업 성공 여부
    2. deletedCount : 삭제된 문서의 수

- 특징
    - update와 마찬가지로 `대상을 찾는` 과정이 먼저 일어난다.
        - 이때 
            1. index가 있다면, 삭제 대상을 index를 통해 빠르게 찾아 `즉시 제거`
            2. index가 없다면, 모든 문서를 `전체 조사(COLLSCAN)`한 뒤 삭제하므로 `속도가 느려짐`

#### deleteOne / deleteMany
- deleteOne : 조건에 맞는 `Document` 중 `첫 번째 하나`를 삭제한다.
- deleteMany : 조건에 맞는 `모든 Document`를 삭제한다.
    - 빈 객체(`{}`)를 넣으면 collection 내의 모든 document가 삭제된다.

#### drop
- Collection 자체를 삭제함.
    - 하지만 MongoDB 특성 상, `없는 Collection`에 `insert`구문 실행이 가능하므로 `deleteMany({})`와 결과가 동일하다고 볼 수 있다.
- `deleteMany({})` vs  `drop()`
    - 결과는 둘이 동일하지만, 아래에서 차이가 있다.
        1. `deleteMany({})` : Document를 하나씩 지우면서 index는 유지한다. -> 데이터가 많으면 시간이 오래 소요된다.
        2. `drop()` : collection과 그와 연결된 모든 index를 한 번에 날려버린다. -> 대량의 데이터를 한 번에 삭제할 땐 이게 훨씬 빠르다.

#### Soft Delete
- 실무에서는 실제로 `데이터`를 `DB`에서 지우는 `Hard Delete` 대신 `status` 필드값을 `deleted` 등으로 바꾸는 `Soft Delete`를 자주 사용한다.
    - 실수로 지운 데이터를 복구하기 쉬움 (실제로 데이터가 사라진 것이 아니기때문) / 데이터 분석(통계)에서 활용할 수 있음    

#### TTL(TIme-To-Live) 인덱스
- `유효기간이 있는 인덱스` : 특정 시간이 지나면, MongoDB가 `알아서 데이터를 삭제`하게 만든다.
- 특징
    1. TTL Monitor 
        - MongoDB 서버 내부의 `TTL Monitor`(Background Thread)가 Collection을 훑는다.
        - `해당 쓰레드는 60초를 주기`로 움직이기 때문에 우리가 원하는 정확한 s단위에 맞지 않을 수 있다.
    2. Replica Set 동작
        - 삭제 작업은 `오직 Primary에서만` 일어난다.
        - Primary에서 삭제되면, 해당 `기록이 Secondary로 전달`되어 함께 지워지는 것
    3. 성능 부하
        - 한 번에 대량의 문서가 `동시에 만료`되면, 이를 삭제하느라, `서버의 I/O 부하가 높아질 수 있다.`
- 사용처
    - 로그
    - 인증번호
    - 세션 정보 
    - etc
- 주의사항
    1. TTL을 적용할 필드는 `Date`타입이어야 한다.
        - 검증을 `현재시간 >= 필드 시간 + TTL 시간`으로 하기 때문
    2. 오차가 있을 수 있음
    3. 복합 인덱스 사용 불가
- 적용 방식
    ```js
    db.컬렉션명.createIndex(
        {필드명:1/-1},
        {expireAfterSeconds: 삭제되길 원하는 시간(s)} 
    )
    ```
- 예시
    1. 로그가 생성되고 24시간이 지나면 삭제됨
        ```js
        db.logs.createIndex(
            {"createdAt":1}, // createdAt 필드를 기준으로 인덱스 생성
            {expireAfterSeconds : 86400} //24시간으로 설정
        )
        ```
    2. 이벤트 collection에서 종료일자가 되면 이벤트가 삭제되도록 함
        ```js
        db.events.createIndex(
            {"due" : 1}, // 마감일 필드를 기준으로 인덱스 생성
            {expireAfterSeconds : 0} // 0으로 설정하면 현재 시간이 정확하게 due가 되었을 때 삭제 된다.
        )
        ```

## Python과 MongoDB 연결

### Driver를 이용해서 연동
#### 연동 방식
```python
from pymongo import MongoClient

# Mongo 데이터 베이스 서버 연결 (포트번호는 27017이 아닐때 적는거)
con = MongoClient("IP")

# 사용할 DB 설정
db = con.데이터베이스이름

# 컬렉션 설정
users = db.users
```
#### 사용법
- MongoDB 함수와 완전히 동일하다.
```python
# find
users.find({name:"길원"}) # 이름이 길원인 것을 찾음
# insert
users.insertOne({name:"kingrangE"}) # 이름이 kingrangE인 객체를 삽입
# update
users.updateOne({name:"kingrangE"},{"$set":{"name":"KingrangE"}}) #KingrangE로 변경
# delete
users.deleteOne({name:"KingrangE"})
```

### ODM을 이용한 연동
> Object와 Document를 매핑하는 도구
- `Document DB`가 다루는 `Json 형태의 데이터`를 `Python의 Class`처럼 다룰 수 있게 해준다.
    - Dictionary 대신 `Object를 이용해서 작업`할 수 있게 된다.

- `ODM v.s. ORM`
    - ODM
        - 대상  : MongoDB같은 Document DB
        - 데이터 구조 : Collection, Document
        - 목적 : 유연한 Document 구조의 schema화 및 Data Modeling
        - 데이터 관계 : Embedding / Reference
        - Python Package : MongoEngine, Beanie
    - ORM
        - 대상 : MySQL,MariaDB같은 Relational DB
        - 데이터 구조 : Table / Row
        - 목적 : SQL Query 추상화 및 복잡한 Join 관리
        - 데이터 관계 : FK를 통한 엄격한 관계
        - Python Package : SQLAlchemy, Django ORM

#### 종류
- `MongoEngine`
    - 동기 ODM
    - Django/Flask 같은 `전통적 웹 프레임워크`와 잘 맞음
    - 특징
        1. Django의 ORM과 유사한 문법
        2. 기능이 다양하고, 안정성이 높음. 생태계가 많이 꾸려짐
        3. 데이터 유효성 검사 기능이 좋음

- 예시
    ```python
    # ODM 연결
    from mongoengine import connect

    connect(db="DB명", host="IP",port=27017)

    from mongoengine import Document, StringField, IntField, EmailField, DateTimeField
    from datetime import datetime

    # 테이블 정의
    class User(Document):
        name = StringField(required=True,max_length=50)
        age = IntField(min_value=0)
        email = EmailField(unique=True)
        created_at = DateTimeField(default=datetime.now)

        meta = {
            "collection":"members" # collection 명
        }

    #데이터 생성
    user = User(
        name="해글러",
        age = 70,
        email = "itstudy@gmail.com"
    )

    #데이터 저장
    user.save()

    # 전체 조회 -> 결과가 List[Objects]
    users = User.objects()
    print(users[0].email)

    # 개별 조회 -> 결과가 Object
    user = User.objects(name="해글러").first()
    print(user.name)
    ```
- `Beanie`
    - 비동기 ODM
    - `FastAPI`와 함께 쓸 때, 성능이 좋아짐
    - 특징
        1. 속도가 빠르다.
            - `Pydantic`을 기반으로 구축되었음
        2. 데이터 모델 정의가 간단
        3. 비동기 드라이버 `Motor` 사용
        

## 참고
1. Obect ID
    - MongoDB에서 사용하는 일련번호
    - 12Byte로 구성됨
    - _id에 데이터를 직접 설정하지 않으면 자동 삽입
        - 직접 설정 -> `new ObjectId()` 이용
            ```sql
            var newId = new ObjectId()
            db.sample.insert({_id:newId,name:"직접하는예시"})
            ```