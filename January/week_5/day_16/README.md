# 사용자 관리

## 사용자 계정 관리 파일

### `/etc/passwd`
- `사용자 계정 정보`가 들어있는 파일
    - `초창기`엔 `암호도 같이 저장`했으나,`해킹 위험이 증가`하며, `암호`는 `/etc/shadow 파일`에 `별도로 저장`한다.
    - `root 계정`으로 `수정이 가능`하지만, 되도록 `명령으로 수정하는 것을 권장`
        - 이유
        - **`로그 확인`**
            1. `history` 명령어를 통해 행한 내용 확인 가능 (`history -c 실행` 시 `안 보임`)
                ```bash
                kingrange@kilwon:~$ sudo useradd -D -f 3
                kingrange@kilwon:~$ history
                1  sudo useradd -D
                2  history
                3  sudo useradd -D -f 3
                4  history
                ```
            2. 관리자 입장에서 `auth.log` 파일(시스템 전체 보안 파일)으로 확인할 수 있다.
                - `auth.log`파일
                    1. `중요한 설정 변경`이나 `관리자 권한의 사용 내역`을 저장
                        - 누가, 언제, 어떤 명령어로 시스템 설정을 변경했는지 확인할 수 있다.
                - `history -c` 로도 삭제되지 않는다.
        - **`문법 오류 방지`**
            - 직접 입력하는 경우, 에러 발생을 알 수 없지만, `명령어`는 `잘못된 형식이 입력`된 경우 `Error를 내보내 알 수 없는 에러를 방지`해준다.
        - **`원자성`**
            - 명령어를 통한 수정은, 시스템이 안전하게 한 번에 처리함을 보장한다.
#### 파일 구조 
```bash
kingrange@kilwon:~$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
kingrange:x:1000:1000:kingrange:/home/kingrange:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
sshd:x:113:65534::/run/sshd:/usr/sbin/nologin
```
- `7개의 항목`으로 구성됨
    - `로그인 ID : x : UID : GID : 설명 : 홈 dir : 로그인 shell`
        - `로그인 ID` : 사용자 계정의 이름
            - 중복 불가
            - 32자를 넘을 수 없다.
            - `소문자`, `대문자`, `숫자`, `_`, `-` `가능`하지만, `-으로 시작`하거나 `로그인 ID 전체가 숫자면 안된다`.
        - `x` : 암호 자리
            - 초기 유닉스에서는 `여기에 암호를 기재`함
            - 현재는 보안상의 이유로 암호를 `/etc/shadow 파일`에 `별도 보관`
                - BUT, 호환성을 위해 그대로 형태를 유지하고 있음
        - `UID` : 사용자 ID 번호
            - 시스템이 `사용자를 구분`하기 위해 사용하는 번호
            - `0~999`, `65534` : `System User`를 위한 `UID`로 예약되어 있다.
            - `1000~60000` : `일반 사용자`를 위한 `UID`
            - `System User 계정`은 System이 `관리 업무를 위해 내부적으로 사용`하기 위해 `예약`된 계정 => `임의로 수정하지 않는다.`
        - `GID` : 그룹 ID 번호
            - `LINUX`에서 `사용자`는 `무조건 1개 이상의 그룹`에 `소속`
                - `기본 그룹` : `사용자 등록 시 정해짐`
                    - 특별히 소속된 그룹을 지정하지 않을 시, `Login ID가 그룹`으로 등록
            - `시스템에 등록된 Group에 대한 정보`는 `/etc/group 파일`에 저장
        - `설명` : 사용자 실명, 부서명, 연락처 등 사용자에 대한 일반적 정보
        - `홈 dir` : 사용자 계정에 할당된 Home Dir의 절대 경로
        - `로그인 shell` : 로그인 쉘
## `/etc/shadow`
- 암호 정보를 가진 파일
- `/etc/shadow`파일은 root 사용자만 읽고 쓸 수 있다. (`shadow` 그룹은 `읽기`만 가능하다.)
    - `/etc/passwd` 파일은 `누구나 읽을 수 있음.`
    - 확인
        ```bash
        kingrange@kilwon:~$ ls -l /etc/passwd /etc/shadow
        -rw-r--r-- 1 root root   1842 Jan  7 03:05 /etc/passwd # 모두가 읽기 가능
        -rw-r----- 1 root shadow 1131 Jan  6 07:43 /etc/shadow # shadow 그룹까지만 읽기 가능
        ```
### 파일 구조
```bash
kingrange@kilwon:~$ sudo cat /etc/shadow
[sudo] password for kingrange:
root:$y$j9T$SkZ248ZsrGwU4il6lEuxI/$imxaSSn6WnwEfiDW4przAORps1J38tRAweRXQrKyT.3:20459:0:99999:7:::
daemon:*:19977:0:99999:7:::
...
kingrange:$6$wj0ercy9sv5UuoY6$RbLO96WHZI59HZ3bIjMCIxsAyNoyZlNV1YE/LYrVSrF2TvMErug1vMdUOy5V2kkS7YQbIqgdDjvj4v6KYQXxE.:20459:0:99999:7:::
lxd:!:20459::::::
sshd:*:20459:0:99999:7:::
```
- 9개의 항목으로 구성된다.
    1. `로그인 ID` : 사용자 계정의 `이름`
        - login ID
    2. `암호` : `password`
        - 실제 비밀번호가 `일방향 암호화`됨
            - `일방향 암호화` : `암호화 가능`, `복호화 불가`(대신 평문과 비교 가능)
                - 요즘엔 대부분 이 방향을 취함 (그래서 비밀번호 찾기 기능이 비밀번호 변경으로 바뀐 것)
            - 사용자가 로그인할 때 `입력하는 비밀번호를 다시 암호화하여 비교`한다.
            - 비어있다면 암호 없는 계정
            - `시스템 계정` : `*` (위 예시의 daemon)
                - `root`가 `*`이 아닌 이유는 이전에, root 로그인이 필요해서 비밀번호를 설정했기 때문이다.
    3. `최종 변경일` : 암호가 `마지막으로 변경된 날짜`
        - 일반적인 연/월/일이 아니다.
            - UNIX 전통을 따라 1970년 1월 1일(기준시)을 기준으로 `day 수`를 기록
    4. `MIN` : 암호를 `사용할 수 있는 최소 기간`
        - X로 설정된 경우, 암호 변경 후 최소한 X일 동안 그 암호를 그대로 사용해야 한다.
    5. `MAX` : 암호를 `사용할 수 있는 최대 기간`
        - X로 설정된 경우, X기간 동안만 암호를 사용할 수 있다는 것
            - 기간이 지나면, 새로운 암호를 입력하도록 함.
    6. `WARNING` : 암호가 `만료되기 전 경고를 시작하는 day` 수
        - X로 설정된 경우, 암호 만료 X일 전부터 로그인 시, 경고 메시지 출력
    7. `INACTIVE` : 암호가 `만료된 이후에도 사용 가능한 day` 수
        - X로 설정된 경우, X일간 로그인 가능, 이 기간이 지나면 계정이 잠긴다.
            - 잠긴 경우, system 관리자만 해결 가능
    8. `EXPIRE` : `사용자 계정이 만료`되는 날
        - 날짜가 지나면, 로그인할 수 없다.
        - `기준일`로부터 `day수를 기록`한다.
    9. `FLAG` : 향후 사용할 수도 있으니 미워둠

