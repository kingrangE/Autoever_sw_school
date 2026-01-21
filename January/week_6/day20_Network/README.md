# 1월 19일

# Network
## Protocol
- 규정, 규약과 관련된 내용
- 누가 만들었는지, 어떤 회사에서 사용하는지에 따라 특징이 많이 달라지고, `다양한 Protocol이 존재`한다.
- `최근엔` 다양한 Protocol 기술이, `Ethernet - TCP/IP 기반 Protocol`들로 `변경`되고 있다.
    1. `물리적 측면`: 데이터 전송 매체, 신호 규약, 회선 규격 등, `Ethernet`이 널리 쓰인다.
    2. `논리적 측면`: 장치들끼리 통신하기 위한 Protocol, `TCP/IP`가 널리 쓰인다.

- 목표: `적은 Computing 자원과 느린 Network 속도 환경`에서 `최대한 효율적으로 통신`하는 것
    - `대부분의 Protocol`이 `2진수 bit 기반`으로 동작한다.
        - `각 위치`에 따라 `엄격히 의미가 약속`되어 있다. (해당 의미를 지켜야 통신 가능)
            - ex, 7~10 bit : 보내는 사람 주소, 15 ~ 20 : ~~~ 등
    - 그러나, `Application Level Protocol`(User가 자주 접한 Protocol)(ex, HTTP/SMTP)에서는 `문자 기반 Protocol`을 사용한다.
        - `문자 기반 Protocol` : `문자 자체를 이용`해 `Header` / `Header 데이터`를 `표현`하고 `전송`하는 방식
            - `효율성`은 bit 기반에 비해 `떨어지지만`, `다양한 확장`이 `가능`
## HTTP Protocol의 헤더
```txt
GET /api HTTP/1.1
Accept: text/html, application/xhtml+xml, */*
Referer: http://zigispace.net/ 
Accept-Language: ko-KR
User-Agent: Mozilla/5.0 (Windows NT 6.1； W0W64； Trident/7.0； 
TCO_20181006113830；
rv：11.0) like Gecko
Accept-Encoding: gzip, deflate
Host: theplmingspace.tistory.com
DNT: 1
Connection: Keep-Alive
```
- `Referer` : 해당 페이지 접속 바로 전의 위치(즉, `접속 바로 이전 경로`)
- `User-Agent` : `어떤 Brower`에서 온 것인지
### TCP/IP : Protocol이라 부르지 않고, Protocol Stack이라 부름.
- `TCP와 IP`는 `별도 계층에서 동작`하는 `Protocol`, But `함께 사용하기 때문에 묶어서 표현`함.
    - 이렇게 `다른 계층에서 동작하는 Protocol을 묶어 말할 때 Protocol Stack`이라고 한다.
        - ELK,EFK 스택도 유사하다.
            - E : Elastic Search, L : Logstash, K : Kibana, F : Fluentd
            - `로그를 저장`하고 `검색`하여 `시각화하는 것`을 `묶어 사용`하기에 `스택이란 용어를 사용`한다.
- TCP/IP 뿐만 아니라 `UDP/ICMP/ARP/HTTP/SMTP/FTP`와 같은 `매우 다양한 application layer protocol이 존재`한다.
- 4개의 계층으로 구분된다.
    1. `Application` - FTP,SSH,TELNET,DNS,SNMP
    2. `Transport` - TCP/UDP
    3. `Network` - IP/ICMP/ARP
    4. `DataLink/Physical` - Ethernet
# OSI 7 계층과 TCP/IP 
## OSI 7계층
- 과거엔 통신용 규약이 표준화되지 않고, 각 Vendor에서 별도 개발했기에 호환되지 않는 시스템이나, Application이 많았고, 통신이 불가했다.
    - 이를 `하나의 규약으로 통합`하기 위해 `OSI 7계층`을 만들었다.
        - 네트워크의 동작으로 나누기 때문에, 이해하고 개발하는데 많은 도움을 주어서, `주요 레퍼런스 모델`로 활용하지만, `최근에는 대부분의 Protocol이 TCP/IP Protocol Stack을 기반`으로 되어있다.
