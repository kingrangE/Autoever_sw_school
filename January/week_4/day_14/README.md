# 프로세스 관리

## 프로세스 구분

### 일반/데몬 프로세스
- `일반 프로세스` : 자신의 작업 수행 후, 종료
- `데몬 프로세스(daemon process)` : 백그라운드에서 무한정 수행
    - `서버 용도` 또는 `시스템 관리 및 감시 용도`로 사용

### 포/백그라운드 프로세스
- `Foreground Process` : 내 Terminal에 보이는 프로세스
    - 동기식 작업처럼 동작한다.
        - 순차적으로 한 번에 하나씩 동작
- `Background Process` : 내 Terminal에 안 보이게 실행되는 프로세스
    - `비동기식 작업처럼 동작`한다.
        - 한번에 여러 개 동작 가능
    - Background로 수행하는 작업
        1. 서버 용도 서비스
        2. 시스템 관리 및 감시
        3. 시간이 오래걸리는 서비스
    - 단, 금방 끝나는 작업을 Background로 넘기는 것은 `성능에 악영향`을 줄 수 있다.
        - Background Process가 늘어나면, 성능에 영향을 줄 수 있기 때문이다.
            - `Thrashing` : `Context Switch`에 `많은 시간이 소요`되는 `Overhead가 커지는 문제 발생`할 수 있다.
    - 참고
        - Q. 현대 CPU는 멀티코어인데, 왜 Context Switch가 발생하지?
        - A. 한 시스템에서 동작하는 Process는 수천개다. 멀티코어/멀티쓰레드라 할지라도 동시에 수천개의 Process를 동작시킬 수는 없다.
            - 그래서 `아주 빠른 속도로 작업을 전환`하며 `Concurrency를 달성`한다.
                - `Parallelism`은 `실제 동일한 시각에 동시 실행`
        - Q. 그러면, 동시 시각에 코어 이상의 Process가 동작한다면 무시당하나요?
        - A. 아뇨. 동시에 작업이 불가능한 Process는 Ready Queue에 들어가고, 앞선 작업이 끝나면 Ready Queue에서 작업을 꺼내 다음 프로세스를 처리하는 방식이기에 누락이 없습니다.
            - 누락 되는 경우는 아래와 같습니다.
                1. Buffer Overflow  
                    - 버퍼가 가득찼는데 새로운 log가 계속 들어올 때
                2. RTOS 
                    - 특수 목적 OS에서는 시간 내에 처리가 되지 않으면 누락하는 경우가 있음

## 작업 전환 명령
1. `CTRL + Z`  : Foreground Process 중단(멈춤)
2. `bg %작업번호` : 작업번호에 해당하는 작업을 `Background`로 전환
3. `fg %작업번호` : 작업번호에 해당하는 작업을 `Foreground`로 전환
### 예시
```bash
kingrange@kilwon:~$ sleep 800 # sleep Foreground 작업 실행
^Z # Foreground 작업 일시 중단
[1]+  Stopped                 sleep 800 # 중단되었다고 나옴
kingrange@kilwon:~$ jobs ### 작업 확인
[1]+  Stopped                 sleep 800 # 위에 나온 로그와 같음
kingrange@kilwon:~$ bg %1 # 백그라운드로 작업 전환
[1]+ sleep 800 &
kingrange@kilwon:~$ jobs # 다시 확인
[1]+  Running                 sleep 800 & # Back에서 Running중
kingrange@kilwon:~$ fg # 다시 fore로 전환
sleep 800 #돌아감
^Z
[1]+  Stopped                 sleep 800
```

## 작업 종료 명령
1. `CTRL+C` : Foreground 작업 종료
    - `CTRL+C`를 입력받으면 `Interrupt Signal`을 `Process에 전달`하며, `시그널을 받은 Process가 종료`된다.
        - 다만, `무시하도록 설정`한 경우엔 `종료되지 않는다.`
2. `kill PID` : Fore/Background 강제 종료
    - ps 명령어로 PID를 찾아 강제 종료할 수 있다.

### 예시
```bash
kingrange@kilwon:~$ sleep 500
^C
kingrange@kilwon:~$ jobs
[1]+  Stopped                 sleep 800
kingrange@kilwon:~$ sleep 500 &
[2] 6407
kingrange@kilwon:~$ jobs
[1]+  Stopped                 sleep 800
[2]-  Running                 sleep 500 & # 백에서 실행 중
kingrange@kilwon:~$ kill 6407
kingrange@kilwon:~$ jobs
[1]+  Stopped                 sleep 800
[2]-  Terminated              sleep 500 # 삭제 됨
```
## nohup 명령
- 로그아웃 후에도 작업하기
- 하다 마노 (Gemini찬스)

