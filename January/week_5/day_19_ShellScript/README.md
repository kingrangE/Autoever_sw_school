# Shell Programming(Script)

## Shell Script
- Unix, Linux, POSIX(Portable Operating System Interface)를 지원하는 Mac OS 등에서 사용하는 명령어들과 if, for과 같은 Programming적인 요소로 이루어진 Interpreter 기반의 Script 언어
### 종류
1. sh
    - ShellScript의 기반
2. bash
    - Linux에서 가장 많이 사용되는 Shell
    - Bourne shell을 기반으로 해서 C Shell과 Korn Shell의 기능을 통합시켜 개발
3. ksh 
    - korn shell
4. csh
    - c shell
5. tsch
6. zsh 
    - bash shell, ksh, tcsh의 일부 기능을 비롯하여 여러가지가 개선된 확장된 Bourne Shell

### 기본 문법
1. 생성 및 실행
    - Script 만들기
        - 확장자 sh 이용
        - 파일 첫 줄에 #!/bin/bash(shebang)을 붙여서 해당 파일이 Shell Script라는 것을 인식시킨다.
        - 실행하고자 하는 명령어를 입력하고 저장
    - 실행
        - sh <shell 경로>
            - Bash 명령어 사용 불가
            - 가볍고 빠르다.
            - 위에 shebang을 적어준다면, 해당 해석기로 동작한다.
        - bash <shell 경로> 
            - Bash 명령어 사용 가능
            - 무겁다.
            - 자체 실행 권한을 가지고 있다.
    - 파일 이름을 가지고 직접 실행
        - 실행 권한을 가지고 있어야 가능 (파일의 소유 권한 변경)
        - PATH에 존재하지 않는다면, `./`을 붙여서 실행
2. 변수 사용
    - 기본 변수 선언, 문자열 출력
        ```bash
        변수명 = 값 #Upsert 방식
        ```
    - 변수 사용
        ```bash
        ${변수명}
        ```
    - 실행 시 변수 전달 방법
        - $1, $2, ... 등 Numbering 표기 시, 아래와 같이 실행 시, 작성한 순서대로 전달된다.
            ```bash
            sh example.sh A B C # $1=A $2=B $3=C 대입
            ```
        - 변수명 전달
            ```bash
            NAME=KILWON sh example.hs # $NAME=KILWON
            ```
3. 함수 사용
    ```bash
     # 정의
    function 이름() {내용} 
     # 호출
    이름 파라미터 파리미터
    ```
4. 전역/지역/환경 변수
    - 전역 변수 : 함수 외부에서 선언하여, 모든 scope에서 사용가능한 함수
    - 지역 변수 : 함수 내부에서 선언하여, 함수 내에서만 사용 가능한 함수
    - 환경 변수 : 시스템을 위해 사전에 예약해두고, 시스템에서 사용하고 있는 변수
        - 자주 사용하는 환경 변수
            1. HOME : 홈 디렉토리
            2. PATH : 실행 파일을 찾는 디렉토리 경로
            3. PWD : 현재 작업 중인 디렉토리
            4. USER : 현재 로그인한 사용자 이름
            5. USERNAME : 현재 로그인한 사용자 이름
            6. HOSTNAME : 현재 컴퓨터 이름
5. 위치 매개변수
    - 스크립트 수행 시, 함께 넘어오는 파라미터
        - `$0` : 스크립트 이름
        - `$1~x` : 파라미터 순서대로 번호 부여, (10번째 부터는 {}로 감싸야 한다.)
        - $* : 전체 인자값 
            - ""를 이용하면, 전체를 하나로 인식
        - $@ : 전체 인자값 (쌍따옴표로 감싸면 다른 결과 나옴)
            - ""를 이용해도 각각으로 인식
        - $# : 매개변수의 총 개수
6. 특수 매개변수
    - 기능
        1. 실행 중인 스크립트나 명령어의 PID를 확인
        2. 실행한 명령어/함수/스크립트 실행 정상 수행 여부 확인
    - 종류
        - $$ : 현재 Script 또는 명령어의 PID
        - $? : 최근에 실행된 명령어,함수,Script 종료 상태
            - 정상 : 0
            - 에러 : 에러코드 (ex, ls에러 = 2)
        - $! : 최근에 실행된 Background 명령의 PID
        - $- : 현재 옵션 플래그
    - 이를 확인하여 현재 스크립트를 백그라운드로 수행할 지 결정할 수 있다.
