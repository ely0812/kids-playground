#!/usr/bin/env python3
"""미로 검증: 크기, 테두리, 유령집 구조, 모든 과자 도달 가능성, 고립 구역."""
import sys
from collections import deque

MAZE1 = [
    'WWWWWWWWWWWWWWWWWWW',
    'W........W........W',
    'WoWW.WWW.W.WWW.WWoW',
    'W.................W',
    'W.WW.W.WWWWW.W.WW.W',
    'W....W...W...W....W',
    'WWWW.WWW...WWW.WWWW',
    'WWWW.WWWW-WWWW.WWWW',
    'W....WW-----WW....W',
    '-....W.WWWWW.W....-',
    'WWWW.W.......W.WWWW',
    'W.WW.W.WWWWW.W.WW.W',
    'W....W...W...W....W',
    'W.WW.WWW.W.WWW.WW.W',
    'W.................W',
    'WoWW.WWW.W.WWW.WWoW',
    'W.WW.WWW.W.WWW.WW.W',
    'W.................W',
    'W.WW.WWWWWWWWW.WW.W',
    'W.................W',
    'WWWWWWWWWWWWWWWWWWW',
]

MAZE2 = [
    'WWWWWWWWWWWWWWWWWWW',
    'Wo.......W.......oW',
    'W.WW.WWW.W.WWW.WW.W',
    'W.W.............W.W',
    'W.W.WWW.W.W.WWW.W.W',
    'W......W...W......W',
    'WWWW.WWW...WWW.WWWW',
    'WWWW.WWWW-WWWW.WWWW',
    'W....WW-----WW....W',
    '-....W.WWWWW.W....-',
    'WWWW.W.......W.WWWW',
    'W....W.WWWWW.W....W',
    'W.WW.W...W...W.WW.W',
    'W..W.WWW.W.WWW.W..W',
    'W.................W',
    'W.WWW.WW.W.WW.WWW.W',
    'W...W.........W...W',
    'WWW.WWW.W.W.WWW.WWW',
    'WWW..WW.....WW..WWW',
    'Wo...............oW',
    'WWWWWWWWWWWWWWWWWWW',
]

MAZE3 = [
    'WWWWWWWWWWWWWWWWWWW',
    'W........W........W',
    'WoWWWWWW.W.WWWWWWoW',
    'W.W......W......W.W',
    'W.W.WW.WWWWW.WW.W.W',
    'W....W.......W....W',
    'WWWW.WWW...WWW.WWWW',
    'WWWW.WWWW-WWWW.WWWW',
    'W....WW-----WW....W',
    '-....W.WWWWW.W....-',
    'WWWW.W.......W.WWWW',
    'W.WW...........WW.W',
    'W.W.W.WWWWWWW.W.W.W',
    'W.W.W.........W.W.W',
    'W.W.WWW.....WWW.W.W',
    'W.W.WWW.W.W.WWW.W.W',
    'W...W.........W...W',
    'WWW.WWWW.W.WWWW.WWW',
    'WoW......W......WoW',
    'W.................W',
    'WWWWWWWWWWWWWWWWWWW',
]

MAZE4 = [
    'WWWWWWWWWWWWWWWWWWW',
    'W.....W.....W.....W',
    'Wo.WW.W.WWW.W.WW.oW',
    'W.W...W.....W...W.W',
    'WWW.W.WWW.WWW.W.WWW',
    'W.................W',
    'WWWW.WWW...WWW.WWWW',
    'WWWW.WWWW-WWWW.WWWW',
    'W....WW-----WW....W',
    '-....W.WWWWW.W....-',
    'WWWW.W.......W.WWWW',
    'W..W...........W..W',
    'W.WWW.WWWWWWW.WWW.W',
    'W.WWW....W....WWW.W',
    'W.WW.W.......W.WW.W',
    'W.WW.WWW.W.WWW.WW.W',
    'Wo...W...W...W...oW',
    'W.WWW.W.WWW.W.WWW.W',
    'W.................W',
    'W..WW....W....WW..W',
    'WWWWWWWWWWWWWWWWWWW',
]