## at 명령
- 정해진 시간에 작업이 수행되도록 하는 명령
    - 화면에 출력하는 작업은 안된다. (즉, 출력 리다이렉션을 이용하면 좋다.)
- `패키지를 설치하여 사용`
### 형식
```bash
at [옵션] [시각]
```
- 옵션
    1. `-l` : 현재 `실행 대기 중`인 `명령의 전체 목록 출력`
    2. `-d 작업번호` : 예약된 작업을 취소 (`atrm 작업번호`와 동일)
    3. `-v` : 정확한 시간을 상세히 표시
    4. `-m` : 출력 결과가 없더라도 작업이 완료되면, 사용자에게 메일로 알려줌
    5. `f 파일` : 터미널 입력 대신 파일에 저장된 Script를 불러와 예약
    
### at 작업 목록 확인
    ```bash
    atq
    sudo ls -l /var/spool/cron/atjobs
    ```

### 사용 제한
- `at.allow` / `at.deny` 파일을 이용하여 사용자를 허용/거부할 수 있다.
    - `at.allow` : 특정 사용자가 사용할 수 있도록 허용
        - 기본적으로 없는 상태
    - `at.deny` : 특정 사용자가 사용하지 못하도록 허용
        - 기본적으로 `빈 at.deny` 제공
            - 즉, 기본적으로 `모든 사용자가 사용 가능`하다.
- 만약, 두 파일이 모두 없다면, `root`만 `at` 사용 가능하다.

### 파일을 이용하여 작업 수행
1. 파일 생성
    ```bash
    kingrange@kilwon:~$ cat << EOF > at.sh
    > date > kingrangE
    > ls >> kingrangE
    > ps -ef | grep kthreadd >> kingrangE
    > EOF
    ```
2. 실행
    ```bash
    kingrange@kilwon:~$ at -f at.sh now + 1minute
    warning: commands will be executed using /bin/sh
    job 5 at Fri Jan  9 01:23:00 2026
    kingrange@kilwon:~$ at -l
    5       Fri Jan  9 01:23:00 2026 a kingrange
    ```
3. 결과
    ```bash
    kingrange@kilwon:~$ ls # 목록에 kingrangE 파일 생김
    22  at.out  at.sh  kingrangE  sales_data.txt  sticky  test  test.out
    kingrange@kilwon:~$ cat kingrangE # 내용 보니까 결과물이 다 잘 들어있음.
    Fri Jan  9 01:23:00 AM UTC 2026
    22
    at.out
    at.sh
    kingrangE
    sales_data.txt
    sticky
    test
    test.out
    root           2       0  0 Jan07 ?        00:00:00 [kthreadd]
    kingran+    6879    6875  0 01:22 ?        00:00:00 grep kthreadd
    ```
### 예시
<details>
<summary> N개의 예시 </summary>

1. 3일 후 오후 4시
    ```bash
    at 4pm + 3days
    ```
2. 7월 31일 오전 10시
    ```bash
    at 10am Jul 31
    ```
3. 내일 오전 1시
    ```bash
    at 1am tomorrow
    ```
4. 오늘 오후 6시
    ```bash
    at 6pm today
    ```
5. 3분 후, 현재 시간 및 날짜 at.out 출력
    ```bash
    kingrange@kilwon:~$ at now + 3minute
    warning: commands will be executed using /bin/sh
    at Fri Jan  9 01:06:00 2026
    at> date > at.out
    at> <EOT>
    job 4 at Fri Jan  9 01:06:00 2026
    kingrange@kilwon:~$ atq
    4       Fri Jan  9 01:06:00 2026 a kingrange
    
    ```
6. 부하가 적은 새벽 시간대 압축 실행
    ```bash
    kingrange@kilwon:~$ at 02:00am
    at> tar -czf /backup/data_$(date +%F).tar.gz /var/www/html # 작업 내용
    at> #CTRL + D
    job 5 at Fri Jan  9 02:00:00 2026
    ```
7. 임시 권한 부여 후 자동 회수
    ```bash
     # 지금 즉시 권한 부여
    sudo chmod 777 /shared_data

     # 1시간 뒤에 다시 원래 권한(755)으로 복구하도록 예약
    echo "chmod 755 /shared_data" | at now + 1 hour # 한 줄로 명령을 남기고 싶은 경우 echo를 사용해야 한다.
    ```