- 7 단계
    1. `Application`
    2. `Presentation`
    3. `Session`
        - 1~3 데이터 유닛 : `Data`
    4. `Transport`
        - 데이터 유닛 : `Segments`
    5. `Network`
        - 데이터 유닛 : `Packets`
    6. `DataLink`
        - 데이터 유닛 : `Frames`
    7. `Physical`
        - 데이터 유닛 : `bits`
    - 1-4계층 : 하위 계층, 5-7 계층 : 상위 계층 (Application 최상위)
        - Network Engineer : 하위 계층 중요
        - Application Developer : 상위 계층 중요
- OSI 모델과 TCP/IP 계층 관계
    ![](image.png)

### 1계층 (Pysical - 물리)
- `물리적 연결과 관련된 정보`를 정의
- `전기 신호를 전달`하는데 `초점`을 맞춤
- 주요 장비 
    - `Hub`(여러 대 장비 연결), `Repeater`(증폭기), `Cable`, `Connector`, `Transiber`, `TAP`(네트워크 모니터링, 패킷 분석을 하기 위해 전기 신호를 복제해주는 장비)
        - `Hub` : 
            - 주소의 개념이 없음
            - 전기 신호가 들어온 포트를 제외, `모든 포트에 같은 전기 신호를 전송`
            - 인터넷이 아닌, `내부 통신용으로 사용하면 많이 느려진다.`

### 2계층 (DataLink)
- `전기 신호를 모아`서 우리가 알아볼 수 있는 `데이터 형태로 처리`
- 정확한 주소로 `통신이 되도록 하는데 초점`이 맞춰져 있다.
- `출발지, 목적지 주소 확인`
- `에러 탐지`, `수정 기능`(최근엔 수행X)도 있다.
- 장비로는 `NIC`(Network Interface Card)와 `Switch`
    - `NIC` : `전송받은 bit`가 `자신의 것이 맞는지 확인`하기 위한 용도
    - `Switch` : `MAC Adress`
        - `쿠버네티스`는 `Switch처럼 동작`
        - 내부 통신 많으면 Switch
        - `MAC Address를 기억`함.(`테이블 관리`)
- `MAC Address` 사용

### 3계층 (Network)
- `TCP/IP`에서는 `Internet`이라 한다.
- `논리적 주소`(IP) 사용
    - IP주소는 `네트워크 주소`와 `호스트 주소로 구분`된다.
- `Routing이 가장 중요`한 역할
    - 경로 찾는 기능
    - `Router`는 `서브넷 마스크를 이용하여 저장`하고, `내/외부 네트웤을 구분`하여 `패킷을 전송`하는 기능을 한다.
        - `서브넷 마스크를 사용`함으로써, `테이블에 저장해야 하는 IP의 개수를 크게 줄일 수 있다.`

### 4계층 (Transport- 전송)
- `데이터`들이 정상적으로 `잘 보내지도록 확인`하는 역할 수행
    - Computer에서 `Application(Process)를 구분`
- `포트 번호`를 사용
    - 여기서부터 `소프트웨어적 개념`
- `Packet 번호를 인식`해서 `Error 여부/Message 조립 여부를 결정`
- `Port 번호`(Application 구분자), `Sequence`(패킷의 번호, 재조립을 위해 필요), `ACK 번호`(긍정 응답)를 `이용`해서 `부하를 분산`하거나 보안 정책을 수립해 패킷을 통과시키거나 차단하는 기능 수행
- `장비` 
    - `Load Balancer`
        - `IP loadbalancing` : `Network Load Balancer`
        - `Port Loadbalancing` : `Application Load Balancer`
        - `각 프로세스를 인식`하고 `요청에 따라 적절한 PC`로 `보낸다.`
        - `소프트웨어 구현이 가능`하다.
    - `Firewall(방화벽)`
        - IP는 Process를 구분하지 못한다.
            - 즉, A 프로세스는 ~~~만 가능, B는 모두 가능 이런 처리를 할 수 없다.
            - `프로세스를 구분하여 처리하는 것`을 가능하게 해주는 것이 `방화벽`이다.
