# 12_23

## 다중 상속
- 여러 개의 클래스로부터 상속받는 것
    - 여러 클래스의 속성을 받을 수 있음
        - 장점 : 확장성이 뛰어남
        - 단점 : 의존성이 높아져서 유지보수가 어려워짐 
        - 단점이 크기에 권장하지 않는 형태
            - JAVA,C++에서 지원하지 않는 이유
- 동일한 메서드가 존재할 때, `메서드 호출 순서 확인`
    - `클래스이름.mro()` 함수를 이용하여 확인
    - 실행
        ```python
        class Super1:
            def __init__(self):
                print("Super1입니다.")
            def method1(self):
                print("Super1의 메서드")

        class Super2:
            def __init__(self):
                print("Super2입니다.")
            def method2(self):
                print("Super2의 메서드")

        class Sub(Super1,Super2):
            pass

        sub = Sub()
        sub.method1()
        sub.method2()

        print(Sub.mro())
        """
        출력 결과
        Super1입니다.
        Super1의 메서드
        Super2의 메서드
        [<class '__main__.Sub'>, <class '__main__.Super1'>, <class '__main__.Super2'>, <class 'object'>]
        ---
        해석
        이름이 동일한 메서드가 존재하면 저 순서대로 가져온다. 즉 __init__()함수가 Super1과 Super2 둘 다 있는데 Super1이 우선이므로, Super1의 __init__만 실행된다.
        만약, Sub에 __init__이 있다면 Sub게 출력된다.
        """
        ```
    - 파이썬의 클래스들은 `object Class`를 상속받는다.

## 추상
- 추상 메서드 : `내용이 없는 메서드`로 `하위 클래스에서 반드시 구현`
- 추상 클래스 : `인스턴스`를 만들 수 없는 클래스, `반드시` `추상 메서드`를 `1개 이상` 가져야 한다.
    - `인스턴스`를 만들 수 없으므로, `상속`해서 사용해야 한다.
    - 생성 방법
        1. abc 모듈 가져오기
        2. class를 만들 때, class 이름 뒤에 (metaclass=ABCMeta)를 추가
        3. 추상 메서드를 만들 때는 메서드 위에 `@abc.abstractmethod`라는 `데코레이터`를 추가하고, 내용은 `pass`
    - 생성 예시
        ```python
        import abc
        class AbstractClass(metaclass=abc.ABCMeta):
            @abc.abstractmethod
            def method():
                pass       
        ```
- 목적
    1. 템플릿 프로그래밍 - 원형을 만들고 내용을 따로 구현
    2. 통일을 강제할 수 있다.
        - ex, 스타에서 T,Z는 attack, P는 offense라고 하면, 같은 기능인데 다른 이름으로 구현한게 된다.
            - 이것을 강제로 attack/offense로 통일시킬 수 있다.
            - Q) 일반 클래스는 왜 안돼?
            - A) 강제성이 없음. Attack을 상위 일반 클래스로 빼고 상속받은 하위 클래스에서 구현하지 않더라도 에러가 발생하지 않는다.

## 모듈
- 의미
    - `독자적인 기능`을 갖는 구성 요소
        - 함수, 클래스, `파일` 등
        - 독자적인 기능을 갖고 실행이 되면 모두 `모듈`이다.
            - 파이썬에서는 `파일`을 모듈이라고 함.
- 종류
    1. `표준 모듈`
        - 파이썬에 포함된 모듈
    2. `사용자 정의 모듈`
        - 직접 작성한 모듈
    3. `3rd party module`
        - 파이썬 재단이 아닌 곳에서 만든 모듈
        - 사용 방식 : 공식 repository에서 `다운로드(pip install) 받아 설치`하기도 하고, `파일을 복사해와서 사용`하기도 한다.
- 모듈 사용
    1. import : ~ 모듈 가져오기
    2. from - import : ~ 모듈에서 속성, 함수 가져오기
        - `*` 사용 : `모든`의 의미
    3. import - as : ~ 모듈을 별명으로 설정
    4. from - import - as : ~모듈의 속성이나 함수를 별명으로 설정

 
## 경로를 직접 추가
- `sys.path.append("경로")` : 현재 프로그램에서만 추가
- `운영체제의 환경 변수`에 추가 : 모든 프로그램에서 추가됨.
    -  windows : set PYTHONPATH = 경로;
    - MAC / Linux Bash Shell : export PYTHONPATH = 경로
    - Linux C Shell : setenv PYTHONPATH 검색 경로

