# Linux
- UNIX 계열의 운영체제다.
    - UNIX : 1969년 벨 연구소에서 `어셈블리어`와`C`로 개발한 운영체제

## LINUX 계통도
1. Debian 계열 : Ubuntu Linux
    - 개인 유저는 Ubuntu 많이 사용함 (구글에서 밀어줌)
    - 플랫폼 기업들이 많이 사용(오픈 소스)
2. Redhat 계열 : Pedora, CentOS(Rocky), RedhatEnterprise
    - 3개의 OS는 같은 것이나 약간 다름
        1. Pedora : `시험판`
        2. CentOS : Pedora의 `안정화버전`(독립한 것이 Rocky)
        3. RedhatEnterprise : `CentOS에 Untility를 얹어` `상용화버전`으로 파는 것
    - 대기업들은 Redhat Enterprise 많이 사용
3. Slackware 계열 : SuSE (IBM 머신에 많이 들어갔었음, 현재는 IBM을 안 쓰니까 거의 안 씀)

## 운영체제의 구조
1. Kernel
    - OS의 핵심
    - `프로세스`/`메모리`/`파일시스템`/`장치관리` 등의 기능 수행
    - 컴퓨터의 `모든 자원 초기화` 및 `제어 기능` 수행
    - Linux는 `Kernel의 대부분`이 `C언어`로 개발
2. Shell
    - 명령어 해석기
    - 유저가 `전달한 명령을 해석`해서 `Kernel에 전달`함
3. Application
    - 개발 도구
    - Utility

## Ubuntu Linux
- Debian GNU/Linux 바탕
- 기본 Desktop 환경 : 과거 Unity -> 현재 GNOME
- Unity 기본 철학 : `누구나 어렵지 않게 Linux 사용하기` -> 근데 왜 어렵게 만들어.


### 가상화
- `하나의 물리적 컴퓨터`에 `여러 운영체제`를 실행할 수 있게 하는 기술 중 하나
    1. `하나의 실제 컴퓨팅 자원`(CPU,Memory,Storage,Network 등)을 `여러 개인 것처럼` 쪼개어 사용
    2. `여러 개의 컴퓨팅 자원`을 묶어서 `하나의 자원인 것처럼` 묶어 사용
- 가상화 방법
    1. `VM(Virtual Machine)사용`하기 - `HyperVisor` 이용
    2. `Container` - OS level에서 `Process를 Container로 격리`

### 가상 머신
- PC에 설치된 OS에 `가상의 머신을 생성`해, `다른 OS를 설치`할 수 있도록 해주는 `Software`
    - `PC OS` : Host OS 
    - `가상머신 OS` : Guest OS
- 종류
    1. `VMWare` 
        - Host OS : Windows, Linux, Mac
        - Guest OS : Windows, Linux, Solaris, Mac OS
    2. `Virtual PC` 
        - Host OS :  Windows
        - Guest OS : Windows, Linux, Solaris
    3. `Virtual Box` 
        - Host OS : Windows, Linux, Mac OS, Solaris
        - Guest OS : Windows, Linux, Mac OS, Solaris, OpenBSD
    4. `UTM`
        - Host OS : Mac OS 중에서 Silicon Chip(M시리즈) 쓰는 거
        - Guest OS : Linux
- `Window WSL` 
    - `PowerShell`에서 설치하면, `Ubuntu Linux Kernel`이 설치되어 `Ubuntu`를 사용할 수 있다.

## Virtual Box를 활용한 Ubuntu Linux설치
### Ubuntu Linux Image Download
1. `Server Version (CLI)`
    - 나중에 GUI 설치 가능
        ```bash
        sudo apt-get update
        sudo apt-get upgrade
        sudo apt-get install --no-install-recommands ubuntu-desktop
        ```
2. `Desktop Version (GUI)`