### 5계층 (Session)
- 역할
    1. 양 끝단의 `응용 프로세스 연결 성립`
    2. `연결이 안정적으로 유지되도록 관리`
    3. 작업 완료 후, 연결 종료
- `에러 복구` 및 `재전송` 담당
- 서버쪽에 저장한 `Hash + Data`를 `Session`이라고 한다.
    - Client의 요청을 받으면, Computer는 Hash와 Data를 다시 전송해주는데, 이것이 Session이다.
    - `Client`는 `Server로부터 받은 Hash를 저장하여 데이터를 Server로 전송할 때마다 Hash를 같이 전송`하게 되고, `Server`는 `이 Hash를 보고 어떤 Client인지 확인`할 수 있다.
        - 이것이 `Cookie`다.

### 6계층 (Presentation)
- `표현 방식이 다른`, `Application`이나 `System 간의 통신`을 돕기 위해 `동일한 형식으로 변환`시키는 역할 수행
    - 즉, `인코딩`, `암호화`, `압축` 등을 수행한다.

### 7계층 (Application)
- `최상위 계층`으로 `Application Service` 수행
- Network를 사용하는 `Software의 UI부분`이나 `사용자 I/O 부분을 정의`하는 계층
- HTTP / FTP와 같은 `실제 서비스가 구동되는 계층`

## Encapsulation & Decapsulation
### Encapsulation
- 하나의 컴퓨터에서 다른 컴퓨터로 데이터를 전송할 때, `데이터를 전기신호로 만들기까지의 과정`
- `Application -> Presentation` : 압축 암호화
- `Presentation -> Session` : 연결 유지
- `Session -> Transport Layer` : `Port`(헤더)를 붙여서 `Segment` 생성
- `Transport Layer -> Network` : `IP`(헤더)를 붙여서 `Packer` 생성
- `Network -> DataLink` : `MAC Address`(헤더)를 붙여 `Frame` 생성
- `DataLink -> Physical` : Frame으로 `전기 신호` 만들어 전송

### Decapsulation
- 다른 컴퓨터로 부터 받은 `전기신호`를 `데이터로 만드는 과정`
- Encapsulation의 역순

## Port
### Known Port(유명 포트)
- TCP 20, 21 : FTP(파일 전송 서비스)
- TCP 22 : SSH (Secure Shell)
- TCP 23 : Telnet
- TCP 25 : SMTP(Simple Mail Transport - 이메일 전송)
- UDP 49 : TACACS(Terminal Access Controller Access Control System) 
    - 네트워크 장비에 접속하려는 사용자 인증 및 권한 부여
    - Authentication(인증), Authorization(인가-권한), Accounting(게정)
- TCP 54 / UDP 53 : DNS
- UDP 67,68 : Bootstrap Protocol
    - 네트워크 장비가 부팅될 때, 자신의 IP 주소와 필요한 설정 정보를 서버로부터 할당받기 위한 프로토콜
- `TCP 80/UDP80 : HTTP (가장 중요)`
- UDP 123 : NTP(Network Time Protocol) 
    - 네트워크에 연결된 컴퓨터들의 시간을 표준 시간과 동기화해서 사용하기 위한 프로토콜
- UDP 161,162 : SNMP(Simple Network Management Protocol)
    - 네트워크 관리 프로토콜
- `TCP 443 - HHTPS (가장 중요)`

### Registered Ports(1024~49151)
- `특정 Application, 기업이 등록하여 사용`하는 포트
- 3306 : MySQL, MariaDB
- 5432 : PostgreSQL
- 6379 : Redis
- 27017 : MongoDB
- 1521 : Oracle

### Dynamic/Private Prots(49152~65535)
- Client가 서버에 접속할 때 `임시로 할당` 받는 포트 