## `/etc/login.defs`
- 사용자 계정의 설정과 관련된 기본값을 정의한 파일
### 파일 구조
```bash
kingrange@kilwon:~$ cat /etc/login.defs # 확인 (너무 길어서 내용 첨부 안함)
```
- 파일 내용
    1. `MAIL_DIR` : 기본 메일 디렉토리
        - 기본 값 : /var/mail
    2. `PASS_MAX_DAYS` : 최대 기간(shadow의 MAX)
        - 기본 값 : 99999
    3. `PASS_MIN_DAYS` : 최소 기간(shadow의 MIN)
        - 기본 값 : 0
    4. `PASS_WARN_AGE` : 경고 출력(shadow의 WARNING)
        - 기본 값 : 7
    5. `UID_MIN`,`UID_MAX` : User 계정 UID 범위
        - 기본 값 : 1000~60000
    6. `SYS_UID_MIN`,`SYS_UID_MAX` : System 계정 UID 범위
        - 기본 값 : 100~999
    7. `GID_MIN`,`GID_MAX` : User 계정 Group ID 범위
        - 기본 값 : 1000~60000
    8. `SYS_GID_MIN`,`SYS_GID_MAX` : System 계정 Group ID 범위
        - 기본 값 : 100~999
    9. `DEFAULT_HOME` : 홈 directory 생성 여부
        - 기본 값 : yes
    10. `UMASK` : umask 값 설정
        - 기본 값 : 022
        - UMASK : 기본 권한 설정할 때 사용하는 마스크 값 (원하는 권한과 반대로 작성)
    11. `USERGROUPS_ENAB` : 사용자 계정 삭제 시, 빈 Group 삭제 여부
        - 기본 값 : yes
    12. `ENCRYPT_METHOD` : 암호화 기법
        - 기본 값 : SHA512

## `/etc/group`
- 그룹의 정보가 저장된 파일
- Linux에서 사용자는 `하나 이상의 그룹`에 속한다.
    - `기본 그룹` : `/etc/passwd` 파일의 GID 항목에 지정된 그룹 
    - `2차 그룹` : `/etc/group` 파일에 지정

### 파일 내용
```bash
kingrange@kilwon:~$ sudo cat /etc/group
[sudo] password for kingrange:
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,kingrange
tty:x:5:
...
tss:x:116:
landscape:x:117:
fwupd-refresh:x:118:
kingrange:x:1000:
```
- 4개의 항목으로 구성
    1. `그룹 이름` : 그룹의 이름
    2. `x` : 암호를 저장하는 곳 
        - `gshadow 파일`에 `그룹 암호 저장`
        - 그룹 암호는 `newgrp 명령`으로 `그룹 임시 전환할 때 필요`하다.
            - `newgrp` : 임시 권한 명령
                - 예를 들어, 내가 속하지 않은 B 그룹의 파일을 잠시 수정해야 하는 경우
                    - 기본적으론, system 관리자에게 권한 요청
                    - 하지만, GroupPW가 설정된 경우, newgrp 명령을 통해 임시로 그룹 권한을 부여받아 사용 가능하다.
                        - 해당 명령을 실행하면, 기존 shell위에 새로운 shell이 생성되어 작업이 가능하다. 
                            - 따라서 shell을 닫으면 권한도 끝난다.
    3. `GID` : 그룹을 식별하는 번호
        - UID와 동일하게 1000~60000은 사용자 계정을 위한 GroupID
    4. `그룹 멤버` : 그룹에 속한 멤버들의 사용자 계정을 ,로 구분하여 입력
        - `사용자의 2차 그룹`을 나타낸다.
            - 사용자의 `1차 그룹은 passwd`에 나와있다.

# 사용자 계정 관리 명령
## `useradd`
- 사용자 계정 생성
### 형식
```bash
useradd [옵션] [로그인 ID]
```
- 옵션
    - `-u UID` : UID를 지정
    - `-o` : UID의 중복을 허용
    - `-g GID` : 기본 그룹의 GID를 지정
    - `-G GID` : 2차 그룹의 GID를 지정
    - `-d Directory명` : 홈 Directory 지정
    - `-s Shell` : 기본 쉘 지정
    - `-c 설명` : 사용자의 이름 등 부가적인 설명 지정
    - `-D` : 기본 값을 설정하거나 출력
    - `-e 유효기간` : EXPIRE 항목을 설정(YYYY-MM-DD)
    - `-f 비활성 날수` : INACTIVE 항목 설정
    - `-k directory` : 계정 생성 시, 복사할 초기 파일이나 Directory를 설정해 놓은 Directory 지정

### 기본 설정 값 확인
1. `useradd -D`
    ```bash
    kingrange@kilwon:~$ useradd -D
    GROUP=100
    HOME=/home
    INACTIVE=-1
    EXPIRE=
    SHELL=/bin/sh
    SKEL=/etc/skel
    CREATE_MAIL_SPOOL=no
    ```

2. `cat /etc/default/useradd`
    ```bash
    kingrange@kilwon:~$ cat /etc/default/useradd
    # Default values for useradd(8)
    #
    # The SHELL variable specifies the default login shell on your
    # system.
    # Similar to DSHELL in adduser. However, we use "sh" here because
    # useradd is a low level utility and should be as general
    # as possible
    SHELL=/bin/sh
    #
    # The default group for users
    # 100=users on Debian systems
    # Same as USERS_GID in adduser
    # This argument is used when the -n flag is specified.
    # The default behavior (when -n and -g are not specified) is to create a
    # primary user group with the same name as the user being added to the
    # system.
    # GROUP=100
    #
    # The default home directory. Same as DHOME for adduser
    # HOME=/home
    #
    # The number of days after a password expires until the account
    # is permanently disabled
    # INACTIVE=-1
    #
    # The default expire date
    # EXPIRE=
    #
    # The SKEL variable specifies the directory containing "skeletal" user
    # files; in other words, files such as a sample .profile that will be
    # copied to the new user's home directory when it is created.
    # SKEL=/etc/skel
    #
    # Defines whether the mail spool should be created while
    # creating the account
    # CREATE_MAIL_SPOOL=yes
    ```

### 기본 설정 값 수정 
- vim,nano 등으로 직접 수정도 가능하지만, `명령(-b,-e,-f,-g,-s)`으로 `수행하는 것`을 권장  
    - 이유
        - **`로그 확인`**
            1. `history` 명령어를 통해 수행한 내용 확인 가능 (`history -c 실행` 시 `안 보임`)
                ```bash
                kingrange@kilwon:~$ sudo useradd -D -f 3
                kingrange@kilwon:~$ history
                    1  sudo useradd -D
                    2  history
                    3  sudo useradd -D -f 3
                    4  history
                ```
            2. 관리자 입장에서 `auth.log` 파일(시스템 전체 보안 파일)으로 확인할 수 있다.
                - `auth.log`파일
                    1. `중요한 설정 변경`이나 `관리자 권한의 사용 내역`을 저장
                        - 누가, 언제, 어떤 명령어로 시스템 설정을 변경했는지 확인할 수 있다.
                - `history -c` 로도 삭제되지 않는다.
        - **`문법 오류 방지`**
            - 직접 입력하는 경우, 에러 발생을 알 수 없지만, `명령어`는 `잘못된 형식이 입력`된 경우 `Error를 내보내 알 수 없는 에러를 방지`해준다.
        - **`원자성`**
            - 명령어를 통한 수정은, 시스템이 안전하게 한 번에 처리함을 보장한다.

- 수정 방식 예시
    ```bash
    kingrange@kilwon:~$ sudo useradd -D -e 2027-12-31
    kingrange@kilwon:~$ sudo useradd -D
    EXPIRE=2027-12-31 # 변경되었다. 다시 비우고 싶으면  "" 입력
    kingrnag
    ```

