# ODM 연결
from mongoengine import connect

connect(db="adam", host="localhost",port=27017)

from mongoengine import Document, StringField, IntField, EmailField, DateTimeField
from datetime import datetime

# 테이블 정의
class User(Document):
    name = StringField(required=True,max_length=50)
    age = IntField(min_value=0)
    email = EmailField(unique=True)
    created_at = DateTimeField(default=datetime.now)

    meta = {
        "collection":"members"
    }

#데이터 생성
user = User(
    name="해글러",
    age = 70,
    email = "itstudy@gmail.com"
)

#데이터 저장
# user.save()

# 전체 조회 -> 결과가 List[Objects]
users = User.objects()
print(users[0].email)

# 개별 조회 -> 결과가 Object
user = User.objects(name="해글러").first()
print(user.name)