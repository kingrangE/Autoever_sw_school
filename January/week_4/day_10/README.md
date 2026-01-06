# Redis

## 특징
1. Memory Key Value Data Store
    - In Memory DB
    - 저장 시, Key Value를 같이 저장한다.
2. 싱글 스레드로 동작한다.
3. 속도가 매우 빠르다. (In Memory DB,No SQL의 특성)
4. 고가용성 (High Availability)
    - 가용성을 높일 수 있는 방법 : `복제`
    - Redis는 가용성을 높이기 위해 `Master-Slave 구조`, `Sentinel`,`Coordinator`,`LoadBalancer`를 이용한다.
        - `Master-Slave 구조` : Redis는 `Master 서버`에 원본 데이터를 저장하고, `원본 데이터 복제`를 통해 `여러 Slave 서버`에 `분산`저장한다. 
        - `Sentinel` : `장애 상황`을 `탐지`하여, `Fail-Over` 자동 수행,
            - `Fail-Over` : `Master 시스템`에 `장애`가 발생했을 때, `Slave 시스템 중 하나`를 `Master 시스템으로 승격`시켜 서비스 중단없이 `운영을 유지`
            - 여러 대로 구성하여 가용성을 높일 수 있으며, 이때 `홀수 개수로 설정`한다.
                - `투표`를 통해 승격을 진행하기 때문이다.
        - `Coordinator` : Client와 통신하며, 현재 Master 서버의 주소가 어딘지 알려줌.
            - Redis에서는 Sentinel이 Coordinator의 역할도 대신하여, `Client`가 `Sentinel과 통신`하여 주소를 알아내기도 한다.
        - `LoadBalancer` : 읽기 요청을 여러 대의 Slave 서버로 고르게 분산시켜 주는 역할
            - Q, Health Check도 되고, 분산도 되는데 Sentinel이 왜 필요한가?
            - A, `데이터의 정합성 유지`를 위해서다. 
                - 예를 들어, LoadBalancer만 존재한다면, Master가 누군지 모른다. 즉, 쓰기 작업이 서버 여러 곳에 분산되어 작업될 수 있다. 그러면 정합성 유지가 어려워지므로, Sentinel이 Master DB를 파악하고 장애 시, 승격시키는 작업을 하는것이다.
        
5. 확장성이 좋음
    - `Cluster 모드`로 `쉽게 확장`이 가능하다.
    - Redis는 `Cluster내`에서 `자동으로 샤딩`된 후, 저장되며, `여러 개의 복제본`이 `생성`될 수 있다. 이러한 `데이터의 분리`는 `데이터베이스 레이어`에서 처리
        - 사용자는 Cluster 전체를 하나의 DB로 보고 데이터를 저장할 수 있다. (자동으로 Cluster 내부에서 샤딩하여 여러 그룹에 저장)
        - 과거에는 Application Layer에서 OO데이터는 A DB, XX데이터는 B DB 이런식으로 분리를 했었는데, 현재는 Database Layer에서 Redis가 알아서 분리한다.

## MSA(Micro Service Architecture)와 Redis
1. 데이터 저장소로서의 Redis
    - 속도가 빠르다.
    - 영속성 문제
        - Redis는 `Memory DB`이므로, `영속성 문제가 존재`한다.
            - `AOF(Append Of File)`와 `RedisDB를 이용`해서 `주기적`으로 `파일 시스템에 저장하여 해결`한다.
2. Message Broker로 활용 가능
    - Redis에는 `pub`,`sub`기능이 존재함.
        - pub : 쓰기 / sub : 구독(읽기)
    - MSA 아키텍처는 `Message Broker`를 통해 `데이터 불일치 문제를 해결`한다.
        - 과거 : TCP를 사용하여 문제 해결
            - 단점 : Write DB가 멈추지 않는 이상 Read는 계속 Write와 같이 일해야 함.
        - 현재 : Message Broker(`Redis`)를 두고, `Pub`으로 쓰고, `Sub`로 읽는 곳에 전송하는 방식
            - 장점 : Write DB가 쓸 만큼 쓰고, Pub하면, 해당 값을 Read하여 반영하면 된다. (즉, 각자의 일을 더 집중할 수 있음)

## Event Loop
- Redis가 Single Thread임에도 초당 수십만의 연산이 가능한 이유.
    - Single Thread라면, Waiting 시간으로 인해, Multi Thread보다 느릴 수 밖에 없다.
    - BUT, Redis는 Event Loop를 이용하여 동작한다.