### 설치과정
1. 새로 만들기 
2. VM Name과 저장할 디렉토리 설정
3. ISO Image에서 다운로드 받은 이미지 선택
4. 무인 설치 해제 (Unattended Intallation)
5. Memory/CPU/Disk Size 설정 -> 주의 : `Kubernetes master node`는 `CPU의 코어 개수`가 `2개 이상`이어야 한다.
6. 다음 -> 완료 -> 끝

### Ubuntu Server에 Open SSH를 설치해서 원격 접속
1. `openssh-server` 설치
    ```bash
    sudo apt update
    sudo apt install openssh-server
    ```
2. ssh 실행 및 확인
    ```bash
    sudo systemctl start ssh # 아무런 메시지 리턴 없음
    sudo systemctl status ssh # 이거에서 Active 있으면 성공
    ```
3. 방화벽에서 포트 개방
    ```bash
    sudo ufw allow ssh
    ```
4. Guest IP 확인
    ```bash
     # 어떠한 것도 설치하지 않았다면 아래 키워드로만 볼 수 있음
    hostname -I #(대문자)
    ```
5. Host Computer(Window)의 IP 확인
    ```bash
    ipconfig
    ```
6. Virtual Box NAT 설정
    - Virtual Box [설정]-[네트워크] -> 포트포워딩 
        - 처음엔 포트포워딩에 아무것도 없다. (안했으니까.)
    - Rule 추가
        - `Host IP`(window)와 `GuestIP`(Linux) 설정
        - Host Port : `아무 포트번호` 가능, Guest Port : `22`

7. 접속
    ```bash
    ssh 계정@호스트IP -p 호스트포트번호
    ```

8. 종료
    - 아래의 4개 중 아무거나 사용 가능
        ```bash
        poweroff
        shutdown -P now
        halt -p
        init 0
        ```
    - Shutdown을 이용해 종료 가능 (다양한 옵션 존재)
        - OPTION
            1. `-p` : x 분 이후 종료
                ```bash
                shutdown -P +숫자
                ```
                ```bash
                shutdown -P +5 # 5분 뒤 종료 예약
                ```
            2. `-r` : 시간에 종료
                ```bash
                shudown -r 시간
                ```
                ```bash
                shutdown -r 13:30 # UTC 기준 13:30:00에 종료한다는 말
                ```
            3. `-k` : x 분 이후에 종료된다는 메시지를 접속자에게 전송 (종료 기능은 없음)
                ```bash
                shutdown -k 숫자
                ```
                ```bash
                shutdown -k 5 # 5분뒤 종료라는 메시지 전송
                ```
                
            4. `-c` : 예약 취소
                ```bash
                shutdown -c
                ```
9. 재부팅
    ```bash
    reboot
    shutdown -r now
    init 6 # run level 이용
    ```


### 원격 접속 방식
#### 텔렛
- `plaintext` 형식으로 데이터를 주고받는 `원격 접속 방식`
- 보안이 매우 취약하다.
- TCP 23번 포트를 주로 사용한다.
#### ssh
- `모든 통신 데이터`를 `암호화`하여 전송한다.
- 보안이 매우 좋다. 중간에 탈취 당하더라도 해독이 불가하다.
    - `공개키/개인키 방식`을 활용하면 더 보안이 강화된다.
- 기능 
    1. 단순 터미널 접속
    2. SFTP : 파일 전송
    3. 터널링 : 다른 통신을 SSH안에 넣어 전송
- TCP 22번 포트를 사용한다.

## 명령의 구조
```bash
형식 : 명령어 [옵션][인자]
```
- `옵션`, `인자` 각 요소는 `공백`으로 `구분`한다.
- 옵션 : `-` 또는 `--`로 시작한다.
    - `-` : 문자 1개로 옵션을 나타내는 경우
        ```bash
        ls -l # 문자 1개
        ```
    - `--` : 문자열로 옵션을 나타내는 경우
        ```bash
        ls --help # help라는 문자열
        ```
    - 옵션은 `동시에 여러 개`를 줄 수 있다.
    - 대부분의 옵션은 `순서가 없다`.
    - 옵션이 문자인 경우 결합 가능하다. 
        ```bash
         # 아래 코드는 모두 결과가 같다.
        ls -l -a
        ls -a -l
        ls -la 
        ls -al
        ```