COLS, ROWS = 19, 21
TUNNEL_ROW, DOOR, HOME_Y = 9, (9, 7), 8
PAC = (9, 14)

def walkable(m, c, r):
    if r == TUNNEL_ROW and (c < 0 or c >= COLS):
        return True
    if c < 0 or c >= COLS or r < 0 or r >= ROWS:
        return False
    return m[r][c] != 'W'

def check(name, m):
    errs, warns = [], []
    if len(m) != ROWS:
        errs.append(f'행 개수 {len(m)} != {ROWS}')
        return errs, warns
    for i, row in enumerate(m):
        if len(row) != COLS:
            errs.append(f'행 {i} 길이 {len(row)} != {COLS}: "{row}"')
        bad = set(row) - set('Wo.-')
        if bad:
            errs.append(f'행 {i} 잘못된 문자 {bad}')
    if errs:
        return errs, warns
    # 테두리
    for c in range(COLS):
        if m[0][c] != 'W': errs.append(f'위 테두리 뚫림 col {c}')
        if m[ROWS-1][c] != 'W': errs.append(f'아래 테두리 뚫림 col {c}')
    for r in range(ROWS):
        for c in (0, COLS-1):
            if r == TUNNEL_ROW:
                if m[r][c] != '-': errs.append(f'터널 행 {r} col {c}는 -여야 함')
            elif m[r][c] != 'W':
                errs.append(f'옆 테두리 뚫림 ({c},{r})')
    # 유령집 구조 (1번 미로와 동일해야 함)
    for r in (7, 8, 9, 10):
        if m[r] != MAZE1[r]:
            errs.append(f'행 {r}이 유령집 표준 구조와 다름: "{m[r]}"')
    if m[6][9] == 'W':
        errs.append('유령집 출구 (9,6) 막힘')
    # 팩맨 시작점
    if m[PAC[1]][PAC[0]] == 'W':
        errs.append(f'팩맨 시작점 {PAC} 막힘')
    # BFS 도달 가능성 (터널 워프 포함)
    start = PAC
    seen = {start}
    q = deque([start])
    while q:
        c, r = q.popleft()
        for dc, dr in ((1,0),(-1,0),(0,1),(0,-1)):
            nc, nr = c+dc, r+dr
            if nr == TUNNEL_ROW:
                if nc < 0: nc = COLS-1
                if nc >= COLS: nc = 0
            if walkable(m, nc, nr) and 0 <= nc < COLS and (nc, nr) not in seen:
                seen.add((nc, nr))
                q.append((nc, nr))
    pellets = 0
    for r in range(ROWS):
        for c in range(COLS):
            ch = m[r][c]
            if ch in '.o' and (c, r) not in seen:
                errs.append(f'도달 불가 과자 ({c},{r}) "{ch}"')
            if ch == 'o':
                pellets += 1
    if pellets != 4:
        errs.append(f'사탕 개수 {pellets} != 4')
    # 모든 통로 셀이 시작점과 연결되어 있는가 (고립 구역)
    for r in range(ROWS):
        for c in range(COLS):
            if m[r][c] != 'W' and (c, r) not in seen:
                errs.append(f'고립된 통로 ({c},{r})')
    # 막다른 길 개수 (경고만)
    dead = []
    for r in range(ROWS):
        for c in range(COLS):
            if m[r][c] == 'W':
                continue
            n = sum(walkable(m, c+dc, r+dr) for dc, dr in ((1,0),(-1,0),(0,1),(0,-1)))
            if n <= 1:
                dead.append((c, r))
    if dead:
        warns.append(f'막다른 길 {len(dead)}개: {dead}')
    return errs, warns

ok = True
for name, m in (('1 바다', MAZE1), ('2 숲', MAZE2), ('3 사탕', MAZE3), ('4 우주', MAZE4)):
    errs, warns = check(name, m)
    dots = sum(row.count('.') + row.count('o') for row in m)
    print(f'--- 미로 {name}: 과자 {dots}개')
    for e in errs:
        ok = False
        print(f'  ERROR: {e}')
    for w in warns:
        print(f'  warn: {w}')
    if not errs:
        print('  OK')
sys.exit(0 if ok else 1)
