# Linux Booting System
## Systemd Service
- Linux System의 `Service 관리자`
    - Unix의 `init process`가 하던 작업을 대신 수행한다.
### 기능
1. 다양한 Service Daemon을 시작
2. Process들의 상태 유지
    - 모든 Process의 부모 역할을 한다.
        - 이 덕분에 `Zombie Process`나 `Orphan Process`를 처리할 수 있다.
3. System의 상태 관리
### Run Level
- System이 부팅될 때, 실행되는 `운영 모드`
    - 어떤 Service나 Process를 활성화할지 결정하는 단계
- Ubuntu는 `systemd` 방식을 사용하며, Run Level이라는 개념이 `target`으로 `대체`되었지만,`호환성`을 위해 `Run Level 개념이 공존`한다.

- `주요 Run Level` 번호
    1. 0 : `시스템 종료` 상태
    2. 1 : `시스템 복구 모드`(network 지원 X, root만 접속 가능)
    3. 2 : `Ubuntu의 기본 값`, 네트워크 기능을 포함한 `다중 사용자 모드`
    4. 3 : 2와 유사, 전통적으로 `text 기반의 다중 사용자 모드`
    5. 4 : Unused, `사용자가 임의로 정의`할 수 있는 `예비 레벨`
    6. 5 : `GUI가 포함`된 `다중 사용자 모드`
    7. 6 : 시스템 재시작 상태
- `Target` 방식
    - Run Level 번호대신 `Target 파일명을 사용`한다.
    - 종류
        1. `poweroff.target` : Run Level `0`
        2. `rescue.target` : Run Level `1`
        3. `multi-user.target` : Run Level `2~4` (Text Mode Multi User)
        4. `graphical.target` : Run Level `5` (GUI Mode Multi User)
        5. `reboot.target` : Run Level `6` (Reboot)
- 명령어
    1. 현재 Run Level 확인
        ```bash
        runlevel
        systemctl get-default
        ```
    2. Run Level 변경
        ```bash
        sudo systemctl isolate multi-user.target
        sudo systemctl isolate graphical.target
        ```
    3. 기본 부팅 모드 변경
        ```bash
        sudo systemctl set-default multi-user.target
        sudo systemctl set-default graphical.target
        ```
### Systemd의 장점
1. **Socket 기반 동작**
    - 과거에는 A 서비스가 B 서비스를 필요로 할 시, B가 완전히 켜질 때까지 A가 대기해야 했다.
    - Systemd는 부팅 시, 필요한 `socket`을 `미리 다 만들어둔다`. 즉, 서비스가 준비되지 않았더라도 `socket에 데이터를 넣어두면`, `Service가 구동되는 즉시 처리`한다.
        - 이 덕분에 `Service들`은 `동시에 실행이 가능`해져, 부팅 속도가 빨라짐.
2. **Shell과 독립적 부팅**
    - 기존에는 수많은 Shell Script를 `순차적으로 실행`하며 `부팅`, Shell Script는 실행 속도가 느리고, 복잡하여 오래걸림
    - Systemd는 `C언어로 작성된 binary 실행 파일`, Shell을 거치지 않고, `Kernel이 바로 Systemd를 실행`하므로, `오버헤드가 적고` `System 자원을 효율적으로 사용`
3. **Mount 및 하드웨어 제어 가능**
    - Linux에서 모든 것은 파일이다. Systemd는 하드웨어와 폴더를 하나의 유닛으로 묶어 관리한다.
    - 장점 : `특정 하드웨어에 장애가 발생`하면, 해당 `Unit만 중지 또는 격리가 가능`하여, 시스템 전체가 멈추는 `Kernel Panic` 등의 `현상을 방지`할 수 있고, `유지보수에 용이`하다.
4. **FSCK(File System Check)가 가능하다.**
    - 과거엔 부팅 시, 모든 파티션 체크
    - Systemd는 필요한 시점에만 Check를 수행하거나, 병렬로 처리한다.
        - 즉, 병목현상 개선
5. **Snapshot을 통한 System 상태 관리**
    - Snapshot : 복사본
    - `현재 실행 중인 서비스들의 상태를 저장`해두었다가, 나중에 `특정 상태로 한 번에 되돌릴 때 사용`한다. (systemctl snapshot 명령어 활용)