- `인자` : 명령어를 수행하기 위해 전달되는 값
    - `--help` 설명 읽을 때 참고 사항
        - `[]` : 생략 가능
            - EX
                ```bash
                ls [-a] # ls 만쳐도 되는데 a 옵션이 있음
                ```
        - `|` : 선택적
            - EX
                ```bash
                sort[-r | -n]  # sort만쳐도 되고 -r 또는 -n 옵션을 선택적으로 줄 수 있음 (동시 안됨)
                ```
        - `문자열`,`{}`,`<>` : 필수
            - EX
                ```bash
                mkdir <문자열이름> # mkdir 사용 시 문자열 필수 입력
                chown {user | user:group} <file> # chown시 user 또는 user:group 둘 중 하나는 필수로 입력 / 파일도
                ```
- 명령어 자동완성
    - Tab을 2번 누르면 아래의 기능이 동작한다.
        1. 입력한 부분으로 시작하는 `명령어 목록` 보여줌
        2. `자동완성` (입력한 부분으로 시작하는 명령어가 1개인 경우)
## 명령어

### history
- 화살표로 `이전` 명령들 확인 가능
- `CTRL + r` : 이전 명령 `검색 모드`

    ```bash
    (CTRL + r) #누르고
    (reverse-i-search)`l': ls -a /tmp # l을 검색하니까 ls -a /tmp 수행했던게 나온다.
    ```
- `history` : 명령어 수행 기록 출력

    ```bash
    history
    ```
- `!!` : 직전 명령어 다시 실행

    ```bash
    !!
    ```
- `!번호` : 번호에 해당하는 명령어 실행
    - history 결과를 보면 `번호) 명령어` 형식으로 나와있다. 이 번호를 보고 실행하고 싶은 명령어를 실행한다.

    ```bash
    !3 # 3번째 명령어 실행
    ```
- `history -d 라인번호` : 명령어 목록에서 특정 라인 삭제
    ```bash
    history -d 3 # 3번쨰 명령어 삭제
    ```
- `history -c` : 명령어 목록 전부 삭제
    ```bash
    history -c # 명령어 실행 목록 클리어
    ```

- `.bash_history` : history로 출력되는 실제 내용 (in 홈디렉토리(~))
    ```bash
     # 홈 디렉토리에서
    nano .bash_history
    ```
### --help
- 명령어의 도움말을 출력해주는 옵션
- 출력 내용
    1. 사용 방법
    2. 명령어 개요
    3. 지정 가능한 옵션과 의미
- 예시 : cat의 사용 방법 궁금
    ```bash
    cat --help
    ```
    <details>
    <summary>출력 결과</summary>

    ```bash
    Usage: cat [OPTION]... [FILE]...
    Concatenate FILE(s) to standard output.

    With no FILE, or when FILE is -, read standard input.

    -A, --show-all           equivalent to -vET
    -b, --number-nonblank    number nonempty output lines, overrides -n
    -e                       equivalent to -vE
    -E, --show-ends          display $ at end of each line
    -n, --number             number all output lines
    -s, --squeeze-blank      suppress repeated empty output lines
    -t                       equivalent to -vT
    -T, --show-tabs          display TAB characters as ^I
    -u                       (ignored)
    -v, --show-nonprinting   use ^ and M- notation, except for LFD and TAB
        --help     display this help and exit
        --version  output version information and exit

    Examples:
    cat f - g  Output f's contents, then standard input, then g's contents.
    cat        Copy standard input to standard output.

    GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
    Full documentation <https://www.gnu.org/software/coreutils/cat>
    or available locally via: info '(coreutils) cat invocation
    ```
    </details>

### PATH 확인
```bash
echo $PATH # : 으로 구분한 PATH들이 나옴
# 결과 : /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```
- Window와 LINUX의 명령어 찾는 기준
    1. Window : 현재 디렉토리 기준
    2. Linux : PATH 기준
        - 따라서, 명령어를 이름만 입력하면, PATH에 등록되어 있는 경로에서만 찾는다.
        - 만약, 현재 디렉토리 기준으로 하고 싶다면 `./명령어` 형태로 입력하면 된다.
        - `압축`을 풀어서 `프로그램 설치`하는 경우, `명령어`나 `실행파일이 속한 디렉토리`를 `PATH`에 추가해주거나, 등록된 경로로 옮겨줘야만 명령어로 실행 가능
