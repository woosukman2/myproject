from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

db.users.insert_one({'name':'스무디킹','age':10})
db.users.insert_one({'name':'스타벅스','age':25})
db.users.insert_one({'name':'커클랜드','age':90})