### 예시
- 이름 : kingrang2 / UID : 6764 / 2차 Group : kingrange / 1월 16일까지 유효 / 비활성 날수 5일 / kingrange의 test_dir 복사 
```bash
    # 생성
kingrange@kilwon:~$ sudo useradd -u 6764 -G kingrange -e 2026-01-16 -c "길원 테스트" -f 5 -m -k /home/kingrange/test_dir kingrang2

    # 확인
kingrange@kilwon:~$ cat /etc/passwd | grep kingrang2 
kingrang2:x:6764:6764:길원테스트:/home/kingrang2:/bin/sh # 2차 그룹의 경우 보이지 않는다. (group 파일에 존재)

kingrange@kilwon:~$ cat /etc/group | grep kingrang2 
kingrange:x:1000:kingrang2 # kingrange그룹에 추가되었다.
kingrang2:x:6764: # 기본 그룹도 잘 나온다.

kingrange@kilwon:~$ sudo cat /etc/shadow | grep kingrang2
kingrang2:!:20466:0:99999:7:5:20469: # 비밀번호 : ! (비밀번호 설정 안 함)/ 만료 전 경고 시작 : 7 / 만료 후 사용 가능 : 5 / 만료 기간 20469 (생성일로부터 3일 뒤(1월 16일) 정확) 

kingrange@kilwon:~$ sudo passwd kingrang2 # 비밀번호 설정
kingrange@kilwon:~$ sudo cat /etc/shadow | grep kingrang2
kingrang2:$y$j9T$v8OMA5yFbUw1Ri0KPIaGu/$V/HPLj4B4pGOWIDSe1bycdXbcXtxBp8Su83doZPj.Z.:20466:0:99999:7:5:20469: # 잘 설정되었다.
```
- 만약, 한 줄로 비밀번호 설정을 하고싶다면? **`chpasswd`** (자동화)
    - `chpasswd` 
        - 비밀번호 변경/설정 등을 하는 명령어
            - `id:pw` 형태로 설정한다.
        - 활용
            ```bash
             # pw.txt 파일에 id:pw 형태의 여러 줄의 정보가 있고 한 번에 수정
            sudo chpasswd < pw.txt
            ```
    ```bash
    echo 'kingrang2:비밀번호123' | sudo chpasswd 
     # 이렇게 설정한 경우 비밀번호가 평문으로 나타나기 때문에 보안에 취약하다.
     # 만약 이렇게 했다면, history -c로 명령어 기록 삭제를 하는 것이 좋다.
    ```

### /etc/skel
- 사용자 계정을 생성할 때, `공통적으로 모든 사용자 계정의 홈 디렉토리에 배포해야 할 파일을 설정`하는 파일
    - `-k` 옵션으로 다른 폴더를 주면, `대체`된다.
- 만약 A,B,C 파일을 공통으로 생성해야 한다면
    ```bash
    kingrange@kilwon:/etc/skel$ ls -a 
    .  ..  .bash_logout  .bashrc  .profile
     # 이 폴더에 A,B,C를 추가하면 된다.
    kingrange@kilwon:/etc/skel$ touch A B C
    kingrange@kilwon:~$ sudo useradd -m test_1 # test_1 계정 생성
    kingrange@kilwon:~$ echo "test_1:1234" | sudo chpasswd # 로그인을 위해 비번 설정
    $ ls # 로그인해서 확인 (sh로 되어있어서 나중에 -S /bin/bash으로 변경해줬음(일단 지금은 sh임))
    A  B  C
    ```

## `adduser`
- `사용자 계정 생성` 명령
    - 기본 설정에 따라 사용자 계정 등록 후, 암호 및 기타 정보를 이어서 입력하도록 한다.
### 형식
```bash
adduser [옵션] 로그인ID
```
- 옵션
    1. `--uid UID` : UID 지정
    2. `--gid GID` : GID 지정
    3. `--home DIR` : 홈 directory 지정
    4. `--shell 쉘` : 기본 쉘 지정
    5. `--gecos 설명` : 사용자 이름 등 부가적 설명 지정
### 예시
```bash
kingrange@kilwon:~$ sudo adduser test_2
Adding user `test_2' ...
Adding new group `test_2' (1001) ...
Adding new user `test_2' (1001) with group `test_2' ...
Creating home directory `/home/test_2' ...
Copying files from `/etc/skel' ...
New password: # 직접 바로 입력받음
Retype new password: # 직접 바로 입력받음
passwd: password updated successfully
Changing the user information for test_2
Enter the new value, or press ENTER for the default
        Full Name []: 길원이야 # 직접 바로 입력받음
        Room Number []: 010 # 직접 바로 입력받음
        Work Phone []: 9843 # 직접 바로 입력받음
        Home Phone []: xxxx # 직접 바로 입력받음
        Other []: 길원이야 # 직접 바로 입력받음
chfn: name with non-ASCII characters: '길원이야'
chfn: '길원이야' contains non-ASCII characters
Is the information correct? [Y/n] Y 

kingrange@kilwon:~$ cat /etc/passwd | grep test_2 # 생성 결과 확인
test_2:x:1001:1001:길원이야,010,9843,xxxx,길원이야:/home/test_2:/bin/bash
```
### 기본 설정 값 확인
- `/etc/adduser.conf`
```bash
kingrange@kilwon:~$ cat /etc/adduser.conf | more
# /etc/adduser.conf: `adduser' configuration.
# See adduser(8) and adduser.conf(5) for full documentation.

# The DSHELL variable specifies the default login shell on your
# system.
DSHELL=/bin/bash

# The DHOME variable specifies the directory containing users' home
# directories.
DHOME=/home

# If GROUPHOMES is "yes", then the home directories will be created as
# /home/groupname/user.
GROUPHOMES=no

# If LETTERHOMES is "yes", then the created home directories will have
# an extra directory - the first letter of the user name. For example:
# /home/u/user.
LETTERHOMES=no

# The SKEL variable specifies the directory containing "skeletal" user
# files; in other words, files such as a sample .profile that will be
# copied to the new user's home directory when it is created.
SKEL=/etc/skel

# FIRST_SYSTEM_[GU]ID to LAST_SYSTEM_[GU]ID inclusive is the range for UIDs
# for dynamically allocated administrative and system accounts/groups.
# Please note that system software, such as the users allocated by the base-
passwd
# package, may assume that UIDs less than 100 are unallocated.
FIRST_SYSTEM_UID=100
LAST_SYSTEM_UID=999

FIRST_SYSTEM_GID=100
LAST_SYSTEM_GID=999

# FIRST_[GU]ID to LAST_[GU]ID inclusive is the range of UIDs of dynamically
# allocated user accounts/groups.
FIRST_UID=1000
LAST_UID=59999
```

## `usermod`
- 사용자 계정 정보 수정
### 형식
```bash
usermod [옵션][로그인 ID]
```
- 옵션
    - **`-u uid`** : UID를 수정
    - **`-o`** : UID 중복 허용으로 수정
    - **`-g GID`** : 기본 그룹 수정
    - **`-G GID`** : 2차 그룹 수정
    - **`-d directory`** : 홈 directory 수정
    - **`-s 셸`** : 기본 셸 수정
    - **`-c 설명`** : 부가적인 설명 수정
    - **`-f inactive`** : 계정 비활성화 날짜 수정
    - **`-e expire`** : 계정 만료 날짜 수정
    - **`-l`** : 계정 이름 수정
### 예시
1. **`이름 변경`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -l changed_test2 test_2 # 이름 변경
    kingrange@kilwon:~$ cat /etc/passwd | grep changed_test2
    changed_test2:x:1001:1001:길원이야,010,9843,xxxx,길원이야:/home/test_2:/bin/bash
    ```
2. **`UID 변경`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -u 59959 changed_test2 # UID 변경
    kingrange@kilwon:~$ cat /etc/passwd | grep changed_test2
    changed_test2:x:59959:1001:길원이야,010,9843,xxxx,길원이야:/home/test_2:/bin/bash
    ```
3. **`GID 변경`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -g 1000 changed_test2
    kingrange@kilwon:~$ cat /etc/passwd | grep changed_test2
    changed_test2:x:59959:1000:길원이야,010,9843,xxxx,길원이야:/home/test_2:/bin/bash
    ```
4. **`2차 그룹 수정`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -G 1000 changed_test2
    kingrange@kilwon:~$ cat /etc/group | grep 1000
    kingrange:x:1000:kingrang2,changed_test2
    ```
5. **`homedir 수정`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -d /home/kingrange changed_test2
    kingrange@kilwon:~$ cat /etc/passwd | grep changed_test2
    changed_test2:x:59959:1000:길원이야,010,9843,xxxx,길원이야:/home/kingrange:/bin/bash
    ```
