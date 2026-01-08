# Linux 파일 시스템
## Directory와 File 관리
- File과 Directory의 Hierachical Tree로 구성
    - 최상위 : Root Directory(/)
    - 하단 : Directories / Files
### 용어
- 작업 Directory 
    - User가 우분투에 접속하여 `현재 사용하고 있는 Directory`
    - 현재 작업 중인 Directory : `.`
        - 현재 작업 경로 확인 : `pwd` 명령
- 상위 Directory
    - `자신을 포함`하고 있는 Directory 
    - `..`으로 표시
- 홈 Directory
    - 각 User에게 할당되는 Directory
    - 사용자 계정을 `처음 만들 때 지정`
    - `~`로 표시
### 절대 경로 / 상대 경로

#### 절대 경로
- `Root Directory`(/) `위치부터 시작`하는 경로
    - 반드시 `/`(Root Directory)부터 `시작`해야 한다.

#### 상대 경로
- `현재 Directory`(.)를 기준으로 하는 경로
    - `'/' 이외의 문자로 시작`
- `..` : 현재 Directory에서 상위 Directory 이동

## 파일의 구성 요소
### Ubuntu 특성
- `모든 처리 과정`을 `파일 단위`로 처리
- 계층적 구조

### Ubuntu의 파일 충족 요건

#### 파일 이름
- 규칙
    1. `/`는 File/Directory 이름으로 `사용 불가`
    2. `알파벳`, `숫자`, `.`만 `사용 가능`
    3. 알파벳 `대/소문자`는 엄격히 `구별`
    4. 이름이 `.으로 시작`하면, `숨김 파일`로 간주
- 확장자는 선택적 요소 (.txt 같은 것)

#### i-node (Index Node)
- `파일을 기술`하는 `Disk 상에서의 데이터 구조`
- `파일의 데이터 블록`이 디스크 상의 `어느 주소에 위치하고 있는가`에 대한 `정보를 기록`하기 위해 사용
- 파일을 생성하게 되면, `i-node의 link가 0인 위치`에 `파일 생성`하고, `i-node의 link가 1로 증가`한다.
    1. 사용하지 않는(Link Count = 0) i-node들 중 하나를 골라 파일의 메타데이터(크기, 권한, 시간 등)를 기록
        - 아직 `파일명`과 연결 X
    2. `파일명`과 `1의 i-node`를 매핑하여 Directory File에 기록
        - 이제 i-node를 가리키는 `이름(파일명)`이 생겼으므로 Link Count를 1 증가시킨다.
    - 참고, 삭제 시에도 데이터가 삭제되는 것이 아니라 `Link Count가 0이 되고`, `해당 i-node가 사용 가능상태로 변경`되는 것이다.

- 저장 정보
    1. 파일의 종류
    2. 소유권 (사용자 및 사용자 그룹)
    3. Access Mode
    4. Time stamp

### 데이터 블록
- `데이터를 저장`하는 블록
- `일반 파일` 및 `디렉토리 파일`의 데이터가 존재
    - 저장 시, `디스크 장치`에 `특별한 구분없이 저장`
    - 즉, 파일 2개를 저장한다 할 때, 특별히 위치를 구분하지 않고 차례대로 저장한다. 
        - 이러면, 디스크의 어느 한 쪽에 데이터가 쌓이게 되고, 이를 `데이터 블록`이라 한다.
        - 이렇게 순서대로 저장하기 때문에 구분이 힘들다.
            - 이 구분을 위해 `i-node`를 이용해 부가 정보를 구분한다.

### 파일은 위 3개(파일명, i-node, 데이터블록)를 모두 충족해야 존재 가치를 가질 수 있다.

# 파일 시스템 관련 명령어

## file 명령
- 지정된 파일의 종류(타입) 확인
- `usr/share/file` directory의 `magic 파일`을 참조하여 파일 종류를 표시
    - `magic file`
        - 파일의 확장자가 아닌 `파일 내부 데이터`를 보고 `파일의 종류`를 판별하는데 사용되는 `DB 파일`
        - `파일의 가장 앞 부분`에 `파일을 나타내는 고유한 데이터 바이트`가 존재, 이를 `magic number`라고 부름
            - `magic file`은 `magic number 목록`을 정리해둔 파일
        - magic 파일을 통해 잘못된 확장자가 입력되더라도 정상적으로 실행될 수 있다.
            - `보안`, `시스템 안정성`, `데이터 복구`의 장점
### 형식
```bash
file [옵션] [파일 및 디렉토리 경로]
```
- 옵션
    1. `-C` : 매직 파일을 컴파일된 매직 파일(.mgc)로 변경
        - 예를 들어, A라는 custom magic file이 있을 때, 이는 ASCII text이므로 파싱에 시간이 소요된다.
            - 이를 미리 mgc로 변경해두면 이후 -m을 사용하여 매직파일을 사용해도 알아서 .mgc로 가져와 빠르게 실행됨
    2. `-f 목록파일` : 많은 파일을 한 번에 확인
        - 목록 파일
            - 파일 리스트를 가짐
            - -f 목록파일은 파일 리스트에 있는 모든 파일을 확인하는 것이다.
    3. `-m 매직파일` : 지정된 매직파일로 대상 파일을 확인

### 예시
> `ERROR라는 내용이 있으면, ERROR LOG FILE이라고 출력/KING이라는 내용이 있으면 TIGER IS KING이라고 출력하는 매직파일 생성` 후, `mgc 변환`하고, `목록 파일로 5개의 파일 한 번에 검사` (A,B,C,D,E)

1. 매직 파일 생성
    - 형식
        ```bash
        [오프셋] [타입] [비교값] [메시지]
        ```
        - 오프셋 : 바이트를 세는 단위
            - 0 : 맨 앞부터 센다.
            - 10 : 10바이트 건너뛰고 11바이트부터 센다.
        - 여러 독립적 규칙을 나열하고싶다면 : `줄바꿈`
            ```bash
            [오프셋] [타입] [비교값] [메시지]
            [오프셋] [타입] [비교값] [메시지]
            ```
        - 복잡한 관계를 조합하고 싶다면 (0번째에서~ 그리고 10번쨰에서 ~) : `줄바꿈` + `>`
            ```bash
            cat << EOF > my_rules
            0  string  MYAPP   My Application File
            >6 string  DATA    - Type: Data
            >6 string  LOGS    - Type: Log
            EOF
            # 0번째가 MYAPP이면 My Application File 근데 7바이트 부터 값이 
            # DATA면 Type: Data 
            # LOGS면 Type :Log
            ```
    ```bash
    cat << EOF > magic_range
    0 string ERROR ERROR LOG FILE
    0 string KING TIGER IS KING
    EOF
    ```
