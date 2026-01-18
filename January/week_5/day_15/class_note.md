# 0112

# Linux
## Linux Booting System
### Systemd Service
- Linux system의 Service 관리자
    - Unix의 init Process가 하던 작업을 대신 수행
- 기능
    - 다양한 Service Daemon을 시작
    - Process들의 상태 유지
        - 모든 프로세스의 부모 역할
            - 덕분에 Zombie Process, Orphan Process를 처리할 수 있다.
    - System의 상태 관리
- init과 관련된 script 파일은 /etc/init.d directory에 존재한다.
    - 아직은 공존 중이다.
- Run Level
    - init process가 system의 상태를 정의하는 7개 구분 방식
        - 이 상태에 따라 Shell script를 실행함.
    - 이건 알아두기  -> Gemini 로 정리

- init을 안 쓰고 Systemd를 사용하는 이유(Systemd의 장점)
    1. Socket 기반 동작
        - inetd와 호환성을 유지함
    2. `Shell`과 `독립적인 Booting이 가능`하다.
    3. Mount 제어가 가능하다.
        - 하드웨어를 폴더와 연결하는 것
        - 장점 : Hardware와 문제가 생겼을 때, 문제가 생긴 Hardware를 격리시키며 작업이 가능하다.
    4. FSCK(File System Check) 제거가 가능하다.
    5. System 상태에 대한 Snapshot을 제공한다.
        - Snapshot: 복사본
    6. Service에 Signal을 줄 수 있다.
    7. Shut down 전에, User Session의 안전한 종료가 가능하다.

- Systemd Unit
    - Systemd는 Unit이라는 구성요소를 사용한다.
    - 관리 대상을 Service이름.Unit종류 형태로 관리한다.
    - 종류
        1. service : 시스템 서비스 유닛, Daemon 시작/종료/재시작/로드
        2. target : Unit을 그룹화
        3. automount : `directory 계층 구조`에서 `자동으로 마운트 포인트를 관리`한다.
        4. device : linux device tree에 있는 장치 관리
        5. mount : directory 계층 구조에서 mount point를 관리
            - auto mount와의 차이 : `자동 여부`
        6. path : 파일 시스템의 파일이나 디렉토리 경로를 관리
        7. scope : 외부에서 생성된 프로세스 관리
        8. slice : system process를 계층적으로 관리
        9. socket : 소켓을 관리하는 유닛
            - NIC(Network Interface Card)를 추상화 한 것
                - NIC : Hardware
            - OS가 NIC를 사용하려면 Software 개념으로 바꿔야 한다. 이를 위해 추상화를 한 것
        10. swap : 스왑 장치 관리
            - Memory Swap을 의미한다.
                - 가상 메모리 구현을 위한 스왑
                    - K8S에서는 Swap 구현이 안된다.
                        - k8s에 올라와있는 모든 application은 항상 수행되어야 하기 때문
                        - Memory Swap을 안하도록 설정해야 한다. (속도는 느려짐)
                
        11. timer : 타이머와 관련된 기능을 관리
- systemctl 명령
    - 형식 : systemctl [옵션][명령][유닛이름]
        - 옵션
            - `-a` : 상태와 관계없이 유닛 전체 출력
            - `-t 유닛종류`: 유닛 종류만 출력
        - 명령
            - `start` : 유닛 시작
                - 많이 사용
                - ex, maria db daemon 시작
                    ```bash
                    systemctl start mariadb
                    ```
            - `stop` : 유닛 중지
            - `reload`: 설정 다시 읽어오기
                - 설정은 맨 처음 시작할 때만 읽는다.
                    - 예를 들어, 터미널 실행 후, 환경 변수 변경시 적용이 안 된다. reload가 필요함.
                - 유사하게, `system 환경 설정 파일을 수정`하면, `source 명령으로 재로드를 수행`해야 한다.
            - `restart` : reload 하기 싫으면 해라
                - 많이 사용
            - `status` : 유닛 상태를 확인
                - 많이 사용
            - `enable` : 부팅 시, 시작하는 유닛으로 등록
                - 많이 사용
            - `disable` : 부팅 시, 시작하지 않도록 등록
            - `is-active` : 유닛이 동작하고 있는지 확인
            - `is-enabled` : 유닛이 시작했는지 확인
            - `isolate` : 해당 유닛만 시작하고 나머지 정지
            - `kill` : unit에 signal을 전송

