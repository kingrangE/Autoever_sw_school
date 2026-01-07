# LINUX

## vi 단축키
- 이거 막 쓰면 멋지다.

### 명령 모드 단축키
#### 특정 행 이동 : `행번호 + G`,`:행번호`
#### 내용 삭제
- `#숫자`를 붙이면 양을 정할 수 있다.
1. 현재 커서 위치 글자 삭제 : `-x`
2. 현재 커서 위치 단어 삭제 : `dw`
3. 현재 커서 위치 행 삭제(잘라내기) : `dd`
4. 커서부터 행의 끝까지 삭제 : `D`

#### 명령 취소
1. 명령 취소 : `u`
2. 해당 행에서 한 `모든 명령 취소` : `U`
3. 마지막으로 작업한 내용으로 돌아가기 : `:e!`

#### 복사/붙여넣기
1. 행 복사 : `yy`
    - `#개수`를 붙이면 `복사할 행 개수 지정`
2. 행 아래에 붙여넣기: `p`
3. 행 위에 붙여넣기 : `P`
4. 잘라내기 : `dd`

#### 검색
- 문자열 `아래 방향 검색` : `/문자열`
- 문자열 `위 방향 검색` : `?문자열`
- 찾던 방향으로 `다음 문자열 검색` : `n`
- 찾던 반대 방향으로 `다음 문자열 검색` : `N`

#### 치환
- `현재 위치 행`에서, `처음 나오는 문자열1`을 `문자열2`로 치환 : `:s/문자열1/문자열2`
- `파일 전체`에서 나오는 문자열1을 문자열2로 치환 : `:s/문자열1/문자열2/g`
- `범위 내 각 행`에서 
    1. `처음 나오는 문자열1`을 `문자열2`로 치환 : `:<범위>s/문자열1/문자열2/`
    2. 나오는 모든 문자열1을 문자열2로 치환 : `:<범위>s/문자열1/문자열2/g`
    3. 나오는 모든 문자열1을 문자열2로 확인하며 치환 : `:<범위>s/문자열1/문자열2/gc`
    - 범위 표현 방식
        1. `%` : 문서 전체
        2. `.` : 현재 줄
        3. `$` : 마지막 줄
        4. `n,m` : n행부터 m행까지

#### 파일 읽기
- 특정 파일 내용을 현재 위치에 삽입 : `:r 파일경로`
- 지정한 파일로 전환 : `:e 파일`
- vi로 여러 파일을 연 경우, 다음 파일로 작업을 이동 : `:n`

#### shell 명령 수행
- vi 내에서 shell 명령 수행 : `:!명령`
    - vi로 돌아오려면 `ENTER` 클릭
- 외부에서 shell 명령 수행 후, 돌아오기 : `:sh`
    - vi로 돌아오려면 `exit` 입력

#### 기타 명령
- `현재 화면 재출력` : `CTRL + I`
- `현재 위치 행을 백분률로 마지막 행에 출력` : `CTRL + g`
- `현재 행과 아랫행 연결` : `SHIFT+j`
- `직전 명령 재수행` : `.`

#### VI 환경 설정
1. 사용자 홈 디렉토리에 `.exrc` 파일에 설정
    - 예시, set list
        ```bash
        vim ~/.exrc # vim으로 켜서 작업
        ```
2. 환경변수 `EXINIT`에 지정
    - 예시, set nu 
        ```bash
        EXINIT='set nu'
        export EXINIT
        ```
3. vi에서 명령으로 실행 (일회성)
    - OPTIONS
        - `set nu` : 줄 번호 출력
        - `set nonu` : 줄 번호 출력 안함
        - `set list` : 눈에 보이지 않는 문자 출력
        - `set nolist` : 눈에 보이지 않는 문자 미출력
        - `set showmode` : 현재 모드 표시
        - `set noshowmode` : 현재 모드 표시하지 않음
        - `set` : set으로 설정한 모든 vi 환경 설정 값을 출력
        - `set all` : 모든 vi 환경 변수와 현재 값을 출력

#### 실습 
1. exec.txt 생성 (vim exec.txt)
2. 내용 작성 (i,a,o로 모드 변경해서 작성하기)
    ```bash
    Hi
    How are you
    Im fine thanks
    Couch potato with beers
    enjoy the cool breeze
    First and foremost
    Last but not least
    In order to keep myself hydrated, I drink a lot of water after riding a bike
    ```