8. 작업 목록 확인 및 취소
    ```bash
     # 예약된 작업 목록 확인 (at -l 도 가능)
    kingrange@kilwon:~$ atq
    5	Fri Jan  9 02:00:00 2026 a kingrange

     # 5번 작업 취소
    kingrange@kilwon:~$ atrm 5
    ```
</details>

## crontab 명령
- `특정 시간`에 `특정 작업`을 `주기적으로 반복`해야 하는 경우 사용
### 형식
```bash
crontab [옵션] [파일명]
```
- 옵션
    1. `-e` : crontab 설정 수정 및 새 작업 추가
    2. `-l` : crontab 내용 출력
    3. `-r` : crontab 파일 삭제
    4. `-u UID` : 특정 User의 crontab 관리
- `crontab`은 `사용자 별`로 `별도의 파일로 생성`
    - `crontab` 파일엔 `여러 개 작업 저장`가능, `한 줄에 하나의 작업` 설정

### crontab 파일 내용
```bash
* * * * * 실행 명령
```
- 앞의 5개의 별(`*`)로 `시간`을 지정한다.
    1. 분(0-59)
    2. 시(0-23)
    3. 일(1-31)
    4. 월(1-12)
    5. 요일(0-6, 0:일)
    - *로 기입 시, `모든 시간`을 의미

- 요소
    1. `-` : 범위
    2. `,` : 여러 시간 나열
    3. `/` : Step

### crontab 관련 파일
- `/var/spool/cron/crontabs` : crontab 파일을 user 당 1개씩 가지고 있다.
    - 해당 경로에 user_name으로 파일이 존재
- 확인
    ```bash
    kingrange@kilwon:~$ sudo ls /var/spool/cron/crontabs/
    kingrange
    ```
### crontab 로그
- 기본 : cron log 기록 `비활성화`
- 활성화 방법 
    ```bash
    sudo service rsylog restart #해당 명령 수행
    ```
# 소프트웨어 관리
## 패키지
- Linux software 2가지 형태로 배포
    1. 소스코드 형태
        - 하나의 `아카이브 파일`로 묶어서 `압축 후 배포`
    2. `패키지 형태`
        - bin 파일로 배포 : rpm,deb 2가지 형식 존재
            - ubuntu : `deb`
            - redhat : `rpm`
        - snap : ubuntu 16.04부터 도입된 `새로운 패키지 형식`
            - `deb의 의존성` 문제를 해결한 것으로 `deb와 호환 가능`

### 특징
1. `bin 파일로 구성`되어 있어서 `compile할 필요가 없음`
2. 설치 시, `패키지 내 파일`이 `관련 Directory`로 `바로 설치`
3. 삭제 시, `관련 파일`을 `일괄 삭제`
4. `기존 패키지`를 `삭제하지 않고, 업그레이드 가능`
5. 패키지 `설치 상태 검증` 가능
6. 패키지 `정보 확인 가능`
7. `apt 명령을 이용`해서 `의존성이 있는 패키지`를 `자동으로 설치 가능`

### Package Repository Category
1. `main` : 우분투가 공식 지원하는 핵심 패키지 (보안 업데이트 보장)
    - FOSS(자유 소프트웨어)
2. `restricted` : 하드웨어 드라이버 등 제조사가 소스를 안 보여주는 필수 도구
    - Proprietary
3. `universe` : 전 세계 리눅스 커뮤니티가 관리하는 방대한 양의 소프트웨어
    - FOSS, 기술적 지원 보장 X
4. `multiverse` : 저작권/특허 문제가 존재하는 소프트웨어
    - 개인이 직접 라이선스를 관리해야 한다.

### 패키지 이름 규칙
```bash
패키지명_버전_데비안리비전_우분투리비전_아키텍처.deb
```
- 데비안 리비전 : 원본 소스를 Debian OS에 맞게 패키징하면서 `수정한 횟수`
- 우분투 리비전 : Debian Package를 Ubuntu OS에 맞게 패키징하면서 `수정한 횟수`
- 아키텍처 : 해당 패키지가 설치될 수 있는 CPU 환경