### Systemd 서비스 등록
- ubuntu에서 서비스 등록은 Systemd 서비스를 이용하는 것이 일반적이다.
- `/etc/systemd/system`에 `.service 파일을 생성`하고, `systemctl daemon-reload` 그리고 `systemctl enable` 명령어를 수행해서 service를 등록하고 활성화 시킴
- 파일의 구성
    ```bash
    [Unit]
    Description=My custom service # 섦ㅕㅇ
    After=network.target

    [Service]
    ExecStart = /path/to/your/script/service.sh
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target
    ```
    - Unit : 서비스의 메타 데이터와의 의존성을 정의
        - After=network.target은 서비스가 시작되기 전에 Network Service가 먼저 실행되어야 한다.
    - Service : 실행할 Script 파일의 경로와 실패했을 때 재시작하는 정책 설정
    - Install : 서비스가 부팅 시, 자동으로 시작하도록 하는 분을 정의/ WantedBy에 런레벨 설정 가능

- 서비스 등록 및 활성화
    - 서비스 등록
        - 새로운 서비스 파일을 읽어서 service daemon을 다시 시작
        ```bash
        systemctl daemon-reload
        ```
        - 서비스 관리 명령을 사용해서 활성화하거나 비활성화
### Systemd 종료
- `Linux`는 `대부분 Server OS`로 사용되기 때문에 `비정상적`으로 `System을 종료`해서 문제가 생기면, `서비스를 제공하지 못할 수 있다.`
- 방식
    1. shutdown 명령
    2. halt 명령
    3. poweroff 명령
    4. Runlevel을 0이나 6으로 전환
    5. reboot 명령
    6. 전원 차단

#### shutdown 명령
```bash
shutdown [옵션][시간][메시지]
```
- 옵션
    1. `k` : 사용자들에게 메시지만 전달
    2. `r` : 재시작
    3. `h` : 종료하고 halt상태(RunLevel 0)으로 이동
    4. `f` : 빠른 재시작 fsck 수행 X
    5. `c` : shutdown 명령 취소

- 시간
    1. hh:mm
    2. now : 즉시 종료

- k나 h 옵션을 사용하면 Message만 전송하고 종료되지 않음

#### RunLevel 변경해서 종료
- 잘 안씀
- sudo init 0 또는 sudo init 6
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

#### Systemctl 명령의 Symbolic link로 종료하기
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
## Daemon Process
- Linux Background에서 동작하며, 특정한 서비스를 제공하는 Process
- Server로 사용되는 Process들이 대부분 Daemon
- 종류
    1. Daemon 혼자서 스스로 동작하는 `독자형`
        - System의 Background에서 동작
        - 자주 호출되는 Daemon이 아니라면, 자원을 낭비한다.
    2. Daemon을 관리하는 Super Daemon에 의해 동작하는 방식
        - 평소에는 `Super Daemon만 동작`하다가 `서비스 요청이 오면`, Super Daemon이 `해당 Daemon을 동작`시키는 것
        - `독자형`보다는 `서비스에 응답하는데 시간이 걸림`, 다만 `자원 절약` 가능
### Super Daemon
- Daemon의 종류가 늘어나자 이를 관리하기 위해 등장
    - Network Service를 제공하는 Daemon만 관리
        - 사용자가 Network 서비스를 요청하면, Super Daemon이 이를 받아서 해당하는 서비스 Daemon을 동작시킴
- Unix의 Super Daemon : inetd / Ubuntu는 보안 기능이 포함된 `xinetd`
### Systemd Daemon
- init을 대체한 Daemon
- 대다수 프로세스의 조상 프로세스
- pstree 명령(프로세스의 트리구조 확인)으로 확인할 수 있다.
- 참고
    1. 기본적으로 Process 들은 격리
        - 때문에 Process 끼리 통신하기 위해서는, RPC, 메모리 공유 등의 작업이 필요하다.
### Kernel Thread Daemon
- Kernel의 일부분을 Process처럼 관리하는 Daemon
- ps 명령으로 확인할 때, []에 들어있는 Process들
- 대부분 `입출력`/`메모리 관리`/`디스크 동기화` 등을 수행, 낮은 번호의 PID를 가진다.