6. **Service에 대한 Singal 및 Control Group(Cgroups) 활용**
    - Systemd는 `Cgroups`라는 kernel 기능을 `활용`하여 `프로세스를 묶어서 관리`한다.
    - 특정 서비스가 자신 process를 많이 생성하더라도 `systemctl stop` 명령어 하나로 모든 자식 process까지 한 번에 종료할 수 있다.
7. **Clean Shutdown**
    - 전원 종료 전, User Session과 Process들에게 `SIGTERM`을 보내 안전하게 데이터를 저장할 시간을 제공한다.
    - 만약 SIGTERM에 대한 응답이 없다면, `일정 시간 후`, `SIGKILL`로 `강제 종료`하여 `File System 손상을 방지`한다.

### Systemd Unit
- Systemd는 Unit이라는 구성요소를 사용한다.
- 형태(서비스이름.유닛종류)
    - ex,
        1. `nginx.service` : 서비스 유닛
        2. `data.mount` : Directory 연결 유닛
- 종류
    1. `service` : 시스템 서비스 유닛, Daemon 시작/종료/재시작/로드
    2. `target` : `system의 상태를 정의`한다.
    3. `automount` : `directory 계층 구조`에서 `자동으로 마운트 포인트를 관리`한다.
    4. `device` : linux device tree에 있는 장치 관리
    5. `mount` : directory 계층 구조에서 mount point를 관리
        - auto mount와의 차이 : `자동 여부`
    6. `path` : 파일 시스템의 파일이나 디렉토리 경로를 관리
        - 특정 파일이나, Directory가 수정되었을 때, `특정 서비스를 실행`시키는` Trigger 역할`을 한다.
    7. `scope` : 외부에서 생성된 프로세스 관리
    8. `slice` : system process를 계층적으로 관리
        - `프로세스의 자원`(CPU,Memory 등) `제한을 설정`할 때 사용
        - System Service 용 Slice / User Service 용 Slice 등으로 나누어 자원 점유율을 조절한다.
    9. `socket` : 소켓을 관리하는 유닛
        - Process간 통신(IPC) 또는 네트워크 통신을 위한 Endpoint를 관리하는 것
        - 덕분에 Daemon이 아직 뜨지 않았어도, Socket Unit이 미리 Port를 열고 관리할 수 있게 해준다.
    10. `swap` : 스왑 장치 관리
        - Memory Swap을 의미한다.
            - 가상 메모리 구현을 위한 스왑
        - k8s에서는 Swap을 하지 않도록 한다.
            - k8s scheduler는 각 Container가 사용할 메모리 양을 정확히 계산해서 Node에 배치한다. 
                - 이때 Swap이 켜져있으면, 임의로 Disk를 사용하게 되고, 이러면 scheduler의 계산을 망쳐 성능 예측을 불가능하게 만든다.
            - 이를 적용하고자 하는 시도가 몇번 있었지만, 여전히 `swapoff`가 정석이다.
    11. `timer` : 타이머와 관련된 기능을 관리