### 패키지 저장소
- `Linux System`에는 `설치 가능한 프로그램 목록`과 `실제 설치 파일들`이 `특정 서버에 저장`되어 있다. 이를 `패키지 저장소`라고 한다.
    - 사용자가 `apt install`을 입력하면, `저장소 주소로 접속`하여 `해당 파일을 찾아 설치`한다.
- `저장소를 이용`하기 위해선 `등록 필수`
    - 새로운 저장소 주소가 필요하다면 새로운 저장소 주소를 sources.list에 추가 (회사에서 보통 이렇게 진행)


### 패키지 관리 명령
```bash
apt-cache
```
- `apt-cache`에 질의해서 `여러 정보 검색 가능`
- `통계 정보` : `apt-cache stats` (잘 안씀)
- 캐시에서 `패키지 확인` : `apt-cache search 패키지 이름`
    - 유무 파악할 때 사용
- 캐시에서 `패키지 정보 출력` : `apt-cache show 패키지 이름`
- `사용 가능한 패키지 이름` 확인 : `apt-cache pkgnames`


### apt-get / apt
- `동일한 의미`
    - `apt-get`은 `예전`에 사용하던 것이고 `현재는 apt`만 해도 된다.
- 형식
    ```bash
    apt [옵션] [서브 명령]
    ```
    - 옵션
        1. `-d` : 패키지를 내려받기만 수행
        2. `-f` : 의존성이 깨진 패키지를 수정하려 시도
        3. `-h` : 도움말 출력
        4. `-y` : `설치 여부를 묻는 부분`을 생략 (자동화(CI/CD)하는데 중요)
    - 서브 명령
        1. `update` : 패키지 저장소에서 `새로운 패키지 정보`를 가져옴
            - linux 첫 설치 후 수행
            - 저장소 파일(sources.list.d)을 수정한 경우 수행
        2. `upgrade` : 현재 설치된 패키지 업그레이드
            - `기존 패키지의 새로운 버전을 적용`하고자 하는 경우
        3. `install` : 설치
        4. `remove` : 삭제
            - `실행 파일만` 삭제
            - 이전에 사용하던 대로 이어서 사용하는 경우 수행
                - 즉, 잠시 삭제해본 경우
        5. `purge` : 삭제
            - `실행 파일 + 설정파일` 삭제
            - 다시는 쓸 일 없는 경우에 수행
            - 초기화가 필요한 경우 수행
        6. `download` : 다운로드
            - 패키지를 시스템에 설치하지 않고, `설치파일(.deb)만 내 컴퓨터에 다운로드`하는 것
                - `패키지의 소스코드만 다운로드`도 가능
                    ```bash
                    sudo apt --download only source 패키지명
                    ```
            - 사용 경우
                - 인터넷이 안 되는 폐쇄망일 때 사용
                - 패키지 분석 때 사용
                - 특정 버전 보관을 위해 사용
        7. `autoclean` : 불완전하게 내려받았거나, 오래된 패키지 삭제
            - 패키지 자동 정리
        8. `clean`: cache 되어있는 패키지를 삭제해서 disk 공간 확보
            - 디스크 공간 정리
        9. `check` : 의존성이 깨진 패키지를 확인
        10. `search` : 현재 패키지가 설치되었는지 확인 가능
#### 실습
- python3 패키지가 있는지 확인해보고 없으면 설치, 있으면 upgrade
    ```bash
    sudo apt search python3
    apt -y upgrade python3
    ```

## dpkg
- debian 계열 패키지 관리 시스템의 low-level  도구 
- `apt 명령`은 fedora의 `yum`/`dnf`와 유사하다.
    - `인터넷이 연결된 환경`에서 pakage를 자동으로 설치
- `dpkg 명령`은 fedora의 `rpm`과 같은 명령
    - apt도 내부적으로 dpkg 명령 사용
- `패키지를 설치`할 땐, `APT 명령` / `패키지를 확인`할 때는 `dpkg 명령` 사용

### 형식
```bash
dpkg [옵션] {파일명 | 패키지 이름}
```
- 옵션
    - `-l` : 목록 출력
    - `-s 패키지명` :  해당 패키지의 상세 정보 출력
    - `-L 패키지명` : 패키지를 설치할 때 사용한 파일 목록 출력
    - `-c .deb파일` : 파일 내용 출력
    - `-i .deb파일` : 해당 파일 설치
    - `-r 패키지명` : 패키지 삭제
    - `-P 패키지명` : 패키지와 설정 파일 모두 지움
    - `-x .deb파일 Directory` : deb파일의 압축을 Directory에 풀기

