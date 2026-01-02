from pymongo import MongoClient

# Mongo 데이터 베이스 서버 연결 (포트번호는 27017이 아닐때 적는거)
con = MongoClient("127.0.0.1")

# 사용할 DB 설정
db = con.admam

# 컬렉션 설정
users = db.users

# 데이터 생성
doc1 = {'empno':1,'name':'해글러1','job':'boxer1'}
doc2 = {'empno':2,'name':'해글러2','job':'boxer2'}
doc3 = {'empno':3,'name':'해글러3','job':'boxer3'}
doc4 = {'empno':4,'name':'해글러4','job':'boxer4'}
doc5 = {'empno':5,'name':'해글러5','job':'boxer5'}

# Create
users.insert_one(doc1)
users.insert_many([doc2,doc3,doc4,doc5],ordered=False)

# Read
result=users.find()
print(result)
for r in result:
    print(r)

# filtering -> find의 결과는 cursor
result = users.find({'name':'해결러3'})


# 데이터 수정
# Update
users.update_one( # 겹치는 것중 가장 처음것만 바꿈
    {"job":"boxer3"},
    {"$set":{"name":"길원이"}}
)
users.update_many( # 겹치는게 5개면 5개를 바꿈
    {"job":"boxer3"},
    {"$set":{"name":"길원이"}}
)

## Delete
users.delete_many( # 이름이 길원이인 애들 다 삭제
    {"name":"길원이"},
)

