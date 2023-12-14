import math

# 배열을 입력 받는다.
arr = list(map(int,input().split()))

n = len(arr) # 데이터의 개수
h = math.ceil(math.log(n,2)) # 트리의 높이
seg = [0]*(2**(h+1)) # 세그먼트 트리

#입력된 배열을 최솟값을 저장한 세그먼트 트리로 저장하기
#n = 리프노드의 수
#2^k = n 일 때마다 높이가 k+1인 완전 이진 트리(perfect binary tree)가 된다.
#ceil(log2(n)+1) = 트리의 높이
#2^(ceil(log2(n)+1)) = 필요한 노드의 수

def init(tree, node, s, e):
    # 양 끝 값이 같아 더 이상 분리할 수 없는 구간인 경우
    if s == e:
        tree[node] = s

    # 양 끝 값이 달라 하위 구간을 나누어 비교해야 하는 경우
    else:
        m = (s + e) // 2  # 구간의 중간
        l = node * 2  # 왼쪽 구간을 다룰 트리의 인덱스
        r = node * 2 + 1  # 오른쪽 구간을 다룰 트리의 인덱스
        init(tree, l, s, m)  # 하위 구간 중 왼쪽 값 얻기
        init(tree, r, m + 1, e)  # 하위 구간 중 오른쪽 값 얻기

        # 하위 구간 값 비교
        if arr[tree[l]] <= arr[tree[r]]:
            tree[node] = tree[l]
        else:
            tree[node] = tree[r]


init(seg, 1, 0, n - 1)


# node = 현재 탐색 중인 노드
# s, e = 노드가 나타내는 구간의 시작과 끝
# l, r = 탐색하려는 구간

def query(tree, node, s, e, l, r):
    # 노드의 구간과 탐색 구간이 겹치지 않는 경우
    if l > e or r < s:
        return -1

    # 노드의 구간이 탐색 구간에 완전히 포함되는 경우
    if l <= s and e <= r:
        return tree[node]

    m = (s + e) // 2  # 노드 구간 분할 기준
    lq = query(tree, node*2, s, m, l, r)  # 왼쪽 하위 노드의 값 불러오기
    rq = query(tree, node*2+1, m+1, e, l, r)  # 오른쪽 하위 노드의 값 불러오기

    # 양쪽 하위 노드 쿼리의 결과를 현재 노드 쿼리 결과로 반환하기
    if lq == -1 or rq == -1:
        return max(lq, rq)
    elif arr[lq] <= arr[rq]:
        return lq
    else:
        return rq


while True:
    l, r = map(int,input().split())
    if l > r or r < 0 or l > n-1:
        print("잘못된 구간 입력")
    else:
        print(arr[query(seg, 1, 0, n - 1, l, r)])