## 패키지
1. 의미 
    - 관련있는 모듈의 모임
        - 직접 생성할 때는 모듈을 `하나의 디렉토리`에 모으고, `__init__.py`파일을 만들어주면, `이 디렉토리는 패키지가 된다.`
2. 다운로드 
    - 패키지에서 모듈을 가져오고자 하는 경우 : `from-import`
    - site-package 디렉토리 : 외부 패키지가 설치되는 디렉토리
3. 외부 패키지 
    - 설치 : `pip install 모듈이름`
    - 업그레이드 : `pip install 모듈이름 -upgrade`
    - 특정 버전 설치 : `pip install 모듈이름=버전`
        - 특정 버전 이상 설치 : `pip install 모듈이름>=버전`
    - **관리자 기능이 없는 경우, --user를 추가해야 할 수 있다.** -> 먼소리? 
    - 삭제 : `pip uninstall 패키지이름 [-y]`
        - 그냥 y 쳐서 해도 되는데, 그럼 자동화가 안 됨 (자동화를 위해 `-y를 뒤에 붙여주어야 한다.`)
4. 기타 관련 명령
    - 설치된 패키지 검색
        - `pip list --format=columns` : 전체 목록
        - `pip search 패캐지 이름` : 특정 패키지
    - 현재 환경에 설치된 패키지 목록을 txt파일로 만들기 -> Docker Image를 위해 중요함
        - `pip freeze > 파일명` 
        - `pip freeze > requirements.txt` 
    - 파일에 작성된 패키지 목록 설치
        - `pip install -r 파일명`
        - `pip install -r requirements.txt`
    - 직접 다운로드 받아 설치
        - `라이선스`문제가 생길 수 있기에 회사에서는 이렇게 작업할 때도 있다고 한다.
        - `pip download 패키지이름`
        - `pip install 패키지경로`

## 파이썬 실행 명령
- `python 파일 경로`
    - BUT, 디렉토리에 `__main__.py` 파일이 있는 경우,`python 디렉토리이름`을 입력해도 된다.

## Python 기본 자료형
1. Scala Data : bool, int, float, complex (What Complex?)
2. Vector Data : bytes(byte 집합), list(sequence, 변경 가능한 데이터 모임), str(문자 집합), set(non sequence, non duplication), tuple(sequence, non-change), dict(is consist of both of key and value)
3. 데이터를 표현하는 Class vs dict 
    - Class : 정형
        - RDBMS
        - 장점 : 안정성 우수
    - dict : 비정형
        - NoSQL
        - 장점 : 읽기 속도 빠름, 유지 보수 유리
    - 예시
        ```python
        # 하나의 데이터를 클래스를 이용해서 만드는 경우
        class Person :
            def __init__(self):
                self.name =""
                self.age = 0
        
        person = Person()
        person.name = "Adam"
        person.age = 1

        # 데이터 출력 
        print("이름 : ",person.name,"나이 :",person.age)
        # dict로 만드는 경우
        person2 = {"이름":"Eve","나이":25}
        for key in person2 :
            print(key,":",person2[key],end =" ")
        ```
        - MVC -> Model, View, Controller를 구분하여 서로 변경했을 때에도 최대한 문제가 안생기도록 의존성을 분리한 것이다.
            - dict와 class 중 MVC에 적절한 것이 무엇일까?
                - dict는 key를 변경해도 출력(View)에 문제가 없다.
                - class는 key를 변경하면 출력(View)에 문제가 생긴다.
            - dict는 모든 데이터를 출력하고자 할 때, 키의 이름없이 출력이 가능하기 때문에 키의 이름이 변경되더라도 변경없이 출력 가능
                - dict는 `구조를 먼저 만들지 않기 때문`에 `여러 개의 데이터를 표현`할 때, `모두 동일한 모양이라고 장담할 수 없다.`
                    - 따라서 모든 dict는 같은 모양이라고 장담할 수 없다.