### 명령어 위치 확인
```bash
{whereis/which} [옵션] <명령어>
```
1. whereis 
    - 검색한 명령어를 아래의 경로에서 찾음
        1. `binary` : /bin, /sbin
        2. `manual` : /man 
        3. `source` : /src 
    
    - 옵션
        1. `-b` : 바이너리에서만 찾기
        2. `-m` : 매뉴얼에서만 찾기
        3. `-s` : 소스에서만 찾기
    - 예시, find명령어 위치 찾기
        ```bash
        whereis find
        ```
2. which
    - 검색한 명령어를 `binary`에서만 찾음
        - 즉, `PATH 환경변수`에 저장된 디렉토리에서 검색
    - 옵션
        1. `-a`,`--all` : 모든 내용 출력
        2. `-v`,`-V`,`--version` : 버전 출력
        3. `-i`,`--read-alias` : 별명 설정 환경 출력
    - 예시
        ```bash
        which -a cat #cat 명령어 모든 내용 출력
        ```

## 기본 명령어

### `passwd` : 비밀번호 변경
```bash
passwd [계정]
```
- 현재 접속 중인 계정 비밀번호 변경
    ```bash
    passwd
    ```
- 특정 계정의 비밀번호 변경
    ```bash
    passwd 계정
    ```
### `exit` : 터미널 종료
### `clear` : 터미널 화면 clear

## 별명 관련 설정
### `alias` : 현재 설정된 별명 확인
```bash
alias
```
### `alias 별명 = 설정값` : 별명 설정
```bash
alias lsalf='ls -a -l -f'
```
### `type` : 별명 여부 확인
```bash
type 명령어
```
- 명령어가 별명이면, `lsalf is aliased to 'ls -alf'` 이렇게 나온다.
- 명령어가 별명이 아니면, `cat is hashed (/usr/bin/cat)` 이런 식으로 나온다.
### `unalias` : 별명 삭제
```bash
unalias 별명
```
```bash
unalias lsalf
```
### 원본 명령어 실행법 (명령어가 별명으로 쓰이는 경우)
1. 전체 경로로 실행 (which로 경로 찾아 실행)
2. command 명령어를 추가하여 실행
3. 역슬래시를 추가하여 실행

- 예시
    1. ls 명령어를 별명으로 등록
        ```bash
        kingrange@kilwon:~$ alias ls="ls -a"
        kingrange@kilwon:~$ ls
        .   .bash_history  .bashrc  .local    .ssh
        ..  .bash_logout   .cache   .profile  .sudo_as_admin_successful
        ```
    2. ls를 그냥 실행하고싶다면, 아래처럼 3개 방법 가능
        ```bash
        kingrange@kilwon:~$ which ls
        /usr/bin/ls # 경로 찾음


        kingrange@kilwon:~$ /usr/bin/ls # 1. 그냥 전체 경로로 실행
        command ls # 2. command를 앞에 붙여 실행
        \ls # 3. 역슬래시를 앞에 붙여서 실행
        ```