## aptitude
- Graphic 화면으로 apt를 사용할 수 있다.
    - ![aptitude 사용 화면](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgwryKvRW9QVlCFE9V0iwyugW5dIVF9nuMyQ&s)

- `패키지를 설치하여 사용`

## sanp
- ubuntu가 `새로 도입`한 `패키지 형식` 
    - Mac의 `sandbox`와 같은 형태의 패키지
- 기존 시스템과 격리된 형태로, `보호된 영역`에서 `실행`
    - `외부 파일`이 `내부 시스템`에 악영향을 주는 것을 방지하는 `보안 기술을 위한 형식`이다.
- 참고
    1. `크기 비대` : sandbox 방식을 이용하면, 각 패키지에 모든 의존성 패키지가 포함되므로, `패키지의 크기가 커진다.`
    2. `DLL 지옥` : `Window에서 사용하는 방식`(`DLL`)은 두 라이브러리가 `종속 관계`가 되어 `서로 지우지도 못하고, 업데이트도 못하는 문제`가 생긴다. `이러한 문제`를 `DLL 지옥`이라 말한다.
        - 예를 들어, A와 B가 1라이브러리를 공유한다면,
            - A -> 1 / B -> 1 이렇게 공유하여 사용하도록 함.
            - DLL은 `패키지를 공유`하므로 `Disk 절약이 가능`하다.

### 형식
```bash
snap [옵션] [명령]
```
- 옵션
    - `-h` : 도움말
- 명령
    - `disable` : snap 서비스 중지
    - `download` : 다운로드
    - `enable` : snap 서비스와 실행 파일의 사용을 시작
    - `find 스냅이름` : 조회
    - `info 스냅이름` : 상세 정보 출력
    - `install 스냅이름` : 설치
    - `list` : 목록 출력
    - `remove 스냅이름` : 삭제

### 실습
1. `hello-world` 스냅 검색
    ```bash
    snap find hello-world
    ```
2. `hello-world` 스냅 설치
    ```bash
    snap install hello-world
    ```
3. 스냅 설치 목록 확인
    ```bash
    sudo snap list
    ```
4. `hello-world` 정보 확인
    ```bash
    snap info hello-world
    ```

## tar
- 파일 아카이빙 명령 (tape archieve)
    - `압축이 아니다.` (`용량이 거의 줄지 않음` (메타데이터로 오히려 증가할 때도 있음))
        - 압축을 하고싶다면, `추가 옵션(j,z)을 이용`하여 할 수 있다. (압축 시 용량 감소)

### 형식
```bash
tar 기능 [옵션] [아카이브 파일] [파일 이름]
```
- 기능
    - `-c` : 새로운 `tar 파일` 생성
    - `-t` : `tar 파일의 내용`을 출력
    - `-x` : 압축 해제
        - 기본적으론 `현재 경로`에서 `압축해제`
        - `-C` : 특정 경로에 압축 해제 (예시 3)
    - `-r` : `새로운 파일`을 `추가`
    - `-u` : `수정된 파일`을 `업데이트`
- 옵션
    - `-f` : 대상이 될 아카이브 파일 이름 지정 
        - 옵션 마지막에 작성
        - 파일 이름을 `-`로 설정하는 경우 파일로 만드는 것이 아니라 `표준 입/출력으로 전달`
            - 예시 3 참고

    - `-v` : `작업 과정`을 `화면에 출력`
    - `-h` : Symbolic Link의 원본 파일을 포함
    - `-p` : 파일을 복구 시, 원래의 접근 권한을 유지
    - `-j` : `bzip2 방식`을 사용하여 압축 병행
        - `.tar.b2`
    - `-z` : `gzip 방식`을 사용하여 압축 병행
        - `.tar.gz`

- 자주 사용하는 결합 옵션
    - 압축 : `cvzf`
    - 압축 해제 : `xvzf`
    - 아카이빙 하는 경우엔 : `z를 제외하고 작성`하면 된다.

- 그 외 좀 사용하는 결합 옵션 
    - 내용 확인 : `tvf`
    - 업데이트  : `uvf`
    - 파일 추가 : `rvf`

### 예시
1. 오늘 날짜를 이름으로 압축
    ```bash
    kingrange@kilwon:~$ tar -cvzf kingrangE_$(date +%y%m%d).tar.gz tar_test
    tar_test/
    tar_test/A
    tar_test/E
    tar_test/B
    tar_test/C
    tar_test/D
    kingrange@kilwon:~$ ls
    date_log  kingrangE_260109.tar.gz  tar_test # 오늘 날짜로 잘 압축되었따.
    ```
    - 나중에 로그파일 같은거 압축 자동화를 한다면, 이 방식으로 오늘 날짜로 압축 백업을 하는 것이다.