### systemctl 명령
- 형식
    ```bash
    systemctl [옵션][명령][유닛이름]
    ```
    - 참고, 실행중인 모든 서비스 유닛 확인하기
        ```bash
        systemctl list-units --type=service
        ```
    - 참고2, 마운트 중인 모든 유닛 확인
        ```bash
        systemctl -a -t mount
        ```
    - 옵션
            - `-a` : 상태와 관계없이 유닛 전체 출력
            - `-t 유닛종류`: 유닛 종류만 출력
        - 명령
            - `start` : 지금 즉시 유닛 시작
                - 많이 사용
                - ex, maria db daemon 시작
                    ```bash
                    systemctl start mariadb
                    ```
            - `stop` : 유닛 중지
            - `reload`: 설정 다시 읽어오기 (설정 파일만 읽어오기)
                - 서비스 중단 없이 다시 읽어오므로, 운영중인 서버에서 많이 선호되는 방식이다.
                    - but, reload 되지 않는 서비스도 있기 때문에 그런 경우 restart를 사용해야 한다.
                - 설정은 맨 처음 시작할 때만 읽는다.
                    - 예를 들어, 터미널 실행 후, 환경 변수 변경시 적용이 안 된다. reload가 필요함. (restart도 가능)
                - ex, nginx 설정 변경 후 적용
                    ```bash
                    systemctl reload nginx
                    ```
            - `restart` : reload 하기 싫으면 해라 (껐다가 다시 키기)
                - 껐다가 다시 키는 것이므로 PID가 새롭게 설정된다. 서비스가 잠시 중단되기 때문에 User가 끊김을 경험할 수 있다.
                - 많이 사용
                - ex, nginx 설정 변경 후, 재시작
                    ```bash
                    systemctl restart nginx
                    ```
            - `status` : 유닛 상태 및 최근 로그를 확인
                - 사용 상황 : 서비스가 죽었을 때 가장 먼저 확인하는 명령
                - 많이 사용
                - ex, 웹 죽었을 때, nginx 현재 상태 및 로그 확인
                    ```bash
                    systemctl status nginx
                    ```
            - `enable` : 부팅 시, 자동 시작하는 유닛으로 등록
                - 많이 사용
                - ex, 부팅 시, nginx가 자동 시작되도록
                    ```bash
                    systemctl enable nginx
                    ```
            - `disable` : 부팅 시, 시작하지 않도록 등록
                - ex, 부팅 시 nginx 시작되지 않도록
                    ```bash
                    systemctl disable nginx
                    ```
            - `mask/unmask` : disable보다 강한 금지
                - Unit을 아예 Mask처리하여, 다른 서비스가 부르거나 실수로 root가 start 하더라도 켜지지 않음
            - `is-active` : 유닛이 동작하고 있는지 확인
                - 확인용으로 주로 사용한다.
                    ```bash
                    systemctl status is-active nginx
                    systemctl status is-enabled nginx
                    ```
            - `is-enabled` : 유닛이 시작했는지 확인
            - `isolate` : 해당 유닛만 시작하고 나머지 정지
                - 사용 상황 : Target 변경에 사용
                    - ex, GUI->textmode
                        ```bash
                        systemctl isolate multi-user.target
                        ```
            - `kill` : unit에 signal을 전송
                - ex, nginx 강제 종료
                    ```bash
                    systemctl kill -s SIGKILL nginx
                    ```
## Systemd Service 등록
- `Ubuntu에서 서비스 등록`은 `Systemd 서비스를 이용`한다.
- 단계
    1. `/etc/systemd/system`에 `.service 파일 생성`
    2. `systemctl daemon-reload` 명령어 수행 (서비스 등록)
    3. `systemctl enable` 명령어 수행 (서비스 자동 수행)
### Service 파일의 구성
```bash
[Unit] # 서비스 간의 관계 및 의존성 정의
Description=설명
After/Before=해당 유닛 실행 후, 서비스가 실행되도록 설정 #대부분의 네트워크 서비스에서 설정함. 네트워크가 안 잡힌 상태로 실행하면 Address Not Found Error 발생하기 때문
Requires=유닛이 시작될 때, 여기에 명시된 유닛도 반드시 함께 시작 #강한 의존성을 형성, ex, DB가 반드시 필요한 Web서버 동작시
Wants=함께 시작하려 시도, 명시된 유닛이 실패해도, 서비스 실행 #약한 의존성, ex,로그 수집기 등 없어도 서비스는 돌아가야할 때 설정
Condition...=실행조건 #condition 종류가 다양함. ex, ConditionPathExists=~~~ 라 작성하면 ~~ 파일이 있을 때만 실행하라 라는 의미

[Service] # 서비스의 실제 동작 정의
Type=실행방식
ExecStartPre/ExecStartPost=메인 서비스 시작 전 후에 실행할 명령
Restart=재시작정책
KillMode=본인만 죽일지/자식까지 죽일지
[Install] #서비스 등록 및 자동 시작 설정 (enable 명령 때 참조되는 부분)
WantedBy=서비스가 어떤 Target에서 시작될 지 결정
RequiredBy=서비스를 활성화하면 명시된 서비스도 이 서비스를 필요로 하게 함(복잡해지기에 잘 사용하지 않음)
Alias=별명설정(서비스의 다른 이름)
```
- 위 외에도 매우 많다. (나중에 한 번 제대로 정리해야 할 듯)