2. mgc 변환
    ```bash
    kingrange@kilwon:~/file_test$ file -C magic_range
    kingrange@kilwon:~/file_test$ ls -l
    total 8
    -rw------- 1 kingrange kingrange 376 Jan  8 07:06 magic.mgc
    -rw------- 1 kingrange kingrange  58 Jan  8 07:05 magic_range
    ```
3. file 목록 생성
    ```bash
    cat << EOF > file_list
    > A
    > B
    > C
    > D
    > E
    > EOF
    ```
4. file -f -m 명령어 사용하여 한 번에 검색
    ```bash
    kingrange@kilwon:~/file_test$ file -m magic_range -f file_list
    A: TIGER IS KING
    B: ASCII text # 사설 magic에 정의되지 않은 것은 기본 magic으로
    C: ERROR LOG FILE
    D: ERROR LOG FILE
    E: ASCII text  # 사설 magic에 정의되지 않은 것은 기본 magic으로
    ```

## pwd 명령
- 현재 작업중인 Directory를 `절대 경로`로 출력
- 현재 Directory 확인용
### 형식
```bash
pwd
```
### 사용 상황
1. 전체 경로 (full_path)가 필요할 때
2. Symbolic Link에 속지 않기 위해
    - 물리적 경로 확인(`pwd -P`) 명령을 사용한다.
3. 화면 구성이 다른 환경인 경우
    - 자동화 Script에서 경로를 확인하고 작업하기 위해 주로 사용

### 예시, file_test 경로에서 pwd
```bash
kingrange@kilwon:~/file_test$ pwd
/home/kingrange/file_test
```

# 디렉토리 관련 명령어
## cd 명령
- change directory의 준말
- 현재 directory에서 `다른 directory`로 이동하기 위해 사용
### 형식
```bash
cd [경로]
```

## ls 명령
- Directory의 내용을 출력하는 명령어
### 형식
```bash
ls [옵션]
```
- 옵션
    1. `-a` : `숨김 파일`을 포함해 `모든 파일의 목록`을 출력
    2. `-d` : `Directory 자체의 정보`를 출력
    3. `-i` : 첫 번째 행에 i-node 번호를 출력
    4. `-l` : 파일의 상세 정보 출력 (권한 등)
    5. `-A` : `.과 ..을 제외`한 `모든 파일 목록` 출력
    6. `-F` : `파일의 종류`를 표시 
        - `*` : 실행 파일
        - `/` : 디렉토리
        - `@` : 심볼릭 링크
    7. `-L` : 심볼릭 링크인 경우, 원본 파일 정보 출력
    8. `-R` : 하위 디렉토리 목록까지 출력

## mkdir
- 폴더를 생성하는 명령어
### 형식
```bash
mkdir [옵션] [폴더명]
```
- 옵션
    - `-p` : 디렉토리 생성 시, 중간 단계의 directory가 없을 때, 필요한 중간 단계의 directory들을 생성해줌 
        - 이 옵션이 없다면 Error
- 여러 폴더명을 입력하여 한 번에 여러 개 생성하는 것도 가능하다.
### 예시
> first 폴더가 없는 상황에서 first 폴더 안에 second 폴더 생성
```bash
kingrange@kilwon:~$ ls #비어있음
kingrange@kilwon:~$ mkdir -p first/second #연쇄로 만듦
kingrange@kilwon:~$ ls -R #확인
.:
first

./first: # first 생성
second

./first/second: # 그 안에 second 생성
```

## rmdir
- 빈 폴더를 삭제하는 명령어
    - `rm -r`로도 가능하다.
### 형식
```bash
rmdir [옵션] [폴더명]
```
- 옵션
    - `-p` 
        - 중간 directory들도 비어있다면 함께 지워준다.
### 예시
```bash
kingrange@kilwon:~/first$ cd second
kingrange@kilwon:~/first/second$ touch empty #second 내부에 파일 생성
kingrange@kilwon:~/first/second$ ls 
empty
kingrange@kilwon:~/first/second$ cd ..
kingrange@kilwon:~/first$ cd ..
kingrange@kilwon:~$ rmdir -p first/second # 삭제 시도 (에러)
rmdir: failed to remove 'first/second': Directory not empty
kingrange@kilwon:~$ cd first/second/
kingrange@kilwon:~/first/second$ rm empty #파일 지워서 빈폴더로
kingrange@kilwon:~/first/second$ cd ../..
kingrange@kilwon:~$ rmdir -p first/second # 삭제 시도
kingrange@kilwon:~$ ls -R #둘다 비었으므로 둘 다 삭제
.:
```

# 파일 관련 명령어

## cat 명령
- `text 형식의 파일`을 출력

- 매개변수로 여러 파일을 지정하여 `여러 파일 출력 가능`
    - 이를 `출력 리다이렉션` 으로 `파일 합치기`로 쓸 수 있다.

- 파일을 지정하지 않으면, 키보드 입력 내용을 출력
    - `출력 리다이렉션`에서 사용 가능

### 형식
```bash
cat [옵션] <파일명>
```
- 옵션
    - `-n` : 모든 행에 번호 출력
    - `-b` : 비어있는 줄 제외 번호 출력
    - `-s` : 연속된 빈 줄 합치기
    - `-E` : 줄 끝에 $ 표시 
        - 각 줄이 끝나는 부분을 명확히 알 수 있음
    - `-A` : 특수문자 시각화 
        - 코드 분석 및 데이터 형식 확인에 필수
### 예시
1. 예시 파일
```bash
cat << EOF > test.txt

KingrangE


Tiger

is

king


I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces
> EOF
```
2. 비어 있는 줄 합치고, 줄 끝 표시하고, 비어있는 줄 제외 번호 출력
```bash
kingrange@kilwon:~$ cat -bsE test.txt
$
     1  KingrangE$
$
     2  Tiger$
$
     3  is$
$
     4  king$
$
     5  I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces I learned to linux by picking up bits and pieces$
```


