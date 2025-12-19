# 실습 1 : 문자열과 list 에 == 와 != 를 사용할 수 있는지 확인해보기
# 결과 : 둘 다 eq, ne 가지고 있으므로 비교 가능
print('__eq__' in dir(str)) 
print('__ne__' in dir(str)) 
print('__eq__' in dir(list)) 
print('__ne__' in dir(list)) 


"""
결과
True
True
True
True
"""