6. **`기본 셸 수정하면서 설명 수정하고 비활성화 날짜 수정`**
    ```bash
    kingrange@kilwon:~$ sudo usermod -s "" -c "this is king" -f 5 changed_test2
    kingrange@kilwon:~$ cat /etc/passwd | grep changed_test2
    changed_test2:x:59959:1000:this is king:/home/kingrange:
    kingrange@kilwon:~$ sudo cat /etc/shadow | grep changed_test2
    changed_test2:$y$j9T$l2VLAMJPk0yHEGM6cNm5s.$KGorcHcRPDV8bIyoSfrniCM9eq2i8d5kzKlLOEOVXx0:20466:0:99999:7:5::
    ```
## 패스워드 에이징
- useradd / usermod / passwd / chage 명령으로 가능
    - chage : 패스워드 에이징을 관리하는 별도의 명령
    

### 항목 별 가능한 명령
1. **`MIN`**
    - `passwd -n 날수 유저명`
    - `chage -m 날수 유저명`
2. **`MAX`**
    - `passwd -x 날수 유저명`
    - `chage -M 날수 유저명`
3. **`WARNING`**
    - `passwd -w 날수 유저명`
    - `chage -W 날수 유저명`
4. **`INACTIVE`**
    - `useradd -f 날수 유저명`
    - `usermod -f 날수 유저명`
    - `chage -I 날수 유저명`
5. **`EXPIRE`**
    - `useradd -e 날수 유저명`
    - `usermod -e 날수 유저명`
    - `chage -E 날수 유저명`
6. **`패스워드 에이징 변경 및 설정 내용 확인`**
    - `chage -l 계정명`
    ```bash
    kingrange@kilwon:~$ sudo chage -l changed_test2
    Last password change                            : Jan 13, 2026
    Password expires                                : never
    Password inactive                               : never
    Account expires                                 : never
    Minimum number of days between password change    : 0
    Maximum number of days between password change    : 99999
    Number of days of warning before password expires : 7
    ```
# 그룹 관리 명령
## `groupadd`
- 그룹 생성 명령
### 형식
```bash
groupadd [옵션] [그룹명]
```
- 옵션
    1. `-g GID` : 그룹의 GID 지정 (`--gid`로도 가능하다.)
    2. `-o` : 중복 허용 
### 예시
1. **`그냥 생성`**
    ```bash
    kingrange@kilwon:~$ cat /etc/group | grep test_group
    test_group:x:6766:
    ```
2. **`GID 지정 및 중복`**
    ```bash
    kingrange@kilwon:~$ sudo groupadd -g 6766 redundant_group # o 없으면 에러
    groupadd: GID '6766' already exists
    kingrange@kilwon:~$ sudo groupadd -g 6766 -o redundant_group 
    kingrange@kilwon:~$ cat /etc/group | grep 6766
    test_group:x:6766:
    redundant_group:x:6766:
    ```
## `groupmod`
- 그룹 정보 수정 명령
### 형식
```bash
groupmod [옵션] [그룹명]
```
- 옵션
    1. **`-g GID`** : 그룹의 GID 수정
    2. **`-o`** : 중복 허용되게 수정
    3. **`-n 그룹명`** : 그룹명 변경
### 예시
1. **`이미 있는 GID로 수정`**
    ```bash
    kingrange@kilwon:~$ sudo groupmod -g 6766 test_2 # o 없으면 에러
    groupmod: GID '6766' already exists
    kingrange@kilwon:~$ sudo groupmod -g 6766 -o test_2 # o 넣어서 수정
    kingrange@kilwon:~$ cat /etc/group | grep 6766
    test_2:x:6766:
    test_group:x:6766:
    redundant_group:x:6766:
    ```
2. **`그룹명 변경`**
    ```bash
    kingrange@kilwon:~$ sudo groupmod -n redundant_group2 test_2
    kingrange@kilwon:~$ cat /etc/group | grep 6766
    test_group:x:6766:
    redundant_group:x:6766:
    redundant_group2:x:6766: # 잘 변경됨
    ```
## `groupdel`
- 그룹 삭제
### 형식
```bash
groupdel 그룹이름
```

## `gpasswd`
- `그룹 암호 설정` 및 `유저 추가`
### 형식
```bash
gpasswd [옵션][그룹명]
```
- 옵션
    1. `무옵션` : 그룹 암호 설정
    1. `-a 계정명` : 사용자 계정을 그룹에 추가
    2. `-d 계정명` : 사용자 계정을 그룹에서 삭제
    3. `-r` : 그룹 암호 삭제

### 예시
1. **`user 추가`**
    ```bash
    kingrange@kilwon:~$ sudo gpasswd -a kingrange test_group
    Adding user kingrange to group test_group
    kingrange@kilwon:~$ cat /etc/group | grep 6766
    test_group:x:6766:kingrange
    redundant_group:x:6766:
    redundant_group2:x:6766:
    ```
2. **`user 삭제`**
    ```bash
    kingrange@kilwon:~$ sudo gpasswd -d kingrange test_group
    Removing user kingrange from group test_group
    kingrange@kilwon:~$ cat /etc/group | grep 6766
    test_group:x:6766:
    redundant_group:x:6766:
    redundant_group2:x:6766:
    ```
3. **`group pw 설정 및 삭제`**
    ```bash
    kingrange@kilwon:~$ sudo gpasswd test_group # 설정
    kingrange@kilwon:~$ sudo cat /etc/gshadow | grep test_group
    test_group:$6$d4H3t/RSUHN7$5mJsNUvVhaTpxm1aKooCQHbr9reLT9z8TXJag9pcCaWM5E6SA6quxkSIRVejXOA4sFBhGLtqAqZglYqqiyIeX0::
    kingrange@kilwon:~$ sudo gpasswd -r test_group #삭제
    kingrange@kilwon:~$ sudo cat /etc/gshadow | grep test_group
    test_group:::
    ```
## groups 
- 사용자가 속한 그룹 확인 명령
### 형식
```bash
groups [계정명]
```
### 예시
```bash
kingrange@kilwon:~$ sudo gpasswd -a kingrange test_group # test_group에 kingrange 넣음
Adding user kingrange to group test_group
kingrange@kilwon:~$ groups 
kingrange adm cdrom sudo dip plugdev lxd # 정보를 갱신하지 않아서 없다.
kingrange@kilwon:~$ newgrp test_group # 그룹 정보 갱신
kingrange@kilwon:~$ groups # 조회
test_group adm cdrom sudo dip plugdev lxd kingrange
kingrange@kilwon:~$ groups test_1 # 다른 계정도 확인 가능 (kingrange 그룹에 추가했었음)
test_1 : test_1 kingrange
```

# 사용자 정보 관리 명령
## UID와 EUID
### UID 
- 실제 UID
- RUID라고 부르기도 함.
- 사용자가 로그인할 때 사용한 계정의 UID
### EUID 
- 유효 사용자 ID
- 현재 명령을 수행하는 주체의 UID
### 두 값이 달라지는 경우
1. su 명령으로 계정을 전환한 경우 : (새로운 Inner Shell 생성)
    - `UID` : `로그인한 ID`
    - `EUID` : `전환한 계정`의 `UID`
    ```bash
    kingrange@kilwon:~$ su test_3
    Password:
    test_3@kilwon:/home/kingrange$ # CTRL + D
    exit
    kingrange@kilwon:~$ # 돌아옴
    ```
2. 실행 파일에 setuid가 설정된 경우
    - `UID` : 파일 `실행한 사용자 계정의 UID`
    - `EUID` : 해당 `파일 소유자 UID`
### 확인 명령
- `whoami`,`who am i`,`id` 명령
```bash
kingrange@kilwon:~$ whoami # 현재는 같은 상황이므로 같음
kingrange
 # 여기서 이름이 나오는 이유는, whoami를 실행하면, program이 kernel에게 `geteuid`를 호출하여 EUID를 가져오고, 해당 값과 passwd를 비교하여 이름을 찾아 화면에 출력하기 때문
kingrange@kilwon:~$ who am i 
kingrange pts/0        2026-01-13 02:18 (192.168.202.226)
kingrange@kilwon:~$ id # 잘 나온다.
uid=1000(kingrange) gid=1000(kingrange) groups=1000(kingrange),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd)
```
## who
- 사용자 확인 명령
### 형식
```bash
who [옵션]
```
- 옵션
    - `-q` : 사용자명만 출력
    - `-H` : 출력 항목의 Column명 함께 출력
    - `-b` : 마지막으로 재부팅한 날짜와 시간을 출력
    - `-m` : 현재 사용자 계정의 정보를 출력
    - `-r` : 현재 Run Level 출력
