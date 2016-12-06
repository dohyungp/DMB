from math import sqrt

critics = {'Lisa Rose' : {'Lady in the Water' : 2.5, 'Snakes on a Plane' : 3.5, 'Just My Luck' : 3.0, 'Superman Returns' : 3.5, 'You, Me and Dupree' : 2.5, 'The Night Listener' : 3.0},
           'Gene Seymour' : {'Lady in the Water' : 3.0, 'Snakes on a Plane' : 3.5, 'Just My Luck' : 1.5, 'Superman Returns' : 5.0, 'The Night Listener' : 3.0, 'You, Me and Dupree' : 3.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree' : 2.5},
           'Mick LaSalle' : {'Lady in the Water' : 3.0, 'Snakes on a Plane' : 4.0, 'The Night Listener' : 4.5, 'Superman Returns' : 4.0, 'You, Me and Dupree' : 2.0},
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 1.0}}
#유클리디안 거리점수
#person1과 person2의 거리 기반 유사도 점수 리턴
def sim_distance(prefs, person1, person2) :
    #공통 항목 목록 추출
    si = {}
    for item in prefs[person1] :
        if item in prefs[person2] :
            si[item] = 1

    #공통평가 항목이 없는 경우 0리턴
    if len(si) == 0: return 0

    #모든 차이 값의 제곱을 더함.
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                            for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sum_of_squares)

#python 3.x version에서 Reload하려면 imp를 import 시킨 후 imp.reload 함수를 호출해야함.

#피어슨 상관점수(pearson correaltion score)

def sim_person(prefs, p1, p2):
    #같이 평가한 항목들의 목록을 구함
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    #요소들의 개수를 구함
    n = len(si)

    #공통요소가 없으면 0 리턴
    if n==0: return 0

    #모든 선호도를 합산함
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #제곱의 합을 계산
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    #곱의 합을 계산
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    #피어슨 점수 계산
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r

#선호도 딕셔너리에서 최적의 상대편 구함
#결과 개수와 유사도 함수 옵션사항
def topMatches (prefs, person, n=5, similarity=sim_person):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    #최고점이 상단에 오도록 정렬
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_person):
    totals = {}
    simSums = {}
    for other in prefs :
        if other == person: continue
        sim=similarity(prefs, person, other)

        if sim<=0: continue
        for item in prefs[other]:

            if item not in prefs[person] or prefs[person][item] == 0:
                #유사도 * 점수
                totals.setdefault(item, 0)
                totals[item]+=prefs[other][item]*sim
                #유사도 합계
                simSums.setdefault(item, 0)
                simSums[item]+=sim

    rankings = [ (total / simSums[item], item) for item, total in totals.items()]

            #정렬된 목록 리턴
    rankings.sort()
    rankings.reverse()
    return rankings
#직접 구현해보니, 실제 프로젝트 팀 구성 시 먼저 했던 선배의 조건에 맞춰보는 형태여야 할듯.
#pip 설치법 cmd에 python -m pip package명 install
#window cmd 명령어 : dir(sub dir 출력), cd(change directory).
#python 3.4는 default로 urllib를 설치하고 있음.
#python 3.X version에서는 beautifulsoup4를 설치해야함.

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n = 10) :
    #가장 유사한 항목들을 가진 딕셔너리 생성
    result = {}
    #선호도 행려을 뒤집어 항목중심행렬로 변환
    itemPrefs = transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        c+=1
        if c % 100 == 0: print("%d / %d" % (c, len(itemPrefs)))
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result

def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSims = {}

    for (item, rating) in userRatings.items() :
        for (similarity, item2) in itemMatch[item] :
            if item2 in userRatings: continue

            scores.setdefault(item2, 0)
            scores[item2]+=similarity*rating

            totalSims.setdefault(item2, 0)
            totalSims[item2] += similarity

    rankings = [(score / totalSims[item], item) for item, score in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings

#movielens Dataset

import codecs

def loadMovieLens(path = './data'):

    movies = {}
    for line in open(path + '/u.item', encoding='ISO-8859-1'):#뭔지는 모르겠지만, utf-8로 인코딩하면 안됨.
        (id, title) = line.split('|')[0:2]
        movies[id] = title

    prefs = {}
    for line in open(path + '/u.data', encoding= 'ISO-8859-1'):
        (user, movieid, rating, ts) = line.split('\t')
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

#함께 풀어보기 1번