## more 명령
- 출력 결과가 한 화면에 보이지 않는 경우 하단의 more로 한 줄씩 넘어가며 확인할 수 있게 하는 명령 
    - 스크롤 기능 X
- 주로 파이프(`|`)와 함께 사용한다.

### 단축키
- `ENTER` : 다음 줄 출력
- `spacebar` : 다음 페이지 출력 
- `b` : 이전 페이지 출력
- `q` : 중단

## less 명령
- more 명령 개선판
    - 방향키로 이전 줄 다시 확인이 가능하게 한 것
- 주로 파이프(`|`)와 함께 사용한다.
### 단축키
- `j`, `방향키 아래` : 다음 줄
- `k`, `방향키 위` : 이전 줄
- `Spacebar`, `CTRL+f` : 다음 화면 이동
- `CTRL + b` : 이전 화면 이동
- `q` : 종료

## head/tail 명령
- 파일의 `앞(head)/뒤(tail)부분`의 `몇 개의 행을 출력`하는 명령
### 형식
```bash
명령 [옵션] [파일]
```
- 옵션
    - `-f` : tail에서 -f를 사용하면, 실시간으로 변경되는 내용을 확인할 수 있다.
        - ex, log 파일 확인할 때 유용
    - `-숫자` : 숫자만큼의 행을 출력 (생략 시 `10`)

## cp 명령
- 파일 및 디렉토리 복사
### 형식
```bash
cp [옵션] [source] [destination]
```
- 옵션
    - `-i` : destination과 동일한 파일이 있을 때, `덮어 씌울건지` 질문
        - 없으면, 그냥 덮어씌움
    - `-r` : directory 복사 시 지정 (없으면 error)
- `여러 개 파일`을 `한 번에 복사`할 수 있다.
    - 이 경우 `destination`은 `무조건 파일들을 담을 폴더`

### 예시
> A B C 파일을 ABC폴더에 복사 
```bash
kingrange@kilwon:~$ ls
A  ABC  B  C
kingrange@kilwon:~$ cp -i A B C ABC #만약 ABC 폴더 내에 동일 파일이 있다면 질문
kingrange@kilwon:~$ cd ABC
kingrange@kilwon:~/ABC$ ls
A  B  C
```

## mv 명령
- 파일 이동 및 파일 이름 변경
### 형식
```bash
mv [옵션] [source] [destination]
```
- 옵션
    - `-i` : cp와 동일, 이미 있는 경우 덮어씌우는지 묻는거
        - 생략시 덮어씌움
### 예시
> 아까 A B C 파일을 ABC 폴더로 이동 덮어씌우는지 묻는거 활용
```bash
kingrange@kilwon:~$ mv -i A B C ABC
mv: overwrite 'ABC/A'? y
mv: overwrite 'ABC/B'? y
mv: overwrite 'ABC/C'? y
kingrange@kilwon:~$ ls
ABC
kingrange@kilwon:~$ ls -R
.:
ABC

./ABC:
A  B  C
```

## rm 명령
- 파일 및 디렉토리 삭제
### 형식
```bash
rm [옵션] [파일 또는 디렉토리]
```
- 옵션
    - `-i` : 삭제할 것인지 한 번 더 확인
    - `-r` : 디렉토리 삭제 (비지 않아도 삭제됨)
### 예시
> A B C 파일이 들어있는 ABC 폴더 삭제
```bash
kingrange@kilwon:~$ rmdir ABC # 이건 안 비어있으면 삭제 못함
rmdir: failed to remove 'ABC': Directory not empty # 에러
kingrange@kilwon:~$ rm -r ABC # 이건 안 비어있어도 삭제 가능
kingrange@kilwon:~$ ls #삭제 됨
```

## ln 명령
- 링크 생성
### 형식
```bash
ln [옵션] <링크할 파일> <링크 이름>
```
- 옵션
    1. `-s` : `심볼릭 링크 생성` (새로운 i-node)
        - 생략 시, `하드 링크 생성` (동일한 i-node)
    2. `-f` : 기존 파일과 겹치면 덮어씌움
        - 생략 시, 겹칠 때 Error
    3. `-v` : 작업 내용 출력
    4. `-i` : 삭제 전 확인 (f와 함께 사용)
- Symbolic Link 
    - 가장 대중적, 파일 뿐 아니라, Directory를 연결할 때도 필수
    - 예를 들어, 버전 업데이트 등에서 사용한다. (Linux 1번 프로세스처럼)

### 예시
> v1.0 html 파일을 v2.0으로 변경, 백업을 위해 하드링크를 냅두고 서비스는 심볼릭 링크로 연결 (무중단 업데이트 방식)
1. 데이터 생성
    ```bash
        # 1. 서비스 폴더 구조 생성
    mkdir -p kingrangE/versions

        # 2. 버전 1.0
    echo "<html><h1>Version 1.0</h1></html>" > kingrangE/versions/app_v1.0.html

        # 3. 버전 2.0
    echo "<html><h1>Version 2.0</h1></html>" > kingrangE/versions/app_v2.0.html
    ```
2. 백업본 생성 (하드 링크)
    - 원본 수정시 하드 링크에도 반영되므로, 백업은 `하드 링크`로 생성
    ```bash
        # v1.0의 하드 링크 생성
    kingrange@kilwon:~$ ln kingrangE/versions/app_v1.0.html kingrangE/backup

    kingrange@kilwon:~$ ls -i kingrangE/versions/app_v1.0.html kingrangE/backup
     # 397562 kingrangE/backup  397562 kingrangE/versions/app_v1.0.html
    ```
3. 1.0을 서비스로 연결 (심볼릭 링크)
    ```bash
    ln -s kingrangE/versions/app_v1.0.html kingrangE/index.html #외부에 보여주는 index.html
    ```
4. 2.0으로 업데이트 (심볼릭 링크)
    ```bash
    ln -sf kingrangE/versions/app_v2.0html kingrangE/index.html
     # index.html를 v2.0 심볼릭링크로 덮어씌움
    ```


## touch 명령
- 빈 파일 생성 명령, `Timestamp 조절 가능`(핵심 기능)
    - Why? Timestamp 조절이 중요
