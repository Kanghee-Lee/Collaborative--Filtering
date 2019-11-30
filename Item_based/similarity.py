'''
2
2
10
5
15
1 1 1.0
2 1 2.0
5 1 1.2
2 2 1.5
3 2 3.0
1 3 2.2
2 3 6.2
7 3 1.5
6 4 1.2
3 4 1.5
1 4 3.1
2 4 4.0
4 5 8.2
2 5 6.5
7 5 8.0
2
1
2
'''



from sys import stdin
from math import sqrt


# user가 평가한 기록이 있는지 검사
def isRated(user):
    global table
    for i in table.keys():
        if user in table[i].keys():
            return True

    return False



num_sim_item_topk = int(stdin.readline()) # 예상 ranking에서 정보이용할 유사한 item top k개
num_rec_item_topn = int(stdin.readline()) # 추천해줄 최종 output item top n개
num_users = int(stdin.readline()) # user 명 수
num_items = int(stdin.readline()) # item 개수
num_rows = int(stdin.readline()) # dummy 정보 입력 개수

#나중에 확장할떄 이용
weight_small_category=0 #두 Item의 Small-category정보가 동일할때 줄 가중치
weight_big_category=0 #두 Item의 Big-category정보가 동일할때 줄 가중치
#나중에 확장할떄 이용

temp_table=[]
norate=[str(_) for _ in range(num_items)]   #rating정보가 하나도 없는 item
for _ in range(num_rows) :
  row = stdin.readline().split()
  u_id, i_id, rating = row
  if str(i_id) in norate :
    norate.remove(i_id)
  rating=float(rating)
  temp_table.append([u_id, i_id, rating])
num_reco_users = int(stdin.readline()) # num_reco_users 추천결과 만들어야할 유저 수
id=[] # 추천결과 만들어야 할 user id
for _ in range(num_reco_users) :
  id.append(int(stdin.readline()))

print(norate)
print(temp_table)




table={}


for row in temp_table:

    u_id, i_id, rating = row

    if i_id not in table:
        table[i_id] = {}
        table[i_id][u_id] = rating
    else:
        table[i_id][u_id] = rating
print("테이블")
print(table)




def sim(tbl, item_i, item_j):
    t=tbl[item_i].values()
    avr_i=sum(t) / len(t)       #item i의 평균 점수 = 뮤i
    t2 = tbl[item_j].values()
    avr_j = sum(t2) / len(t2)   #item j의 평균 점수 = 뮤j

    sum_ij=0 # 분자에 있는식
    r_iPow=0
    r_jPow=0



    for user in tbl[item_i]:  # item_i를 평가한 user가
        if user in tbl[item_j]:  # item_j역시 평가했을 경우
            #rx += (tbl[usr1][i] - avr_rx)
            #ry += (tbl[usr2][i] - avr_ry)
            sum_ij+=(tbl[item_i][user] - avr_i)*(tbl[item_j][user] - avr_j)      #r(u, i) - (item_i평균) X r(u, j) - (item_j평균)
            r_iPow += pow((tbl[item_i][user] - avr_i), 2)                      # (r(u, i) - (item_i평균))^2
            r_jPow += pow((tbl[item_j][user] - avr_j), 2)                      # (r(u, i) - (item_i평균))^2

    if r_iPow ==0 or r_jPow ==0 :
        return 0
    return sum_ij / (sqrt(r_iPow * r_jPow))
item_sim=[[float('-inf') for i in range(num_items)] for j in range(num_items)]      #2차원 행렬로 이루어진 item 유사도행렬
for item_i in table.keys() :
    for item_j in table.keys() :
        if item_i == item_j :
            continue
        else :
            item_sim[int(item_i)][int(item_j)] = sim(table, item_i, item_j)
print(item_sim)
sorted_item_sim=[[float('-inf') for i in range(num_items)] for j in range(num_items)]      # 유사도 값으로 정렬하고 index(item번호)를 value로 갖는 테이블
for idx in range(len(item_sim)) :
    sorted_item_sim[idx]=[i[0] for i in sorted(enumerate(item_sim[idx]), key=lambda x:x[1], reverse=True)][:num_sim_item_topk]   # 유사도 값으로 정렬하고 index(item번호)를 value로 갖는 테이블

print(sorted_item_sim)

#sim(table, 'user1', 'user2')
#if 2 in real_table['user1'].keys() :
''''''
print(table.keys())
def rating(s_item_sim, tbl, u1, i) :
    if i not in tbl.keys() :
        print(i, "가 없습닌다")
        return float('-inf')

    avr_i=sum(tbl[i].values()) / len(tbl[i].values())
    sum_w=0
    sum_rw=0
    for j in s_item_sim[int(i)] :
        if u1 in tbl[str(j)].keys() :
            w_ij=sim(tbl, i, str(j))
            sum_w+=w_ij
            avr_j=sum(tbl[str(j)].values()) / len(tbl[str(j)].values())
            print(tbl[str(j)])
            sum_rw+=(tbl[str(j)][u1]-avr_j) * w_ij

    if sum_w==0 :
        return avr_i
    else :
        return float(avr_i + sum_rw / sum_w)

rui=[[float('-inf') for i in range(num_items)] for j in range(num_users)]

for u in range(num_users) :
    for item in range(num_items) :
        rui[u][item]=rating(sorted_item_sim, table, str(u), str(item))

print("rui입니다")
print(rui)
for idx in range(len(rui)) :
    rui[idx]=[i[0] for i in sorted(enumerate(rui[idx]), key=lambda x:x[1], reverse=True)]
print("rui입니다")
print(rui)
result=[[] for _ in range(num_users)]
print(table.keys())
for user in range(len(rui)) :
    if not isRated(str(user)) :                 # 아무것도 평가하지 않은 유저한테는 그냥 예상 rating 순으로 추천바로넘겨줘
        for item in rui[user] :
            result[user].append(item)
    else:                                       # 그렇지않은 경우 이미 평가한 item은 추천해주면 안돼
        for item in rui[user] :
            if (str(item) in norate) :
                result[user].append(item)
            elif (str(user) in table[str(item)].keys())   :
                continue
            else :
                result[user].append(item)

print(result)
for uid in id :
    print(' '.join(list(map(str, result[uid][:num_rec_item_topn]))))

for i in table.keys() :
    print(sum(table[i].values()) / len(table[i].values()))