- Event Loop의 차이
    - **`대기 시간`** 차이
        - `Single Thread Queue` : 아래의 과정으로 진행
            - 패킷 도착 대기 : 프로세스의 모든 패킷이 도착하기까지 대기 
                - 이때, 먼저 도착한 프로세스의 패킷 전체가 도착하기까지 대기이므로, 뒤에 도착한 프로세스의 패킷이 먼저 전부 도착해도 나중에 처리된다.
            - 처리 : 프로세스 처리
            - 결과 응답 : 프로세스 처리 결과에 대한 응답 전송

        - `Event Loop` : 아래의 과정으로 진행
            1. `이벤트 대기` : `epoll`(linux 시스템 콜)을 호출하여 `새로운 파일 이벤트가 발생할 때까지 대기` (이때는 CPU 점유 X)
            2. `파일 이벤트 처리` 
                - 파일 이벤트 : Client와의 통신에서 발생하는 이벤트, Redis에서는 **`aeApiPoll`**함수를 통해 파일 이벤트를 수집함.
                    - `Accept` : 새로운 Client가 연결
                    - `Read` : Client가 쿼리(`GET`,`SET`)를 보냈을 때
                    - `Write` : Redis가 처리 결과를 Client에게 보낼 준비가 되었을 때
            3. `시간 이벤트 처리` : 현재 시간에 처리해야 할 관리 작업
            - `이벤트 처리 결과`를 전송할 때도 바로 보내는 것이 아닌 Client가 받을 수 있는 상태가 될 때까지 `응답 버퍼`에 기록해두고 다른 일을 먼저 한다.
        - 즉, Event Loop는 epoll을 이용해서 `일 처리`에만 집중하고 `다른 지연 사항(Write, Packet 대기)`를 고려하지 않아 더 빠른 처리가 가능하다.

- 참고) `Single Thread 6.0` 변경 사항
    - 6.0 이전 : 전체를 Single Thread로 처리
    - 6.0 이후 
        - 명령어 실행 -> Single Thread
        - 패킷 읽고 쓰기 -> 보조 I/O Thread 여러개
    - 변경 이유
        1. `네트워크 한계` : 최근 서버의 네트워크 속도가 매우 빨라지며, Single Thread 하나로 유지하는 것은 CPU에 큰 부담을 줬기 때문
        2. `CPU 활용` : CPU의 코어 개수가 매우 많은데, Redis가 더 많이 활용할 수 있게 한 것

## 사용 사례
### `Main Data Storage`
- 되긴 하는데, Memory를 `대용량 저장소로 사용하기엔 부적합`하다.(가성비 문제)

### `Caching`
- 다른 DB 앞단에 배치시켜, `Access Latency`를 낮추고, `Throughput`을 늘리며, 다른 DB에 대한 부담을 절감시키는 목적
- Cached Data를 한 개의 Redis에 저장하는 `중앙 집중형 구조`로 구성하면, `MSA 환경`의 `수평 확장되는 모든 Application`이 `Redis`만 바라보도록 만들 수 있다. (데이터 일관성을 유지하는데 장점)
    - EX, API-Gateway가 모든 API를 모아두고, 접근하게 하는 것처럼 한다는 말임
### `세션 관리`
- 게임, 전자상거래, SNS 등의 `세션 관리`에 많이 이용
### `실시간 순위표`
- Redis에서 `Z가 붙는 자료구조들`은 점수에 따라 `자동으로 정렬`해서 저장
### `분산 락`
- 공유 자원에 대한 Lock의 관리
### `속도 제한`
- Event 속도를 측정하고, 필요한 경우 속도를 낮출 수 있다.
    - ex, DDOS 방어, Traffic 폭주로 인한 서버 보호 등
### `대기열 생성`
- 작업들을 Redis에 넣고, 하나씩 꺼내서 쓰기 
    - Redis는 Single Thread고, Queue 기반이므로 가능하다.
### `채팅 및 메시지(알림)`
- Redis가 `여러 서버`로부터 `구독(sub)`을 받고, 해당 등록 서버들에게 `게시(pub)`된 메시지를 보내줌.

## Architecture
- Redis는 2가지 모드를 가지고 있다. 각 모드에 따라 Architecture가 달라진다.
    1. Redis Sentinel Mode
    2. Redis Cluster Mode

### Redis Sentinel Mode
!['ClusterMode Arcitecture'](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2Fb879Y4%2Fbtq16tHGvXM%2FAAAAAAAAAAAAAAAAAAAAANJAvkbFxqRpisPGphjn9JY-KBpuvvDpB-z1sxEtarW_%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1769871599%26allow_ip%3D%26allow_referer%3D%26signature%3DpmNBJrQQ08XMsjC1QYoT07E%252FS28%253D)
- 단 `한 대의 Master`로 운용하는 모드
    - 데이터를 Master 1개에서만 작성
- `Sentinel`이 `Fail-Over처리`를 하고, `Master 주소`를 `Client에게 제공`한다.
- 단 한 대의 Master만 두기떄문에, 해당 Master 용량이 가득차면, 더 이상 저장이 불가하다. (당연)