# 네트워크 연결 
## 네트워크 규모에 따른 분류
1. `LAN` : Local Area Network
    - 홈 네트워크용, 사무실용,작은 사무실, 건물 정도의 네트워크
    - 스위치와 같은 비교적 간단한 장비로 연결된 네트워크
    - 현재: `대부분 이더넷 기반 전송 기술` 사용
        - 과거: 소모비용, 신뢰도, 구축 및 관리를 위해 다양한 기술 사용
2. `MAN` : Metro Area Network
    - 한 `도시를 연결하고, 관리`하는 네트워크
    - `x~xxkm 범위`의 `한 도시를 네트워크로 연결`하는 개념
        - 통신사가 이미 가진 네트워크로 구축: `WAN`
        - 자체 인프라를 통해 네트워크를 구축: `MAN`
3. `WAN` : Wide Area Network
    - `멀리 떨어진 LAN을 서로 연결`하거나 `인터넷을 접속하기 위해 사용`하는 네트워크
    - 특별한 경우가 아니면, `직접 구축할 수 없는 범위의 네트워크`
        - `통신 사업자로부터 회선을 임대`해서 사용한다.

- 예전에는 LAN,MAN,WAN 모두 사용하는 기술,프로토콜이 달랐으나 `현재는 대부분 이더넷을 사용하기 때문에 거리에 따라 구분`한다.

## 네트워크 회선
- 인터넷 회선
    - `인터넷 접속을 위해 통신 사업자와 연결하는 회선`
    - `전용 회선`/`선로 공유 회선`으로 나눈다.
    - `전용 회선`이 선로 공유 회선보다 `속도도 빠르고 안정적`이다.
- 전용 회선
    - 가입자와 통신 사업자 간의 `대역폭(Bandwidth)을 보장`하는 서비스
    - `가입자 - 통신 사업자간 전용 케이블로 연결` -> TDM같은 기술로 마치 직접 연결한 것처럼 통신 품질 보장하는 것
        - `TDM : Time Division Multiplexing`
            - `시간에 따라 나누어 여러 사용자에게 분배`하는 `Multiplexing`방식
    - 일반 전용 회선 => 본사-지사 연결에 사용
    - 구분
        1. 저속
            - 음성 전송 기술 기반
            - 64kbps 단위로 구분되어 사용
            - 작은 기본 단위를 묶어 회선 접속 속도를 높이는 방법
            - 높은 속도가 필요하지 않을 때나 높은 신뢰성이 필요할 때 사용
            - 사용 빈도는 줄어들지만, 전문 전송(Clear Text)를 위한 VAN 연결에는 저속 회선을 사용한다.
                - 전문 전송 -> 결제 승인과 같은 것
                    - 속도가 중요하지 않으나, 신뢰성이 중요
            - 기술 사용을 위해 원격지 전송 기술로 변환할 수 있는 라우터 필요
            - 2계층 protocol 통신 상태 확인 기능 존재
                - 따라서, 라우터에서 상대방 링크가 끊긴 경우 감지 가능 
                - 즉, LLCF 설정 별도로 필요없다.

        2. 고속 
            - 메트로 이더넷 (광케이블 기반의 이더넷)
            - 가입자와 통신 사업자 간의 접속 기술은 이더넷을 사용하고, 통신 사업자 내부에서는 이런 개별 가입자를 묶어 통신할 수 있는 다른 고속 통신 기술을 사용한다.
- LLCF(Link Loss Carray Forward)
    - LLCF는 한쪽 링크가 다운되면 반대쪽 링크도 다운시키는 기능
    - 이더넷으로 전용회선을 구성시, 회선사에서 LLCF를 설정하지 않는다면 아래의 문제가 발생
        -  전용회선이 한 곳에서 다운되더라도 반대쪽에서는 회선이 그대로 살아있는 것처럼 보인다.
        - 따라서 LLCF 설정이 되어있는지 확인해야 한다.