### 형식
```bash
touch [옵션] [파일]
```
- 옵션
    - `-a` : 파일의 `접근 시간 변경`
        - `접근 시간(atime)` : 실제로 누군가 읽은 시간
        - 리소스 관리 프로그램에서 중요 (아무도 안 읽으면 삭제)
    - `-c` : 새 파일 생성하지 않음 
        - 이미 존재하는 경우에만, `생성 시간 업데이트`를 위해 사용
    - `-m` : 파일의 `수정 시간`만 변경
        - `수정 시간(mtime)` : 파일 내용이 변경된 시간
        - 백업 프로그램에서 중요
    - `-t time` : 현재 시간 대신 사용자가 지정한 시간으로 설정
    - `-r ref_file` : ref_file의 시간과 똑같이 맞춤
### Timestamp가 중요한 이유
1. `빌드 자동화` 효율성 (`make` 프로세스)
    - `make`와 같은 빌드 도구는 `파일의 수정시간`을 기준으로 동작
        - time_{소스 코드}가 time_{파일}보다 최신이라면 컴파일을 진행
        - 아니라면 작업을 건너뜀
2. `백업 및 동기화`
    - 대규모 서비스에서는 모든 파일을 매번 백업할 수 없다.(resource 낭비)
        - `증분 백업` 방식을 취한다.
            - 마지막 백업 시간 이후, 변경된 파일만 선택적 백업
    - 따라서, 다시 백업해야 하는 경우, 파일들의 시간을 백업하도록 조절할 수 있다.
        - 만약, 시간이 정확하지 않으면 누락되거나 불필요하게 모두 백업해서 자원 낭비가 발생한다.
3. `로그 분석` 및 `시스템 모니터링`
    - 특정 시간대의 로그를 재현해야 한다면, 시간을 특정 시점으로 돌려서 시뮬레이션을 할 수 있다.
4. 파일 `생명 주기 관리`
    - 일정 시간이 지난 파일을 삭제한다 가정할 때, 삭제되지 않도록 최신 시간으로 갱신 시킬 때 사용
### 예시
<details>
<summary>너무 길어서 예시 토글로 변경</summary>

1. 기본 (생성 및 시간 업데이트(존재하는 경우))
    ```bash
    kingrange@kilwon:~$ touch A
    kingrange@kilwon:~$ stat A
    File: A
    Size: 0               Blocks: 0          IO Block: 4096   regular empty file
    Device: fd00h/64768d    Inode: 394993      Links: 1
    Access: (0600/-rw-------)  Uid: ( 1000/kingrange)   Gid: ( 1000/kingrange)
    Access: 2026-01-08 09:02:42.234140122 +0000
    Modify: 2026-01-08 09:02:42.234140122 +0000
    Change: 2026-01-08 09:02:42.234140122 +0000
    Birth: 2026-01-08 09:02:42.234140122 +0000
    ```
2. 접근 시간을 변경 (Access와 Change가 모두 변경됨)
    ```bash
    kingrange@kilwon:~$ stat A
    File: A
    Size: 0               Blocks: 0          IO Block: 4096   regular empty file
    Device: fd00h/64768d    Inode: 394993      Links: 1
    Access: (0600/-rw-------)  Uid: ( 1000/kingrange)   Gid: ( 1000/kingrange)
    Access: 2026-01-08 09:05:39.129865356 +0000
    Modify: 2026-01-08 09:02:42.234140122 +0000
    Change: 2026-01-08 09:05:39.129865356 +0000
    Birth: 2026-01-08 09:02:42.234140122 +0000
    ```
3. 수정 시간을 변경 (Modify와 Change가 모두 변경됨)
    ```bash
    kingrange@kilwon:~$ stat A
    File: A
    Size: 0               Blocks: 0          IO Block: 4096   regular empty file
    Device: fd00h/64768d    Inode: 394993      Links: 1
    Access: (0600/-rw-------)  Uid: ( 1000/kingrange)   Gid: ( 1000/kingrange)
    Access: 2026-01-08 09:05:39.129865356 +0000
    Modify: 2026-01-08 09:06:16.905819169 +0000
    Change: 2026-01-08 09:06:16.905819169 +0000
    Birth: 2026-01-08 09:02:42.234140122 +0000
    ```
4. B 파일을 생성하여 A가 B와 동일한 시간을 갖도록 함
    ```bash
    kingrange@kilwon:~$ touch -r B A
    kingrange@kilwon:~$ stat A
    File: A
    Size: 0               Blocks: 0          IO Block: 4096   regular empty file
    Device: fd00h/64768d    Inode: 394993      Links: 1
    Access: (0600/-rw-------)  Uid: ( 1000/kingrange)   Gid: ( 1000/kingrange)
    Access: 2026-01-08 09:06:41.941790641 +0000
    Modify: 2026-01-08 09:06:41.941790641 +0000
    Change: 2026-01-08 09:06:47.269784773 +0000
    Birth: 2026-01-08 09:02:42.234140122 +0000
    ```
</details>

## grep 명령
- 문자열에서 `내용을 검색`할 때, 사용하는 명령어
### 형식
```bash
grep [옵션] [패턴] [파일경로]
```
- 패턴에 정규식 사용 가능 : `^`, `$`, `[]`, `-` 등
- 옵션
    1. `i`(ignore case) : 대/소문자를 구분 없이 모두 검색
    2. `l` : 지정한 패턴이 포함된 `파일명 출력`
    3. `n` : 지정한 패턴이 포함된 `행번호 출력`
    4. `v` : 패턴이 포함되지 않은 `행 출력`
    5. `r`(recursive) : `하위 디렉토리`까지 검사
    6. `c`(count) : 개수 세기
- 컨텍스트 매핑 옵션
    - Error를 읽는 경우 많이 사용한다.
        - Error의 상세 내용을 읽기 위해 
    - `-A 숫자` : 찾아서 그 뒤의 숫자개수만큼 행 출력
        ```bash
        grep -A 5 ERROR error.log #error.log에서 ERROR를 찾고 그 뒤 5줄 출력
        ```
    - `-B 숫자` : 찾아서 그 앞의 숫자개수만큼 행 출력
        ```bash
        grep -B 5 ERROR error.log #error.log에서 ERROR를 찾고 그 앞 5줄 출력
        ```
    - `-C 숫자` : 찾아서 그 앞 뒤의 숫자개수만큼 행 출력
        ```bash
        grep -C 5 ERROR error.log #error.log에서 ERROR를 찾고 그 앞 뒤 5줄 출력
        ```