## 시간 정보
### `date` : 현재 시각과 날짜 출력
- 설치하고, 시스템 설정을 확인할 때 사용
```bash
kingrange@kilwon:~$ date
Tue Jan  6 07:25:49 AM UTC 2026
```
### `timectl` : 시간과 관련된 모든 설정 출력
```bash
kingrange@kilwon:~$ timedatectl
               Local time: Tue 2026-01-06 07:26:39 UTC
           Universal time: Tue 2026-01-06 07:26:39 UTC
                 RTC time: Tue 2026-01-06 07:25:48
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```
## 시스템 사용자 정보 확인
### `logname` : 사용 중인 로그인 네임 확인
```bash
kingrange@kilwon:~$ logname
kingrange
```
### `users` : 접속한 모든 사용자의 아이디
```bash
kingrange@kilwon:~$ users
kingrange kingrange
```
### `who` : 로그인한 모든 사용자 계정 (가장 많이 씀)
- 어디서(접속위치:IP), 언제(접속시간) , 어떻게(접속도구)가 같이 출력
    - pts/0 : 터미널
```bash
kingrange@kilwon:~$ who
kingrange tty1         2026-01-06 05:13
kingrange pts/0        2026-01-06 05:14 (192.168.203.79)
```
### `whoami` : 현재 Ubuntu 사용자
```bash
kingrange@kilwon:~$ whoami
kingrange
```
### `hostname` : 사용자 이름
```bash
kingrange@kilwon:~$ hostname
kilwon
```

## 시스템 정보 확인
### `uname [옵션]`
- 옵션
    1. `a` : 모든 정보 확인
    1. `m` : 하드웨어 정보 확인
    1. `n` : 호스트 네임 확인
    1. `r`: 운영체제 릴리즈 번호 (kernel의 release 번호)
    1. `s` : 운영체제 이름
    1. `v` : 버전 출시 일자
### `arch` : CPU 정보
```bash
kingrange@kilwon:~$ arch
x86_64
```
### `env` : 환경변수
```bash
kingrange@kilwon:~$ env
SHELL=/bin/bash
...(생략)
XDG_RUNTIME_DIR=/run/user/1000
SSH_CLIENT=xxx
XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
SSH_TTY=/dev/pts/0
_=/usr/bin/en
```

## sudo / su
### `sudo` : 관리자 권한 대여
- 관리자 권한을 빌려 실행
    - 명령어 앞에 `sudo`를 붙임
    - 첫 실행 시, 비밀번호 입력
- 예시
    ```bash
    sudo apt-get update
    ```
### `su` : 계정 전환
- `shell을 덮어씌우는 방식`으로 전환하는 것이다. (stack처럼 shell이 쌓임)
    - su로 전환한 후, 원래 상태로 돌아오고 싶다면 다시 su를 쓰는게 아니라, `exit으로 전환된 shell을 삭제`해야 한다.

1. `su 계정` : `현재 계정의 환경 변수`들을 가진 `다른 계정 shell` 실행
    - 사용하는 경우
        1. 현재 작업중인 경로(`PWD`)를 유지해야 할 때
        2. 현재 계정의 설정 (Alias, 변수 등)을 사용해야 할 때
        3. 특정 파일의 권한만 잠깐 수정하고, 지금 개발을 이어가고 싶은 경우
2. `su - 계정` : `새로운 계정`의 환경 변수로 `새로운 계정 shell` 실행
    - 사용하는 경우
        1. DB 관리자 계정으로 전환할 때
            - DB 관리자 계정에 설치된 경로, 데이터 저장 위치, 등의 정보가 담겨있는데, 이는 다른 계정에서 확인 불가능하므로 새로운 계정의 환경 변수로 실행되도록 해야 한다.
        2. 특정 언어/프레임워크 전용 계정
            - ex, Python 3.11 전용 계정으로 실행해야 하는 프로그램을 실행하려면 그 계정의 정보로 넘어가서 실행해야 한다.
        3. 시스템 설정 파일(ex, Shell)을 테스트할 때