- 참고
    - Terminal 
        - `pts/0` : 가상 터미널(telnet이나 ssh)로 접속
        - `tty1` : 로컬 터미널로 접속
### 예시
1. 로그인한 사용자 조회
    ```bash
    kingrange@kilwon:~$ who
    kingrange tty1         2026-01-07 00:05
    kingrange pts/0        2026-01-13 02:18 (192.168.202.226) #window 터미널(1)로 접속
    test_3   pts/1        2026-01-13 04:46 (192.168.202.226) #window 터미널(2)로 접속
    ```
2. 로그인한 사용자 조회 with Column명
    ```bash
    kingrange@kilwon:~$ who -H
    NAME     LINE         TIME             COMMENT
    kingrange tty1         2026-01-07 00:05
    kingrange pts/0        2026-01-13 02:18 (192.168.202.226)
    test_3   pts/1        2026-01-13 04:46 (192.168.202.226)
    ```
3. 로그인한 사용자 이름 및 인원수 확인
    ```bash
    kingrange@kilwon:~$ who -q
    kingrange kingrange test_3
    # users=3
    ```
3. 모든 옵션 다 켜서 확인
    ```bash
    kingrange@kilwon:~$ who -a
            system boot  2026-01-07 00:05
            run-level 5  2026-01-07 00:05
    kingrange - tty1         2026-01-07 00:05 21:46         974
    kingrange + pts/0        2026-01-13 02:18   .         13561 (192.168.202.226)
    test_3   + pts/1        2026-01-13 04:46 00:01       14514 (192.168.202.226)
            pts/2        2026-01-09 00:45              6453 id=ts/2  term=0 exit=0
    ```
## w
- 사용자 로그인 정보 및 작업 확인 명령 (who 보다 훨씬 자세한 내용)
### 형식
```bash
w [options]
```
- 옵션
    - `-h`, `--no-header` : do not print header
    - `-u`, `--no-current` : ignore current process username
    - `-s`, `--short` : short format
    - `-f`, `--from` : show remote hostname field
    - `-o`, `--old-style` : old style output
    - `-i`, `--ip-addr` : display IP address instead of hostname (if possible)
    - `-V`, `--version` : output version information and exit

- 실행 결과
    ```bash
    kingrange@kilwon:~$ w
    05:10:39 up 5 days,  9:58,  3 users,  load average: 0.00, 0.00, 0.00 # 시스템 정보
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT # 로그인한 사용자 정보 
    kingrang tty1     -                07Jan26 22:09m  0.07s  0.04s -bash
    kingrang pts/0    192.168.202.226  02:18    0.00s  0.83s  0.01s w
    test_3   pts/1    192.168.202.226  05:03    6:47   0.07s  0.07s -bash
    ```
    - IDLE : 아무것도 하지 않고 대기한 시간 
    - JCPU : 해당 터미널에서 실행된 모든 프로세스가 사용한 CPU 시간
    - PCPU : WHAT 필드에 표시된 현재 프로세스가 사용한 CPU 시간
    - WHAT : 현재 실행중인 명령어

## last
- 로그인했던 사용자 기록 확인 명령
### 형식
```bash
last [options] [<username>...] [<tty>...]
```
- 옵션
    - -<number>            : how many lines to show
    - -a, --hostlast       : display hostnames in the last column
    - -d, --dns            : translate the IP number back into a hostname
    - -f, --file <file>    : use a specific file instead of /var/log/wtmp
    - -F, --fulltimes      : print full login and logout times and dates
    - -i, --ip             : display IP numbers in numbers-and-dots notation
    - -n, --limit <number> : how many lines to show
    - -R, --nohostname     : don't display the hostname field
    - -s, --since <time>   : display the lines since the specified time
    - -t, --until <time>   : display the lines until the specified time
    - -p, --present <time> : display who were present at the specified time
    - -w, --fullnames      : display full user and domain names
    - -x, --system         : display system shutdown entries and run level changes
    -     --time-format <format>  show timestamps in the specified <format>:
    -                               notime|short|full|iso
    - -h, --help           : display this help
    - -V, --version        : display version

- 실행 결과
    ```bash
    kingrange@kilwon:~$ last
    test_3   pts/1        192.168.202.226  Tue Jan 13 05:03   still logged in
    test_3   pts/1        192.168.202.226  Tue Jan 13 04:46 - 04:49  (00:03)
    kingrang pts/0        192.168.202.226  Tue Jan 13 02:18   still logged in
    test_1   pts/0        192.168.202.226  Tue Jan 13 02:18 - 02:18  (00:00)
    kingrang pts/0        192.168.202.226  Tue Jan 13 02:17 - 02:18  (00:00)
    kingrang pts/0        192.168.202.226  Mon Jan 12 00:07 - 02:17 (1+02:09)
    kingrang pts/1        192.168.203.79   Thu Jan  8 08:11 - 01:09  (16:58)
    kingrang pts/0        192.168.203.79   Wed Jan  7 08:13 - 10:16 (2+02:03)
    kingrang pts/0        192.168.203.79   Wed Jan  7 08:12 - 08:13  (00:01)
    kingrang pts/0        192.168.203.79   Wed Jan  7 07:55 - 08:11  (00:16)
    kingrang pts/0        192.168.203.79   Wed Jan  7 07:04 - 07:55  (00:50)
    kingrang pts/0        192.168.203.79   Wed Jan  7 07:03 - 07:04  (00:00)
    kingrang pts/0        192.168.203.79   Wed Jan  7 03:05 - 07:03  (03:57)
    kingrang pts/0        192.168.203.79   Wed Jan  7 03:04 - 03:05  (00:01)
    kingrang pts/0        192.168.203.79   Wed Jan  7 00:06 - 03:04  (02:57)
    kingrang tty1                          Wed Jan  7 00:05    gone - no logout
    reboot   system boot  5.15.0-164-gener Wed Jan  7 00:05   still running
    reboot   system boot  5.15.0-164-gener Tue Jan  6 09:41   still running
    kingrang pts/0        192.168.203.79   Tue Jan  6 05:14 - 08:36  (03:21)
    kingrang tty1                          Tue Jan  6 05:13 - down   (04:33)
    reboot   system boot  5.15.0-164-gener Tue Jan  6 05:12 - 09:46  (04:34)
    reboot   system boot  5.15.0-164-gener Tue Jan  6 03:43 - 09:46  (06:03)
    kingrang pts/0        192.168.203.79   Tue Jan  6 03:29 - 03:43  (00:13)
    kingrang tty1                          Tue Jan  6 03:29 - down   (00:13)
    reboot   system boot  5.15.0-164-gener Tue Jan  6 03:29 - 03:43  (00:13)
    kingrang pts/1        192.168.203.79   Tue Jan  6 03:27 - 03:28  (00:01)
    kingrang tty1                          Tue Jan  6 02:44 - down   (00:43)
    reboot   system boot  5.15.0-164-gener Tue Jan  6 02:42 - 03:28  (00:46)
    wtmp begins Tue Jan  6 02:42:15 2026
    ```

## root 권한 사용
- 2가지 방법 존재
    1. `su 명령을 사용`하여 `root 계정으로 전환`
        - `권장 X`
            - 간단하지만, `일반 사용자`가 `모든 시스템 관리 권한`을 갖게 되어 `보안상 매우 위험`
    2. `일반 사용자`에게 `시스템 관리 작업 중 특정 작업만 수행할 수 있는 권한 부여`
        - ex, 사용자 추가 / 시스템 종료 권한 부여
            - `sudo 명령`으로 `제한적인 권한 부여가 가능`하다.
            - 권한은 `/etc/sudoers` 파일에 설정, `root 계정으로만 수정`할 수 있음
                - but, 파일 직접 수정 대신 `visudo 편집기 사용 권장`

