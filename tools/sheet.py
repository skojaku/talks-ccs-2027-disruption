import sys
from PIL import Image, ImageDraw
N='/private/tmp/claude-501/-Users-skojaku-Documents-projects-talks-ccs-2027-disruption/11d07a1c-f5b8-4d5b-bf44-db2061f42b38/scratchpad'
ids=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[1]
cols=int(sys.argv[3]) if len(sys.argv)>3 else 3
W,H=(420,236) if cols<=3 else (320,180)
rows=(len(ids)+cols-1)//cols
sh=Image.new('RGB',(cols*(W+6),rows*(H+16)),(150,150,150)); d=ImageDraw.Draw(sh)
for i,n in enumerate(ids):
    im=Image.open(f'review/slide.{n:03d}.png').convert('RGB').resize((W,H))
    x=(i%cols)*(W+6); y=(i//cols)*(H+16); sh.paste(im,(x,y+14)); d.text((x+3,y+1),f's{n}',fill=(0,0,0))
sh.save(f'{N}/{out}.png')