### 예시
```bash
[Unit]
Description=High Availability API Server
After=network.target mysql.service
# DB가 반드시 있어야 하므로 강한 의존성 추가
Requires=mysql.service

[Service]
Type=simple
User=api-user
Group=api-group
WorkingDirectory=/var/www/api

# 실행 전 임시 파일 정리
ExecStartPre=/usr/bin/rm -rf /tmp/api-cache/*
ExecStart=/usr/bin/python3 main.py

# 재시작 전략: 죽으면 3초 뒤에 무조건 다시 살림
Restart=always
RestartSec=3

# 보안 및 자원 제한: 파일은 최대 6만개, 메모리는 1GB만 써라
LimitNOFILE=65535
MemoryMax=1G

[Install]
# 부팅 시 일반 다중 사용자 모드에서 자동 실행
WantedBy=multi-user.target
```

## Systemd 종료
- `Linux` " 대부분 `Server OS`
    - 따라서 `정상적 System 종료`가 중요하다.
        - 비정상적인 종료로 문제가 생기면 Service를 제공할 수 없기 때문
### 종류
1. Shutdown 명령
    - 실무에서 가장 권장되는 방식
    ```bash
    shotdown [옵션][시간][메시지]
    ```
    - 옵션
        1. `k` : 사용자들에게 메시지만 전달 (종료 X, 예고)
        2. `r` : 재시작
        3. `h` : 종료하고 halt상태(RunLevel 0)으로 이동
        4. `f` : 빠른 재시작 fsck 수행 X
        5. `c` : shutdown 명령 취소

    - 시간
        1. hh:mm
        2. now : 즉시 종료
2. RunLevel 변경해서 종료
    - 잘 안 씀
    ```bash
    sudo init 0
    sudo init 6
    ```
    - 종료
        ```bash
        sudo systemctl isolate poweroff.target
        sudo systemctl isolate runlevel0.target
        ```
    - 재시작
        ```bash
        sudo systemctl isolate reboot.target
        sudo systemctl isolate runlevel6.target
        ```
3. systemctl 명령의 Symbolic link로 종료
    - 아래의 모든 폴더가 /bin/systemctl로 연결되어 있다.
    1. halt
        ```bash
        /sbin/halt
        ```
    2. poweroff 
        ```bash
        /sbin/poweroff
        ```
    3. reboot
        ```bash
        /sbin/reboot
        ```
### 팁
- 안전한 종료를 위한 체크
    1. 현재 접속 중인 user 체크
        ```bash
        who
        w
        ```

    2. 로그확인
        ```bash
        tail -f /var/log/syslog
        ```
        - 서비스가 잘 멈추는지 모니터링
# Daemon Process
- `Linux Background에서 동작`하며, `특정한 서비스를 제공`하는 Process
- `Server로 사용`되는 `대부분의 Process`가 `Daemon`이다.
- 이름 규칙 : `끝에 d`가 붙는다. (Daemon이라는 표시)
- 특징 
    - 사용자와 직접 `상호작용 하지 않기에` `제어 터미널이 없다.`
        - ps -ef에서 tty : ?로 나오는 것이 모두 Daemon
- 종류
    1. `독자형` :Daemon 혼자서 스스로 동작
        - System Background에서 동작
        - 트래픽이 많고, 빠른 응답이 필요한 서비스는 대부분 `독자형`
    2. `Super Daemon`에 의해 동작
        - 현재는 거의 사용하지 않음 (RAM 값의 저하, 빠른 응답 중요)
        - `Systemd 자체`가 `Socket Activation`을 통해 `Super Daemon의 역할`을 `대체`

### Systemd Daemon
- 모든 Process의 부모
    - 부팅 시, 커널이 가장 먼저 만드는 Process
    - PID 1번
- pstree 명령(process의 트리구조 확인)으로 확인할 수 있다.
- 참고
    1. 기본적으로 Process들은 격리
        - 서로 다른 Process의 Memory를 볼 수 없다.
        - 따라서, Process끼리 통신하기 위해선 RPC, 메모리 공유, IPC 등의 작업을 이용한다.