### Redis Cluster Mode
!['ClusterMode Arcitecture'](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FvS6TI%2Fbtq4Bw8T16g%2FAAAAAAAAAAAAAAAAAAAAAPjMGWC0yLYkAYZt7QvpKa4MPEFB2zY16RmtcOodevTu%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1769871599%26allow_ip%3D%26allow_referer%3D%26signature%3DgdGeDPxQjmfz3GkhYqQGe4Yu32o%253D)
- `여러 대(최소 3)의 Master`를 두고 운용하는 모드
    - 데이터를 여러 Master에서 작성
- `Sentinel`이 없다. 
    - Q. 그럼 내가 원하는 정보를 가진 Master를 어떻게 찾나요?
    - A. Client는 아무 Master에게 정보를 요청한다. 만약 그 Master에게 정보가 없을 시, Moved Error를 내보내고, 정보를 가지고 있는 Master의 주소를 Client에게 알려준다. 이때 Client는 Smart Client로 가정한다.(재접속 해야하는 경우 캐싱해두고, 이후 접속 시 캐싱된 주소를 통해 접근)
    - Q2. 그럼 `Fail-Over처리`는 어떻게 하나요? 
    - A2. Cluster Mode에서는 Master-Slave(Replica)끼리 끊임없이 통신을 한다(`Gossip Protocol`). Master 하나가 죽으면, 나머지 `Master끼리 투표`하여 `죽은 Master의 Slave를 Master로 승격`시킨다.
- 데이터를 쓸 때, Sharding 과정을 거친다.

    - Cluster는 데이터 저장 시, 어떤 Master에 저장할 지 결정하기 위해 16384(14bit)개의 Hash slot을 Master 개수로 나눈다.
        - 이 나누는 과정은 2가지 존재
            1. **`수동`**
                - 특정 Master가 CPU/Memory가 유난히 좋다면, 해당 Master에 더 많은 HashSlot을 할당할 수 있음
            2. **`자동`**
                - 기본적으로는 `자동`, 0~N번까지 1/N해서 개수를 분배함
        - Hash Slot
            - 단순히 어떤 Master에 저장할지를 결정하기 위해 존재하는 것
            - Hash Slot 하나 당 수만 개의 키를 저장할 수 있다. 
                - 즉 공간이 부족할 일이 없다.
- Master들의 용량이 가득찬 경우, 새로운 Master를 추가하는 것으로 저장 공간을 확장할 수 있다.(`높은 확장성`)

## 설치 및 접속
1. 설치
    - Public Cloud의 서비스 사용
        - AWS ElastiCache
    - Window 직접 설치
        - power shell에 WSL을 설치해서 Ubuntu 방식으로 설치 (Mac은 블로그 많다. 나도 맥이지만 실습은 윈도우라, 대충 보니까 홈브루 써서 하는 듯)
        - docker를 설치하여 Container로 실행
        - MSI 버전을 다운로드 받아 설치 (GITHUB, Latest 버전이 3.0.xx -> 기능 많이 없음 ㅠㅠ)

2. 접속
    - 설치 시 제공된 `redis-cli`를 이용해서 접속
        ```bash
        redis-cli -h <IP주소> -p <포트 번호> -a <패스워드>
        ```
        - IP주소 : 생략 시, 127.0.0.1
        - 포트번호 : 생략 시, 6379
        - 패스워드 : 설정된 경우 사용

## 이용

### 데이터 저장 및 조회
1. 데이터 1개 저장 : `SET`
    ```bash
    SET 키 데이터
    ```
    ```bash
    SET "name" "kingrangE"
    ```
2. 데이터 1개 읽기 : `GET`
    ```bash
    GET 키 
    ```
    ```bash
    GET "name" # 결과 : kilwon
    ```
3. 데이터 삭제 : `DEL`
    ```bash
    DEL 키
    ```
    ```bash
    DEL "name"
    ```
4. 데이터 여러 개 저장 : `MSET`
    ```bash
    MSET 키 값 키 값 ...
    ```
    ```bash
    MSET name kilwon age 100 # 100을 저장해도 "100"으로 저장된다. 
     # 자료형을 고정하지 않을 경우, 프로그래밍 언어마다 처리하는 방식이 다르기에 까다롭다. 문자열로 고정하게 되면
     # 처리가 쉬워진다. (즉, 생산성 향상, 호환성에 좋다.)
     # 만약 정수처리가 필요하여 작업하는 경우, 자동으로 문자열을 정수로 변환하여 계산하여 저장한다.
    ```
5. 패턴에 맞는 키 조회
    ```bash
    KEYS
    ```
6. 일정 수의 키를 반복해서 조회
    ```bash
    SCAN 
    ```