4. 2차원 데이터 표현법
    - 종류
        1. Matrix(2차원 배열) - numpy
            - 예시
                ```python
                kia = ["전상현","김도영"]
                hanwha = ["문동주","리베라토"]
                lg = ["문보경","김현수"]
                baseball = [kia,hanwha] # 2차원 배열

                for i in range(len(baseball)):
                    if i == 0 :
                        print("기아 :",end="\t")
                        print(*baseball[i],sep=", ")
                    else :
                        print("한화 :",end="\t")
                        print(*baseball[i],sep=", ")
                ```
            - 이 형태의 단점은 위 코드에서 baseball 2차원 배열에 lg를 추가할 시, 출력 부분(view)도 elif i == 1: 이런 식으로 수정을 해야한다.
                - 즉, 데이터 변경에 유연하지 못하다.
        2. Table(Dict, Class의 배열) - pandas (번거롭고 어려움)
            - 예시
                ```python
                kia = ["전상현","김도영"]
                hanwha = ["문동주","리베라토"]
                lg = ["문보경","김현수"]
                kbo =[
                    {"team":"기아","players":kia},
                    {"team","한화","plyaers":hanwha}
                ]
                for team in kbo :
                    print(team["team"],end ="\t")
                    print(*kbo["players"],sep =", ")
                ```
            - 여기서는 `kbo.append({"team":"lg","players":lg})`로 값을 추가해줘도 view를 고치지 않아도 잘 나온다.

5. Comprehension 
    - sequence 객체에 연산을 적용해서 `새로운 sequence를 얻어내는 문법`
    - 형식
        - `[연산식 for 임시변수 in sequence 객체 [if 조건식]]`
        - sequence 객체의 `모든 요소를 임시 변수에 대입`한 후, `조건식을 확인`해서 `연산식을 적용`한 후, `새로운 list로 생성`
    - 장점
        - 속도가 빠름 -> 병렬로 적용되기 때문
        - 코드가 짧음
    - 차이 비교
        - 일반적 방식
            ```python
            data = [1,2,3,4,5]
            result = []
            for val in data :
                result.append(val*2)
            print(result)
            ```
        - comprehension
            ```python
            data = [1,2,3,4,5]
            result = [i*2 for i in data]
            print(result)
            ```

6. queue, itertools, collections 
    1. `collections 모듈`
        - Counter Class
            - 기능 : `데이터의 개수` 혹은 `집계`를 편리하게 해주는 클래스
            - `Counter Class`에 `Sequence 형태의 데이터를 설정`해서 `Instance를 생성`하면 `sequence 요소의 개수를 집계`하여 `dictionary 형태로 반환`함
            - 사용 상황
                - 집계를 사용한 후, 상위 몇 개의 요소를 추출할 때 사용 (ex, WordCloud)
                - 예시
                    ```python
                    from collections import Counter
                    portfolio = [
                        ("GOOG",100,490.1),
                        ("IBM",50,91.1),
                        ("CAT",150,83.4),
                        ("GOOG",110,83490),
                        ("AAPL",980,83490),
                    ]

                    total_shares = Counter()
                    # 레코드 형태의 데이터는 무엇을 기준으로 개수를 셀 것인지 정해주면 된다.
                    for name, shares, price in portfolio:
                        total_shares[name] = total_shares[name]+shares
                    print(total_shares) # Counter({'AAPL': 980, 'GOOG': 210, 'CAT': 150, 'IBM': 50})

                    print(total_shares.most_common(3)) #[('AAPL', 980), ('GOOG', 210), ('CAT', 150)]
                    ```
    2. `itertools 모듈`    
        - `순열`,`조합` 등에 사용되는 함수와 클래스를 가지고 있는 패키지
        - `permutations` : 순열
        - `combinations` : 조합
        - `products` : 중복 순열
        - `combinations_with_replacement` : 중복 조합

- 1~4 : 실제 데이터 관련 문제, 5~6 : 코테 관련 문제

## Exception Handling(예외 처리)
1. 오류
    - 종류
        1. 컴파일 오류 : 문법에 맞게 작성되지 않아서, `프로그램 실행이 되지 않는 오류`
            - 컴파일 할 때는 자료형만 확인한다. (값을 확인하는 것이 아님)
        2. 런타임 오류 : 프로그램은 동작하지만, `알고리즘의 오류로 잘못된 결과가 만들어지는 경우`