### Kernel Thread Daemon
- 실행 파일이 존재하는 일반 Daemon과 달리, `Kernel Source Code내에 포함된 함수들`을 말한다.
- ps 명령으로 확인할 때, []에 들어있는 Process 들
    ```bash
    root           2       0  0 Jan07 ?        00:00:00 [kthreadd]
    root           3       2  0 Jan07 ?        00:00:00 [rcu_gp]
    ```
- 대부분 `입출력`/`메모리 관리`/`디스크 동기화` 등을 수행하며, `낮은 번호의 PID`를 가진다.

### 주요 Daemon

-  Daemon을 이해하면 좋은 점
    1. 보안 강화 및 자원 최적화
    2. 장애 복구 원인 파악 시간 줄여줌
    3. 자동화 시스템 구축 (crond)

#### 자동화 / 스케줄링 관련
- `atd` : `특정 시간에 실행`되도록 예약한 명령을 실행하도록 해주는 Daemon
    - `일회성` 예약 작업 처리기 (`한 번만 실행될 작업`에 사용)
- **`crond`** : `주기적으로 실행`되도록 예약한 명령을 실행하도록 해주는 Daemon
    - 실무에서 `백업`,`로그 정리`,`정기 결제`등에 필수적으로 사용된다.
#### 네트워크 설정 및 관리 관련
- `dhcpd` : `IP 주소 자동 할당`
    - `새로운 컴퓨터`가 `네트워크에 연결`될 때, `남는 IP를 빌려주고 관리`
- `routed` : 자동 `IP 라우터 테이블 제공`
    - 네트워크 `패킷`이 `목적지까지 가는 경로`를 `자동으로 갱신하고 관리`
#### 파일 공유 및 전송 관련
- `nfs` : 네트워크 파일 시스템 서비스 제공
    - 멀리 떨어진 서버의 하드디스크를 나에게 있는 것처럼 사용할 수 있게 함
- `smb` : 삼바 서비스 제공
    - linux와 window 운영체제 간 File/Printer 공유할 수 있도록 함
- `ftpd` : 파일 송수신 서비스
    - FTP 프로토콜을 이용하여 파일을 업로드/다운로드 할 수 있게 함
#### 웹 및 도메인 관련
- **`httpd`** : 웹서버
    - Apache가 대표적
    - web brower가 요청하는 웹 페이지 정보를 전달해주는 역할
- `named` : DNS
    - DNS 서버
    - 문자열 주소를 IP 주소로 변환해준다.
#### 이메일 관련
- `sendmail` : 메일 전송 데몬
- `smtpd` : 메일 전송 데몬
    - 이메일을 보내는(SMTP) 역할 (sendmail/smtpd)
- `popd` : 기본 메일 서비스
    - 도착한 메일을 User Computer로 가져오는 역할
#### 시스템 관리 및 보안 관련
- `syslogd` : 로그기록 정보 제공
    - 시스템에서 발생하는 `모든 log를 수집하여 저장`
    - 문제가 생겼을 때, 원인을 찾는 기록 보관소
- **`sshd`** : 보안 쉘
    - 멀리 떨어진 서버에 원격 접속하여 명령을 내릴 수 있게 해줌
    - 데이터가 암호화되어 전송되므로 안전하다.
    - 22번 포트를 사용한다.
- `ntpd` : 시간 동기화 서비스
    - 서버 시간을 인터넷 표준 시간 서버와 동기화 

# Boot Loader
- Kernel을 Memory에 Loading하는 역할 수행
- Linux에서는 `LILO`와 `GRUB` 존재, Ubuntu : GRUB
- GRUB (Grand Unified Bootloader)
    - LILO의 단점을 보완
- GRUB 장점
    1. LILO : Linux에서만 사용 가능. GRUB : Window에서도 사용 가능
    2. 설정과 사용이 편리
    3. 부팅할 때 명령을 사용하여 수정 가능
    4. 멀티 부팅 기능 제공
- 최신 버전 : GRUB2
- 관련 디렉토리 및 파일 (조심히 다뤄야 함)
    - /boot/grub/grub.cfg
        - 직접 수정 불가
        - 해당 파일이 `/etc/default/grub`과 `/etc/grub.d` Directory 아래에 있는 Script를 읽어서 생성
            - `/etc/grub.d` : GRUB 관련 Script를 가진다.
            - `/etc/default/grub` : GRUB 메뉴에 설정 내용이 저장되어 있다.
        - 파일의 내용을 수정하고자 하는 경우, `위의 파일`과 `Directory 안에 있는 파일`을 수정