## VPN
- 물리적으로 전용 선이 아니지만, 직접 연결한 것 같은 효과를 만들어주는 기술
- 다양한 VPN 기술이 있고, 가입자 입장에서 기술/통신사 입장에서 기술이 별도포맢넡

### 통신 사업자 입장에서 VPN
- 전용선, 거리가 늘어날 수록 비용 증가
    - 전용선 : 사용 가능한 대역폭 보장
        - 가입된 계약자가 항상 대역폭을 Full로 쓰지 않으므로, 비용 낭비를 줄이기 위해 VPN 기술을 이용하여 직접 가입자를 구분하고 비용을 줄임

### 가입자 입장에서 VPN
- 일반 인터넷 망을 이용하여 직접 가상 전용 네트워크 구성 가능
    - 대부분의 경우 VPN 내부에서 통신은 비용 지불 X

## DWDM
- Dense Wavalength Division Multiplexing
    - 파장으로 분할하는 기술 (광케이블)
        - 초창기 광케이블은 `하나의 회선에 하나의 통신만 가능` -> `ㅌ`
    - Multiplexing - 다중화(회선 공유 기술)
        - 초창기 : FDM(Frequency Division Multiplexing)
            - ex, 라디오
            - 완충 대역이란 것이 존재하여, 사용하는 대역끼리의 거리가 존재한다.(모두 사용 불가)
        - 다음 : TDM(Time Division Multiplexing)
            - 시간 단위로 전송
            - 동기식으로 동작하기 때문에 네트워크를 안 쓰는 주체도 시간이 할당된다.
                - 비동기식의 경우엔 네트워크를 쓰는 친구들에게만 할당하는 것

## NIC(Network Interface Card)
- LAN카드라고 많이 부른다.
- 컴퓨터를 네트워크에 연결하기 위한 하드웨어 장치
- 서버는 여러 네트워크에 동시에 연결되어야 하거나, 더 높은 대역폭이 필요한 경우 네트워크 인터페이스를 추가로 장착
- 역할
    1. Serialization(직렬화)
        - 전기적 신호<->데이터 신호 변환
        - 케이블로 전송할 수 있게 변환할 때, 또는 케이블로 받은 정보를 변환할 때 사용
    2. MAC Address 
        - 네트워크 인터페이스 카드는 MAC 주소를 가짐
        - 받은 데이터를 읽어, 도착지 MAC 주소가 자신의 MAC 주소를 비교,
            - 맞으면 시스템 내부에서 처리, 아니면 폐기
    3. Flow Control
        - 패킷 기반 네트워크에서는 다양한 통신이 하나의 채널을 이용
            - 이때, 해당 채널을 이용하고 있다면, 새로운 데이터를 받지 못해 데이터 유실이 일어날 수 있음
            - 이때, 데이터 유실 방지를 위해 상대방에게 통신 중지를 요청하는 것이 흐름 제어
## 케이블과 커넥터
- 무선을 많이 이용하는 추세이기는 하지만, `신뢰도 높은 통신`은 `유선을 사용`한다.
- 이더넷 네트워크 표준
    1. 1000BASE-T/10GBASE-T
    2. 1000BASE-ST/10GBASE-SR
    3. 1000BASE-LX/10GBASE-LR
    - 앞의 1000은 외부 네트워크 속도 / 뒤의 10은 내부 네트워크 속도
    - BASE는 채널 / T는 케이블 타임 
    
## HUB
- 케이블과 동일한 1계층(Physical)에서 동작하는 장비
- 거리가 멀어질수록 줄어드는 전기 신호를 재생성/여러 대의 장비를 연결할 목적으로 사용
- 단순하게 받은 신호를 모든 포트로 보낸다.
    - 네트워크에 접속한 모든 단말이 경쟁하게 되어, 전체 네트워크 성능이 줄어드는 문제가 존재한다.
    - 루프와 같은 다양한 장애의 원인이 된다.
        - 루프 : 패킷이 무한 순환하여 네트워크 전체를 마비시키는 현상