7. 숫자 증가 
    - 4번에서 정수 처리가 필요한 경우에는 자동으로 정수로 변환하여 작업한다 했다.
    ```bash
    INCR 키 #키에 저장된 숫자 1증가
    INCRBY 키 값 # 키에 저장된 값에 값만큼 증가
    ```

### 데이터 유효기간 설정
- `유효 기간이 지나면` 메모리에서 `데이터를 삭제`하도록 할 때 사용한다.
    - 사용자의 별도 개입 없이 `메모리를 효율적으로 사용`할 수 있다.
```bash
EXPIRE 키 시간(s)
```
```bash
EXPIRE name 10 # 10초뒤 name 키 삭제
```

### 자료구조
- Redis에서는 기본적으로 key : value로 저장을 하는데, 여기서 `value는 여러종류의 자료구조의 형태로 존재`한다.
    1. String
    2. List
    3. Hash 
    4. SET
    5. Sorted Set
    6. Bitmap
    7. Hyperloglog
    8. Geospatial
    9. Stream

#### String
- `문자열`로 저장 : `512MB 길이`까지 `저장 가능`하다.
- Key : Value가 1:1로 저장되는 `유일한 자료구조`
- 기존 키에 데이터를 저장 시, 수정
- OPTIONS
    1. NX : 키가 없을 때만 저장 (키가 있으면 PASS)
    2. XX : 이미 존재하는 경우 수정 (키가 없는경우엔 PASS)
- 숫자 STRING으로 저장 가능

#### LIST
- `순서`를 가지는 `문자열`의 목록
- 최대 `43억개(32bit)의 데이터를 저장`하는 것이 가능
- `Index를 이용`해서 `데이터에 직접 접근 가능`
- Deque 구조 채택
    - Deque 구조이기에 `LPUSH`,`RPUSH`,`LPOP`,`RPOP` 모두 O(1)
    - list의 중간 데이터 접근 시, O(n) 
- `데이터 삽입` : LPUSH, RPUSH
    ```bash
    LPUSH 키명 값 # LPUSH -> 앞쪽(인덱스 작은쪽)부터 삽입
    RPUSH 키명 값 # RPUSH -> 뒤쪽(인덱스 큰쪽)부터 삽입
    ```
    ```bash
    LPUSH test_list 1 # test_list의 0번 index에 1 삽입
    LPUSH test_list 2,3,4 # test_list의 0번 index에 {2,3,4} 리스트 삽입
    RPUSH test_list 5 6 7 # test_list의 맨 뒤에 5 6 7 순서대로 삽입 
    LPUSH test_list 8 9,10 # test_list의 0번 index에 8 {9,10} 순서대로 삽입
    ```
- `데이터 조회` : LRANGE
    - `Index 2개`를 인수로 받음
        - `작성한 인덱스`를 `모두 포함`한다. 
    - `음수 인덱스` : 맨 뒤부터 -1 (Python과 같음)
    ```bash
    LRANGE 키명 시작idx 끝idx
    ```
    ```bash
    LRANGE test_list 0 -1 # 시작(0)부터 끝(맨뒤:-1)까지 조회
    LRANGE test_list 0 1 # 앞에서 2개 값 조회 (0,1번 인덱스)
    ```
- `데이터 삭제` : LPOP(앞에서부터 삭제) / RPOP(뒤에서부터 삭제)
    ```bash
    LPOP 키명 # list에서 가장 작은 인덱스의 값을 추출 후 삭제
    RPOP 키명 # list에서 가장 큰 인덱스의 값을 추출 후 삭제
    ```
    ```bash
    LPOP test_list 
    RPOP test_list
    ```
    - 6.2 이상 버전에서는 아래와 같이 COUNT로 몇 개 삭제할지 지정해서 사용할 수 있다.
        ```bash
        LPOP/RPOP 키명 COUNT # COUNT 개수만큼 앞/뒤에서부터 삭제
        ```
- `범위 외 데이터 삭제` : LTRIM
    - `인덱스 2개`를 받아서 `두 인덱스 사이에 포함되지 않는 요소 모두 제거`
    ```bash
    LTRIM 키명 시작idx 끝idx # 시작idx와 끝idx에 포함되지 않는 요소 전체 삭제
    ```
    ```bash
    LTRIM test_list 1 3 # 1,2,3 인덱스 제외하고 모두 삭제
    ```
- `데이터 삽입` : LINSERT
    ```bash
    LINSERT 키명 (AFTER/BEFORE) 기준값 넣을값
    ```
    ```bash
    LINSERT test_list AFTER 5 51 # 5값 뒤에 51 저장 
    LINSERT test_list BEFORE 5 15 # 5값 앞에 15 저장 
    ```
    - 값이 여러 개라면, 더 앞쪽(작은 인덱스)에 위치한 요소 기준
    
- `특정 위치 데이터 조회` : LINDEX
    - 없으면 
    ```bash
    LINDEX 키명 idx값 
    ```
    ```bash
    LINDEX test_list 2 # index = 2에 무슨 값이 있나요?
    ```