3. 내용 저장 (:w / :wq!)
4. 커서를 3행으로 이동 (:3 / 3G)
5. 파일의 내용 중 you를 kilwon으로 수정 (i,a,o로 모드 변경 수정)
6. 2행의 are를 삭제 (are로 커서 이동 후, dw)
7. 8행의 to부터 끝까지 삭제 (to로 커서 이동 후, D)
8. 삭제한 내용 모두 복원 (:e!)
9. 다시 저장 (:w / :wq!)


## Shell
- 역할
    - 사용자 명령 해석 후, Kernel 전달
    - Kernel의 처리 결과를 사용자에게 전달
- 형태 : `명령을 입력`하는 `인터페이스`
    - Server : Text Mode
    - GUI(X window) : Terminel
---
### 기능
1. **명령어 해석기**
2. **프로그래밍**
    - `Shell Programming` : 자체적인 프로그래밍 기능
    - `Shell Script` : 반복적인 수행 작업을 하나의 프로그램으로 만드는 것
3. **사용자 환경 설정**
    - `사용자 환경을 설정`할 수 있도록 `초기화 파일 기능` 제공
        - `사용자 로그인` 시, `초기화 파일 실행`
            - 사용자 별 특성에 맞게 `초기 환경` 설정
    - 설정 내용
        1. 초기화 파일에 PATH 설정
        2. 파일과 디렉토리를 새로 생성할 때, 기본 권한 설정
        3. 다양한 환경 변수 설정
        4. etc.
---
### 종류
1. 본쉘(sh) : 최초의 쉘, 현재 bash shell로 대체
2. C쉘(csh) : 2BSD UNIX에서 발표
3. 콘쉘(ksh) : SVR4 UNIX에서 발표
4. `bash shell (bsh)`
    - sh와 호환성 유지, csh,ksh의 편의기능 모두 포함
    - LINUX의 기본 쉘로 제공
5. tsch : c쉘 계열의 쉘
6. dash shell
    - sh를 기반으로 개발
    - 작은 크기로 개발
7. `z쉘(zsh)` 
    - 최근에 개발된 shell
    - bash tsch의 기능에 독작적인 기능을 추가
    - 다양한 기능을 제공
---
### login shell & sub shell

#### login shell
- `linux에 접속`했을 때, 보여지는 쉘
- 종료 시 : `터미널 종료` / `원격 접속 해제`
#### sub shell
- 사용자가 Prompt에서 실행한 다른 쉘
- 종료 시 : `이전 쉘 환경`으로 돌아감
- 생성 방법
    1. `()` : 괄호 사용
        ```bash
        (ls) # sub shell에서 ls 명령어 실행
        ```
    2. `|` : 파이프 사용
        ```bash
        ls -a | ls -l # 뒤에 있는 명령어가 sub shell에서 실행
        ```
    3. `쉘 스크립트 실행`
        ```bash
        ./script.sh
        ```
    4. `명령 &`
- 사용 이유
    1. 작업 환경 관리
        - 환경 오염과 같은 side effect로부터 안전하게 메인 작업을 지키기 위해 사용
        - 예시, 다른 디렉토리 이동 후, 파일 삭제
            ```bash
            cd /tmp
            rm -rf *
            cd -    # 다시 원래 디렉토리로 돌아와야 함
            ```
            ```bash
            (cd /tmp && rm -rf *) # 서브로 실행 후 그냥 하던거 하면 된다.
            ```
    2. 병렬 처리
        - 여러 작업을 동시에 실행하고 싶을 때,
        - 예시, 1,2를 실행하고 난 3을 메인으로 작업하고 싶을 때,
            ```bash
            (command1; command2) &  # 두 명령을 묶어서 백그라운드에서 실행
            command3  # command1, 2가 도는 동안 바로 다음 작업 수행 가능
            ```
    3. 복잡한 파이프라인 구성
        - `데이터를 처리`하여 `여러 명령어의 출력`을 묶어 `다른 프로그램에 전달`하고 싶을 때 사용
        - 예시, echo와 cat의 결과 전달
            ```bash
            (echo "--- 로그 시작 ---"; cat app.log; echo "--- 로그 끝 ---") | mail -s "로그 리포트" admin@test.com
            ```
#### shell 종료
- `CTRL+d`, `exit`
---
### bash shell
- 우분투에서 `기본제공`

#### 특징
1. alias 기능 제공
2. history 기능 제공
3. 연산 기능 제공
4. job control 기능 제공
5. 자동 완성 기능 제공
6. Prompt Control 기능 제공
7. 명령 편집 기능
---
### 지원하는 shell 확인
- 지원하는 shell은 /etc/shells 파일에 기재되어 있다.
    - 즉, 해당 파일 확인
