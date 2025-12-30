from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker

DB_URL = "mysql+pymysql://root:6764@localhost:3306/adam?charset=utf8mb4"
#mysql+pymysql://사용자ID:사용자PW@IP:PORT/DATABASE?charset=

#데이터베이스 연결 통로생성
engine = create_engine(DB_URL,echo=True)
#echo가 True면 실제 수행되는 SQL을 확인할 수 있다.

#세션 설정 (통신할 수 있는 통로)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#모델 생성할 기본 클래스 생성
Base = declarative_base()
# 테이블 모델 정의
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100),unique=True)

#테이블 자동 생성
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try :
    """ 추가
    new_user = User(name="졸려요",email="iwanna")
    db.add(new_user)
    db.commit()
    """

    """ 조회
    user = db.query(User).filter(User.name=="졸려요").first()
    if user :
        print(user)
        print(user.name, user.email)
    else:
        print("졸려요씨는 없다.")
    """
    
    """ 수정1
    db.query(User).filter(User.name=="졸려요").update({"name":"김똥개"})
    db.commit()
    """
    """ 수정2
    user = db.query(User).filter(User.name=="졸려요").first()
    if user :
        user.name = "김똥개"
        db.commit()
    else :
        print("안졸리나졸리")
    """
    """ 삭제
    user = db.query(User).filter(User.name=="김똥개").first()
    db.delete(user)
    db.commit()
    """

except Exception as e:
    print("Error :",e)
finally:
    db.close()