3. `su` : root 계정으로 전환

## VI
### Linux 편집기 종류
1. `행 단위 편집기` (한 번에 한 행씩 편집) : ed, ex, sed
2. `화면 단위 편집기` : vi, emacs, nano(메뉴기반)
3. `GUI 편집기` : gedit
4. `모드형 편집기` : vi
    - 입력 모드 / 명령 모드 존재
        1. 입력 모드 : `텍스트 입력`, `커서 이동`만 가능
        2. 명령 모드 : `텍스트 수정/삭제`, `복사/붙이기` 등 편집 가능
5. `비모드형 편집기` : nano
    - 따로 모드가 없음
    - 편집 기능 : `CTRL`, `ALT` 같은 특수키와 함께 사용
### VIM
- vi 이후에 개발된 editor
- 설치
    ```bash
    sudo apt install vim
    ```
- 3가지 모드
    1. `명령` : vi 시작 시 모드
        - 입력 모드로 전환 : `i`,`I`,`a`,`A`,`o`,`O`
            - i,a,o의 차이
                - `i` : 커서 앞에 입력
                - `a` : 커서 뒤에 입력
                - `o` : 커서 다음 줄에 입력
        - 마지막 행모드 전환 : `:`,`/`,`?`
        - 저장하고 종료 : `zz`
        - 커서 이동 : k,j,l,h,^,$,-,+,H,M,L,w,b,e
            - `^` : 커서를 현재 행의 맨 앞으로 이동
                - 정규식에도 같은 의미 (시작하는)
                    - ex, 휴대폰 번호 010 시작 -> ^010
            - `$` : 커서를 현재 행의 맨 마지막으로 이동
                - 정규식에도 같은 의미 (끝나는)
                    - ex, 6764로 끝나는 -> 6764$
            - `H` : 커서를 화면의 맨 윗 행으로 이동
            - `M` : 커서를 화면의 중간 행으로 이동
            - `L` : 커서를 화면의 맨 아랫행으로 이동

    2. `입력` : 문자를 입력하기 위한 모드
        - 명령 모드 전환 방법 : `ESC`
    3. `마지막 행` : 화면의 가장 아랫줄에 명령어를 입력해 문서에 영향을 주는 모드
        - 명령 모드 전환 방법 : `ESC`, `ENTER`
        - 저장하지 않고 종료 : `q`, `q!`(변경 사항 있을 시)
        - 저장하고 종료 : `wq`, `wq!`(변경 사항 있을 시)
- 명령어
    ```bash
    vim [파일 경로]
    ```
    - 파일이 존재하면 편집, 없으면 빈 파일
    - 파일 경로 생략 시, vim 설명 출력
    - 수정 권한이 없으면 읽기 전용이다.

# 참고
1. `GO` : Docker, Kubernetes 만드는데 사용함.
    - GO가 OS를 만들기 위해 나온 언어라서 가상환경을 구축하는데 유용했기 때문
    - 국내 기업들도 GO로 많이 이전하는 중

