N = int(input())
dot = [list(map(int(input().split()))) for _ in range(N)]
dot.sort()

# 세 점이 주어졌을 때 꺾이는 방향을 판단
def clock(a,b,c):
    k = (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-a[0])
    if k < 0:
        return

def graham(dots):
    if len(dots) < 3:
        return 0

    # 기준점을 두고 반시계방향, 시계방향으로 돌며 양쪽의 볼록껍질을 찾는다.
    # 파이썬은 기하 연산이 어렵기 때문에 이 방법을 사용함
    ccw = []
    cw = []

    # 기준점 정하기
    # 점들의 배열을 정렬한 시점에서 0번째 점이 사실 기준점이 되어야 한다.
    # 하지만 원리를 기억하기 위해 일단 만들어 봄.
    left = 0
    for i in range(1,len(dots)):
        if dots[left][0] > dots[i][0]:
            left = i

        # 만약 x좌표가 같다면 y좌표가 더 작은 것으로 기준으로 정하기
        elif dots[left][0] == dots[i][0] and dots[left][1] > dots[i][1]:
            left = i

    for k in dots:
        while len(ccw) >= 2 and cc