### 예시
<details>
<summary>예시, data 파일에서 NNTP라는 문자열 검색</summary>

```bash
kingrange@kilwon:~/test_autocd$ grep hello test.txt
hello
kingrange@kilwon:~/test_autocd$ grep -n hello test.txt
8:hello
kingrange@kilwon:~/test_autocd$ grep -l hello test.txt
test.txt
kingrange@kilwon:~/test_autocd$ grep -i hello test.txt
hello
kingrange@kilwon:~/test_autocd$ grep -c hello test.txt
1
kingrange@kilwon:~/test_autocd$ grep -v hello test.txt
abc
def
hi
world
python
```
</details>

<details>
<summary>예시2, 실행 중인 특성 프로세스 확인</summary>

```bash
ps -ef # 현재 실행 중인 전체 프로세스 -> 많음
ps -ef | grep -n python # python이 실행중인지 몇 번 행에 있는지 확인
#결과 
89:root         668       1  0 Jan07 ?        00:00:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
98:root         726       1  0 Jan07 ?        00:00:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
115:kingran+    3975    2880  0 05:11 pts/0    00:00:00 grep --color=auto pytho
```
</details>

<details>
<summary>예시3, 실시간으로 수정되는 logfile(access.log)에서 특정 단어(404) 강조</summary>

```bash
tail -f access.log | grep --color 404 
```
</details>

## find 명령
- `파일을 검색`하는 명령
    - 검색 후, `동작 지정` 가능
### 형식
```bash
find [경로] [검색 조건] [동작]
```
- 검색 조건
    - name : 파일명
    - type : 파일 종류
        - `f` : 파일 검색
        - `d` : 폴더 검색
        - `l` : 링크 검색
    - user : 계정
    - group : 그룹
    - perm : 접근 권한
    - size : 크기
    - newer : 수정시간
        - 예시
            ```bash
            find -newer 파일명 
             # 파일명보다 더 최근에 수정된 파일 검색
            ```
        - 예시
            ```bash
            find -newer "년-월-일"
             # 년-월-일 이후에 수정된 파일 검색
            ```
        - 예시
            ```bash
            find -neweraa "파일명"
             # 파일명보다 더 최근에 접근한 파일 검색
            ```
        - 예시
            ```bash
            find -newer "파일명1" ! "파일명2"
             # 파일명1과 파일명2 사이 기간에 수정된 파일 검색
            ```