#### HASH
- Dictionary, HashMap 같은 것이다.
- key:value 쌍을 가진 value의 집합이다.
- `Hash Value 추가` : HSET
    ```bash
    HSET 키명 밸류키1 밸류값1 밸류키2 밸류값2 ...
    ```
    ```bash
    HSET hashtest name kingrangE age 25 univ sejong # name : kingrangE, age : 25 , univ :sejong 저장
    ```
- `Hash Value 여러 개 추가` : HMSET
    ```bash
    HMSET 키명 밸류키1 밸류값1 밸류키2 밸류값2 ...
    ```
    ```bash
    HMSET hashtest age 25 univ sejong # age : 25 , univ :sejong 저장
    ```
    
- `Hash Value 읽어오기` : HGET
    - 단일 문자열 반환
    ```bash
    HGET 키명 밸류의 키
    ```
    ```bash
    HGET hashtest name # kingrangE
    ```
- `Hash Value 여러 개 읽어오기` : HMGET
    - 배열 반환
    ```bash
    HMGET 키명 밸류의 키1 밸류의 키2
    ```
- `Hash Value 전체 읽어오기` : HGETALL
    - 우리가 아는 json 형태로 안 보여주고 아래 형식으로 보여준다.
        ```txt
        1) 필드1키
        2) 필드1값
        3) 필드2키
        4) 필드2값
        .
        .
        .
        ```
    ```bash
    HGETALL 키명
    ```
    ```bash
    HGETALL hashtest
    ```
- `Hash Value 삭제` : HDEL
    ```bash
    HDEL 키명 삭제할밸류의키
    ```
    ```bash
    HDEL hashtest univ #univ 정보 삭제됨
    ```
#### SET
- 정렬되지 않은 `문자열의 모임`
- 데이터 `중복없이 저장`
- 집합 관련 연산 지원 (UNION,INTER,DIFF 등)
- `SET Value 저장` : SADD
    ```bash
    SADD 키명 값 (여러 개 나열 가능)
    ```
    ```bash
    SADD setest A
    SADD setest B C D A A A A A B B C D D E F G #B C D E F G 1개씩만 추가됨
    ```
- `SET Value 전체 읽기` : SMEMBERS
    ```bash
    SMEMBERS 키명
    ```
    ```bash
    SMEMBERS setest
    ```
- `SET Value 지정 삭제` : SREM
    ```bash
    SREM 키명 삭제할값
    ```
    ```bash
    SREM setest A # setest 키에 저장된 SET에 있는 Value 중 A를 삭제
    ```
- `SET Value 랜덤 삭제` : SPOP
    ```bash
    SPOP 키명
    ```
    ```bash
    SPOP setest
    ```

- 합 / 차 / 교집합  : SUNION / SDIFF / SINTER
    ```bash
    (SUNION / SDIFF / SINTER) SET키1 SET키2
    ```
#### Sorted Set
- `Score 값에 따라 정렬`되는 문자열의 집합
- `Score`와 `Value`를 쌍으로 가짐
- SET/HASH와 유사함.
    - SET과 유사 : `데이터 중복없이 저장` 
    - HASH와 유사 : `각 값은 스코어라는 데이터와 연결되어 있음`
- 모든 데이터는 Score 순으로 정렬되어 있어, list처럼 index를 통해 아이템에 접근할 수 있다.
    - BUT, sorted list가 더 효율적
        1. Sorted List는 이미 정렬되어 있으므로 내부적으로 `skip list`와 `hash map`을 동시에 사용한다.
            - 즉 `O(log N)의 시간 복잡도`를 가짐
            - 절반씩 점프하며 탐색하므로
        2. List는 정렬되어 있지 않으므로, 앞에서부터 차례대로 접근한다.
            - 즉, `O(N)의 시간 복잡도`를 가짐
- OPTIONS
    1. NX : 키가 없을 때만 저장 (키가 있으면 PASS)
    2. XX : 이미 존재하는 경우 수정 (키가 없는경우엔 PASS)
    3. GT : `변경할 Score가 기존보다 작을 때만` 업데이트, 없으면 삽입
    4. LT : `변경할 Score가 기존보다 클 때만` 업데이트, 없으면 삽입
- `ZSET Value 저장` : ZADD
    ```bash
    ZADD 키명 스코어 저장할 값 
    ZADD 키명 스코어1 저장할 값1 스코어2 저장할 값2 스코어3 저장할 값3 # 여러 개도 가능
    ```
    ```bash
    ZADD score:260105 150 user:kilwon 100 user:etcUser 125 user:whoRU 
     # 위와 같이 :을 사용하는 이유는 도메인을 알려주기 위함이다.(값만 저장하면 이게 무슨 값인지 모르니까)
    ```