## Switch
- `허브와 동일`하게 `여러 장비를 연결`하고 `통신을 중개`하는 `2계층 장비`
- 내부 동작 방식은 허브와 다르지만, 여러 장비를 연결하고 케이블을 한 곳으로 모아주는 역할은 유사하다.
- `허브의 역할`과 `통신을 중재`하는 `2가지 역할을 모두 포함`하므로, `스위칭 허브`라고 하기도 한다.

## Router
- OSI 7계층 중 3계층에서 동작하면서 먼 거리로 통신할 수 있는 Protocol로 변환하는 장비
- 역할
    1. 원격지로 쓸데없는 패킷이 전송되지 않도록 BroadCast와 Multicast 컨트롤
    2. 불분명한 주소로 통신을 시도할 경우 이를 해당 패킷 버림
    3. 정확한 방향으로 통신하도록 함
    4. 최적 경로로 패킷을 포워딩
- 일반 사용자가 라우터 장비를 접하기는 어렵지만, 라우터와 유사한 역할을 하는 L3 Switch와 공유기는 쉽게 찾아볼 수 있다.

## Load Balancer
- OSI 7계층 중 4계층 장비
- Application 계층에서 Application Protocol의 특징을 이해하고 동작하는 7계층 Load Balancer는 별도로 ADC라고도 한다.
- L4 Switch라고 불리는 장비도 Load Balancer의 한 종류로 스위치처럼 여러 포트를 가짐
- Load Balancer가 가장 많이 사용되는 곳은 Web Server
- Web Server 증설하고 싶을 때, 로드밸런서를 웹 서버 앞에 두고, 웹 서버를 여러 대로 늘려준 후, 대표 IP는 로드 밸런서가 갖고, Load Balancer가 사용자의 요청을 받아 패킷의 목적지를 변경해서 전송하는 원리를 이용해 여러 대의 웹 서버가 동시에 동작해서 서비스 성능을 높여주는 동시에 서버에 문제가 발생하더라도 빠른 시간안에 서비스가 복구되도록 도와준다.
- 로드밸런서 기능
    1. IP 변환
    2. 서비스 헬스 체크
    3. 대용량 세션 처리 기능

## 보안 장비
- 보안 장비 -> 정보 잘 제어, 공격 방어에 초점
    - 대부분의 네트워크 장비 -> 정확한 정보 전달에 초점
- 방어 목적, 보안 장비 설치 위치에 따라 다양한 보안 장비가 사용된다.
- 가장 유명한 보안 장비 : 방화벽
    - OSI 7 계층 중 4계층에서 동작
    - 방화벽을 통과하는 패킷의 Network, Transport 계층 정보를 확인 후, 패킷 정책과 비교하여 패킷 버리거나 포워딩

## IP 공유기
- 2계층의 스위치, 3계층의 라우터, 4계층의 NAT와 간단한 방화벽 기능을 모아놓은 장비
- 공유기 내부는 스위치, 무선, 라우터 회로로 나눈다.

## Modem
- 짧은 거리 통신 기술과 먼거리 통신 기술이 달라서 이 기술을 변환해주는 장비
- 공유기 LAN 포트와 WAN 포트는 모두 일반 이더넷
    - 100M 이상 먼거리로 데이터를 보내지 못하기 때문에 먼 거리 통신이 가능한 기술로 변환해주는 모뎀이 별도로 필요하다.
- 기가 인터넷의 경우 FTTH 모뎀 사용, 동축 케이블 인터넷은 케이블 모뎀을 사용, 전화선을 사용할 경우 ADSL, VDSL 모뎀 사용

# 네트워크 통신
## 수신자의 범위에 따른 분류
### 종류 - 목적지 주소를 기준으로 구분
1. Unicast
2. Multicast
3. Broadcast
4. Anycast

### Unicast 
- 1:1 통신
- 출발지와 목적지가 1:1 통신
- 출발지와 목적지가 명확히 하나로 정해져 있는 대부분의 통신은 Unicast