2. `A 파일 제외`하고 압축
    ```bash
    kingrange@kilwon:~$ tar -cvzf exclude_A.tar.gz --exclude="A" tar_test
    tar_test/
    tar_test/E
    tar_test/B
    tar_test/C
    tar_test/D
    ```
3. 압축 후 ssh로 전송
    ```bash
    tar -cvf - . | ssh user@remote_server "tar -xvf - -C /target/dir"
    ```
    1. `tar -cvf - .`
        - `-cvf` (압축옵션)으로 압축 후, `-`(표준 출력 전달),`.` : 모든 파일
        - 즉, 모든 파일 압축 후, stdout 
    2. `|` : 앞의 출력을 파이프로 넘김
    3. `ssh user@remote_server` : 특정 ssh 서버로 넘기기 위한 연결
    4. `"tar -xvf - -C /target/dir"` 
        - `-xvf` (압축해제)하는데, 압축 파일은 `-` (지정이 아니라 stdin으로 받은 것 이용), `- C`를 이용하여 `/target/dir`에 해제

### 압축없이 아카이빙만 하는 이유
1. CPU 절약
    - 압축 과정에선 `CPU가 많이 사용`된다.
    - 이미 CPU 점유율 99%인 상황에서 압축까지 시도하면, 서비스가 멈출 수 있다. 이를 방지하기 위함.
2. 이미 압축된 파일을 모으는 경우
    - 이미 압축된 것을 모으는 것이므로 아카이빙만 한다.
    - `그림`이나 `동영상`도 `압축이 거의 의미없기` 때문에 압축파일과 같은 취급한다.
3. 속도가 중요한 경우
    - `압축 파일`은 `압축을 해제해야` 확인 가능
    - `아카이빙 파일`은 `압축 해제 없이` 바로 확인 가능
        - Indexing으로도 바로 찾기 가능
## gzip/gunzip
- 압축률이 좋은 유틸
- 지정한 파일을 압축해서 크기를 줄여서 저장 / 확장자는 일반적으로 gz 사용

### 형식
```bash
gzip [옵션] [파일명]
```
- 옵션
    1. `d` : 해제
    2. `l` : 정보 출력
    3. `r` : 하위 디렉토리를 탐색하여 압축
    4. `t` : 압축 파일 검사
    5. `v` : 압축 정보 화면 출력
    6. `g` : 최대 압축

## bzip2/bunzip2
- 압축률은 gzip보다 좋지만, 속도가 느리다.

### 형식
```bash
bzip2 [옵션] [파일명]
```
- 옵션
    1. `d` : 해제
    2. `l` : 정보 출력
    4. `t` : 압축 파일 검사
    5. `v` : 압축 정보 화면 출력
    6. `--best` : 최대 압축

## xz
- 가장 최근에 등장한 압축 방식
- 압축률이 가장 뛰어남
- BUT, 잘 사용하지 않음

## zip/unzip
- 윈도우와 호환성 때문에 zip 제공

## wget
- wwwget
- 웹서버로부터 contents를 가져오는 도구
- HTTP HTTPS FTP 프로토콜 지원 
- 네트워크 연결이 불안정해도 다운로드를 재개할 수 있는 강력한 복구 기능
### 주요 특징
1. `비 대화형` : 사용자가 로그아웃해도 Background에서 Download 진행 가능
2. `재귀적 다운로드` : Website의 구조를 그대로 다운로드하여 로컬 저장 가능
3. `복구 능력` : 중단된 다운로드를 이어서 다운로드 받을 수 있다.
### 형식
```bash
wget [옵션][URL]
```
- 옵션
    1. `-O` : 저장될 파일 이름 지정
        ```bash
        wget -O test_file "https://example.com/data.zip"
        ```
    2. `-c` : 중단된 다운로드 이어 받기
        ```bash
        wget -c "https://example.com/large_video.mp4"
        ```
    3. `-b` : 백그라운드에서 실행
        ```bash
        wget -b "https://example.com/backup.tar.gz"
        ```
    4. `-P` : 저장할 Directory 지정
        ```bash
        wget -P /kingrangE/ "https://example.com/tiger.jpg"
        ```
    5. `-r` : 재귀적으로 `하위 페이지`까지 다운로드
        ```bash
        wget -r https://example.com/docs/
         # docs의 하위 페이지 다운로드
        ```
    6. `--limit-rate` : 다운로드 속도 제한
        ```bash
        wget --limit-rate=500k https://example.com/file.iso
        ```
    7. `-i` : 파일에 적힌 URL 목록 한 번에 다운로드
        ```bash
        wget -i url_list.txt
        ```