- `ZSET Value 조회` : ZRANGE
    ```bash
    ZRANGE 키명 start_idx stop_idx
    ```
    ```bash
    ZRANGE score:260105 0 -1 #위에서 저장한 값 전체 조회
    ```
    - WITHSCORES 옵션을 추가하면, SCORE까지 볼 수 있다. 
        ```bash
        ZRANGE score:260105 0 -1 WITHSCORES 
        ```
- `ZSET Score로 조회` : ZRANGE + BYSCORE (6.2부터)
    - 각 score는 기본적으로 포함(<=,>=)이다.
        - 그러나 열린 괄호 처리를 하고싶은 경우, 해당 값 앞에 `(`를 작성하면 된다.
    ```bash
    ZRANGE 키명 시작score 끝score BYSCORE
    ```
    ```bash
    ZRANGE 키명 110 150 BYSCORE # 110<= Score <= 150추출
    ZRANGE 키명 (110 150 BYSCORE # 110< Score <= 150추출
    ZRANGE 키명 110 (150 BYSCORE # 110<= Score < 150추출
    ```
    - 팁. 최대, 최소를 쓰고싶은 경우 리터럴 값 대신 `-inf` `+inf`를 사용하라.

#### BITMAP
- 내부적으로 String 사용
    -  `String 데이터`의 `개별 비트를 직접 제어`하는 방식
- 속도 
    - `비트 연산` (AND,OR,XOR,NOT)을 통해 `빠르게 처리` 가능
- 사용 사례
    - 출석 정보를 저장한다고 할 때, 개별적으로 Key-Value를 하나씩 만드는 것은 `용량이 매우 소모적`
    - But, bit를 활용하면, 12MB정도로 1억의 개별 출석 정보를 표시할 수 있다. (출석 1 결석 0)
#### HyperLogLog(HLL)
- 대용량 데이터의 `중복을 제거한 개수(카디널리티)`를 적은 메모리를 사용하여 추측해내는 자료구조 
    - SET을 사용하는 것에 비해 수만배 이상 절약 가능
- 특징
    1. 메모리 12KB 고정
    2. 근사치 계산
        - 추정 오차 0.81%
    3. 개수만 셀 뿐, 어떤 데이터가 들어갔는지는 다시 꺼내거나 알 수 없음.
- 원리
    - 해시 함수를 활용하여 이진수로 변환한 뒤, 앞부분에 0이 연속으로 몇 번 나오는지 기록
- `값 저장(데이터 추가)` : PFADD
    ```bash
    PFADD 키명 값
    ```
    ```bash
    PFADD hyper_test 123
    PFADD hyper_test 456 789 159 357 
    ```
- `개수 조회` : PFCOUNT
    ```bash
    PFCOUNT 키명
    ```
    ```bash
    PFCOUNT hyper_test # 결과 : 5
    ```
- `HLL 병합` : PFMERGE
    ```bash
    PFMERGE 합친거저장할키명 합칠키명1 합칠키명2
    ```
    ```bash
    PFMERGE merge_test hyper_test hyper_test2
    ```
#### GEOSPATIAL
- 경도-위도 데이터 쌍의 집합
- 지리 데이터 저장에 이용한다.
    - Q. 왜 굳이 이거 쓰나요 그냥 저장하면 되는데
    - A. 각종 거리 계산이 편리하게 가능하고, 속도 또한 매우 빠름, 또한 `위치좌표`를 `GeoHash`라는 `52비트 숫자로 변환`하여 `ZSET 내부에 저장`하기 때문에 `검색 속도가 매우 빠르다.`


- 내부적으로는 `sorted set`으로 저장, 하나의 자료구조 안에 `key`는 중복돼서 저장되지 않는다.
- `데이터 추가` : GEOADD
    ```bash
    GEOADD 키명 경도 위도 "위치명"
    ```
    ```bash
    GEOADD restaurants 127.0732 37.5473 "Sejong_Univ_Store"
    GEOADD restaurants 127.0708 37.5385 "Konkuk_Univ_Store"
    ```
- `두 지점 사이 거리 구하기` : GEODIST
    ```bash
    GEODIST 키명 위치명1 위치명2 단위
    ```
    ```bash
    GEODIST restaurants "Sejong_Univ_Store" "Konkuk_Univ_Store" m # 두 지점 사이 거리 출력
    ```
- `키명에 저장된 정보 중 현재 내 위치 주변 검색하기` : GEOSEARCH
    ```bash
    GEOSEARCH 키명 FROMLONLAT 경도 위도 BYRADIUS 반경 WITHDIST (ASC/DESC) #오름차순/내림차순    
    ```
    ```bash
    GEOSEARCH restaurants FROMLONLAT 127.07 37.54 BYRADIUS 1 WITHDIST ASC 
    ```