### Broadcast
- 1:전체 통신
- 동일 네트워크에 속한 모든 호스트가 목적지
- 사용 환경
    1. 목적지 주소가 모든으로 표기되어 있는 통신 방식
        - Unicast로 통신하기 전, 상대방의 정확한 위치를 알기 위해 사용한다.
    2. 주소 체계에 따라 브로드 캐스트를 다양하게 분류할 수 있지만, 기본 동작은 local network에서 모든 호스트로 패킷을 전달해야 할 때 사용한다.

### Multicast
- 1:그룹(멀티캐스트 구독 호스트) 통신
- 하나의 출발지에서 특정 목적지 다수로 데이터 전송

- 용도
    1. Multicast Group 주소를 이용하여 해당 Group에 속한 다수의 Host로 패킷을 전송하기 위한 방식으로 IPTV와 같은 실시간 방송을 볼 때, 이 통신 방식 사용
    2. 사내 방송, 증권 시세 전송과 같이 단방향으로 다수에게 동시에 같은 내용을 전달할 때 사용
    3. 화상 회의에도 이용
### Anycast
- 1:1 통신(목적지가 동일 그룹 내의 1개의 호스트)
- 다수의 동일 그룹 중 가장 가까운 호스트에서 응답
- Ipv4에서는 일부 기능 구현
- IPv6에서 모두 구현 가능

- 용도
    1. Anycast 주소가 같은 호스트들 중에서 가장 효율적으로 서비스할 수 있는 호스트와 통신하는 방식
        - 이런 Anycast Gateway의 성질을 이용해서 가장 가까운 DNS 서버를 찾을 때 사용하거나 가장 가까운 Gateway를 찾는 Anycast Gateway 기능에 사용

- 결론
    - 최종 통신은 1:1이라는 점을 보면, Unicast와 Anycast가 동일하지만, 통신할 수 있는 후보자는 서로 다른데, Unicast는 출발지와 목적지가 모두 한 대씩이지만, Anycast는 같은 목적지 주소를 가진 서버가 여러 대여서 통신 가능한 다수의 후보군이 있다.
    - 현재 주로 사용하고 있는 네트워크 주소 체계는 IPv4기반
        - 일부 모바일 네트워크, 데이터 센터 위주로 IPv6주소 체계 사용
        - IPv6에서는 link local multicast로 대체되어 사용

### Link Local Multicast
- 같은 물리적 네트워크 안에 있는 특정 그룹의 장치들에게만 데이터를 전송하는 방식
- Link Local은 Router를 넘어가지 않는 동일한 Local Network 내로 범위를 한정

- 특징
    1. 범위 한정 
        - 데이터가 Router를 통과하지 못하기 때문에, 같은 Switch나 Hub에 연결된 장치들끼리만 통신 가능
    2. Network 상의 장치들을 찾거나 자동으로 설정을 주고 받을 때 주로 사용
    3. Broadcast와 다르게 해당 데이터를 받기로 설정된 그룹 멤버들에게만 전달되어 불필요한 Traffic을 줄인다.
- 사용 사례
    1. IPv6환경에서는 Broadcast가 존재하지 않기 때문에 Link Local Multicast가 그 역할을 대신 수행한다.
    2. 주소 자동 설정 (SLAAC) : 장치가 Network에 접속하자마자 자신의 존재를 알리거나 중복 주소를 확인할 때 사용한다.
    3. BOOTP나 DHCP가 서버에게 주소를 할당받는 방식이라면, 이 방식은 가이드를 받아 Client가 알아서 주소를 만들어내는 방식
    4. Router에게 Network 주소를 물어보고 응답을 받으면, 거기에 MAC address를 붙여서 IPv6 생성
    5. IoT 장치에 이용
    6. IP 할당내역, 기업망, 엄격한 IP 관리 필요한 곳 -> DHCPv6사용
    7. 인근 장치 탐색(Neighbor Discovery): IPv4의 ARP대신 상대방의 MAC 주소를 알아내기 위해 Multicast Message를 보낼 때 사용