- 동작
    - `print(default)` : 절대 경로명 출력
    - `exec` : 파일 찾아 특정 명령 실행
        - 예시, A 폴더 내의 .txt 파일을 모두 삭제
            ```bash
            find A -name "*.txt" -exec rm {} \;
            ```
            - rm : 삭제 명령
            - {} : 찾은 파일의 이름을 담을 `Place Holder`
            - \;  
                - `\` : ;을 문자로 전달하기 위해 처리해주는 Escape
                - `;` : -exec 옵션이 여기까지라는 것을 알리는 마침표
                    - `-exec 옵션`을 사용할 때는 `;를 무조건 사용`해야 한다. 
    - `ok` : 파일 찾아 확인받고 실행
    - `ls` : 검색 결과 목록으로 출력

## locate 명령
- 파일을 빠르게 찾는 명령
- find와 유사하나, 속도가 훨씬 빠르다.
- 내장 패키지가 아니기에, 설치해야 한다.

## wc
- `단어 수`,`줄 수`,`문자 수`등을 셀 때 사용하는 명령어
### 형식
```bash
wc [옵션] [파일 경로]
```
- 옵션
    1. `-l` : 라인 수
    2. `-w` : 단어 수
    3. `-c` : 바이트 수
    4. `-m` : 문자 수
    5. `-L` : 가장 긴 줄의 길이
- 예시
    ```bash
    kingrange@kilwon:~$ cat test.txt
    hi hello
    kingrange@kilwon:~$ wc -l test.txt
    1 test.txt
    kingrange@kilwon:~$ wc -w test.txt
    2 test.txt
    kingrange@kilwon:~$ wc -c test.txt
    9 test.txt
    kingrange@kilwon:~$ wc -m test.txt
    9 test.txt
    kingrange@kilwon:~$ wc -L test.txt
    8 test.txt
    ```

## sort 명령
- 파일의 내용을 정렬하여 출력
### 형식
```bash
sort [옵션] [파일 경로]
```
- 옵션
    1. `-r` : `내림차순` 정렬
    2. `-n` : `숫자` 순으로 정렬 (기본은 `숫자를 문자로 인식`)
    3. `-f` : `대소문자 구분 X` 정렬
    3. `-u` : `중복 제거`
    4. `-k` : `특정 필드 기준` 정렬
    5. `-t` : `필드 구분자 지정` (기본 공백)
    6. `-M` : `월 기준` 정렬
    7. `-b` : `공백 무시` 정렬
### 예시
1. 데이터 생성 
    ```bash
    kingrange@kilwon:~$ cat << EOF > sales_data.txt
    Kim     50      Seoul
    Lee     120     Busan
    Park    30      Seoul
    Choi    120     Incheon
    Jung    80      Gwangju
    EOF
    kingrange@kilwon:~$ ls
    sales_data.txt
    ```
2. 판매량 높은 순 정렬
    ```bash
    kingrange@kilwon:~$ sort -r -n -k 2 sales_data.txt
     # 2번째 열(판매량)으로 정렬하고, 숫자를 숫자로 인식하고, 역순 정렬
    Lee     120     Busan
    Choi    120     Incheon
    Jung    80      Gwangju
    Kim     50      Seoul
    Park    30      Seoul
    ```
3. 지역별로 정렬하고 같은 지역이면 이름 순
    ```bash
    kingrange@kilwon:~$ sort -k 3 -k 1 sales_data.txt
     # k 인자를 두 번써서 3으로 먼저 정렬하고 1로 정렬
    Lee     120     Busan
    Jung    80      Gwangju
    Choi    120     Incheon
    Kim     50      Seoul
    Park    30      Seoul
    ```

## awk 
- Text 처리 도구
    - 데이터를 열 단위로 인식하여 `계산`,`조건문`,`반복문` 등을 수행할 수 있는 도구
    - 패턴을 기반으로 동작
    - `Stream 및 기타 데이터 형식`을 `조작`하고 `처리`
- Record : 각 줄
- Field : Record 안의 각 단어

### 형식
```bash
awk 옵션 'pattern {action}' file경로
```
- 옵션
    - `-F` : 구분자 지정 (기본 : 공백/Tab)
    - `-v` : 외부 변수 전달
### 예시
- 기본 사용
    ```bash
    kingrange@kilwon:~$ ls -l
    total 4
    -rw-rw-r-- 1 kingrange kingrange 74 Jan  8 09:12 sales_data.txt
    ```
- `-F` 사용
    - passwd 목록에서 이름(첫 열)만 가져오기
    ```bash
    kingrange@kilwon:~$ awk -F ":" '{print $1}' /etc/passwd
    root
    daemon
    bin
    sys
    sync
    games
    man
    lp
    mail
    ...
    landscape
    fwupd-refresh
    usbmux
    kingrange
    lxd
    sshd
    ```
- `-v` 사용
    - 과소비한 (판매량이 너무 높은 사람 필터링)
    ```bash
    kingrange@kilwon:~$ awk -v lim=$limit '$2 > lim {print $1, "너무 커요"}' sales_data.txt
    Lee 너무 커요
    Choi 너무 커요
    ```
- 실제론 `로그 분석`, `시스템 자원 확인`에서 많이 사용한다.
## sed
- Stream Editor(SED)
    - 파일을 직접 열지 않고, Stream을 따라가며 텍스트를 변환하는 도구 
### 형식
```bash
sed [옵션] 스크립트 [파일경로]
```
- 옵션
    1. `-n` : 기본 출력 억제
    2. `-i` : 파일 직접 수정
    3. `-e` : 여러 명령을 순차적으로 실행
    4. `-E` : 확장된 정규 표현식 사용 
### 예시
1. 샘플 데이터 생성
    ```bash
    kingrange@kilwon:~$ cat test
    kingrangE
    king
    KingrangE
    kilwon
    Tiger
    Is
    King
    ```
2. king을 King으로 치환 후 출력 (`-i` 없음)
    ```bash
    kingrange@kilwon:~$ sed 's/king/King/' test
    KingrangE
    King
    KingrangE
    kilwon
    Tiger
    Is
    King
    ```
3. king을 King으로 수정
    ```bash
    kingrange@kilwon:~$ sed -i 's/king/King/g' test
    kingrange@kilwon:~$ cat test
    KingrangE
    King
    KingrangE
    kilwon
    Tiger
    Is
    King
    ```
4. KingrangE랑 King이 들어간 내용만 출력
    ```bash
    kingrange@kilwon:~$ sed -n '/KingrangE/p' test
    KingrangE
    KingrangE
    kingrange@kilwon:~$ sed -n '/King/p' test
    KingrangE
    King
    KingrangE
    King
    ```

# 파일 접근 권한 관리
- 접근 권한 : 파일이 가지는 속성 중 하나
    - 확인 명령 : `ls -l`
- 사용자 group 확인 : `groups [사용자명]`
    - 사용자는 기본적으로 1개 이상의 그룹에 속한다.
        - `Group을 이용`하여 `동일 그룹의 사용자`에게 `파일 공유`가 `가능`하다.
        - `System 관리자`가 `사용자를 등록`할 때, `Group을 같이 지정`한다.
        - 그룹 정의 위치 : `etc/group`
            - System 관리자만 수정 가능하다.
## 권한의 종류
1. read (r)
    - 파일 : 내용을 `읽거나 복사`
    - 폴더 : ls 명령으로 확인 (`폴더 내 파일 확인 가능`)
2. write (w)
    - 파일 : 파일을 수정/이동/삭제
    - 폴더 : 파일 생성 및 삭제
3. execute (x)
    - 파일 : 실행
    - 폴더 : cd 명령으로 이동
4. 권한없음 (-)

## chmod 명령
- 접근 권한 변경 명령
### 형식
```bash
chmod [옵션] 권한 [파일/디렉토리 경로]
```
- 옵션
    - `R` : 하위 Directory까지 모두 변경
- 변경 방식
    1. 기호 모드 
        ```bash
        chmod [사용자 카테고리 문자] [연산자 기호] [접근 권한 문자]
        ```
        - 사용자 카테고리 문자
            1. `u` : user
            2. `g` : group
            3. `o` : others
            4. `a` : all

        - 연산자 기호
            1. `+` : 권한 부여
            2. `-` : 권한 제거
            3. `=` : 권한 설정
        
        - 접근 권한 문자
            1. `r` : 읽기
            2. `w` : 쓰기
            3. `x` : 실행
        - 예시
            ```bash
            mkdir ex
            cd ex
            ls -l # rw-r--r-- (소유자:읽쓰/그룹:읽/기타:읽)
            cp /etc/hosts test.txt # 복사 테스트 -> 가능 (소유자)

            chmod g + wx # 그룹에 쓰기,실행 권한 부여
            chmod u - w # 유저 그룹에 쓰기 권한 삭제
            cp /etc/hosts test.txt # 불가
            cp: cannot create regular file 'test.txt': Permission denied
            ```
    2. 숫자 모드 
        - 8진수 3자리로 표기한다.
        - 읽기 : 4 / 쓰기 : 2 / 실행 : 1
        - 예시
            - 모든 사용자에게 읽기 권한만 부여
                ```bash
                chmod 444 test.txt
                ```
            - 그룹에게만 모든 권한 부여
                ```bash
                chmod 474 test.txt
                ```
## 기본 접근 권한
- File/Directory 생성 시, 주어지는 접근 권한
    - 파일 : 664 (폴더와 동일하나, 파일은 execute가 기본적으로 빠져있다.)
        - 실행 권한은 매우 위험성 있는 권한이기 때문
    - 폴더 : 775

## 특수 접근 권한
- `umask` 명령 결과의 맨 앞자리
    - 0 : 일반 접근 권한
    - 1 : sticky bit
        - 누구나 파일 생성이 가능한 directory 만들 때 사용
        - 우분투의 `/tmp 폴더`가 sticky bit를 가진다.
    - 2 : SetGID
        - 2 권한을 가진 폴더 내부 파일은 생성 시 자동으로 부모 폴더의 소유 그룹의 권한을 상속한다.
            - 즉, 그룹 teamA의 dev1과 dev2가 있다고 가정하겠다.
                - 이때 teamA 폴더는 2 권한을 갖는다 가정.
                    - 만약, dev1이 teamA 폴더에 파일을 생성한다면, 일반적으로는 dev2가 접근할 수 없다.(dev1의 소유 그룹이 접근 가능하기 때문) 
                    - 하지만, teamA 폴더가 2 권한을 가지므로 dev1이 생성한 파일은 dev2가 접근할 수 있다.(같은 teamA 그룹 취급)
        - 공동 작업 폴더 생성 시 사용
    - 4 : SetUID
        - 4 권한을 가진 파일은 `실행 시` User의 권한이 아니라, `파일 소유자의 권한`이 `자동으로 적용`된다.
        - passwd가 4 권한을 가진다. 일반적으로 password 파일은 root가 관리한다. 하지만, 사용자도 비번 변경이 가능하다.
            - 이 이유가 passwd가 4 권한을 갖기 때문이다.
        - 4를 남발하면, `권한 상승 공격`의 대상이 될 수 있으므로 유의하길 바람.
            - ex, vi 명령어에 4를 사용하면, 유저가 vi를 통해 root와 동일한 작업을 할 수 있음


## umask 명령
- 기본 접근 권한을 변경
    ```bash
    umask [옵션] [마스크값]
    ```
    - 마스크 값 
        - mask 연산 = 반대 연산
        - 즉, 마스크 값을 내가 원하는 값의 보수로 주면 된다.
            - 만약 내가 554를 원한다면
                - 223 이라고 입력하면 된다.
    - 옵션
        - `S` : 마스크 값을 문자로 표현

- 마스크 확인
    ```bash
    umask # 0002 (맨앞(0) : 특수 접근 권한 표시)
    umask -S # u=rwx, g=rwx, o=rx
    ```

- 예시, 소유자 모든 권한, 그 외 아무 권한 X
    ```bash
    umask 077
    ```
- 예시2, sticky폴더가 stickty bit를 가지도록 변경
    ```bash
    kingrange@kilwon:~$ chmod 1744 sticky/
    drwxr--r-T 2 kingrange kingrange 4096 Jan  8 10:23 sticky
    ```

# 프로세스
- 실행 중인 프로그램을 의미한다.
- Linux : `다중 프로세스 시스템`
    - `다중 프로세스 시스템` : `여러 개의 프로세스`를 `동시에 실행`
- 종류
    1. `운영`에 필요한 `다양한 기능`을 수행하는 프로세스
    2. `사용자가 실행`한 프로그램 (사용자 프로세스)
- 프로세스는
    1. `부모-자식 관계`를 가진다.
        - 부모 프로세스가 없는 프로세스는 오직 2개 뿐
            - Linux 부팅 시, 스케줄러가 실행한 프로세스
                1. systemd
                2. kthreadd
    2. 기본적으로 `자신이 수행할 작업`을 `전부 수행하면 종료`된다.

## PID
- `프로세스 번호`를 의미한다.
    - 프로세스는 각각 `고유한 번호`를 가진다.
- `1부터 시작`하고, `추가 프로세스가 실행`되며 `1씩 증가`한다.
- systemd : 1 / kthreadd : 2
    - `systemd`와 `kthreadd`는 `처음 부팅 시 실행`되는 프로세스로 `각각` `1`과 `2`다.
    - `ps -ef로 확인`하면, `systemd`는 `/sbin/init`로 표시되어 있다.
        - 해당 폴더의 설명을 확인하면 아래와 같다.
            ```bash
            kingrange@kilwon:~$ ls -l /sbin/init
            lrwxrwxrwx 1 root root 20 Aug 26 15:23 /sbin/init -> /lib/systemd/systemd
            ```
            - 보이듯이 `심볼릭 링크`다.
            - `과거`에는 `/sbin/init`이라는 이름이었는데 `현재`는 `systemd로 변경`되었다. 하지만 `기존 시스템과 변경되지 않은 것처럼 보이도록` `symbolic link로 숨긴 것`이다.
## 데몬(daemon) 프로세스
- 사용자가 직접 제어하는 terminal 뒤에서 `Background`로 상주하며, `서비스를 제공`하는 프로세스
    - 현대에는 서비스와 혼동하여 `service`라고 부르기도 한다.
        - 굳이 구분하자면, `service`는 user가 daemon을 통해 제공받는 `기능`이나 `작업 단위`
- 사용자가 `logout해도 종료되지 않고`, `System이 켜져있는 동안 계속 실행`
### 주요 특징
1. `Background 실행` : 사용자와 직접 상호작용 X
2. `지속성` : 시스템 부팅 시, 시작되어 종료까지 살아있음
3. `제어 터미널 X` : tty와 같은 특정 터미널에 종속되지 않음
    - 터미널을 닫아도 종료되면 안되기 때문 
4. `이름 규칙 존재(d)` : 관례적으로 이름 뒤에 d를 붙여 표시한다.
    - systemd,kthreadd

## 고아(orphan) 프로세스
- `자식 프로세스`가 `실행 중`인데, `부모 프로세스`가 `종료되었을 때`의 `자식 프로세스`를 이르는 말
    - 기본적으로 자식 프로세스는 종료되면, 부모 프로세스로 돌아간다.
        - 돌아갈 곳이 없어져서 `고아`가 되었다는 것
    - 의도적으로 부모 프로세스가 자식 프로세스를 Background에 두고 돌아가서 고아 프로세스로 만드는 경우도 있다.
- `고아 프로세스 처리`
    - 고아 프로세스의 새로운 부모 프로세스로 systemd process를 지정
    - 작업 종료 후, systemd가 종료 상태(Exit Status)를 받아주고, 자원을 회수한다.
- 좀비 프로세스와 다르게 위험하지 않다. (systemd가 처리해주므로)
## 좀비 프로세스
- 자식 프로세스가 종료되면, OS는 바로 모든 정보를 삭제하지 않고, Exit Status를 보관해둔다.
    - 이 Exit Status를 부모 프로세스가 확인하고 부모 프로세스 테이블에서 삭제를 해주어야 `진짜 종료`가 된다.
    - 이 확인 및 삭제를 안해주면, 자식 프로세스는 `좀비 프로세스`가 된다.
- 특징
    1. `자원 소모 X` : `좀비 프로세스`는 이미 종료되었으므로 `CPU`나 `Memory`를 사용하지 않는다.
    2. `PID 점유` : 하지만, 하나의 프로세스로서 프로세스 테이블을 차지하고 PID를 점유하고 있다.
        - 이로 인해 PID가 부족해지면, 새로운 프로세스를 실행하지 못하게 된다.
- 확인 방법
    - `ps 명령어` 실행 후, `STAT 열`에 `Z`라고 표기되거나, `<defunct>`라는 문구가 붙어있으면 `좀비 프로세스`
- 해결 방법
    1. SIGCHLD 시그널을 부모 프로세스에 보내서 정리하도록 하기
    2. 부모 프로세스를 종료 

## 프로세스 관리
- 프로세스 목록 확인
    ```bash
    ps [옵션]
    ```
    - 옵션 
        - UNIX와 같은 옵션
            - 프로세스 목록, 좀비 프로세스 확인 등 (`ps -ef`)
            1. `-e` : 실행 중인 모든 프로세스 확인
            2. `-f` : 자세한 정보
            3. `-u uid` : UID를 전달해서 특정 유저가 실행한 것만 확인
            4. `-p pid` : PID를 전달해서 PID에 해당하는 프로세스 정보만 확인
        - BSD 옵션 (`-`안붙임)
            - 서버 상태, CPU 점유율 등 확인 (`ps aux`)
            1. `a` : 터미널에서 실행시킨 것 확인
            2. `u` : 상세정보 (CPU, MEMORY 사용량, 가상 메모리 크기(VSZ), 실제 메모리 크기(RSS) 등)
            3. `x` : 모든 프로세스 정보 확인
- 프로세스 종료
    - `프로세스에 시그널`을 보내서 `프로세스를 종료`
    - 종류
        1. kill (PID로 종료)
            ```bash
            kill [-시그널] PID
            ```
            - 많이 사용하는 시그널
                1. 2 : Interrupt
                2. 9 : 강제 종료
                3. 15 : 프로세스와 관련된 파일들을 정리하고 종료 (종료되지 않는 프로세스가 있을 수 있음)
        2. pkill (프로세스 명으로 종료)
            ```bash
            pkill 프로세스이름
            ``` 
            - 동일한 이름의 `모든 프로세스` 종료
                - `killall`로도 모든 프로세스 종료가 가능하다.
    - 시그널 종류 확인
        ```bash
        kill -l
        ```
    - 예시
        - 터미널 1개에서 man ps 명령 수행
        - 다른 터미널을 열어서 man 돌아가는지 확인
            ```bash
            kingrange@kilwon:~$ ps -ef | grep man
            root         126       2  0 Jan07 ?        00:00:00 [charger_manager]
            kingran+    4896    2880  0 08:11 pts/0    00:00:00 man ps #이게 찐또
            kingran+    4912    4881  0 08:11 pts/1    00:00:00 grep --color=auto man
            ```
        - 강제 종료
            ```bash
            kill 4896 # 4896(man) 강제 종료
            ```
            - 그러면, 다른 터미널에서 실행하던 man이 종료됨
## 작업 제어
### Foreground 작업
- 사용자가 입력한 명령이 실행되어 결과가 출력될 때까지 기다리는 방식으로 처리되는 프로세스
- ex : sleep 100 (100초 동안 대기)
    ```bash
    kingrange@kilwon:~$ sleep 1100000
    kingrange@kilwon:~$ ps -ef | grep sleep #터미널 2 확인
    kingran+    4974    2880  0 08:27 pts/0    00:00:00 sleep 1100000
    kingran+    4976    4881  0 08:27 pts/1    00:00:00 grep --color=auto sleep
    ```
### Background 작업
- 명령의 처리가 끝나는 것과 상관없이 `곧바로` Prompt를 출력해서 `다른 작업을 수행`할 수 있도록 하는 것
- 명령의 실행의 시간이 오래 걸리거나 명령 실행한 후 다른 작업을 할 필요가 있을 때 사용함.
    - 사용 방법
        ```bash
        명령 & # sub shell로 넘겨서 처리하는 것임
        ```
    - 예시
        ```bash
        kingrange@kilwon:~$ sleep 10&
        [1] 4978 # 이 숫자는 뭐노?
        kingrange@kilwon:~$ sleep 30&
        [2] 4979
        ```
        ```bash
        kingrange@kilwon:~$ ps -ef | grep sleep
        kingran+    4978    2880  0 08:31 pts/0    00:00:00 sleep 10 # 각각
        kingran+    4979    2880  0 08:31 pts/0    00:00:00 sleep 30 # 찍힘
        kingran+    4981    4881  0 08:31 pts/1    00:00:00 grep --color=auto sleep
        ```
- 백그라운드 작업이 내용을 출력할 때, 현재 작업 내용과 겹쳐져서 출력될 수 있다.

### jobs 명령
- `현재 세션`(터미널 창)에서 `백그라운드`로 실행 중이거나 `일시 중지된 작업들의 목록`을 확인
    - `ps` : `전체 프로세스` 확인
    - `jobs` : `이 터미널 창에서 시킨 일들`만 관리
- 종류
    1. Running : 현재 Background에서 실행 중 
    2. Stopped : CTRL+Z 등으로 실행이 일시 중지된 상태
    3. Done : 작업이 완료됨
    4. Terminated : 강제 종료되었음
- 기호와 의미
    1. `[숫자]` : 작업 번호
    2. `+` : 가장 최근에 접근/생성된 작업
    3. `-` : + 작업 바로 이전에 다룬 `이전 작업`
#### 형식
```bash
jobs [옵션]
```
- 옵션
    1. `-l` : `작업 번호`와 함께 `PID` 표시
    2. `-r` : 현재 `실행 중인 작업` 표시
    3. `-s` : 현재 `정지된 작업` 표시

#### fg/bg
```bash
fg/bg [%작업번호]
```
- 작업 번호에 해당하는 작업을 
    - fg : foreground로 이동 
        - 다시 작업 재개
    - bg : background로 이동
        - 계속 background에 있게 함.