- `파일의 내용`을 `바로 확인` : `cat 파일경로`
---
### shell 변경
- shell 변경은 `login shell`을 변경하는 것이다.
- 변경 후, 다시 접속해야 반영된다.

#### 기존 login shell 확인 : `/etc/passwd`
- 예시, kingrange 계정의 login shell 확인
    ```bash
    grep kingrange /etc/passwd
        #결과 : kingrange:x:1000:1000:kingrange:/home/kingrange:/bin/bash  
        #결과가 /bin/bash로 bash shell을 사용하는 것을 알 수 있다.
    ```
#### 쉘 변경 명령 
1. `chsh [옵션] [사용자계정]`
    ```bash
    chsh -s /bin/csh kingrange
    ```
2. `쉘이름 -s sh 사용자계정`
    ```bash
    csh -s sh kingrange
    ```
- 옵션
    1. `-s 쉘절대경로` : 경로에 있는 쉘로 login shell 변경
    2. `-l` : /etc/shells 파일에 지정된 shell 출력
---
### shell 내장 명령
- Shell이 갖는 자체적 내장 명령어
- 종류
    1. `cd` : change directory
    2. `echo` : 
        - 화면에 `한 줄의 문자열` 출력
        - 형식
            ```bash
            echo [-n] [문자열 또는 변수]
            ```
            - `-n` : 마지막에 줄 바꿈을 하냐 안 하냐 여부
        - 예시, kingrangE 출력
            ```bash
            kingrange@kilwon:~$ echo kingrangE
            kingrangE
            kingrange@kilwon:~$ echo -n kingrangE
            kingrangEkingrange@kilwon:~$
            ```
    3. `printf`
        - 형식
            ```bash
            printf [서식] [데이터]
            ```
            - 서식 : C언어와 동일
        - 예시
            ```bash
            kingrange@kilwon:~$ printf "%d + %d = %d \n" 50 40 90
            50 + 40 = 90 #위에 적은대로 출력된다.
            ```        

## 특수 문자
- 명령을 편리하게 입력 및 실행할 수 있도록 다양한 특수 문자를 제공한다.
- 특수 문자 사용법은 모든 쉘에서 거의 유사
- 사용자 : 명령 입력
    1. 쉘 : 입력한 내용 중 특수 문자가 포함 여부 확인
    2. 쉘 : 특수문자를 해독하여 적절한 형태로 변경한 후, 명령 실행

### 문자 매칭
#### `*` : 모든 문자 / 문자열 의미 (개수 상관 X)
- 예시,
    1. `ls *` : `모든 directory` 내용 출력
    2. `cp * /tmp` : `모든 내용`을 tmp directory로 복사

#### `?` : 하나의 문자와 매칭
- 예시
    1. `ls kingrang?` : kingrang으로 시작, 그 뒤에 1글자 오는 것과 모두 매칭

#### `[]` : 대괄호 안의 문자 하나와 매칭 (띄어쓰기 구분)
- 예시
    1. ls -l tmp[1 3 5].txt : tmp1.txt ,tmp3.txt, tmp5.txt 파일 검색

#### `-` : 범위를 나타냄
- 예시
    1. 알파벳 소문자 : a-z
    2. 영문으로 시작하고 두 번째 글자는 숫자 : [A-Za-z][0-9]
    3. 한글로 시작 : [가-힣]

### 경로
#### `~` : 사용자의 홈 디렉토리
#### `-` : 직전 디렉토리
- 예시, 
    ```bash
    kingrange@kilwon:~/test$ cd ..
    kingrange@kilwon:~$ cd -
    /home/kingrange/test # 이렇게 이동할 절대 경로가 한 번 출력되고 이동된다.
    kingrange@kilwon:~/test$
    ```

### 명령 관련
#### `백틱` : 문자열 내의 명령어를 수행 후, 결과로 대체
- 예시, Today is {오늘 날짜}출력
    ```bash
    kingrange@kilwon:~$ echo "Today is `date`" # date 명령어를 ``으로 감싸서 출력에 날짜가 나오도록 함.
    Today is Wed Jan  7 05:06:58 AM UTC 2026
    ```