### 주요 Daemon
- `atd` : 특정 시간에 실행되도록 예약한 명령을 실행하도록 해주는 Daemon
- `cron` : 주기적으로 실행되도록 예약한 명령을 실행하도록 해주는 Daemon
- `dhcpd` : 동적 IP 주소 할당
- `httpd` : 웹서버
- nfs : 네트워크 파일 시스템 서비스 제공
- named : DNS
- sendmail : 메일 전송 데몬
- smtpd : 메일 전송 데몬
- popd : 기본 메일 서비스
- routed : 자동 IP 라우터 테이블 제공
- smb : 삼바 서비스 제공
- syslogd : 로그기록 정보 제공
- sshd : 원격 보안 서비스 제공
- ftpd : 파일 송수신 서비스
- ntpd : 시간 동기화 서비스

## Boot Loader
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

## Namespace & Cgroup
### Container 기술
- Application을 효율적이고, 독립적으로 실행할 수 있는 경량화된 환경을 제공
- 컨테이너 기술의 근간이 되는 기술 3가지
    1. Cgroup (Control Group)
    2. Namespace
    3. Union Mount Filesystem

### Cgroup
- Process들이 사용하는 시스템 자원의 사용정보를 수집 및 제한시키는 커널의 기능
- 어떤 Process가 자원을 얼마나 사용하는지 확인하고 관리할 수 있음
- 사용 가능한 SubSystem
    1. CPU
        - 자동화를 위해 실제 작업에서는 명령어로 수정해줘야 한다.
            ```bash
            ex, echo "50000 100000" | sudo tee /sys/fs/cgroup/mygroup/cpu.max
             # sudo tee -> 입력 리다이렉션과 같이 뒤에 오는 경로에 입력 해주는 것이다.
            ```
    2. Memory
    3. Freezer : cgroup의 작업을 일시 중지하거나 다시 시작
    4. blkio : Block 장치에 대한 I/O를 제한
    5. net_cls : Traffic Controler가 특정 cgroup 작업에서 발생하는 패킷을 식별하게 하는 Network Packet Tag를 지정
    6. cpuset : 개별 CPU 메모리 노드를 cgroup에 할당
    7. cpuacct : CPU 자원 보고서 생성
    8. devices : cgroup의 작업 단위
    9. ns : namespace 서브 시스템#

### Namespace
- Process를 격리하기 위해 사용하는 Kernel의 기능
- Docker와 같은 Container 기술의 핵심 기반
- "이름을 붙여 구분해보자."의 개념

# File System & Disk Management
## Linux File System
- Disk 기반 파일 시스템
    - `파일`과 `Directory`를 `관리`하려면 `파일 시스템이 필요`하다.
- Linux는 초기 Minix File System(MFS)을 이용했으나, 현재는 ext 파일 시스템으로 알려진 Linux 고유의 파일 시스템을 만들어 사용한다.
    - ext 파일 시스템은 계속 버전이 업그레이드되며, 현재는 ext4까지 제공
    - 대용량 파일 시스템을 위한 XFS 파일 시스템도 도입되었다.
- 파일 : i-node로 관리
- Directory : 단순히 파일 목록을 가진 파일
- 특수 파일을 통해 장치 접근
### 하나의 파일 시스템 구성
- 하나의 파일 시스템으로 구성할 경우, `/`에 File System을 연결
    - Windows는 Drive별로 파일 시스템을 연결
- 여러 파일 시스템으로 구성도 가능
    - 방식 : 파일 시스템 하나는 `/`에 연결, 다른 하나는 `/usr`에 연결하는 형태
        - Q. 왜 그렇게 함?
        - A. 여러 개의 디스크나 여러 개의 파티션을 서로 간에 간섭없이 사용하기 위해
###  종류
1. ext4
    - 1EB(1024*1024TB = 1PB) 이상의 볼륨과 16TB이상의 파일 지원
        - `Directory 개수`도 `32000 -> 64000`으로 증가
        - `온라인 조각 모음`도 제공
    - 효율적으로 디스크를 사용하기 위해 저장 장치를 논리적인 `블록의 집합`으로 구분한다.
        - 일반적으로 블록은 4KB
        - 블록 그룹의 개수 = 장치 크기/블록 크기
2. XFS
    - eXtended File System
    - 64비트 파일 시스템, 최대 16EB 지원
    - 우분투에서 사용하기 위해서는 xfsprogs라는 패키지 필요