### 매개변수 개념 확장
1. 기본 변수 사용
    - $변수명을 사용하는데, 뒤에 공백없이 문자열 붙여야 하는 경우, {}를 이용하여 변수와 문자열을 구분할 수 있다.
        - ex, URL 변수로 입력받고 /user를 확인하고싶은 경우
            ```bash
            echo https://${URL}/user
            ```
2. 변수에 Default 제공
    1. 변수가 없을 때만 적용
        - ${변수-문자열} : 문자열로 치환
        - ${변수=문자열} : 문자열을 변수에 저장하고, 변수 치환
        - ${변수+문자열} : 문자열로 변수 치환
        - ${변수?에러메시지} : 변수가 없는 경우, 표준 오류 출력으로 에러메시지 출력
    2. 변수가 없거나 NULL일 때 적용
        - ${변수:-문자열} : 문자열로 치환
        - ${변수:=문자열} : 문자열을 변수에 저장하고, 변수 치환
        - ${변수:+문자열} : 문자열로 변수 치환
        - ${변수:?에러메시지} : 변수가 없거나 null인 경우, 표준 오류 출력으로 에러메시지 출력
    3. 길이 
        - ${변수:시작위치} : 변수가 문자열인 경우, 시작 위치부터 문자열 길이 끝까지 출력
        - ${변수:시작위치:길} : 변수가 문자열인 경우, 시작 위치부터 문자열 길이까지 출력