- `삭제` : ZREM
    ```bash
    ZREM restaurants "Sejong_Univ_Store"
    ```
#### STREAM
- Append-Only인 자료구조
    - Log 데이터를 처리하는데 최적화
    - Kafka와 유사한 `소비자그룹 기능`을 Redis로 구현
- 사용 이유
    1. List와 차이 : List는 `조회`만 하는 기능이 없음. STREAM은 `조회만 가능`(즉, 기록이 보존) / List는 인덱스를 기반으로 정렬, Stream은 `시간 기반 ID`로 `정렬`
    2. Pub/Sub와 차이 : Pub/Sub는 보낼 때, 수신자가 없으면 Message가 증발, `Stream`은 소비자가 `나중에 접속`해도 `과거의 메시지를 다시 읽을 수 있다.`
- 핵심 개념
    1. Entry : Stream에 저장되는 개별 데이터 (ID-Field 쌍)
    2. ID : `숫자-숫자`형태, 앞 숫자 - 타임스탬프(ms)/뒷 숫자 - 같은 시간에 들어온 메시지를 구분하는 순번
    3. Consumer Group : 
        - 하나의 데이터 흐름을 여러 사용자가 `중복 없이` 나누어 처리할 수 있게 하는 기능
        - 제공 기능
            1. 메시지 분배 : 소비자 그룹 내 대기중인 소비자에게 메시지를 골고루 분배함.(절대 같은 메시지를 중복하여 받지 않음)
            2. 메시지 보장 : 소비자가 작업을 완료하면, ACK를 보냄.(만약 ACK 받기 전 서버를 종료했다면, 완료되지 않은 것으로 보고 다시 다른 소비자에게)
            3. 소비자 상태 추적 : 그룹 내 소비자가 각 작업을 어디까지 처리했는지 파악 가능

## Redis에서 키를 관리하는 방법
### 키의 `자동 생성`/`삭제`
- 키가 존재하지 않을 때
    - 아이템 삽입 전에 `빈 자료구조를 생성`한다.
    - `No-SQL 구조`이므로 `Mongo DB와 같음` (없으면 만들고 넣고, 있으면 있는데다가 넣음)
        - 그래서 `자료구조마다 명령어가 다 다름.`(`자료구조 구분`을 해야하기 때문)
        - `Reids`에서는 그래서 `자료구조에 대한 이해가 굉장히 중요`하다.
            - "데이터를 어떻게 저장해서 어떻게 사용할 것이냐"
- `모든 아이템을 삭제`하면 `키도 자동 삭제`(Stream은 예외)
    - 키의 존재여부는 `EXISTS로 확인 가능`
  
        ```bash
        EXISTS 키 
         # 없으면 (integer) 0
         # 있으면 (integer) 1
        ``` 
### 키 관련 명령어
#### `패턴 일치하는 모든 키 조회` : KEYS
```bash
KEYS 패턴
```
```bash
# * : 글자 수 상관없는 와일드 카드
KEYS * # 모든 키 조회
# 127.0.0.1:6379> KEYS *
# 1) "test_1"
# 2) "test_list2"
# 3) "test_sortedset"
# 4) "test_list"
# 5) "test_2"
```
```bash
# ? : 와일드카드 (1글자 매칭)
KEYS test_?
# 1) "test_1"
# 2) "test_2"
```
```bash
# []안에 나열하면 그 중 하나가 된다.
KEYS test_[l1]* #test_ 뒤에 l 또는 1이 오고 그 뒤에는 아무거나 
# 1) "test_1"
# 2) "test_list2"
# 3) "test_list"
```
```bash
# ^는 제외의 의미 
KEYS test_[^l1]* # test_ 뒤에 1또는 l이 오지 않는 모든 것
# 1) "test_sortedset"
# 2) "test_2"
```
- `KEYS *` 단점 : 키가 무수히 많은 상황에서 수행하게 되면, `모든 키의 정보를 반환`함
    - Redis는 `Single Thread 기반`이라서, `실행 시간`이 `오래 걸리는 커맨드를 수행`하면 `다른 모든 커맨드가 차단`된다.
        - 문제점 
            1. 다른 Client가 Redis에 `데이터 저장 불가` (`대기열 증가`)
            2. 모니터링 도구의 `health check에 응답 불가` (의도치 않은 `fail-over 발생`)
  
#### `존재 여부 확인` : EXISTS
```bash
EXISTS KEY(여러개 가능)
```
```bash
EXISTS name id addr # name, id, addr 키가 존재하는지 확인 -> 존재하는 키의 개수만큼 return
```
    