### Linux에서 지원하는 File System
1. msdos
2. iso9660 : CDROM, DVD 등의 읽기 전용 파일시스템
3. nfs : 원격 서버의 디스크를 연결할 떄 사용

### 특수 용도의 가상 파일 시스템
1. swap
    - swap 영역을 관리하기 위한 파일 시스템
    - RAM을 보완하여 부족한 메모리를 Disk 공간으로 확장하고, 시스템이 안정적으로 동작하도록 돕는 역할
2. tmpfs
    - Temporary File System으로 Memory에 임시 파일을 저장하기 위한 파일 시스템
    - 시스템이 재시작할 때 기존 내용이 소멸된다.
    - /tmp 디렉토리
3. ramfs
    - 디스크 대신 메모리를 저장 공간처럼 활용하는 가상의 파일 시스템
    - 임베디드 장치나 테스트 용도로 사용, tmpfs와다른점은 tmpfs는 메모리를 사용하지만 필요시 swap을 이용한다.
4. rootfs
    - RootFileSystem
    - 시스템 초기화 및 관리에 필요한 내용 저장
5. proc
    - /proc 디렉토리
    - kernel의 현재 상태를 나타내는 파일을 소유
    - Linux의 가상 파일 시스템으로 Kernel과 Process 관련 정보를 사용자 공간에서 확인할 수 있도록 제공
    - 실제 디스크에 저장된 파일이 아니고, `메모리에 존재`하는 인터페이스
    - 주요 내용
        1. `/proc/cpuinfo` - `CPU 정보`
        2. `/proc/meminfo` - `메모리 정보`
        3. `/proc/uptime` - `부팅 후 경과시간`
        4. `/proc/loadavg` - `시스템 평균 부하`
        5. `/proc/[PID]/status` - `특정 프로세스 상태`
        6. `/proc/sys/net/ipv4/ip_forward` - `패킷 포워딩 여부`
### 현재 시스템에서 지원하는 파일 시스템 확인
```bash
cat /proc/filesystems
```
### i-node 구조
- 파일에 대한 정보를 저장한 자료구조
- i-node 구성
    1. 파일 정보를 저장하는 부분
        - 파일 종류, 파일 접근 권한, 파일 크기, 소유자, 접근 및 수정 시간
    2. 실제 파일 내용이 저장된 데이터 블록의 주소를 저장하는 부분
        - 직접 블록, 간접 블록, 이중 간접 블록 등
            - 직접 블록 :

- 참고
    1. 기본 구조 
        - 파일이름(유일무이) -> i-node -> 데이터 블록
        - Symbolic link는 여기서 파일 이름으로 연결해주는 것이고. Hardlink는 여기서 inode로 연결해주는 것이다.
    2. 파일 삭제 명령은 i-node의 reference count를 1 감소 시키는 것이다.
        - i node의 reference count가 0이 되면, i node가 삭제된다.
            - i node가 삭제되면, 연결된 파일 경로도 전부 삭제된다.
            - Data Block은 연결된 i-node가 없다면, 읽기 기능이 사라지고, 할당만 가능하도록 변경된다.
# 파일 시스템 마운트
- 파일 시스템이 Directory 구조와 연결되지 않으면, 사용자가 해당 파일 시스템에 접근할 수 없음
- 파일 시스템을 Directory 계층 구조의 `특정 Directory에 연결하는 것`을 `Mount`라고 한다.
## 마운트 포인트
- Directory 계층 구조에서 File System이 연결되는 Directory
## 파일 마운트 설정 파일
- Linux에 System이 부팅될 떄, 자동 마운트가 되게 하려면 
    - `/etc/fstab` 파일에 관련 사항을 설정한다.
        - `/etc/fstab` 파일의 구조
            1. 장치 이름
            2. 마운트 포인트
            3. 파일 시스템 종류
            4. 옵션 
                - defaults: 일반적인 파일 시스템에 지정하는 속성으로 rw, nouser, auto, exec, suid 속성을 모두 포함
                - auto: 부팅 시 자동으로 마운트
                - exec: 실행 파일이 실행되는 것을 허용
                - suid: setuid, setgid의 사용을 허용
                - ro: 읽기 전용 파일 시스템
                - rw: 읽기 및 쓰기가 가능한 파일 시스템
                - user: 일반 사용자도 마운트가 가능하다
                - nouser: 일반 사용자의 마운트가 불가능하고 root 만 마운트 가능
                - noauto: 부팅 시 자동으로 마운트하지 않음
                - noexec: 실행 파일이 실행되는 것을 허용하지 않음
                - nosuid: setuid, setgid 의 사용을 금지
                - usrquota: 사용자 별로 디스크 쿼터 설정이 가능
                - grpquota: 그룹 별로 디스크 쿼터 설정이 가능
            5. 덤프 관련 설정
                - 0 : 덤프 명령으로 덤프되지 않은 파일 시스템
                - 1 : 데이터 백업을 위해 dump 명령 사용이 가능한 파일 시스템
            6. 파일 점검 옵션
                - 0 : 부팅할 때 fsck 명령으로 파일 시스템을 점검하지 않도록함
                - 1 : 루트 파일 시스템
                - 2 : 루트 파일 이외의 시스템
    

