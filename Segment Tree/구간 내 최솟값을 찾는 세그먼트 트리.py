import sys
import math
input = sys.stdin.readline
array = list(map(int,input().split()))
n = len(array)

#입력된 배열을 최솟값을 저장한 세그먼트 트리로 저장하기
#n = 리프노드의 수
#2^k = n 일 때마다 높이가 k+1인 완전 이진 트리(perfect binary tree)가 된다.
#ceil(log2(n)+1) = 트리의 높이
#2^(ceil(log2(n)+1)) = 필요한 노드의 수

#트리 만들기
segment_tree = [sys.maxsize]*(2**(math.ceil(math.log(n,2)+1)))

def init(tree, node, start, end):
    if start == end:
        tree[node] = start
    else:
        mid = (start+end)//2
        left = node*2
        right = node*2+1
        init(tree, left, start, mid)
        init(tree, right, mid+1,end)
        if array[tree[left]]>array[tree[right]]:
            tree[node] = tree[right]
        else:
            tree[node] = tree[left]

init(segment_tree, 1, 0, n-1)

def query(tree, node, start, end, left, right):
    if left>end or right<start:
        return 0
    if left<=start and end<=right:
        return tree[node]
    mid = (start+end)//2
    leftq = query(tree, node*2, start, mid, left, right)
    rightq= query(tree, node*2+1, mid+1, end, left, right)
    if array[leftq] > array[rightq]:
        return rightq
    else:
        return leftq

while True:
    l, r = map(int,input().split())
    print(array[query(segment_tree, 1, 0, n-1, l, r)])