### BUM Traffic
- 트래픽 종류에 대한 내용을 다루다보면, BUM 트래픽이라는 용어를 사용하는 경우가 있다.
    - B : Broadcast
    - U : Unicast
    - M : Multicast
    - 3가지는 서로 다른 종류의 트래픽이지만, 네트워크에서의 동작은 유사하다.
- Unknown Unicast는 목적지 주소가 명확히 명시되어 있지만, 네트워크에서의 동작은 Broadcast와 유사한데 Switch가 목적지에 대한 주소를 학습하지 못한 상황
    - 스위치는 패킷을 모든 포트로 플러딩하는데, 이런 Unicast가 Unknown Unicast
    - 실제로 동작하는 방식은 Broadcast와 유사하다.
    - Network 자원을 쓸데없이 사용하므로, Network 상에서 불필요한 BUM 트래픽이 많아지면 네트워크 성능이 저하될 수 있다.

- 이더넷 환경에서는 ARP Broadcast를 먼저 보내고, 이후 통신을 시작하므로 BUM Traffic이 많이 발생하지 않는다.

### MAC Address
- MAC Address체계
    - MAC Address는 변경할 수 없도록 하드웨어에 고정되어 출하되므로, 네트워크 구성 요소마다 다른 주소를 가진다.
- 모든 네트워크 장 제조업체에서 장비가 출하될 때마다 MAC 주소를 할당하게 되는데 매번 이 주소의 할당 여부를 확인할 수 없으므로 한 제조업체에 하나 이상의 주소 풀을 주고, 그 풀 안에서 각 제조업체가 자체적으로 MAC 주소를 할당
- 네트워크 장비 제조업체에 주소 풀을 할당하는 것을 제조사 코드라 한다.
    - 이 주소를 관리하는 것이 IEEE
- MAC Address
    - 48비트의 16진수 12자리 표현
- 앞의 24비트와 뒤의 24비트로 나누어 구분하는데 , 제조사 코드가 MAC주소 앞의 24비트(OUI값)이고, 뒤의 24비트 값(UAA)은 제조사에서 자체적으로 할당하여 네트워크에서 각 장비를 구분하게 한다.
- 유일하지 않은 MAC 주소
    - 네트워크 장비 제조업체는 자신의 제조업체 코드 내에서 뒤의 24비트의  UAA 값을 할당하는데, 실수나 의도적으로 MAC주소가 중복될 수 있다.
        - MAC 주소는 동일 네트워크에서만 중복되지 않으면, 동작하는데 아무런 문제가 없기 때문이다.
        - MAC주소는 Switch가 내부 네트워크 구분에 사용하는 것이기 때문이다.
            - 네트워크를 넘어가면, 기존 출발지와 도착지 MAC 주소를 유지하지 않는다.
- MAC주소 변경
    - MAC 주소는 BIA 상태로 NIC에 할당
    - 일반적으로 ROM 형태로 고정되어 출하되므로, NIC에 고정된 MAC 주소를 변경하기는 어렵다.
        - 다만, MAC 주소도 메모리에 적재되어 구동되기 때문에 여러가지 방법을 이용하여 변경된 MAC 주소로 NIC를 동작시킬 수 있습니다.
    - 보안 상의 이유로 MAC 주소 변경을 막아놓은 운영체제도 있지만, 손쉽게 명령어나 설정파일 변경만으로 MAC 주소를 변경하는 운영체제도 있습니다.
        - Windows의 경우 Driver 상세 정보에서 MAC 주소 변경을 제공하기 때문에 쉽게 변경 가능하다.
        - Linux의 경우 GNU Macchanger/Linux 배포판의 Network 설정 파일에 MAC주소를 입력하면, 주소 변경이 가능하다.
# 참고
- LAN,WAN,Router
    - 최근엔 내부냐 외부냐로 LAN/WAN을 구분한다.
        - Router를 지나서 나가면 WAN, 지나기 전의 네트워크는 LAN이라 한다.