#### `범위 키 조회` : SCAN 
- KEY 대신 쓰면 좋은 조회 커맨드
- `커서를 기반`으로 `특정 범위의 키만 조회`한다.
```bash
SCAN cursor [MATCH pattern][COUNT count][TYPE type]
```
- `파라미터`
    - `cursor` : `조회 시작 idx` (0으로 설정 시, 처음부터 조회 시작)
    - `MATCH` : `특정 패턴`에 맞는 키만 `필터링`하기 위한 `패턴 명시`
    - `COUNT` : `한 번의 iteration`에서 `반환할 데이터의 개수` (생략 시, 10)
    - `TYPE` : 특정 데이터 타입 명시
- `return값` : `다음 cursor`의 위치
- 예시

    ```bash
    SCAN 0 
    # 1) "0"
    # 2) 1) "test_1"
    #    2) "test_list2"
    #    3) "test_sortedset"
    #    4) "test_list"
    #    5) "test_2"
    ```
    - 결과의 1 부분이 다음 cursor의 위치
        - 0으로 표시되었다는 것은 조회가 끝났다는 것이다.
    ```bash
    SCAN 0 COUNT 2 # 0부터 시작해서 0,1,2 보여달라

    # 1) "4" -> 다음 커서 위치 4 즉, 이어서 읽고싶으면 다음엔 SCAN 4로 읽어라
    # 2) 1) "test_1" # 0
    #    2) "test_list2" # 1
    #    3) "test_sortedset" # 2
    ```
#### `Value 정렬` : SORT
- `list, set, sorted set`에서만 `사용가능`
- `키에 대응되는 Value`를 `정렬하여 반환`
- `OPTIONS`
    - `LIMIT` : 원하는 개수만큼 반환
    - `ASC/DESC` : 오름차순, 내림차순
    - `ALPHA` : 문자열로 변환해서 정렬
```bash
LPUSH mylist c # [c]
LPUSH mylist a # [a,c]
LPUSH mylist b # [b,a,c]
SORT mylist # ERROR : 그냥 정렬하면 에러
LPUSH mylist HELLO # ["HELLO",b,a,c] 
SORT mylist alpha # 1) "HELLO" 2) "a" 3) "b" 4) "c" # 대문자가 앞, 소문자가 뒤 (아스키코드)
```

#### `키 이름 변경` : RENAME
```bash
RENAME 기존키 새로운키
```
```bash
SET name "kilwon"
RENAME name kilwonname
GET kilwonname
```
#### `키 복제` : COPY
- 6.2부터 생긴 기능
```bash
COPY source destination [REPLACE]
#키가 존재하면 에러인데, REPLACE 옵션을 사용하면, 기존의 키를 지우고 생성해서 복제
```
```bash
SET B BANANA
COPY B BB  
GET B # RENAME과 다르게 원본 값이 사라지지 않는다.
```

#### `자료구조 확인` : TYPE
```bash
TYPE key이름 
```
```bash
TYPE name # name 키의 자료구조가 출력된다.
```

#### `키 전체 삭제` : FLUSHALL
```bash
FLUSHALL [ASYNC/SYNC]
```

#### `키 삭제` : DEL / UNLINK
```bash
DEL 키
```
```bash
UNLINK 키
```
- 둘의 차이 : 동기/비동기
    - DEL은 `동기식`, UNLINK는 `비동기식`이다.
        - 즉, DEL은 삭제 작업을 요청하면 Redis의 Main Thread를 막아 작업을 진행한다. (삭제가 완료될 때까지 Thread가 멈춘다.)
        - UNLINK는 비동기적으로 `KeySpace`에서 먼저 키를 제거(Client는 Key가 사라진 것으로 인식), 실제 `데이터를 메모리에서 해제`하는 작업(무거움)은 `백그라운드 스레드에서 진행`



#### `키의 만료시간 확인` : TTL
```bash
TTL 키
```
- EXPIRE로 설정한 만료 시간을 확인하는 명령어
- Return
    1. 유효시간
        - 유효시간 없으면 -1
    2. 키가 없으면 -2 

# 참고
1. Key-Value 라는 용어가 나올 때 같이 생각하는 자료구조
    - `Dictionary`, `Map(HashMap)`
    - 항상 
        - Key => set으로 생성 (중복 없음->Upsert 구조로 동작)
            - Key는 통상적으로 `String으로 제작`함
                - ex, int 형인 경우, 그냥 List로 만들면 더 쉬움
2. Sentinel과 Data 저장소 하드웨어
    - Sentinel (제어 도구) 
        - 알고리즘 계산을 위해 `CPU`와 `Memory` 많이 할당
    - 데이터 저장소
        - 저장을 하므로 `디스크 공간 크게 할당`
3. Istio - 토스가 쓰는거
    - 나중에 프로젝트 때 써보기
4. Proxy, 방화벽
    - 방화벽 : InBound(외부 네트워크에서 내부 네트워크로 들어오는 것)을 막음
    - Proxy : OutBound(내부 네트워크에서 외부 네트워크로 나가는 것)을 막음