fruit = {"봄" : "딸기", "여름" : "토마토", "가을" : "사과"}

season_user = input("계절을 입력하세요: ")
# if season_user in fruit.keys() :
#     print("정답입니다")
# else :
#     print("오답입니다")

if season_user in fruit :
    print("정답입니다")
else :
    print("오답입니다")