### 활용 사례
1. `대용량 데이터셋` 또는 `배포 파일` 다운로드
    - cli에서는 파일을 다운로드 받기 힘들다.
    - `-c` 옵션을 사용하여 중단되는 경우 이어서 받을 수 있게 해야한다.
2. `웹 사이트 정적 미러링`
    - 특정 web의 html,css,images를 그대로 로컬에 보관하기 위해 사용
    ```bash
    wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://example.com
    ```
    - `--convert-links` : local에서 연결되었을 떄, link가 서로 연결되도록 수정
    - `--page-requisites` : 페이지 표시를 위한 이미지, 스타일시트 등을 모두 포함하라.
3. `API 호출 및 결과 확인`
    - curl을 보통 사용하나, JSON 등의 결과를 빠르게 분석하는데 가끔 유용하다.
4. `인증이 필요한 파일 다운로드`
    ```bash
    wget --user=myname --password=mypassword https://secure.example.com/confidential.pdf
    ```
## curl
- 명령줄이나 Script에서 데이터를 전송하기 위해 사용하는 도구
    -dd `wget` : 파일 다운로드/웹사이트 미러링 특화
    - `curl` : 다양한 프로토콜 지원/ 데이터 전송/수신 기능에 치중
### 주요 특징
1. `다양한 프로토콜 지원` : 웹 요청/메일 전송/파일 업로드 등도 가능하다.
2. `디버깅 최적화` : request/response 헤더 확인이 쉬워 `API테스트`/`Truble Shooting`에 좋다.

### 형식
```bash
curl [옵션] [url]
```
- 옵션
    1. `-X` : GET/POST/PUT/DELETE 메서드 지정
        ```bash
        curl -X POST https://api.com/v1
        ```
    2. `-H` : HTTP 요청 헤더 설정
        - 인증 토큰 전달할 때 사용
        ```bash
        curl -H "Autorization: Bearer \"TOKEN\" URL"
        ```
    3. `-d` : 전송할 데이터(Body) 지정 (POST 요청)
        ```bash
        curl -d "id=user1&pw=1234" https://api.com/login
        ```
    4. `-i` : 응답 본문과 함께 HTTP 헤더 정보도 출력
        ```bash
        curl -i https://www.naver.com
        ```
    5. `-L` : URL이 Redirect 될 경우 추적
        - ex, http://www.google.com 은 이제 https://www.google.com으로 자동 redirected 된다.
        - 이때, L 옵션없이 http로 요청하면, Error가 발생하지만, L 옵션을 포함하면 https로 자동 리다이렉트
        ```bash
        curl -L http://google.com
        ```
    6. `-u` : 사용자 인증 정보 전달시 이용
        - `id:pw`
        ```bash
        curl -u id:pw https://www.test.com
        ```
    7. `-o` : 결과 내용을 파일로 저장
        ```bash
        curl -o 파일명 https://example.com
        ```
    8. `-v` : 실행 과정 및 통신 상세 정보 확인
        ```bash
        curl -v https://example.com
        ```