### visudo 설정 형식
- visudo 편집기를 켜서 설정한다.
```bash
User_Alias Host_Alias = (Runas_Alias) Command_Alias
```
- `User_Alias` : 유저명 (누가)
- `Host_Alias` : 호스트 (어디서)
- `Runas_Alias` : 누구의 권한으로
    - 형식 (User:Group)
        - 둘 중 하나만 작성할 수도 있다.
    - 비워둘 경우, (root)
    - 만약, mysql root 접근이 필요하다면, (mysql) 혹은 (ALL)이라고 기재해야 한다.
        - mysql root는 mysql user가 root기 때문
    - (ALL:ALL) : 모든 유저, 모든 그룹 권한
- `Command_Alias` : 커맨드 (무엇을)
    - `ALL` : `모든 명령어`
    - `절대경로 나열` : `권한을 주고 싶은 기능들`의 `절대 경로를 나열`한다.(공백 없이 `,`로 구분)
- 예시
    1. test_1 계정에 useradd할 수 있는 root 권한 부여
        ```bash
        test_1 ALL=/usr/sbin/useradd # ()를 비워둬서 root 권한으로 자동 설정
        ```
        - 결과 : test_1으로 로그인해서 성공
            ```bash 
            $ sudo useradd test_1_test_1
            [sudo] password for test_1:
            $ cat /etc/passwd | grep test_1_test_1
            test_1_test_1:x:59961:59961::/home/test_1_test_1:/bin/bash
            ```
        - IF : root 권한이 아니라 test_3 권한이라면?
            ```bash
            $ sudo useradd test_1_cannot_do_that
            [sudo] password for test_1:
            Sorry, user test_1 is not allowed to execute '/usr/sbin/useradd test_1_cannot_do_that' as root on kilwon.
             # 미안행, 저건 kilwon에서 root로만 돌아가는거야 라고 함.
            ```

## passwd
- 사용자 계정의 암호를 수정하는 명령
    - 암호를 잠그면 암호를 이용한 로그인, sudo 명령 불가 (BUT, 이미 로그인된 세션에는 영향 없음)

### 형식
```bash
passwd [옵션] [사용자 계정]
```
- 옵션
    - `-l 사용자계정` : 지정한 계정의 잠금
    - `-u 사용자계정` : 지정한 계정의 잠금 해제
    - `-d 사용자계정` : 지정한 계정의 암호 삭제

### 예시
1. test_1 계정 잠구기
    ```bash
    kingrange@kilwon:~$ sudo passwd -l test_1
    passwd: password expiry information changed.

    C:\Users\USER>ssh test_1@192.168.202.226
    test_1@192.168.202.226's password:
    Permission denied, please try again. # 거부.
    test_1@192.168.202.226's password:
    ```
2. test_1 잠금 해제
    ```bash
    kingrange@kilwon:~$ sudo passwd -u test_1
    passwd: password expiry information changed.

    C:\Users\USER>ssh test_1@192.168.202.226 # 잘 된다.
    test_1@192.168.202.226's password:
    Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-164-generic x86_64)

    * Documentation:  https://help.ubuntu.com
    * Management:     https://landscape.canonical.com
    ```
3. test_1 암호 삭제
    ```bash
    kingrange@kilwon:~$ sudo passwd -d test_1 
    passwd: password expiry information changed.

    C:\Users\USER>ssh test_1@192.168.202.226
    test_1@192.168.202.226's password: # 암호가 없어져서 로그인이 안된다.
    Permission denied, please try again.
    test_1@192.168.202.226's password:
    ```

## `chown`
- 파일과 디렉토리의 소유자와 소유 그룹을 변경하는 명령

### 형식

```bash
chown [옵션][사용자 계정][파일/디렉토리명]
```
- 옵션 
    - `-R` : recursive (subdirectory까지 변경)

### 예시
- user를 test_1으로 변경
    ```bash
    kingrange@kilwon:~$ ls -l test_dir
    total 0
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 A
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 B
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 C
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 D 
    
    kingrange@kilwon:~$ sudo chown test_1 test_dir/A
    kingrange@kilwon:~$ ls -l test_dir
    total 0
    -rw-rw-r-- 1 test_1    kingrange 0 Jan 13 01:30 A # 잘 변경 되었다.
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 B
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 C
    -rw-rw-r-- 1 kingrange kingrange 0 Jan 13 01:30 D
    ```

## `chgrp`
- `파일`과 `디렉토리의 소유 그룹을 변경`하는 명령

### 형식
```bash
chgrp [옵션] [사용자 계정] [파일명/디렉토리명]
```
- 옵션
    - `-R` : subdirectory도 변경

### 예시
- 그룹을 test_group으로 변경
    ```bash
    kingrange@kilwon:~$ sudo chgrp test_group test_dir/A
    kingrange@kilwon:~$ ls -l test_dir
    total 0 
    -rw-rw-r-- 1 test_1    test_group 0 Jan 13 01:30 A # 잘 변경 되었다.
    -rw-rw-r-- 1 kingrange kingrange  0 Jan 13 01:30 B
    -rw-rw-r-- 1 kingrange kingrange  0 Jan 13 01:30 C
    -rw-rw-r-- 1 kingrange kingrange  0 Jan 13 01:30 D
    ```

---
# 디스크 사용량 설정
- linux는 기본적으로 여러 사용자가 함께 사용하는 시스템이다.
    - 즉, 특정 사용자가 과도하게 디스크를 사용하지 않도록 제한할 필요가 있다.
        - 이 제한을 `디스크 쿼터`라고 한다.
- 디스크 쿼터 설정 방법
    1. 하드디스크에서 사용자가 사용할 수 있는 파일의 전체 용량을 설정
    2. 사용자가 사용할 수 있는 총 파일 수를 설정
## `Hard Limit, Soft Limit`
- 쿼터 값 설정 시, 설정하는 값
- Hard Limit >= Soft Limit

### Hard Limit 
- 사용자가 절대로 넘을 수 없는 최대치
### Soft Limit
- Soft Limit을 넘으면 User에게 경고를 전송
    - 하지만, Hard Limit을 넘지 않았기에 파일 저장은 계속 가능
- Grace Period(유예 기간) :  `Soft Limit을 넘는 것을 허용해주는 기간`, 이 기간을 넘으면 `SoftLimit -> Hard Limit`이 되어 `추가 저장이 불가`해진다.

## `quota`
- ubuntu에서 `disk quota를 설정하기 위해 설치`해야 하는 패키지

### 실무 사용 예시
1. `웹 호스팅` 및 `클라우드 환경`
    - 가장 전형적
    - A User가 대용량 파일을 올려 다른 B User의 사이트가 멈추는 것을 방지하기 위해 쿼터 사용
2. 개발 서버의 `로그 폭주 방지`
    - 특정 Application의 버그로 인해 Log File이 무한대로 쌓여서 Full Disk로 서버가 죽는 사고가 자주 발생
    - 서비스 실행 계정에 쿼터를 걸어 놓으면, 해당 서비스 디스크만 Full Disk가 되므로 전체가 마비되는 현상을 막을 수 있다.
3. ML/빅데이터 워크스테이션
    - 여러 연구자에게 쿼터별로 공정하게 분배하기 위함.

# 네트워크 기초
## TCP/IP 프로토콜
### 프로토콜
- 컴퓨터와 컴퓨터 사이에 데이터를 어떻게 주고 받을 것인지 정의한 통신 규약
- 동일한 프로토콜을 사용하는 기기 간에 통신이 가능하다.
### TCP/IP
- 인터넷 네트워크에서 데이터를 주고받기 위한 프로토콜

### 구조
1. `응용 계층`
    - 기능 : 서비스 제공 Application
    - 프로토콜 : DNS,FTP,SSH,HTTP
    - 장비 : Gateway
    - 전송단위 : Message
