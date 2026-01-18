# 1월 15일

# C Programming
- Window의 C 컴파일러랑 다르다. (Window는 VisualC MS-C)
- 오픈소스 코드를 이를 이용해서 수정한 후, 나에게 맞게 사용할 수 있다.
## GCC (GNU Compiler Collection)
- 오픈 소스 개발자들이 개발한 Linux용 Compiler
- Ubuntu 배포판에는 기본적으로 GCC가 설치되어 있음.
    - 터미널을 열어서 gcc를 입력하면 확인 가능
- 설치(없으면 설치해야지...)
    ```bash
    sudo apt install gcc
    ```
### 소스코드 작성 및 실행
1. vim 파일명.c 입력 후, 작성
    ```c
    #include <stdio.h>
    int main(){
        printf("Hello World");
        return 0;
    }
    ```
2. 컴파일 및 실행
    ```bash
    gcc <파일명> -o <생성할 실행 파일명> # 컴파일 (실행할 수 있게 만드는 것)
    ./<생성된 실행 파일명> # 실행
    ```
    ```bash
    kingrange@kingrang2:~$ gcc my_first.c -o test # my_first.c 파일의 실행 파일 생성 (컴파일)
    kingrange@kingrang2:~$ ls # 실행 파일 생성 확인
    my_first.c  test  test_dir
    kingrange@kingrang2:~$ ./test # 실행
    Hello World
    ```
    - `./`으로 실행하는 이유
        - 이전에 말했던 것처럼 명령어는 PATH에 등록된 경우에만 이름으로 실행이 가능하다.
            - 만약 PATH에 없는데 실행하고 싶다면
                1. 절대 경로를 입력한다.
                2. ./(현재디렉토리)를 기준으로 상대 경로를 입력한다.
                3. PATH에 등록한다. (export를 이용하여 PATH 환경 변수에 새로운 경로 추가)
        - 실행 가능한 명령어
            1. Shell에 내장된 명령어 (이름만으로 가능)
            2. PATH에 등록된 명령어 (이름만으로 가능)
            3. PATH에 등록되지 않은 명령어 (경로 입력으로 가능)

## make
- makefile에 설정된 정보를 읽어, 여러 소스 파일을 컴파일하고 링크하여 최종 실행 파일을 만드는 명령어
    - 실제 패키지는 많은 파일로 구성되어 있어서, gcc로 일일히 컴파일하여 하나의 실행파일로 만드는 것은 매우 번거롭다.
- 많은 Open Source Software는 Source Code와 함께 makefile을 배포한다.
- 설치(없으면 하쇼)
    ```bash
    kingrange@kingrang2:~$ make --help
    Command 'make' not found, but can be installed with:
    sudo apt install make        # version 4.3-4.1build1, or
    sudo apt install make-guile  # version 4.3-4.1build1
    kingrange@kingrang2:~$ sudo apt install make
    ```
### 예시
1. 소스 코드 작성
    ```c
    #include <stdio.h>
    extern int two();
    /*
    extern : 외부에 있는 링크 파일과 연결될 것이라는 것을 의미
    */
    int main(){
        printf("Go To Module Two--\n");
        two();
        printf("End--\n");
        return 0;
    }
    ```
    ```c
    #include <stdio.h>
    int two(){
        printf("In Module Two--\n");
        printf("Two Logic...\n");
        printf("End Two--\n");
    }
    ```
2. makefile 작성
    ```c
    // 1. 변수 설정: 나중에 이름을 바꾸기 편하게 미리 이름을 정의
    TARGET=main //최종 실행 파일명
    OBJECTS=main.o two.o //중간 단계 오브젝트 파일명

    // 2. 빌드 규칙 설정 : 대상 : 의존성
    ${TARGET} : ${OBJECTS}  // main : [main.o two.o] 라는 의미 main을 만드는데 2개 필요
        gcc -o ${TARGET} ${OBJECTS} // 최종 파일(main) 컴파일 하는데 objects 2개 써라
    main.o : main.c //main o 만들기 위해 main c 필요
        gcc -c main.c // main.c 컴파일 하라
    two.o : two.c // two o 만들기 위해 two c 필요
        gcc -c two.c // two.c 컴파일 하라
    ```