### 활용 사례 
1. REST API 호출 (JSON 데이터 전송)
    - 백엔드 서버 테스트/외부 API 연동 시 JSON으로 데이터를 보내고 결과를 확인할 때 사용
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{name:kingrangE}' https://example/user
    ```
2. 웹 서버 상태 체크 (HTTP 상태 코드만 확인)
    - 서버 health check, 응답 속도 테스트에 사용
    ```bash
    curl -o /dev/null -s -w "%{http_code}\n" https://www.example.com
    ```
    - `-o /dev/null` : 응답 파일 경로를 /dev/null로 설정하여 버리도록 설정
    - `-s` : 진행 상태 표시 제거
    - `-w` : 특정 포맷("%{http_code\n}")으로 출력하도록 함.
3. 인증 Token을 이용한 보안 데이터 요청
    - Github API 또는 AWS 서비스 등 인증이 필요한 리소스에 접근할 때 사용
    ```bash
    curl -H "Authorization: token GITHUB_TOKEN" https://example.com
    ```
4. 파일 업로드
    - 웹 폼을 통해 파일을 업로드하는 것과 동일한 동작
    ```bash
    curl -F "image=@image.png" -F "title=My Photo" https://api.img-up.com/upload
    ```
### wget과의 차이
1. `목적`
    - wget : 단순 파일/사이트 `다운로드`
    - curl : 데이터 전송 및 API 테스트 (`데이터 주고 받기`)
2. `재시도`
    - wget : 재시도 가능
    - curl : 재시도 불가
3. `재귀적 다운로드` 
    - wget : 가능
    - curl : 가능하지 않음
4. `복잡성`
    - wget : 단순하고 직관적
    - curl : 매우 다양한 프로토콜 및 옵션 제공

- 다운로드 : wget / 데이터 주고 받기 : curl

# 리눅스 부팅 시스템
- Linux 부팅 : PC를 켜는 순간~Linux 동작해서 로그인 Prompt가 출력될 때까지
- 배워야 하는 이유
    1. 부팅에 필요한 서비스가 시작되도록 결정
    2. 부팅 과정에서 문제가 발생한 경우, 해결하기 위함

## 부팅
- 순서
    1. 전원 ON - linux와 무관
    2. BIOS 단계 - linux와 무관
    3. BootLoader
    4. Kernel Initialize
    5. Systemd 서비스
    6. login prompt

### BIOS 단계
- BIOS : Basic Input Output System
    - ROM에 주로 저장되어 `ROM BIOS`라고도 한다.
- 작업
    1. Computer에 장착된 키보드, 디스크 상태를 확인
    2. 부팅할 장치 선택
    3. 선택한 부팅 장치에 부팅 디스크의 섹션에서 MBR(Master Boot Record)를 로딩한다.

- 최근엔 UEFI를 주로 사용한다. 이때는 MBR이 아니라, GPT, ESP를 사용한다.

### BootLoader
- 기능
- `부팅할 OS`나 `부팅 방법`을 선택하도록 `메뉴를 제공`한다.
    - Kernel을 메모리에 Loading한다.
        - Kernel은 /boot 폴더 내에 `vmlinuz-버전명`으로 제공된다.
        - ubuntu를 `업데이트`하면 `새로운 버전의 커널이 추가로 생성`된다.
- Ubuntu는 GRUB을 BootLoader로 사용한다.
    - Multi Booting이 아니라면, GRUB 메뉴를 출력하지 않고, 바로 부팅
        - Q. 이때, GRUB 메뉴를 보이도록 하고싶다면?
        - A. `/etc/default/grub` 파일 수정
            - 기본값 : `"GRUB_TIMEOUT_STYLE=hidden"` 
                - 해당 항목을 주석처리하면, 싱글 부팅에서도 메뉴를 확인할 수 있다.
                - 이때, `GRUB_TIMEOUT 값`을 설정해주면, 몇 초 뒤에 실행될지 설정할수 있다.
            - 해당 파일을 수정한 후, `sudo update-grub`을 수행해서 적용되도록 해주어야 한다.

### Kernel Initialize
- 기능
    - System에 `연결된 하드웨어를 사용`할 준비
    - `initrd`를 로드하여 root partition을 mount하기 위한 임시 드라이버를 로드한다.
        - 이 과정이 끝나야 systemd 사용 가능
### Systemd 서비스 시작
- User Space 구성
- Systemd가 실행되며, 각종 daemon(네트워크,디스크 마운트,GUI 등)을 실행한다.

# 참고
1. S3 / 글래셔
    - 글래셔 : 압축해서 보관
        - 저장소 절약 가능
    - S3 : 파일을 그대로 보관
        - 빠르게 찾기 가능
    - 효율적 사용
        - x 기간 이하 파일 : S3에 저장
            - 최근 것일수록 자주 확인하므로, 자주 봄 (압축 해제 과정이 없는게 좋음)
        - x 기간 이상 파일 : 글래셔로 압축하여 저장
            - 일정 기간 이상 지나면, 잘 안 봄
2. Mount
    - 물리적인 저장장치(하드디스크, USB, CD-ROM 등)를 디렉토리 구조의 특정 위치에 연결하는 과정
        - Linux는 Day 13에서 정리했듯이 하나의 거대한 Tree구조로 디스크를 폴더로서 관리하기에 Mount과정이 부팅에 포함된다.