2. `전송 계층`
    - 기능 : 데이터 전달 및 흐름제어
    - 프로토콜 : TCP/UDP
    - 전송 단위 : Segment
3. `네트워크 계층`
    - 기능 : 주소 관리 / Routing
    - 프로토콜 : IP/ICMP
    - 장비 : Router
    - 전송 단위 : Packet
4. `링크 계층`
    - 기능 : 네트워크 장치 드라이버
    - 프로토콜 : ARP
    - 장비 : Switch
    - 전송 단위 : Frame
5. `물리 계층`
    - 기능 : 전송 매체
    - 프로토콜 : 케이블 / 무선
    - 장비 : Hub,(리피터 같은 것들)
    - 전송 단위 : Bit

## 주소
### MAC 주소
- Media Access Control의 약자
    - 하드웨어를 위한 주소
    - `Ethernet주소`, `하드웨어 주소`, `물리 주소`라고도 한다.
    - `MAC 주소` -> `NIC카드(Network Interface Card)(랜카드)에 저장`된 주소
- `NIC가 만들어질 때 부여되는 주소`로 `일반적으로 수정 불가`하다.
    - BUT, `일부 NIC`의 경우 `사용자가 MAC 주소를 수정`할 수 있도록 허용한다.
        - 특별한 경우가 아니면, 수정하지 않는 것이 좋다.
- `MAC주소`는 `각 하드웨어를 구별하는 역할` 수행
- 형태
    - `:` 이나 `-`으로 `구분`되는 `16진수 12자리`를 `2개씩 묶어` 구성
        - 앞 세자리 : `제조사 번호` (IEEE에서 지정)
        - 뒷 세자리 : `일련 번호` (제조사에서 지정)
    - `총 48bit`

### IP Address
- 3계층(Network) 주소
- 인터넷 주소 (Internet Protocol Address)(IP Address)
- 인터넷으로 연결된 네트워크에서 각 컴퓨터를 구분하기 위해 사용한다.
- IPv4주소 : 1바이트(8bit) 크기의 숫자 4개로 구성, 총 4바이트
    - `숫자 4개`와 `.`으로 구성
- IPv6 : IPv4 주소가 고갈문제를 해결하기 위해 나온 주소
    - 16진수로 표기하며, 128bit(16바이트)크기
### NetMask
- IP 주소에서 `네트워크부분을 알려주는 역할을 하는 것`이 netmask
    - 즉, Netmask가 동일하면 동일 네트워크로 간주
        - Router의 경로 탐색 과정에서 `나갈 필요`가 없다는 것을 알려주는 시스템

- netmask는 `하나의 네트워크`를 다시 `작은 네트워크(서브넷)`로 분리할 때도 사용한다.
    - 이러한 이유로 `subnet mask`라고 부르기도 한다.
- EX, `C 클래스 IP 주소`의 경우 `기본 넷마스크 255.255.255.0 (24)`
    - 즉, 192.168.202.152에서 네트워크 부분은 192.168.202.0이다.
        - 이런 경우 `192.168.202.152/24 라고 표현`하기도 한다.
- 기억할 IP
    - `0.0.0.0` : 모든 서버 (모두가 동일 네트워크라 간주)
### Broadcast Address
- 자신의 네트워크 대역에서 `가장 마지막 IP 주소`, 이 주소에 데이터를 전송하면, `네트워크에 속한 모든 컴퓨터에게 데이터 전송`
- ex, 192.168.0.101/24인 경우, Broadcast Address : 192.168.0.255
### Network Address
- 자신의 네트워크 대역에서 `첫 번째 IP 주소`, `네트워크를 찾아가기 위한 주소`
- ex, 192.168.185.132/24의 경우 `Network Address : 192.168.185.0`
### 호스트이름
- 문제 : 컴퓨터가 인터넷에 연결되려면 IP 주소가 있어야 하는데, 이 주소는 숫자로 되어 있어서 기억하기 어렵다.
- 해결 : 문자로 된 주소를 고안했는데,이것이 호스트이름 또는 도메인
- 호스트이름 구성 (ex, www.naver.com)
    1. 네트워크 (도메인) (naver.com)
    2. 호스트 (www)
        - 웹 서버와 같이 `Network Service를 제공하는 서버 컴퓨터`는 `용도에 따라 호스트 이름을 붙여서 사용`해야 한다.

### 포트 번호
- Process를 구분하는 번호
- Packet은 IP주소를 보고 PC를 찾아간다.
    - PC에 도착한 `Packet`은 `어떤 서비스에 요청한 것인지 확인`한 다음 `해당 Daemon에 패킷을 전달`한다.
- 웹 서비스를요청 -> 웹 서버 데몬(httpd)에 전달
- 사용 중인 포트번호 확인
    ```bash
    cat /etc/services | grep ftp
    ```
- `/etc/services` 파일에 저장된 포트 번호는 `국제 표준`으로 합의하여 사용하고 있는 것
    - 즉, 사용자가 개발한 네트워크 프로그램은 `/etc/services`에 `정의되지 않은 번호를 사용`해서 `서비스를 제공하는 것을 권장`

## 인터넷에 연결하려면 설정해야 하는 주소
1. IP Address
2. Subnet Mask
3. Broadcast Address
4. Gateway Address
5. DNS Address

## 네트워크 관리자
- 네트워크 제어와 설정을 관리하는 Daemon을 말한다.
- IP주소 설정, 고정 라우터 설정, DNS 설정 등을 수행할 수 있다.
- NetworkManager : Ubuntu에서 제공하는 네트워킹 서비스
- Unix/Linux가 제공하던 ifcfg 형식의 설정 파일도 지원한다.

## 네트워크 관리와 관련된 도구
- 명령 기반
    - `네트워크 관리자` : 기본 네트워킹 데몬
    - `nmcli 명령` : 네트워크 관리자를 사용하는 명령 기반 도구
    - `ip 명령` : 네트워크를 설정하는 명령을 제공
- GUI 기반
    - `[설정]-[네트워크]` : GNOM에서 제공하는 `GUI 기반 도구`
    - `nm-connection-editor` : 네트워크 관리자를 사용하는 `GUI 기반 도구`
        - [설정]-[네트워크]에서 설정할 수 없는 부분도 설정 가능
### nmcli
```bash
nmcli [OPTIONS] OBJECT { COMMAND | help }
```
- 옵션
    - `-a`, `--ask` :  ask for missing parameters
    - `-c`, `--colors auto|yes|no` :  whether to use colors in output
    - `-e`, `--escape yes|no` :  escape columns separators in values
    - `-f`, `--fields <field,...>|all|common` :  specify fields to output
    - `-g`, `--get-values <field,...>|all|commo` :  shortcut for -m tabular -t -f
    - `-h`, `--help` :  print this help
    - `-m`, `--mode tabular|multiline` :  output mode
    - `-o`, `--overview` :  overview mode
    - `-p`, `--pretty` :  pretty output
    - `-s`, `--show-secrets` :  allow displaying passwords
    - `-t`, `--terse` :  terse output
    - `-v`, `--version` :  show program version
    - `-w`, `--wait <seconds>` :  set timeout waiting for finishing operations
- OBJECT(명령)
    - g[eneral] {status | hostname} : NetworkManager's general status and operations
        ```bash
        kingrange@kilwon:~$ nmcli general
        STATE         CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
        disconnected  unknown       enabled  enabled  enabled  enabled
        ```
        - CONNECTIVITY 
            - none : 네트워크에 연결되어 있지 않음
            - limited : 네트워크에 연결되어 있지만, 인터넷 연결되지 않음
            - full : 네트워크와 인터넷 모두 가능
            - unknown : 네트워크 연결 상태를 알 수 없음
    - n[etworking] {on | off | connectivity} : overall networking control
        ```bash
        kingrange@kilwon:~$ nmcli network
        enabled
        kingrange@kilwon:~$ nmcli network off
        Error: failed to set networking: Not authorized to enable/disable networking
        kingrange@kilwon:~$ sudo nmcli network off
        kingrange@kilwon:~$ nmcli network
        disabled
        ```
    - r[adio] : NetworkManager radio switches
    - c[onnection] {show | up | down | modify | add | delete | reload | load} : NetworkManager's connections
    - d[evice] {status | show} : devices managed by NetworkManager
    - a[gent]      : NetworkManager secret agent or polkit agent
    - m[onitor]    : monitor NetworkManager changes