3. 치환
    - 패턴 변환
        - ${변수#패턴} : 패턴 앞의 모든 문자열 제거
        - ${변수##패턴} : 가장 마지막 패턴 앞의 모든 문자열 제거
        - ${변수%패턴} : 가장 앞 패턴 뒤의 모든 문자열 제거
        - ${변수%%패턴} : 가장 마지막 패턴 뒤의 모든 문자열 제거
        - ${#변수} : 문자열 길이
    - 문자열 치환
        - /를 2개 사용하면, 찾은 모든 문자열 대상으로 적용된다.
        - 바꿀 문자열 자리를 비워두면, 찾은 문자열은 삭제가 된다.
        - 종류
            - ${변수/찾을문자열/바꿀문자열} : 첫 번쨰 패턴을 뒤에 문자열로 치환
            - ${변수/#찾을문자열/바꿀문자열} : 시작 문자열이 일치하면 치환
            - ${변수/%찾을문자열/바꿀문자열} : 마지막 문자열이 일치하면 치환
### 조건문
1. if
    ```bash
    if [ 첫 번째 조건식 ]
    then
        수행문
    elif [ 두 번째 조건식 ]
    then 
        수행문
    else
        수행문
    fi
    ```
    ```bash
    value1=10
    value2=20
    if [ $value1 = $value2 ] #공백 필수
    then
        echo True
    else
        echo False
    fi
    ```
    - 활용
        1. -z : 문자열의 길이가 0인지 확인
            ```bash
            if [ -z $value ]
            then
                echo True
            else
                echo False
            fi
            ```
        2. -gt,-lt : 크다 작다
            ```bash
            if [ $value -gt $value2 ]
            then 
                echo True
            else 
                echo False
            fi
            ```
            ```bash
            if [ $value -gt $value2 ]
            then
                echo True
            else
                echo False
            fi
            ```
2. case
    - 스크립트 파일을 만들 때, case로 여러 OS에 대응할 수 있어야 한다.
        - 그래야 스크립트 파일의 개수가 줄어듦
    ```bash
    case $변수 in
        조건값)
        수행할문장
        ;;
        조건값2)
        수행할문장2
        ;;
        ...
        *)
        수행할문장
    esac
    ```
    ```bash
    case $1 in
        start)
        echo "Start"
        ;;
        restart)
        echo "Restart"
        ;;
        *)
        echo "END"
    esac
    ```
### 반복문
1. for
    - 형식
        ```bash
        for 변수 in [범위(리스트 또는 배열, 묶음)]
        do
            수행할 내용;
        done
        ```
    - 기본 예시
        ```bash
        for num in 1 2 3
        do
            echo $num;
        done 
        1
        2
        3
        ```
        ```bash 
        # 변수 사용
        nums="1 2 3"
        for num in $nums
        do
            echo $num;
        done 
        1
        2
        3
        ```
    - 디렉토리 경로 설정 - 디렉토리 내의 파일 전체 순회 출력
        ```bash
        for file in $HOME/* #$HOME(환경변수)(home dir) 내의 *(전체 파일)목록
        do 
            echo $file
        done
        /home/kingrange/shell
        /home/kingrange/test_dir
        ```
    - {}를 이용하면 python의 range와 같은 의미 (, 대신 .. 사용)
        ```bash
        for num in {1..5..2} #1~5 2개씩 건너뛰기
        do 
            echo $num
        done
        1
        3
        5
        ```
    - 배열 사용
        ```bash
        for fruit in ${array}
        do
            echo $fruit;
        done
        ```
    - C언어처럼 사용
        ```bash
        for ((num=0;num<3;num++))
        do
            echo $num;
        done
        0
        1
        2
        ```
2. while
    - 형식
        ```bash
        while [$변수1 연산자 $변수2]
        do
            반복할 문장
        done
        ```
    - 기본
        ```bash
        v1=1
        v2=5
        while [ $v1 -lt $v2 ]
        do
            echo $v1
            v1=$((v1 + 1))
        done
        1
        2
        3
        4
        ```

### 연산자
1. 문자열 연산자
    - `-z` : 문자열의 길이가 0이면 참
    - `-n` : 문자열의 길이가 0이 아니면 참
2. 숫자 비교 연산자
    - 부등호 사용 가능 : () 안에서 사용
    - `-eq`,-ne,-gt,-lt,-ge,-le도 사용 가능
3. 문자열 비교 연산자
    - ==,!=,=,<,>
4. 논리 연산자
    - -a : and
    - -o : or
    - && : and인데, 이거 쓸 땐, 조건식을 []나 [[]]를 사용
    - || : or인데, and처럼 사용

5. 디렉토리 연산자
    - `-d` : 변수 유형이 directory라면 참
    - `-e` : 변수 유형이 directory/file이라면 참
6. 파일 연산자
    - `-f` : 파일 여부 확인
    - `-L` : 파일이면서, 심볼릭 링크 여부 확인
    - `-r` : 파일이거나 디렉토리면서, 읽기 권한이 있으면 참
    - `-w` : -r과 같고, 쓰기권한
    - `-x` : -r과 같고, 실행 권한
    - `-s` : 파일/디렉토리, 사이즈가 0보다 크면 참
    - `-O` : 파일/디렉토리, 스크립트 실행 소유자와 동일하면 참
    - `-G` : 파일/디렉토리, 스크립트 실행 그룹이 동일하면 참

7. 파일 비교 연산자
    - -nt : 앞의 파일이 뒤의 파일보다 최신 파일이면 참
    - -ot : 앞의 파일이 뒤의 파일보다 오래된 파일이면 참
    - -ef : 동일 파일이면 참
    - 활용 예시
        - sudo apt install
            1. 설치 여부 확인 : directory 존재 여부 확인
            2. 폴더 크기 확인 : -s
            3. 날짜 확인 : 업데이트 할지 말지 결정

### 정규 표현식
- linux나 unix의 특별한 특징을 부여하는 문자들과 메타 문자들의 집합
- 검색에 유용
- 메타문자
    - `.` : 줄바꿈을 제외한 한 개의 문자와 일치
    - `?` : 자신 앞에 나오는 정규 표현식이 없거나, 하나가 일치하는 것을 찾는데, 대부분 한 개의 문자와 매칭할 때 사용
    - `*` : 바로 앞 문자열이나 정규 표현식에서 한 번 이상 반복되는 문자
    - `+` : *과 유사하지만, 반드시 하나 이상의 문자
    - `{숫자}` : 정확하게 N 번
    - `{숫자,}` : N번 이상
    - `{숫자1,숫자2}` : 숫자 1 이상 숫자 2 이하
    - `-` : 범위
    - `^` : 시작하는 문자열 ([^]로 사용 시, 목록의 범위에 없는 문자열 의미)
    - `$` : 라인의 끝 문자열
    - `[]` : 문자들의 집합
    - `\` : 특수 문자를 원래의 문자 의미대로 해석
    - `\b` : 단어 의미
    - `\B` : 줄 의미
### 문자 클래스
- `[:alnum]` : 알파벳이나 숫자
- `[:alpha:]` : 알파벳
- `[:blank:]` : 스페이스나 탭
- `[:cntrl:]` : 제어문자
- `[:digit:]` : 숫자
- `[:graph:]` : 출력 가능한 문자
- `[:print:]` : 출력 가능한 문자(스페이스 포함)
- `[:lower:]` : 소문자
- `[:upper:]` : 대문자
- `[:punct:]` : 문장 부호
- `[:space:]` : 줄바꿈, 스페이스, 탭
- `[:xdigit:]` : 숫자, 16진수 문자
- 텍스트 파일 SSH를 통해 전송
    ```bash
    scp -p 포트번호 파일경로 계정@IP:도착 경로
    ```
- 실습 with expression.txt
    -  C로 시작하고 U로 끝나는 3글자 조회
        ```bash
        grep 'C.U' expression.txt
        ```
    - q로 시작해서 ?로 끝나는 단어, 중간에는 영어 소문자만 존재
        ```bash
        grep -E 'q[[:lower:]]*\?' expression.txt # 클래스는 [[]]안에 표현해야 한다. # 메타문자나 확장 클래스 사용시, -E 옵션 주는 것이 좋다.
        grep -E 'q[a-z]*\?' expression.txt
        ```
    - `-`다음에 2가 1번 이상 나타나고 그 뒤에 -를 포함하는 문자열 조회
        ```bash
        grep -E '\-2+\-' expression.txt
        ```
    - 알파벳 5글자로 시작하고, 알파벳 뒤에 :으로 끝나는 단어가 있는 라인을 검색
        ```bash
        grep '^[a-z][A-Z]{5}\:' expression.txt
        grep '^[[:alpha:]]{5}:' expression.txt
        ```
## Script에서 많이 사용하는 명령
### 1. grep : 문자열 조회
- 기본 사용법
    ```bash
    grep [옵션] 패턴 [파일 경로]
    grep [옵션] [-e 패턴|-f 파일] [파일] 
    ```
    - e : 한 번에 여러 개의 정규식 사용
    - f : 패턴이 파일에 존재
    ```bash
    명령어 | grep [옵션] [패턴 | -e 패턴]
    ```
### 2. find : 파일 찾기
- 기본사용
    ```bash
    find [대상 경로][표현식]
    ```
### 3. awk : 특정 인덱스 문자열 출력
- csv형식으로 되어 있는 파일에서 특정 열의 데이터만 추출하는 것이 가능

### 4. sed : 찾은 문자열 치환
- /etc/ssh/sshd_config 파일에서 #PermitRoot를 찾아서 주석을 해제
    ```bash
    sed 's/#PermitRoot/PermitRoot/' /etc/ssh/sshd_config | grep '^PermitRoot'
    ```
### 5. date : 날짜/시간 반환
- 기본적인 사용법
    ```bash
    date [옵션]
    ```
    - date : 현재 날짜를 설정된 locale 형식으로 보여줌
    - date -d yesterday : 어제 날짜 보여줌
- 기본 사용법 2
    ```bash
    date '+%Y-%m-%d %l:%M %p'
    ```
## 사용자 
### 필요한
- 사용자
- 사용자
- 관련 명
### 수행 과정
- 사용자 계정과 패스워드를 입력 받음
- 입력 정보가 없으면 에러 메시지를 출력하고 스크립트를 종료
- 여러 명의 사용자 계정을 생성하는 경우는 for문을 사용
- 기존 사용자 계정이 있는지 확인
- 사용자 계정이 없으면 생성 + 패스워드 설정
- 사용자 계정 존재시, 계정 있다고 message 출력
### 스크립트 작성 - adduser-script.sh
```bash
#!/bin/bash

if [[ -n $1 ]] && [[ -n $2 ]]
then
    UserList=($1)
    Password=($2)
    for ((i=0; i<${#UserList[@]};i++))
    do 
        if [[ $(cat /etc/passwd | grep ${UserList[$i]} | wc -l)==0]]
        then # 존재 X
            sudo useradd ${UserList[$i]}
            echo ${Password[$i]} | passwd ${UserList[$i]} --stdin
        else # 존재하는 경우
            echo "this User ${UserList[$i]} is existing"
        fi
    done
else
    echo -e '"Input User ID and Password\n "user01 user02" "pw01 pw02"'
fi
```

## Shell Script 예시
### 예시, Hello World를 출력하는 Python File 만드는 Script
1. 파일 생성
    ```bash
    kingrange@master:~/shell$ cat make_py.sh
    #!/bin/bash # bash로 해석

    echo 'print("Hello World!")' > Hello.py
    ```
2. 실행
    ```bash
    kingrange@master:~/shell$ sh make_py.sh
    kingrange@master:~/shell$ ls -l
    total 12
    -rw-rw-r-- 1 kingrange kingrange 32 Jan 16 00:17 A.sh
    -rw-rw-r-- 1 kingrange kingrange 22 Jan 16 00:22 Hello.py
    -r-------- 1 kingrange kingrange 53 Jan 16 00:21 make_py.sh
    ```
3. 파이썬 실행
    ```bash
    kingrange@master:~/shell$ python3 Hello.py
    Hello World!
    ```
4. 삭제 후, 파일 이름으로 실행
    ```bash
    kingrange@master:~/shell$ rm Hello.py #삭제
    kingrange@master:~/shell$ ls #확인
    A.sh  make_py.sh
    kingrange@master:~/shell$ ./make_py.sh #직접 실행
    kingrange@master:~/shell$ ls #확인
    A.sh  Hello.py  make_py.sh #잘 됨
    ```
### 예시2, 이름을 출력해주는 speak_{이름}.py 파일 생성하는 Script
1. 파일 생성
    ```bash
    kingrange@master:~/shell$ cat speak_name.sh
    #!/bin/bash

    echo "print('Hello ${NAME}')" > speak_${NAME}.py
    kingrange@master:~/shell$ cat make_three.sh
    #!/bin/bash

    NAME=길원 sh speak_name.sh
    NAME=KINGRANGE sh speak_name.sh
    NAME=홍길동 sh speak_name.sh
    ```
2. 외부에서 값을 전달해 실행
    ```bash
    kingrange@master:~/shell$ sh make_three.sh
    kingrange@master:~/shell$ ls -l
    total 20
    -rw-rw-r-- 1 kingrange kingrange 106 Jan 16 00:42 make_three.sh
    -rw-rw-r-- 1 kingrange kingrange  16 Jan 16 00:44 speak_KINGRANGE.py
    -rw-rw-r-- 1 kingrange kingrange  62 Jan 16 00:44 speak_name.sh
    -rw-rw-r-- 1 kingrange kingrange  16 Jan 16 00:44 speak_홍길동.py
    -rw-rw-r-- 1 kingrange kingrange  16 Jan 16 00:44 speak_길원.py
    kingrange@master:~/shell$ python3 speak_KINGRANGE.py
    Hello KINGRANGE
    ```
### 예시3, 이름을 전달하면 이름과 현재 시간을 출력해주는 함수 script
1. 파일 생성
    ```bash
    kingrange@master:~/shell$ cat function_test.sh
    #!/bin/bash

    function print(){
            echo "${NAME}님 현재 시간은 $(date)"
    }
    print ${NAME}
    ```
2. 실행
    ```bash
     # function은 bash 기능이므로 bash 실행
    kingrange@master:~/shell$ NAME=KILWON bash function_test.sh
    KILWON님 현재 시간은 Fri Jan 16 01:09:56 AM UTC 2026
    ```
### 예시 4, 파일 여부 체크
```bash
kingrange@master:~/shell$ ls -l /etc/localtime
lrwxrwxrwx 1 root root 27 Jan  6 02:38 /etc/localtime -> /usr/share/zoneinfo/Etc/UTC # 심볼릭 링크
kingrange@master:~/shell$ ls -l /usr/share/zoneinfo/Etc/UTC #해당 파일 확인
-rw-r--r-- 1 root root 114 Apr 22  2025 /usr/share/zoneinfo/Etc/UTC
kingrange@master:~/shell$ FILE=/etc/localtime
kingrange@master:~/shell$ if [ -f FILE ];then echo True; else echo False; fi
False # FILE에 $없음
kingrange@master:~/shell$ if [ -f $FILE ];then echo True; else echo False; fi
True # $붙여서 이제 True
```
# 참고
## 트래픽
- 트래픽 줄이는거 중요함. 돈 내야댐