#### `;` : 여러 개 명령어 연결
- 명령어가 `개별적 실행` (앞에서 실패해도 뒤에 이어서 실행)
- 예시, date,ls,pwd 순차실행
    ```bash
    kingrange@kilwon:~$ date; ls; pwd
    Wed Jan  7 05:24:53 AM UTC 2026
    exec.txt  test  test.txt
    /home/kingrange
    ```
- 예시2, dat,ls,pwd 순차실행 (dat -> error)
    ```bash
    kingrange@kilwon:~$ dat;ls;pwd
    Command 'dat' not found, but can be installed with:
    sudo apt install liballegro4-dev # 결과가
    exec.txt  test  test.txt #잘
    /home/kingrange #나옴
    ```

#### `&&` : 여러 개 명령어 연결
- 명령어가 합쳐서 실행 (앞에서 실패하면 뒤에 시도 X)
- 예시, date,ls,pwd 실행
    ```bash
    kingrange@kilwon:~$ date&&ls&&pwd
    Wed Jan  7 05:26:10 AM UTC 2026
    exec.txt  test  test.txt
    /home/kingrange
    ```
- 예시2, dat,ls,pwd 순차실행 (dat -> error)
    ```bash
    kingrange@kilwon:~$ dat&&ls&&pwd
    Command 'dat' not found, but can be installed with:
    sudo apt install liballegro4-dev
    ```

#### `|` : 앞 프로그램의 출력(stdout)을 가지고 뒤 프로그램의 입력(stdin)으로 연결
- 예시, `ls -al /` 명령어의 길이가 너무 길어서 `more` 명령어로 페이지 단위 출력하기
    ```bash
    ls -al / | more # |을 사용하여 앞의 명령어의 결과를 more로 넘긴다.
    ```
### 특수 문자 무력화
- 특수 문자가 파일 이름 같은 것에 껴있는 경우 사용한다.
#### `\` 
- 특수 문자 앞에 사용하여 `해당 특수 문자 1개를 무력화`한다.
    ```bash
    echo $SHELL
    /bin/bash
    echo \$SHELL
    $SHELL
    ```
#### `''`
- 작은 따옴표로 문자열을 감싸 `내부의 모든 특수 문자를 무력화`한다.
    ```bash
    echo '$SHELL'
    $SHELL
    ```
#### `""`
- 큰 따옴표로 문자열을 감싸 `$ \ ${} {}를 제외`한 `모든 특수 문자를 무력화`한다.
    ```bash
    echo "$SHELL"
    /bin/bash
    ```

## 표준 입출력 장치
- 프로그램이 실행될 때 기본적으로 연결되는 데이터의 입출력 통로

### 종류
1. 표준 입력 (stdin)
    - FD(File Descriptor) : 0
    - 기본 장치 : 키보드
    - 역할 : 프로그램에 데이터 전달
2. 표준 출력 (stdout)
    - FD : 1
    - 기본 장치 : 모니터
    - 역할 : 프로그램의 처리 결과를 보여줌
3. 표준 에러 (stderr)
    - FD : 2
    - 기본 장치 : 모니터
    - 역할 : 프로그램 실행 중 발생한 오류 메시지를 보여줌

### 리다이렉션
- 입출력의 방향을 변경하는 것
1. 출력 변경
    1. `>` : 덮어쓰기
        - 기존 파일에 출력 내용을 덮어씀
        - 예시
            ```bash
            kingrange@kilwon:~$ date > date1.txt # 출력을 date1.txt파일에 덮어쓰도록
            kingrange@kilwon:~$ cat date1.txt
            Wed Jan  7 05:45:43 AM UTC 2026
            kingrange@kilwon:~$ date > date1.txt # 출력을 date1.txt파일에 덮어쓰도록
            kingrange@kilwon:~$ cat date1.txt # 덮어써짐 아까 43초거 없어짐
            Wed Jan  7 05:45:53 AM UTC 2026
            ```
    2. `>>` : 이어쓰기
        - 기존 파일의 내용 뒤에 출력 내용을 이어씀
        - 예시
            ```bash
            kingrange@kilwon:~$ date >> date2.txt # 출력을 date2.txt파일에 이어쓰도록
            kingrange@kilwon:~$ cat date2.txt
            Wed Jan  7 05:48:37 AM UTC 2026
            kingrange@kilwon:~$ date >> date2.txt # 출력을 date2.txt파일에 이어쓰도록
            kingrange@kilwon:~$ cat date2.txt #이어써짐
            Wed Jan  7 05:48:37 AM UTC 2026 
            Wed Jan  7 05:48:45 AM UTC 2026
            ```