- 네트워크 활성화 또는 비활성화
    ```bash
    kingrange@kilwon:~$ nmcli net con # 상태 확인
    unknown
    nmcli net on # 활성화
    nmcli net off # 비활성화
    ```

- 디바이스(NIC) 상태 확인
    ```bash
    kingrange@kilwon:~$ nmcli dev status # 전체 상태 확인
    DEVICE  TYPE      STATE      CONNECTION
    enp0s3  ethernet  unmanaged  --
    lo      loopback  unmanaged  --
    ```
    ```bash
    kingrange@kilwon:~$ nmcli dev show enp0s3 # 특정 기기 상태 확인
    GENERAL.DEVICE:                         enp0s3
    GENERAL.TYPE:                           ethernet
    GENERAL.HWADDR:                         08:00:27:E7:D2:6A
    GENERAL.MTU:                            1500
    GENERAL.STATE:                          10 (unmanaged)
    GENERAL.CONNECTION:                     --
    GENERAL.CON-PATH:                       --
    WIRED-PROPERTIES.CARRIER:               on
    IP4.ADDRESS[1]:                         10.0.2.15/24 #IPv4 
    IP4.GATEWAY:                            10.0.2.2 #게이트웨이
    IP4.ROUTE[1]:                           dst = 0.0.0.0/0, nh = 10.0.2.2, mt = 100
    IP4.ROUTE[2]:                           dst = 8.8.8.8/32, nh = 10.0.2.2, mt = 100
    IP4.ROUTE[3]:                           dst = 10.0.2.0/24, nh = 0.0.0.0, mt = 100
    IP4.ROUTE[4]:                           dst = 10.0.2.2/32, nh = 0.0.0.0, mt = 100
    IP4.ROUTE[5]:                           dst = 164.124.101.2/32, nh = 10.0.2.2, mt = 100
    IP6.ADDRESS[1]:                         fd17:625c:f037:2:a00:27ff:fee7:d26a/64
    IP6.ADDRESS[2]:                         fe80::a00:27ff:fee7:d26a/64
    IP6.GATEWAY:                            fe80::2
    IP6.ROUTE[1]:                           dst = fd17:625c:f037:2::/64, nh = ::, mt = 100
    IP6.ROUTE[2]:                           dst = fe80::/64, nh = ::, mt = 256
    IP6.ROUTE[3]:                           dst = ::/0, nh = fe80::2, mt = 100
    ```

### ip
- 네트워크 설정이 가능하지만, 재부팅 시 내용 사라짐
    - 내용 보존 : 설정 파일에 저장 필요
```bash
ip [ OPTIONS ] OBJECT { COMMAND | help }
ip [ -force ] -batch filename
```
- 옵션
    - `-V` : 버전 출력
    - `-s` : 자세한 정보 출력
    - 그 외 : {-d[etails] | -r[esolve] |
                    -h[uman-readable] | -iec | -j[son] | -p[retty] |
                    -f[amily] { inet | inet6 | mpls | bridge | link } |
                    -4 | -6 | -M | -B | -0 |
                    -l[oops] { maximum-addr-flush-attempts } | -br[ief] |
                    -o[neline] | -t[imestamp] | -ts[hort] | -b[atch] [filename] |
                    -rc[vbuf] [size] | -n[etns] name | -N[umeric] | -a[ll] |
                    -c[olor]}
- COMMAND
    - `address [add | del | show | help]` : ip 주소 관리
    - `route [add | del | help]` : 라우팅 테이블 관리
    - `link [set]` : NIC 활성화/비활성화

- 정보 조회
    ```bash
    kingrange@kilwon:~$ ip address show # 전체 조회
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
    2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:e7:d2:6a brd ff:ff:ff:ff:ff:ff
        inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
        valid_lft 75450sec preferred_lft 75450sec
        inet6 fd17:625c:f037:2:a00:27ff:fee7:d26a/64 scope global dynamic mngtmpaddr noprefixroute
        valid_lft 86263sec preferred_lft 14263sec
        inet6 fe80::a00:27ff:fee7:d26a/64 scope link
        valid_lft forever preferred_lft forever
    kingrange@kilwon:~$ ip address show enp0s3 # 특정 기기의 IP 조회
    2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:e7:d2:6a brd ff:ff:ff:ff:ff:ff
        inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
        valid_lft 75307sec preferred_lft 75307sec
        inet6 fd17:625c:f037:2:a00:27ff:fee7:d26a/64 scope global dynamic mngtmpaddr noprefixroute
        valid_lft 86120sec preferred_lft 14120sec
        inet6 fe80::a00:27ff:fee7:d26a/64 scope link
        valid_lft forever preferred_lft forever
    ```

- ip 추가
    ```bash
    kingrange@kilwon:~$ sudo ip address add 192.168.0.5/24 dev enp0s3
    [sudo] password for kingrange:
    kingrange@kilwon:~$ ip address show enp0s3
    2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:e7:d2:6a brd ff:ff:ff:ff:ff:ff
        inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
        valid_lft 75249sec preferred_lft 75249sec
        inet 192.168.0.5/24 scope global enp0s3 # IP 추가가 되었다.
        valid_lft forever preferred_lft forever
        inet6 fd17:625c:f037:2:a00:27ff:fee7:d26a/64 scope global dynamic mngtmpaddr noprefixroute
        valid_lft 86062sec preferred_lft 14062sec
        inet6 fe80::a00:27ff:fee7:d26a/64 scope link
        valid_lft forever preferred_lft forever
    ```


## 실습
- 설치
    ```bash
    sudo apt install network-manager
    ```
- 실행 및 상태 확인
    ```bash
    kingrange@kilwon:~$ sudo systemctl start NetworkManager
    kingrange@kilwon:~$ systemctl status NetworkManager
    ● NetworkManager.service - Network Manager
        Loaded: loaded (/lib/systemd/system/NetworkManager.service; enabled; vendor preset: enabled)
        Active: active (running) since Tue 2026-01-13 08:07:53 UTC; 1min 4s ago
        Docs: man:NetworkManager(8)
    Main PID: 16387 (NetworkManager)
        Tasks: 3 (limit: 4555)
        Memory: 2.9M
            CPU: 103ms
        CGroup: /system.slice/NetworkManager.service
                └─16387 /usr/sbin/NetworkManager --no-daemon
    ```
- 부팅 시 자동 활성화
    ```bash
    sudo systemctl enable NetworkManager
    ```


# 참고
## Group ID 중복
- 권한을 똑같이 복제하고 싶을 때 주로 사용한다.
    - `ex, 사용자 계정에서 root 권한 사용`
        - 이를 "별명(Alias)을 만든다."라고 함
    - `ex2, 시스템 이관`
        - 시스템 이관된 경우 새 서버에서 기존 그룹 명칭을 유지하면서 권한 숫자를 일치시켜야 할 때 사용한다.
    - `ex3, NFS 공유`
        - 네트워크 파일 시스템으로 공유할 때, 서버마다 그룹 이름은 달라도 GID를 일치시켜야 파일 접근 권한이 꼬이지 않는다.

- 아래의 이유로 권장하지 않는다.
    1. Linux System은 Group의 이름이 아닌 Group ID로 식별하기 때문에, GID가 같으면 동일한 그룹으로 보고 동일한 권한을 준다.
    2. 보안 문제 : GID가 중복되는 것을 잊고, 권한을 줄 경우, 알 수 없는 중복 그룹에도 권한이 생긴다.
    3. 로그 분석 : 로그 분석에 동일한 GID가 찍히므로 정확히 어떤 그룹에서 한 건지 알기 힘들다.