3. make 명령 실행
    ```bash
    kingrange@kingrang2:~/make_file_test$ vim makefile
    kingrange@kingrang2:~/make_file_test$ make
    gcc -c main.c
    gcc -c two.c
    gcc -o main main.o two.o
    kingrange@kingrang2:~/make_file_test$ ls # 파일 생성 확인
    main  main.c  main.o  makefile  two.c  two.o  #잘 생성 되었네.
     # 실행 파일을 준다 -> main 만 준다.
     # 소스 코드를 준다 -> main.c two.c를 준다.
     # 패키지를 준다. -> source code + makefile
    ```
4. 컴파일된 실행 파일 실행
    ```bash
    kingrange@kingrang2:~/make_file_test$ ./main
    Go To Module Two--
    In Module Two--
    Two Logic...
    End Two--
    End--
    ```
# Java Programming
- openjdk를 설치해야 한다.
    ```bash
    sudo apt update
    sudo apt install openjdk-21-jdk
    ```
- 설치 확인
    ```bash
    java -version
    javac -version
    ```
## 예시
1. 소스코드 작성
    ```java
    //자바는 파일명과 클래스 명이 맞아야 한다.
    public class JavaTest{
        public static void main(String[] args){
            System.out.println("Hello Java");
        }
    }
    ```
2. 컴파일 (javac)
    ```bash
    kingrange@kingrang2:~/java_test$ javac JavaTest.java # 컴파일
    kingrange@kingrang2:~/java_test$ ls #확인
    JavaTest.class  JavaTest.java #class 파일(컴파일된 파일) 존재
    ```
3. 실행 (java)
    ```bash
    kingrange@kingrang2:~/java_test$ java JavaTest # 실행 (class 확장자 제외)
    Hello Java # 굿
    ```

# Python Programming
- 없으면 설치
    ```bash
    python3 --version # 확인
    sudo apt upgrade python3 # 업그레이드
    sudo apt install python3-venv #venv 가상환경 모듈
    ```
## 예시
1. 폴더 생성 및 가상 환경 생성
    ```bash
    kingrange@kingrang2:~$ mkdir python_test && cd python_test # 생성 및 이동
    kingrange@kingrang2:~/python_test$ python3 -m venv python_test_venv # 가상환경 생성
    kingrange@kingrang2:~/python_test$ ls
    python_test_venv
    kingrange@kingrang2:~/python_test$ source python_test_venv/bin/activate # 활성화
    ```
2. 코드 작성
    ```python
    print("Hello World")
    ```
3. 실행
    ```bash
    (python_test_venv) kingrange@kingrang2:~/python_test$ python3 main.py
    Hello World
    ```
4. 환경 정보(의존성 등) 내보내기
    ```bash
    (python_test_venv) kingrange@kingrang2:~/python_test$ pip freeze > requirements.txt
    (python_test_venv) kingrange@kingrang2:~/python_test$ ls
    main.py  python_test_venv  requirements.txt
    ```
    - 이 파일을 이용해서 외부 패키지 정보를 알려줄 수 있다.
    - 파이썬은 외부 패키지를 현재 환경에 설치해서 사용한다.
        - 즉, 다른 곳에서 실행하려면 사용한 모든 패키지가 설치되어 있어야 한다.