2. 에러 변경
    1. `2>` 
        ```bash
        kingrange@kilwon:~$ ls abc 
        ls: cannot access 'abc': No such file or directory
        kingrange@kilwon:~$ ls abc 2> error.txt # 에러 출력을 error.txt로 변경
        kingrange@kilwon:~$ cat error.txt
        ls: cannot access 'abc': No such file or directory
        ```
    2. `error 메시지 버리기`
        ```bash
        ls abc 2> /dev/null #이렇게 하면 기록도 안되고 출력도 안됨
        ```
3. 출력과 에러를 한 번에 변경
    - 예시, 다른 파일에 기록
        ```bash
        kingrange@kilwon:~$ ls abc > ls.out 2> ls_error.txt
         # ls abc의 결과를 ls.out 파일에 기록하고
         # 결과가 에러면 ls_error.txt에 기록
        ```
    - 예시2, 한 파일에 에러와 출력 모두 기록
        ```bash
        kingrange@kilwon:~$ ls abc > ls.out 2>&1
         # ls abc의 결과를 ls.out 파일에 기록하고
         # 결과가 에러면 FD1(현재 ls.out으로 변경되어있는 상태)에 기록
         # 즉, 에러면 ls.out에 기록된다.
        ```
4. 입력 변경
    1. `<` : 앞 프로그램의 입력으로 뒷 파일의 내용을 입력
        ```bash
        kingrange@kilwon:~$ vim test.py
        kingrange@kilwon:~$ cat test.py # 입력을 받아 그대로 출력하는 프로그램
        a = input()
        print(a)
        kingrange@kilwon:~$ python3 test.py < input.txt # Hello World!가 적힌 input.txt를 입력으로 전달
        Hello World! #출력이 나옴
        ```

## 변수

### 종류
1. SHELL 변수 
    - 현재 SHELL에서만 유효함.
    - 자식 프로세스에서는 SHELL변수를 이용할 수 없음.
2. 환경변수
    - 시스템 전체에 적용되는 변수
    - 자식 프로세스에서도 환경변수를 이용할 수 있다.
### 변수 생성, 수정, 확인, 삭제
#### `변수명=값` : SHELL 변수 생성 및 수정
- `일시적으로 이용`할 
```bash
KING=TIGER # KING이라는 쉘 변수에 TIGER 값을 넣음
```
#### `export 변수명=값` : 환경변수 생성 및 수정
- `일시적으로 이용`할 `환경변수를 생성하는 명령어`다. 
    - 해당 `명령어를 실행`하면, `메모리에 변수가 등록`된다. 
    - 메모리이므로, logout 시 생성한 명령어가 사라진다.
```bash
export KING # 위에서 만든 KING을 환경변수로 설정
export TIGER=KING # TIGER 환경변수에 KING 값을 넣어 설정
```

#### `export -n 변수명` : SHELL 변수로 수정
```bash
export -n KING # 환경변수였던 KING을 SHELL변수로
```

#### `echo $변수이름` : 변수의 값 확인
```bash
echo -n $KING && echo $TIGER 
```

#### `env` : 환경 변수 전부 출력
```bash
env
```

#### `set` : 모든 변수와 함수를 출력
```bash
set
```

#### `unset 변수이름` : 변수 삭제
```bash
unset KING # KING 변수 삭제
```

#### 환경 변수 영구 등록
- `.bashrc` 파일을 수정해야 한다. (환경설정 파일)
    - 해당 파일 하단에 원하는 변수를 EXPORT로 등록하면 된다.
- 기본적으로 LINUX에 로그인을 하게되면, bashrc가 실행되며, bashrc에 등록된 환경변수들이 env에 등록된다.
    - 따라서, 환경 변수 추가 명령어를 .bashrc에 등록해두어야 `영구적으로 사용`이 가능하다.
- `source ~/.bashrc` : 즉시 등록
    - .bashrc에 수정한 내용은 아직 불러지지 않았다. (즉, 현재 메모리에 반영되지 않음)
    - 위 명령어를 수행하면, bashrc에 저장된 내용을 기반으로 현재 메모리에 다시 불러온다.
        - 즉, 우리가 추가한 환경변수를 즉시 이용할 수 있게 된다.