# LVM 
- 리눅스의 저장 공간을 효율적이고 유연하게 관리하기 위한 Kernel의 한 부분
- 여러 개의 하드디스크를 합쳐서 한 개의 파티션으로 구성해서 사용할 수 있는 것
## LVM과 Disk Partitioning
- Disk Partitioning : 하드 디스크를 Partitioning한 후에 OS 영역에 마운트해서 read/write를 수행하는 경우 저장 공간의 크기가 고정되어서 증설/축소가 어렵다.
- LVM은 partition 대신에 Volume 이라는 단위로 저장 장치를 다루는데 Storage의 확장,변경에 유연해서 크기를 변경할 때 기존 데이터의 이전이 필요없다.

## LVM 장점
1. 유연한 용량 조절
2. 크기 조절이 가능한 storage pool
    - storage pool이 뭘까
3. 편의에 따른 장치 이름 지정
4. disk spriping, mirror volume 등을 제공
    - disk spriping이 뭘까
    - mirror volume이 뭘까

## 기본 개념
- PV(Physical Volume) : 실제 하드디스크의 파티션
- VG(Volume Group) : 여러 개의 PV를 그룹으로 묶은 것
- LV(Logical Volume) : VG를 다시 적절한 크기의 파티션으로 나눌 때 사용하는 파티션
- PE(Physical Extent) : PV가 가진 일정한 블록
- LE(Logical Extent) : LV가 가진 일정한 블록

## 생성과정
- 기존 파일 시스템 종류 변경 : `fdisk`
- PV 생성 : `pvcreate`
- VG 생성 : `vgcreate`
- VG 활성화 : `vgchange -a y`
- LV 생성 : `lvcreate`
- LV에 파일 시스템 생성 : `mkfs`,`mke2fs`
- LV 마운트 : `mount`

## 예시
- 위 생성 과정을 어떻게 내가 실무적으로 이용할 수 있나?

## 디스크 사용량 확인
- disk 남은 공간에 대한 정보 출력
### 형식
```bash
df [옵션][파일시스템]
```
- 옵션
    - `-a` : 모든 파일 시스템을 대상으로 사용량 확인
    - `-k` : KB 단위
    - `-m` : MB 단위
    - `-h` : 알기 쉬운 단위
    - `-t 파일 시스템 종류` : 파일 시스템 종류에 맞는 것만 출력
    - `-T` : 파일 시스템 종류 출력
### 예시


## 디렉토리나 사용자 별 사용량 확인
### 형식
```bash
du [옵션][디렉토리]
```
- 옵션
    - 옵션/디렉토리 미기재 : 현재 디렉토리 정보 출력
    - `-s 디렉토리 이름` : Directory의 사용량 출력
    - `-h` : 알기 쉬운 단위와 함께 출력
### 예시
- 현재 Directory 정보 출력
    ```bash
    kingrange@kilwon:~$ du
    4       ./.cache
    8       ./.vim
    4       ./.local/share/nano
    8       ./.local/share
    12      ./.local
    4       ./.ssh
    84      .
    ```
- 알기 쉬운 단위와 함께 출력
    ```bash
    kingrange@kilwon:~$ du -sh
    84K
    ```
## 파일 시스템 검사
1. fsck
2. f2fsck
### fsck 형식
```bash
fsck [옵션] [장치명]
```
- 옵션 
    - `f` : 강제로 점검
    - `b` : 슈퍼블록