2. 예외(Exception)
    - `예외`는 `런타임 오류`다.
    - 문법적 오류가 없어 실행은 되지만, 실행 중 예기치 않은 상황이 발생해서 프로그램이 중단되는 현상
        - 예시
            ```python
            def ten_div(x:int)->float:
                return 10/x
            ten_div(0) # 자료형이 int 맞으므로 compile은 된다. -> but, 0으로 나누기는 불가능하므로, 런타임 오류 발생
            ```
    - 예외 처리 용도
        1. 정상 종료하기 위함
        2. 예외 내용 기록하기 위함
        3. 예외가 발생하더라도 계속해서 실행하도록 하기 위함
        4. 예외가 발생했을 때, **정상적인 값으로 변경해서 실행**하기 위해서
    - 예외처리 방법 :
        ```python
        try : 
            예외가 발생할 가능성 있는 구문
        except : 
            예외가 발생했을 때 처리할 구문
        finally : 
            예외 발생 여부에 상관없이 수행할 구문
        ```
    - 기본적인 예외 처리 : 예외가 발생하면 0이 Return되도록 설정
    - 특정한 예외 처리 방법: 정해진 예외만 처리하도록 하는 방법
        ```python
        try :
            예외가 발생할 가능성이 있는 구문
        except 처리할 예외 클래스 : # ex, ZeroDivisionError
            처리할 내용
        ```
        - 특정한 예외 클래스를 이용하고자 하는 경우
            - 예외 클래스 뒤에 `as instance_name`을 추가하면, 블럭 내에서 이용할 수 있는 예외에 대한 내용을 가진 instance가 생긴다.
                ```python
                try :
                    예외가 발생할 가능성이 있는 구문
                except 처리할 예외 클래스 as e: # e라는 이름을 가진 instance가 생김
                    처리할 내용
                ```
    - 여러 개의 Except 처리: 
        - excpet를 여러번 사용할 때, ``상위 클래스 에러 처리를 상단에 작성`하면 `하단에서는 처리되지 않는다.`
            - 예외 클래스 레벨 확인 : https://docs.python.org/3/library/exceptions.html
            - EX) Exception 클래스가 IndexError 클래스보다 상위 클래스이므로, `Exception 클래스`의 `예외처리구문`이 `먼저 호출`된다.
        ```python
        try :
            예외가 발생할 가능성이 있는 구문
        except 예외 클래스 1 : # ex, ZeroDivisionError
            처리할 내용
        except 예외 클래스 2 : # ex, ZeroDivisionError
            처리할 내용
            ...
        ```
    - else와 finally
        - except 절 다음 else와 finally 절을 추가하는 것이 가능하다.
            1. else (예외가 발생하지 않았을 때만 실행됨.)
                ```python
                try : 
                    예외가 발생할 가능성이 있는 구문
                except :
                    예외가 발생한 경우 처리
                else :
                    예외가 발생하지 않았을 때 처리
                finally :
                ```
            2. finally (예외와 관계없이 실행됨.)
                ```python
                ```

3. 단언(Assertion)
    - 개발자가 의도적으로 `특정 조건을 만족하지 않는 경우` `프로그램을 중단시키는 것`
    - 강제로 예외 발생
        -  방식
            1. 
            ```python
            raise Exception("예외 내용") # -> 이렇게 강제로 프로그램을 중단하는 것을 `assertion`이라고 한다.
            ```
- 오류 발생 시 조치
    - `컴파일 오류`는 `수정`해야 한다.
    - `논리적 오류`는 `디버깅을 통해서` 알고리즘의 `문제점을 찾고 수정`
    - 예외는 `디버깅을 통해서 수정` or `예외 처리 구문(많이 중요하다.)`을 삽입
        - 디버깅
            - Exception이나 논리적 오류의 원인을 찾아내고 수정하는 과정
            - 방법
                1. Logging 
                    - 직접 로깅 : 
                    - 로깅 툴 : ELK 등
                2. IDE가 제공하는 Debugging Tool
                3. Testing Tool
- 예외 처리는 아주 중요
    - 예외 처리를 잘 안하면, 작은 외부 요인에도 프로그램이 죽어버린다.
    - 서버의 경우, 고가용성이 중요하기 때문에, 예외처리를 더 잘해야 한다.

## 파일 핸들링
1. 파일 처리
    1. 파일 처리 코드 작성
    2. Program은 OS에게 `파일 처리`를 요청
    3. OS가 `요청한 업무 처리`
    4. OS가 결과 프로그램에게 돌려줌
2. 파일 처리 과정
    1. 파일 포인터 = 파일 개방(open)
    2. 파일 포인터를 이용해서 작업 (읽기, 쓰기)
    3. 파일 포인터.close()
3. 실습
    1. 파일 쓰기
        - 파일 쓰기를 하고자 하는 경우, `2개나 3개 매개변수를 이용`해서 `쓰기모드 개방`
            - 매개변수 : 파일 경로, "w", 인코딩 방식(ms949,cp949,euc-kr,utf-8 등)
            - 인코딩 방식을 생략하면, `시스템의 기본 인코딩 방식`으로 설정된다.
            ```python
            file_url = ""
            file = open(file_url,"w","euc-kr") 
            ```
        - 파일 포인터.write(기록할 내용)를 이용해서 쓰기 수행
        - \n이 있는 경우 writelines를 이용해서 줄 단위 기록 가능, `join`을 이용해서도 기록 가능
            - write와 writelines의 차이 : ? 
            - join을 왜 쓴다는거임? :

    2. 파일 읽기
        - 매개변수("w")생략 or "r"로 설정 -> 읽기 모드 개방
        - 인코딩 방식 설정 가능
        - 전체를 하나의 문자열로 읽을 때 -> read() 함수를 이용
        - 줄 단위로 읽고자 할 때는 `readline()`, `readlines()`를 이용해서 읽어낸다.
            - 둘의 차이는 무엇?>
        - read(정수)를 이용하면, 정수 바이트만큼만 읽어서 return 
- 파일의 경로 설정
    - 절대 경로 : 루트로부터 전부 작성한 경로
    - 상대 경로 : 현재 디렉토리를 기준으로 작성한 경로
    - `./` : 현재 디렉토리
    - `..` : 상위 디렉토리

## Serializable(직렬화)
- **instance를 파일에 기록**하는 것
- 응용 프로그램이 **파일에 기록**하고 **읽어올 때 사용**하는 방식
- `파일에 기록`할 때 
    - `pickle.dump(출력할 데이터, 파일 객체)`
- `파일에서 읽어올` 때
    - `pickle.load(파일 객체)`
    - 1개씩 읽거나, `loads`를 이용하여 한 번에 읽음


## 숙제
- 지금까지 배운 내용을 토대로 나만의 RDB를 만들기
- pickle을 이용해서 객체를 저장하고 불러오고 할 수 있다.

## 참고
1. 자바는 `다중 상속`을 지원하지 않는다. (인터페이스도 `다중 구현`)

2. `Template Programming`
    - `Template(원형)`을 만들고, `Implementation(구현)`
        - ex, 로그인 기능을 해야되면, Template으로 `login()->str` 이렇게 적으면 된다.
            - C언어의 함수 원형 쓰는거랑 비슷하다고 보면 된다.
        - 이 `Template 만드는 것`을 `추상`이라고 한다.
    - 이 `Template`만 가지면, `Interface`, Implementation까지 가지면 `Abstract`라고 한다.
        - 추상 메서드 -> `반드시 구현`
            - 이 `반드시 구현을 강제`하는게 상위 클래스에 `추상 메서드`를 만드는 것
                - 이 `추상 메서드`를 하위 클래스에서 각자 구현하는게 `polymophism`

3. Controller - Service - Repository 구분
    - Controller -> Domain -> DTO 
    - Service -> Domain -> VO/DTO (실제로 우리가 분리 개발하는 것이 유리한 부분은 여기)
        - 실제 비즈니스 로직, Common Concern 저장
    - Repository -> Entity 
        - 저장/읽기

4. 코딩은 `리눅스`에서 하쇼.

5. 외부 파일을 이용하는 것 -> File 다루기 or Network다루기
    - Application 내부에서 통신 : Memory 이용(공유변수, 전역변수, 파라미터 등)
    - 외부 파일을 이용하는 것 -> Exception Handling 필수 
        - 내가 만든게 아니니까 `이게 있다 없다를 보장`할 수 없음
        - slack을 사용해서 issue를 기록하도록 하게 함.
            - slack 아니어도 되는데 개발자들은 대부분 slack 쓰니까 slack하쇼
    - 동일한 호스트의 두 Application이 통신하려면 
        1. pid를 통해 OS에게 연결을 요청
        2. 포트넘버를 통해 OS에게 연결을 요청
        - 2번 방법이 더 좋다.
            -  WHY?
            - PortNumber는 내가 설정하는 것, pid는 OS가 설정하는 것 따라서 Port가 인간한테 더 좋음

6. 프로젝트 한거는 Blog에 기록하던지 `Remember에 기록`하기