- Root 암호 잃어버림
    1. GRUB 메뉴 초기화면 출력
    2. e를 눌러서, `편집 모드` 전환
    3. 아래에 `ro splash $vt_handoff 부분`을 `rw init=/bin/bash`로 수정
    4. 재부팅 시, 비밀번호 없이 root 계정 로그인

# Namespace
- Linux에서 Process에게 독립적 공간을 만들어주는 기술
    - 프로세스가 실행될 때 시스템의 자원을 논리적으로 분리하여 마치 `자신이 독립된 컴퓨터에서 돌아가고 있는 것처럼 착각`하게 한다.
- linux kernel 수준에서 제공
## 종류
### Mount(mnt)
- 격리 대상 : 파일 시스템
- 역할 : `프로세스`마다 `다른 Mount Point`(Directory 구조)를 가진다.
### Process id(PID)
- 격리 대상 : Process ID
- 역할 : 독립된 PID 번호 체계
### Network(net)
- 격리 대상 : Network
- 역할 : 독립된 IP, 라우팅 테이블, 방화벽 설정
### Interprocess(ipc)
- 격리 대상 : 공유 메모리
- 역할 : 프로세스 간 통신(IPC) 자원 격리
### UTS
- 격리 대상 : 호스트 명
- 역할 : 독립된 호스트 이름 및 도메인 이름 설정
### User(user)
- 격리 대상 : 사용자/그룹
- 역할 : 방 안의 일반 사용자가 밖에서는 Root 권한을 가질 수 있음
### Cgroup
- 격리 대상 : 제어 그룹
- 역할 : 프로세스가 사용하는 리소스 제한 보임.

## 활용
### Container 기술
- Docker : Namespace 기술을 쉽게 사용할 수 있도록 만든 도구
    - Docker로 한 서버에서 80번 포트에 여러 개의 nginx를 띄울 수 있는 것은 `Network Namespace`로 `네트워크 환경을 분리`했기 때문
### 보안 Sandbox
- 특정 Application이 해킹당하더라도 전체 시스템으로 피해가 확산되지 않는다.
    - 의심스러운 웹 페이지나 프로그램을 다운로드 받을 때, `User/Mount Namespace를 활용`하여 `실제 시스템 파일에 접근하지 못하도록 격리`된 환경에서 진행한다.
### 가상 네트워크 구축
- Cloud 환경에서 가상 Router나 Switch를 만들 때 사용한다.
    - 물리적인 랜카드는 1개지만, Network Namespace를 여러 개 생성하여, 각각에 가상 IP를 할당하고, 독립적인 방화벽을 구축할 수 있다.
### 네임스페이스 실습
1. ip 확인
    ```bash
    kingrange@kilwon:~$ ip addr
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
    2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:e7:d2:6a brd ff:ff:ff:ff:ff:ff
        inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
        valid_lft 16531sec preferred_lft 16531sec
        inet6 fd17:625c:f037:2:a00:27ff:fee7:d26a/64 scope global dynamic mngtmpaddr noprefixroute
        valid_lft 86123sec preferred_lft 14123sec
        inet6 fe80::a00:27ff:fee7:d26a/64 scope link
        valid_lft forever preferred_lft forever
    ```
2. red라는 이름의 Network namespace 생성
    ```bash
    kingrange@kilwon:~$ sudo ip netns add red
    [sudo] password for kingrange:
    ```
3. 네트워크 확인
    ```bash
    kingrange@kilwon:~$ sudo ip netns exec red ip addr
    1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    ```
## Container / Namespace
- Container는 Namespace를 통해 `자원을 격리`하고, cgroup을 통해 `자원 사용량`을 제한하여 `독립된 환경`처럼 작동하게 만든 Process 단위

# Cgroup
- Control Groups
- `자원`을 얼마나 쓸 수 있는지 결정
- `/sys/fs/cgroup`으로 관리된다.
    