- 리다이렉션을 이용한 한 번에 등록
    - echo는 명령을 그대로 다시 내뱉는다는 특징이 있다. 그것을 이용
        ```bash
        echo 'export C=D' >> ~/.bashrc && export C=D
         # echo 'export C=D' 결과는 export C=D
         # 이것을 >>(이어쓰기)로 ~/.bashrc에 추가함.
         # 그리고(&&) export C=D 실행
         # 그럼 영구 반영도 되고, 현재 메모리 반영도 된 상태
        ```
## 기타 환경 변수
### PATH
- 실행 파일(프로그램,명령어)의 위치를 찾아보는 경로들의 list
- 환경변수 중 하나다.
- 명령어를 찾을 위치를 :으로 구분해서 설정
    ```bash
    kingrange@kilwon:~$ echo $PATH
    /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin # : 으로 각각 구분되어 있다.
    ```
#### 동작 원리
1. 사용자가 `x 명령어` 입력
2. Linux는 PATH에 등록된 첫 번째 directory부터 마지막 directory까지 탐색
3. 탐색 결과 x라는 실행파일을 찾음 -> 실행
4. 탐색 결과 x라는 실행파일을 찾지 못함 -> command not found 에러 발생

#### 새로운 경로 추가하기
- 변수에 반영하는 것이다.
    - 즉, 
        1. 현재 SHELL에서만 변경하고 싶다면 : `PATH="$PATH:추가경로"`
        2. 현재 로그인 상태의 모든 자식 프로그램에 적용 : `export PATH="$PATH:추가경로"`
        3. 껏다켜도 적용하고 싶다면 : `echo 'export PATH="$PATH:추가경로"' >> ~/.bashrc && export PATH="$PATH:추가경로"`
    - 사실 이때, `$PATH(기존 경로)` 앞에 경로를 넣어도 되고, 뒤에 넣어도 된다.
        - 그러나, 보통은 내 경로를 뒤에 넣는 것을 추천한다.
            - 수정의 용이함 등의 이유
#### 주의
- 그냥 바로 `PATH=$PATH:추가경로`로 작업하게 되면 잘못되었을 때, 골치아프다.
    - 따라서, `다른 임시 변수에 기존 경로를 저장해두고 작업`하자.
    
### LANG
- Locale 정보(국가, 언어, 문자 인코딩)를 결정하는 기본적인 환경 변수
#### 구성 형식
```bash
언어_국가.인코딩
#ex, ko_KR.UTF-8
```
#### 현재 LOCALE 확인
-  `locale` 명령어 실행
    ```bash
    kingrange@kilwon:~$ locale
    LANG=en_US.UTF-8
    LANGUAGE=
    LC_CTYPE="en_US.UTF-8"
    LC_NUMERIC="en_US.UTF-8"
    LC_TIME="en_US.UTF-8"
    LC_COLLATE="en_US.UTF-8"
    LC_MONETARY="en_US.UTF-8"
    LC_MESSAGES="en_US.UTF-8"
    LC_PAPER="en_US.UTF-8"
    LC_NAME="en_US.UTF-8"
    LC_ADDRESS="en_US.UTF-8"
    LC_TELEPHONE="en_US.UTF-8"
    LC_MEASUREMENT="en_US.UTF-8"
    LC_IDENTIFICATION="en_US.UTF-8"
    LC_ALL=
    ```
    - 시스템에서 지원하는 LOCALE 목록 확인
        ```bash
        kingrange@kilwon:~$ locale -a
        C
        C.utf8
        en_US.utf8
        ko_KR.utf8
        POSIX
        ```
#### 로케일 설정
- LANG 변수에 원하는 내용 입력
    - 한국어로 변환하길 바람
        ```bash
        LANG=ko_KR.utf-8
        ```
    - 영구적으로 바꾸고싶다면 똑같이 bashrc에 등록하면 된다.

## 환경 설정 파일
### 시스템 환경 설정 파일
- 모든 사용자에게 영향을 미침
- root(관리자)가 시스템의 일관성을 위해 설정한다.
- 종류
    1. `/etc/profile` : `login shell`이 실행될 때 `가장 먼저` 읽히는 파일
        - 모든 사용자의 공통 `PATH`, `UMASK`, `HOSTNAME` 등을 초기화합니다.
    2. `/etc/bash.bashrc` : `Bash Shell`이 실행될 때마다(`비 로그인 포함`) 적용되는 `공통 설정`
        - 터미널 프롬프트(`PS1`)의 기본값, `sudo` 명령어 사용 시, 오타 수정 제안(`command not found`)등의 편의 기능을 가지고 있음
    3. `/etc/profile.d/*.sh` : `모듈형 설정 방식`
        - 특정 패키지(언어 설정, Bash Completion 등)를 설치했을 때, 전체 파일을 수정하지 않고, 이 폴더에 script를 넣는 것만으로도 시스템 전체 설정을 추가할 수 있다.

