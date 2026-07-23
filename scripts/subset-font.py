"""주아체 웹폰트 서브셋 생성 스크립트.

index.html의 문구를 수정해 새로운 한글 글자가 추가되면 이 스크립트를 다시 실행해
assets/fonts/jua.woff2 를 갱신한다. (없는 글자는 맑은 고딕으로 대체 표시됨)

사용법:
    pip install fonttools brotli
    # 주아체 원본: https://raw.githubusercontent.com/google/fonts/main/ofl/jua/Jua-Regular.ttf
    python scripts/subset-font.py Jua-Regular.ttf
"""
import sys
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

src = open('index.html', encoding='utf-8').read()
used = {ord(ch) for ch in src if 0xAC00 <= ord(ch) <= 0xD7A3}
unicodes = list(range(0x20, 0x7F)) + sorted(used) + list(range(0x3131, 0x3164)) \
    + [0x00B7, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x00D7]

font = TTFont(sys.argv[1] if len(sys.argv) > 1 else 'Jua-Regular.ttf')
opts = Options()
opts.flavor = 'woff2'
opts.drop_tables += ['DSIG']
s = Subsetter(opts)
s.populate(unicodes=unicodes)
s.subset(font)
font.save('assets/fonts/jua.woff2')
print('완료: assets/fonts/jua.woff2 (한글', len(used), '자 포함)')