## 핵심 개념
- `프로세스들의 집합`에 대해 `시스템 자원의 할당`을 `제어`하고 `감시`하는 `Linux Kernel 기능`
## 주요 기능
1. 자원 제한(Resource Limiting) : 특정 프로세스가 메모리를 1GB이상 사용하지 못하도록 막음
2. 우선순위(Prioritization) : 중요한 작업에 CPU 시간을 더 할당
3. 회계(Accounting) : 어떤 그룹이 자원을 얼마나 사용했는지 모니터링
4. 제어(Control) : 한 번의 명령으로 그룹 내 모든 Process를 정지시키거나 재시작
## Sub Process
### CPU / cpuset / cpuacct
- 계산 능력 통제
- 특정 프로세스가 CPU 코어 중 몇 번만 쓸지(cpuset)
- 얼마나 점유할지(CPU)
- 얼마나 썼는지 보고(cpuacct)
### Memory
- 메모리 폭주 방지
- 프로세스가 RAM을 다 써서 서버가 뻗는 것을 막는 가장 중요한 설정
### Freezer
- 일시 정지 버튼
- 프로세스를 종료하지 않고 잠시 멈췄다가 나중에 다시 재개
    - (예: 컨테이너 스냅샷/백업 시)
### blkio
- 디스크 속도 제한
- 특정 프로그램이 하드디스크를 너무 세게 읽어서 다른 프로그램이 버벅대는 걸 방지
    - (초당 Read/Write 제한)
### net_cls
- 네트워크 우선순위
- 특정 서비스의 데이터 패킷에 '이름표'를 붙여서, `중요한 데이터 먼저 보내게 설정`
### devices
- 하드웨어 접근 권한
- `특정 프로세스`가 그래픽카드(GPU)나 `특정 하드웨어에 접근`할 수 있는지 `결정`

## 실무적 예시 
- 공유 서버의 자원 독점 문제를 해결할 수 있다.
    - `cgroup이 없을 때` : 어떤 하나의 process가 `CPU를 100% 점유`하면, 실제 고객이 접속하는 `웹 서비스가 응답불능 상태에 빠진다.`
    - `cgroup이 있을 때` : process를 특정 group에 넣고, CPU 최대 사용량을 제한한다. 아무리 process가 튀어도 70%의 CPU가 남으므로, 안정적 서비스 제공이 가능하다.

## 예시
### Memory 제한 설정
1. cgroup directory 생성
    ```bash
    sudo mkdir /sys/fs/cgroup/test_cgroup # test_cgroup 생성
    ```
2. 메모리 제한 설정 (100MB)
    ```bash
    echo 100M | sudo tee /sys/fs/cgroup/test_cgroup
    ```
3. 그룹 등록
    ```bash
    # 이 그룹에 현재 쉘의 PID를 등록
    echo $$ | sudo tee /sys/fs/cgroup/my_limit/cgroup.procs
    ```
### Disk 속도 제한
1. 내 Disk Major:Minor번호 확인
    - Major 번호 : 장치의 종류(카테고리)
        - 해당 장치를 다루기 위해 어떤 Driver를 사용해야 하는지 알려주는 용도
    - Minor 번호 : 같은 종류의 장치들 중 구분하는 용도
    ```bash
    lsblk
    ```
2. cgroup 생성 및 제한 설정
    - io.max 파일을 이용해 Disk의 최대 속도(10MB)를 제한한다.
    ```bash
    sudo mkdir /sys/fs/cgroup/1MV
    echo "8:0 wbps=1048576" | sudo tee /sys/fs/cgroup/test_disk_limit/io.max
    ``` 
3.  속도 측정
    1. 제한 X
        ```bash
        dd if=/dev/zero of=test_file_normal bs=1M count=50 oflag=direct
        ```
    2. 제한 O
        ```bash
         # 현재 쉘 등록
        echo $$ | sudo tee /sys/fs/cgroup/test_disk_limit/cgroup.procs
         # 실행 (50초 걸림)
        dd if=/dev/zero of=test_file_normal bs=1M count=50 oflag=direct
        50+0 records in
        50+0 records out
        52428800 bytes (52 MB, 50 MiB) copied, 50.005 s, 1.0 MB/s
        ```


# File System & Disk Mangament
## Linux File System
- Disk 기반 파일 시스템
    - `파일`과 `Directory`를 `관리`하려면, `파일 시스템`이 필요하다.
- Linux는 초기 `Minix File System`을 사용했으나