### 사용자 환경 설정 파일
- 각 사용자의 홈 디렉토리(`~`)에 위치하는 파일
- 사용자의 개개인의 취향 및 작업 환경 설정을 결정한다.
- 종류
    1. `~/.profile` : 가장 범용적인 login 파일
        - Bash 뿐 아니라, 다른 Shell에서도 읽힌다.
    2. `~/.bashrc` : 가장 자주 수정되는 파일
        - 사용자의 `실제 작업 설정`, Alias,Functions,History 설정 등을 정의한다.
        - 로그인하지 않고, bash라고 작성해, 새 shell을 띄울 때도 이 파일은 다시 읽힌다.
    3. `~/.bash_alias` : 별명용 보조파일
        - alias가 너무 많아질 경우, bashrc가 지저분해지는 것을 막기 위해 별도로 관리하는 파일
        - 기본적으로 존재하는 파일 X
            - bashrc가 이 파일을 불러오는 코드를 있을 때만 작동한다.
    4. `~/.bash_logout` 
        - exit으로 `로그아웃`할 때, 수행되는 명령을 저장
        - 보안을 위해 `화면을 지우거나`(clear), `임시 파일을 삭제`하는 등의 용도로 사용한다.
### 파일 로딩 순서와 우선 순위
1. `/etc/profile` 호출
    - 내부적으로 `/etc/profile.d/*.sh` 호출
2. `~/.profile` 호출
    - 내부적으로 `~/.bashrc` 호출
    - 내부적으로 `/etc/bash.bashrc` 및 `~/.bash_alias` 호출
- `나중에 실행되는 파일`이 `먼저 실행된 설정`을 `덮어쓴다.`

### 수정 후 즉시 반영 : `source`,`.`
- 두 명령어는 완전히 동일하다.
- 단, source의 경우 한 줄 씩 `덮어쓰기`를 하는 것이므로, 삭제는 반영이 안 될 수 있다. (삭제는 덮어쓸 것이 없으므로)
    - 따라서, 삭제를 했다면 `exit 후 재로그인` 하는 것이 깔끔하다.

## bash 옵션
- Shell이 명령어를 해석하고, 실행하는 방식을 세밀하게 조정하는 옵션
- 참고
    1. `세션 한정` - 세션이 종료되면 옵션도 삭제된다.
    2. `영구 적용` - `.bashrc` 파일에 옵션 설정을 적어두면 삭제 되어도 매번 불러오므로 영구 적용이 된다.

### SET 명령
- 구조
    ```bash
    set {+o | -o} [기능]
    ```
- `+o` / `-o`로 `비활성화`/`활성화` 시킬 수 있다.
- 기능 종류
    1. `ignoreeof` 
        - 쉘을 빠져나가는 기능 (`CTRL + D를 무시`)
    2. `noclobber` 
        - 덮어쓰기 방지 (`고치기 방지`)
    3. `xtrace` 
        - 실행과정 추적 (`디버깅`)
        - 명령어 실행전, 변수가 치환된 최종형태를 화면에 출력
    4. `nounset`
        - 미선언 변수 에러 (`오타 방지`)
        - 선언 안된 변수를 호출하면 에러 발생 
- 예시
    1. `ignoreeof 기능`을 활성화시켰다가 비활성화 시키기
        ```bash
        set -o ignoreeof # 활성화
        set +o ignoreeof # 비활성화
        ```
    2. `noclobber` 기능을 활성화시켰다가 비활성화 시키기
        ```bash
        touch test.txt # 빈 파일 생성
        echo $PWD > test.txt # PWD 결과를 test.txt에 기록
        echo $date > test.txt # 현재 시간으로 덮어씀
        set -o noclobber # 덮어쓰기 막음
        echo $PWD > test.txt # 다시 PWD 로 덮어쓸라했는데 안댐 에러 = -bash: test.txt: cannot overwrite existing file
        ```
### SHOPT 명령
- 구조
    ```bash
    shopt {-s | -u} [기능] 
    ```