# Node.js Programming
- [NVM 설치 스크립트 실행](https://www.nvmnode.com/guide/installation-sh.html)
    - 이걸 설치해야 nvm install이 가능하다.
    - 설치 후, `source ~/.bashrc`로 환경에 등록해준다.
- 최신 LTS 버전 설치
    ```bash
    nvm install --lts
    ```
- 설치 확인
    ```bash
    node -v
    npm -v
    ```
- 노드는 설치 시, 가상환경이 자동으로 생긴다.

## 예시
1. node 실행 폴더 및 파일 생성
    ```bash
    mkdir node_test && cd node_test # 폴더 생성 및 이동
    npm init -y # 프로젝트 생성
    kingrange@kingrang2:~/node_test$ ls # 프로젝트 생성하면 아래와 같은 파일 생김
    app.js  package.json
    ```
    - 노드는 모듈을 project 안에 설치
        - 모듈 정보는 package.json에 존재한다.
        - 노드 프로젝트는 modules directory에 모듈을 설치, 
            - 따라서 실제 파일들이 포함된 modules를 포함하면 패키지가 엄청 커지므로, package.json만 업로드한다는 것이다. (like requirements in python)

2. app.js 작성
    ```js
    const http = require("http")
    const hostname = '127.0.0.1';
    const port = 3000;

    const server = http.createServer((req,res)=>{
        res.statusCode = 200
        res.setHeader('Content-Type','text/plain;charset=utf-8')
        res.end('Hello World')
    })

    server.listen(port,hostname,()=>{
        console.log('Server Running')
    })
    ```
3. 실행
    ```bash
    const http = require("http")
    const hostname = '127.0.0.1';
    const port = 3000;

    const server = http.createServer((req,res)=>{
        res.statusCode = 200
        res.setHeader('Content-Type','text/plain;charset=utf-8')
        res.end('Hello World')
    })

    server.listen(prot,hostname,()=>{
        console.log('Server Running')
    })
    ```
    - 새로운 터미널에서 시도하면 잘 나온다.
        - 다른 PC에서 접속하고 싶다면, 방화벽을 해제하는 등의 작업이 필요
# Go Programming
- 설치
    - 압축된 파일을 다운로드 받아, 압축 해제 후 PATH에 추가하여 사용
    - 파일 다운로드
        ```bash
        curl -OL https://golang.org/dl/go1.22.0.linux-amd64.tar.gz
        ```
    - 압축 해제
        ```bash
        kingrange@kingrang2:~$ rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
        [sudo] password for kingrange:
        kingrange@kingrang2:~$ ls /usr/local/go # 잘 다운로드 됨
        api  codereview.cfg   doc     lib      misc     pkg        SECURITY.md  test
        bin  CONTRIBUTING.md  go.env  LICENSE  PATENTS  README.md  src          VERSION
        ```
        - 명령어 : bin (경로에 이걸 추가해야한다.)
        - 소스 : src
    - PATH 추가
        ```bash
        kingrange@kingrang2:~$ export TMP=$PATH # 혹시 모르니까 백업
        kingrange@kingrang2:~$ echo $TMP # 확인
        /home/kingrange/.nvm/versions/node/v24.13.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
        kingrange@kingrang2:~$ export PATH=$TMP:/usr/local/go/bin # 이어 붙이기
        kingrange@kingrang2:~$ echo $PATH # 확인
        /home/kingrange/.nvm/versions/node/v24.13.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/go/bin
        kingrange@kingrang2:~$ source ~/.profile #환경 설정 후 바로 적용
        ```
    - 설치 확인
        ```bash
        kingrange@kingrang2:~$ go version
        go version go1.22.0 linux/amd64 # 아키텍처 확인 중요 (특히 Mac에서 개발하고 Window에서 실행하는 경우 -> 알 수 없이 안될 수 있음)
        ```
## 예시
1. Project 생성 및 실행
    - 작업 디렉토리 생성 / 모듈 생성
        ```bash
        mkdir go_test && cd go_test # 작업 폴더 생성 및 이동
        kingrange@kingrang2:~/go_test$ go mod init go_test
        go: creating new go.mod: module go_test
        kingrange@kingrang2:~/go_test$ ls
        go.mod
        ```
2. main.go 파일 작성
    ```go
    // kingrange@kingrang2:~/go_test$ vim main.go
    // kingrange@kingrang2:~/go_test$ cat main.go
    package main
    import "fmt"
    func main(){
        fmt.Println("GO 테스트")

        a := 10
        b := 20
        sum := a+b
        fmt.Printf("%d + %d = %d\n",a,b,sum)
    }
    ```
3. 실행
    ```bash
    kingrange@kingrang2:~/go_test$ go run main.go 
    GO 테스트
    10 + 20 = 30
    ```

# 원격 접속
## Telnet
- Telecommunication Network
- Internet이나 LAN 연결에 사용되는 Network Protocol
- 보안 문제로 SSH로 원격 제어를 대체했지만, 아래의 용도로 Telnet을 자주 사용한다.
    1. 포트 개방 확인 (네트워크 진단) : 특정 서버의 특정 포트가 열려 있는지 확인할 때 유용
        - telnet 1.2.3.4 80 (특정 IP의 80번 포트가 열려 있는지 테스트)
    2. Application Test : HTTP, SMTP 등 text 기반 프로토콜의 응답을 직접 확인하기 위해
- 우분투에는 기본적으로 설치되어 있다.
    ```bash
    kingrange@kingrang2:~/go_test$ dpkg -l | grep telnet
    ii  telnet                                 0.17-44build1                           amd64        basic telnet client
    ```
### 특징
1. 원격 접속 : CLI를 통해 원격 접속 제어
2. TCP 기반 : 기본적으로 TCP 23번 포트 사용 통신
3. 플랫폼 독립성 : 서로 다른 OS 간에도 표준화된 방식으로 통신 가능
4. NVT(Network Virtual Terminal) : 가상 단말기 개념을 사용하여 데이터를 주고 받는다.
    - 장점 : 서로 다른 System 환경에서도 명령어 인식 가능
### 장점
1. 설치가 간편하고 사용법이 매우 쉽다.
2. 시스템 리소스를 적게 차지한다.
3. 오래된 장비(Legacy System - Router/Switch같은 장비)와도 호스트 호환성이 뛰어나다.
### 단점
1. 데이터를 암호화되지 않은 평문으로 전송한다.
    - 패킷 스니핑 등을 통해 정보가 유출될 위험이 크다.

## ssh
- Secure Shell
- 네트워크 상의 다른 컴퓨터에 로그인하거나 원격 시스템에서 명령을 실행할 수 있게 해주는 보안 네트워크 프로토콜
- 모든 통신 내용을 암호화하여 보안성을 획기적으로 높였다.
    - 데이터를 평문으로 전송하는 Telent,FTP -> 보안에 취약
- 기본적으로 Client-Server 모델로 동작 (표준 포트 : 22)
- 가장 권장되는 인증 방식 : SSH Key(공개/개인) 사용하는 방식
    - 공개키 : 서버에 저장 / 누구나 봐도 상관없음 / 데이터를 암호화하기 위한 도구
    - 개인키 : Client PC에 보관 / 유출 금지 / 암호화된 데이터를 복호화하는데 사용

### 특징
- 암호화 : 패스워드뿐 아니라, 전송되는 데이터 전체를 암호화한다.
- 인증 : 접속 시도하는 사용자가 올바른 사용자인지 확인한다.
    - 비밀번호 / 공개키 이용
- 무결성 : 전송된 데이터가 위변조되지 않았음을 보장한다.
- 압축 : 데이터를 압축하여 전송하므로, 네트워크 효율이 좋다.

### 주요 활용 사례
- 원격 터미널 접속 : Linux 서버 등에 접속해서 명령어를 입력하고 관리
- SFTP/SCPSSH : 보안 채널을 이용한 안전한 파일 전송
- SSH 터널링 : 보안이 취약한 다른 프로토콜을 SSH안에 넣어 안전하게 전달
- Git 원격 저장소 : Github,GitLab 등에서 코드 Push를 위한 인증 수단으로 사용

### SSH 서버 설치 예시
1. ssh 서비스 구동 및 확인
    ```bash
    kingrange@kingrang2:~$ sudo systemctl start ssh # ssh 서비스 시작
    kingrange@kingrang2:~$ sudo systemctl enable ssh  # ssh 서비스 부팅시 자동 시작 설정
    Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
    Executing: /lib/systemd/systemd-sysv-install enable ssh
    kingrange@kingrang2:~$ sudo systemctl status ssh # ssh 상태 확인
    ● ssh.service - OpenBSD Secure Shell server
        Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
        Active: active (running) since Thu 2026-01-15 01:41:08 UTC; 3h 42min ago
        Docs: man:sshd(8)
                man:sshd_config(5)
    Main PID: 774 (sshd)
        Tasks: 1 (limit: 4555)
        Memory: 6.5M
            CPU: 301ms
        CGroup: /system.slice/ssh.service
                └─774 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
    ```
2. 방화벽에서 22번 포트 해제
    ```bash
    kingrange@kingrang2:~$ sudo ufw allow 22/tcp
    Skipping adding existing rule
    Skipping adding existing rule (v6)
    ```
### SSH 서버 키 방식 접속
- 비밀번호보다 안전 / 한 번 설정하면, 비밀번호를 매번 입력하지 않아도 되므로 매우 편리

1. SSH key pair 생성
    - 접속하고자 하는 Client의 Terminal에서 수행
        - 완료되면, ~/.ssh/ 폴더에 id_rsa(개인키)와 id_ras.pub(공개키) 파일이 설정된다.
    ```bash
    ssh-keygen -t rsa -b 4096 -C 이메일
    ```
    - `-t` : 알고리즘 종류 (rsa로 설정)
    - `-b` : 키의 길이 (바이트)(4096바이트 설정)
    - `-C` : 코멘트 (주석)(제작자 식별할 수 있는 코멘트 작성)
2. 공개키를 서버로 전송
    ```bash
    ssh-copy-id -p 포트번호 [사용자명]@[ip주소]
    ```
    ```bash
    ssh-copy-id -p 6764 kingrange@192.168.202.226
    ```

### 접속 방식 설정 시 파일 전송을 하지 않고 설정 가능
- id_rsa.pub 파일의 내용을 서버의 ~/.ssh/authorized_keys 파일의 뒤에 붙여넣으면 된다.

## scp(Secure Copy)
- SSH가 설정된 경우 SSH 프로토콜을 기반으로 네트워크를 통해 파일을 안전하게 전송하는 명령어
### 기본 문법
```bash
scp <옵션> <원본 경로> <대상 경로>
```
### 예시, 클라이언트의 파일(폴더)을 서버로 전송
- 폴더 전송하고 싶을 땐 포트 번호 뒤에 -r 인자 추가
```bash
scp -p <포트번호> <파일경로> <유저이름@IP주소:서버경로>
```
```bash
kingrange@master:~$ scp -P 6765 test.txt kingrange@192.168.202.226:/home/kingrange #master->worker 전송
test.txt            
kingrange@worker1:~$ ls # worker 받음
test.txt
kingrange@worker1:~$ scp -P 6764 -r test_dir/ kingrange@192.168.202.226:/home/kingrange # worker->master 폴더 전송
A                                                                                     100%    0     0.0KB/s   00:00
B                                                                                     100%    0     0.0KB/s   00:00
C                                                                                     100%    0     0.0KB/s   00:00
```

### 예시, 서버 파일 다운로드 받기
```bash
scp -p <포트번호> <파일경로> <유저이름@IP주소:서버경로> <로컬경로>
```
```bash
kingrange@master:~$ scp -P 6765 -r kingrange@192.168.202.226:/home/kingrange/test_dir /home/kingrange
A                                                                                     100%    0     0.0KB/s   00:00
B                                                                                     100%    0     0.0KB/s   00:00
C                                                                                     100%    0     0.0KB/s   00:00
```

# Database Server
## Maria DB
- 설치
    ```bash
    sudo apt install mariadb-server
    ```

### 서비스 활성화 및 확인
```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo systemctl status mariadb
```
### 로컬에서 접속
```bash
sudo mysql # 바로 접속
```
### root 계정 비밀번호 생성
```bash
kingrange@master:~$ sudo mysqladmin -u root password 'tigerisking'
kingrange@master:~$ sudo mysql -u root -p
Enter password:
```
- mysqladmin 명령 사용
    - MariaDB 서버를 관리하는 명령으로 version,status,password 명령을 수행할 수 있다.
        ```bash
        kingrange@master:~$ sudo mysqladmin status
        Uptime: 575  Threads: 1  Questions: 60  Slow queries: 0  Opens: 33  Open tables: 26  Queries per second avg: 0.104
        kingrange@master:~$ sudo mysqladmin version
        mysqladmin  Ver 10.0 Distrib 10.6.22-MariaDB, for debian-linux-gnu on x86_64
        Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

        Server version          10.6.22-MariaDB-0ubuntu0.22.04.1
        Protocol version        10
        Connection              Localhost via UNIX socket
        UNIX socket             /run/mysqld/mysqld.sock
        Uptime:                 9 min 51 sec

        Threads: 1  Questions: 61  Slow queries: 0  Opens: 33  Open tables: 26  Queries per second avg: 0.103
        kingrange@master:~$ sudo mysqladmin password # 그럼 이건 뭐지?
        New password:
        Confirm new password:
        ```
### 유저 생성
```sql
CREATE USER '계정'@'%' IDENTIFIED BY '비밀번호';
```
```sql
MariaDB [(none)]> CREATE USER 'kingrangE'@'%' IDENTIFIED BY 'userpassword';
Query OK, 0 rows affected (0.004 sec)
```
- % 대신에 IP 를 입력하면 설정한 IP에서만 접속이 가능해진다.
    - root의 경우, 127.0.0.1로만 접속 가능하게 한다.
        - ssh로 접속하면 되기 때문에 상관없다.
### 권한 설정
```sql
GRANT ALL PRIVILEGES ON *.* TO '계정'@'접속위치';
FLUSH PRIVILEGES
```
```sql
MariaDB [(none)]> GRANT ALL PRIVILEGES ON *.* TO 'kingrangE'@'%';
Query OK, 0 rows affected (0.004 sec)
MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.001 sec)
```
- 접속
    ```bash
    kingrange@master:~$ sudo mysql -u kingrangE -p
    [sudo] password for kingrange: # sudo 비밀번호
    Enter password: # mysql 비밀번호
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 39
    Server version: 10.6.22-MariaDB-0ubuntu0.22.04.1 Ubuntu 22.04

    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]>
    ```
### 외부 접속이 가능하도록 생성
- 설정 파일에서 Binding 부분을 수정
    ```bash
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    # 파일에서 bind-address = 0.0.0.0으로 수정
    ```
- 수정 후, 서비스 재시작
    ```
    sudo systemctl restart mariadb
    ```
- 3306(sql) 포트를 외부에서 접속할 수 있도록 방화벽 설정
    ```bash
    sudo ufw allow 3306/tcp
    ```
- 포트포워딩 진행
    - 호스트 IP의 포트 번호를 3306과 다르게 하는 것이 좋다. (누구나 SQL 포트번호를 알기 때문)

### 외부 접속 확인
```bash

```
### 백업
```bash
mysqldump -u <사용자 계정> -p <비밀번호> <원본 DB이름> > <파일 경로>
```
### 복원
```bash
mysql -u <사용자 계정> -p <비밀번호> <원본 DB이름> < <파일 경로>
```

## Mongo DB
- 설치
    ```bash
    sudo apt update && sudo apt install gnupg curl
    ```
- MongoDB 공개 GPG 키 등록
    ```bash
    curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
    ```
### 저장소 리스트 추가
    ```bash
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    ```
### 업데이트 및 설치
    ```bash
    sudo apt update
    sudo apt install -y mongodb-org
    ```
### 서비스 활성화 및 확인
    ```bash
    sudo systemctl start mongod
    sudo systemctl enable mongod
    sudo systemctl status mongod
    ```
### 접속 확인
    ```bash
    mongosh
    ```
### 외부 접속 허용
1. /etc/mongod.conf 에서 bind를 0.0.0.0으로 변경

2. 서비스 재시작
    ```bash
    sudo systemctl restart mongod 
    ```
3. 방화벽 추가
    ```bash
    sudo ufw allow 27017/tcp
    ```
### 외부에서 접속
```bash
mongodb://IP주소:포트번호
```
- 계정없이 외부에서 접속하도록 하면, 보안이 취약해지기 때문에, 계정을 생성하여 계정 정보를 포함해서 접속하도록 생성한다.
    - `mongosh`로 접속해서 js 코드를 수행
    ```mongodb
    use admin
    db.createUser({user: "adminUser",pwd:"password123",roles:[{role:"userAdminAnyDatabase",db:"admin"},"readWriteAnyDatabase"]})
    ```
- 인증 모드 수정
    ```bash
    sudo nano /etc/mongod.conf # 파일 접속

    security :  # 파일 내용 중 이 부분 찾아 주석 해제
        authrization: enabled # 추가
    ```
- 서비스 재시작
    ```bash
    sudo systemctl restart mongod
    ```
- 변경 후, 외부 접속
    ```bash
    mongodb://계정:비밀번호@서버주소:포트번호/
    ```

## Redis
- 설치
    ```bash
    sudo apt install redis-server
    ```
- 서비스 활성화 및 확인
    ```bash
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    susdo systemctl status redis-server
    ```
- redis 접속
    ```bash
    redis-cli
    ```
- 외부 접속 가능 설정
    ```bash
    sudo vim /etc/redis/redis.conf # 접속
    bind 0.0.0.0 #으로 변경
    ```
- 서비스 재시작
    ```bash
    sudo systemctl restart redis-server
    ```
- 방화벽
    ```bash
    sudo ufw allow 6379/tcp
    ```
- 실행 후, redis-cli를 실행하고, AUTH 비밀번호를 해야만 명령어 사용이 가능하다.
    ```bash
     #외부접속 URL
    redis-cli -h 서버IP -p 포트번호 -a 비밀번호 #권장 X
    redis-cli -h 서버IP -p 포트번호 # 권장 / 이렇게 로그인하고 AUTH 비밀번호 명령어 입력해서 로그인하기
    ```


# 참고
## IaC (Infrastructure as Code)
- Infra구조를 Code로 만들자
    - yaml같은 설정 파일로 구성하는 것
- makefile도 프로그램 구성하는데, 실수 없이 하기 위해 text로 자동화하는 것