2. IP
    - `컴퓨터`를 구분하기 위한 주소
    - 종류
        1. `Private IP` : 내부에서 이용되는 네트워크 주소 
            - `중복 가능`하다.
            - 종류
                1. 10.0.0.0 - 10.255.255.255
                2. 172.16.0.0 - 172.16.31.255
                3. 192.168.0.0 - 192.168.255.255
        2. `Public IP` : 외부에서 이용되는 네트워크 주소 
            - `중복되면 안된다.`
    - IPv4 
        - `32bit` 주소 체계
            - 8bit씩 나누어 10진수(0-255) 4자리로 표현한다.

        - `초창기 버전` : A~C Class로 나누어 Class별로 용도가 정해져있었다.
            1. `A 클래스` : 0.0.0.0 - 127.255.255.255 (서브넷 마스크 : 8비트)
            2. `B 클래스` : 128.0.0.0 - 191.255.255.255 (서브넷 마스크 : 16비트)
            3. `C 클래스` : 192.0.0.0 - 223.255.255.255 (서브넷 마스크 : 24비트)
            4. `MultiCast 용도` : 224.0.0.0 - 239.255.255.255 
            5. `예비 IP` : 240.0.0.0 - 255.255.255.255

        - `Classless 버전`(`CIDR`) : 클래스 기반 방식의 `주소 낭비 문제`를 해결하기 위해 등장한 방식
            - 문제 예시, 300개만 필요한 경우 A는 너무 많고, B는 모자람
            - 클래스의 구분 없이 필요한 크기만큼 bit단위로 네트워크를 나누어 할당한다.
                - 주소 뒤에 `/`와 `숫자`를 붙여 네트워크 범위를 나타내는 `Prefix 표기법`을 사용
            - 장점
                1. `유연성`: 클래스 경계에 관계없이 원하는만큼 나눌 수 있다.
                2. `효율성` : 필요한 만큼만 할당하기에 IP 주소 낭비를 어느정도 해결
                3. `서브네팅` : 하나의 큰 네트워크를 여러 개의 작은 네트워크로 나눔
                4. `슈퍼네팅` : 여러 개의 작은 네트워크를 하나의 큰 네트워크로 합쳐 라우팅 테이블을 간소화함.

    - IPv6
        - `IP 주소가 부족함`의 문제를 해결하기 위해 `128bit`로 늘린 버전
3. Port 
    - 컴퓨터에서 동작하는 `프로세스를 구분`하기 위한 주소 (기본적 정의)
    1. `Known Port` : 0 ~ 1023 / 기본 용도가 확정된 포트 (ex, 80-HTTP / 443-HTTPS)ㅡ
    2. `Unknown Port` : 그 외의 번호

4. NAT/PAT
    1. `NAT` (Network Address Translation) : `네트워크 주소`를 `1:1로 변환`하는 기술
        - `내부 네트워크`의 `사설 IP`(`Private IP`) 1개를 `외부 네트워크`의 `공인 IP`(`Public IP`)1개로 직접 매핑
        - 종류
            1. `동적 NAT`
                - `Public IP 주소 Pool`을 만들어 두고, `내부 사용자가 접속`할 때마다 `Pool에서 남는 IP`를 하나씩 `할당`
            2. `정적 NAT`
                - Private IP와 Public IP를 `고정적`으로 `1:1 매핑`, 주로 외부에서 접속하는 `웹 서버`등에 사용된다.
        - 장점
            1. 보안에 유리하다.
                - 외부 해커가 private IP를 볼 수 없다.
                - 내부 ->외부는 가능하지만, `외부->내부로 먼저 들어오려는 시도`는 `NAT 테이블에 정보가 없으면 차단`된다. 
            2. 임시로나마 `네트워크 부족문제를 해결`할 수 있다.
            3. `유연성이 증가`한다.
                - 예를 들어, 내가 사용하는 통신사가 바뀌더라도 공유기의 공인 IP만 변경하면 되기 때문에 내 PC의 IP엔 영향이 없다.
        - 용도
            - 서버 공개
    2. `PAT`(Port Address Translation) : `IP 주소` 뿐만 아니라 `Port 번호`까지 한 번에 교환 (NAT Overload)
        - `내부 네트워크 여러 개`가 단 `하나의 공인 IP를 공유`함.
            - 각 `연결마다 내부 네트워크에 포트 번호를 부여`하여 누가 보낸 패킷인지, 누가 받아야 하는지 구분한다.
        - 장점
            1. `네트워크 부족 문제`를 `크게 해결`한다.
                - `하나의 공인 IP`로 `수만개의 사설 IP` 대응 가능
        - 용도
            - 일반 가정, 사무용 공유기