- `-s` / `-u` 로 `활성화`/`비활성화` 할 수 있다.
- 기능 종류
    1. `autocd` : cd없이 경로 입력만으로 이동 가능 (단, 명령어와 폴더명이 겹치면 동작 X)
        ```bash
        kingrange@kilwon:~$ mkdir test_autocd
        kingrange@kilwon:~$ shopt -s autocd
        kingrange@kilwon:~$ test_autocd/
        cd -- test_autocd/
        kingrange@kilwon:~/test_autocd$
        ```
    2. `cdspell` : cd 입력 시, 사소한 철자(대소문자, 순서바뀜)을 교정해 이동
        ```bash
        kingrange@kilwon:~$ shopt -s cdspell
        kingrange@kilwon:~$ cd etst_aUtocd # 복잡한건 안되는 듯
        -bash: cd: etst_aUtocd: No such file or directory
        kingrange@kilwon:~$ cd test_uatocd
        test_autocd
        kingrange@kilwon:~/test_autocd$
        ```
    3. `globstar` : `**` 문법을 사용해 모든 디렉토리의 파일을 검색
        ```bash
        shopt -s globstar
        ls **/ *.txt # 현재 폴더 및 모든 하위 폴더의 txt 파일 출력
        ```
    - 그 외 너무 많음 ㅠ 나중에 정리해야 할듯
## 파일 시스템
- Linux는 `시스템과 관련된 정보`와 `하드웨어 같은 장치`를 모두 `파일로 관리`
    - Window : disk(hardware)가 2개면 directory 구조도 2개
    - Linux : 언제나 System 전체의 1개 Tree만 가짐
        - hardware가 아무리 늘어나도 Tree 내부에 하나의 폴더로 생성됨.
### 디렉토리와 파일

#### 파일의 종류
1. 일반 파일 : 우리가 아는 파일
    - 문서 파일 
        - 해석 방식 : `문자로 변경하여`
    - 바이너리 파일
        - 해석 방식 : `바이트 코드 그대로`

2. 디렉토리 파일
    - 해당 `디렉토리에 저장`된 파일
    - `하위 디렉토리`에 대한 `정보 소유`

3. 링크 파일
    - 시스템 사용자에게 편의 제공을 위한 파일
    - 종류
        1. 하드링크
            - 원본 파일과 동일한 내용의 `다른 사본 파일`을 만드는 것
            - `원본 파일`과 `링크 파일`이 `서로 다른 파일` 취급
                - Q. Copy&Paste와 차이가 무엇?
                - A. `한 쪽 파일 수정`시, `연결된 다른 파일도 수정`된다.
            - `백업의 용도`로 아주 좋다.
            - 가능한 이유
                - 파일에 대한 정보를 가진 `i-node`라는 것을 공유
                    - `i-node` : 파일의 실제 내용을 제외한 모든 정보를 가짐
                        - 운영체제 내부에서는 i-number라는 고유 숫자로 파일을 관리함.
                        - 포함 정보
                            1.  파일 유형
                            2. 권한 
                            3. 소유자 정보
                            4. 파일 크기
                            5. 시간 정보
                            6. 링크 수 : 이 i-node를 가리키는 하드 링크의 수
                            7. 데이터 블록 포인터 
                        - i-node가 꽉차면, 용량이 남아있어도 더 이상 파일을 생성할 수 없다. 
        2. 심볼릭 링크(소프트 링크)
            - `바로 가기` 기능처럼 `원본 파일`의 위치를 기억해서, `심볼릭 링크 파일` 실행 시, `원본 파일`을 찾아서 실행할 수 있게 만들어진 링크
            - `원본 파일 삭제 시 동작 X`
            - 하드 링크와 다르게 새로운 `i-node`를 갖는다.
4. 장치 파일
    - Linux 시스템에 부착된 장치(하드웨어)들을 관리하기 위한 특수 파일
    - `/dev` directory 아래에 위치한다.

#### 파일의 종류 확인
- 형태
    ```bash
    file 경로
    ```
- 예시
    ```bash
    kingrange@kilwon:~$ file test.py # 일반 file
    test.py: ASCII text

    kingrange@kilwon:~$ file /usr/bin/pwd # binary file (실행 파일)
    /usr/bin/pwd: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=51d4cdbecd25e5303ab3129f3ee4436b75778057, for GNU/Linux 3.2.0, stripped

    kingrange@kilwon:~$ file /usr/bin/ # directory file
    /usr/bin/: directory
    ```

# 참고
1. Server는 GUI 설치 잘 안한다.
    - Why?
        1. 불필요한 종속 삭제
        2. 불필요한 사이즈 증가 삭제
    - 따라서, vi/nano 같은 편집기 잘 사용하는 연습 필수
