# 2x (660 dpi) inspection crops of every region; coordinates in cm from the page's top-left corner
import fitz, os
D = os.path.dirname(os.path.abspath(__file__)); cm = 72 / 2.54
p = fitz.open(os.path.join(D, 'fig_method.pdf'))[0]
R = {'stream': (0, 0.2, 2.3, 2.5), 'vlm_glyphs': (2.0, 0.1, 4.4, 2.6), 'bank': (4.0, 0.9, 8.4, 2.8),
     'fusion': (7.9, 0.4, 12.3, 2.4), 'ood_key': (9.4, 0, 12.3, 1.8), 'zoom': (3.5, 2.2, 8.6, 3.6),
     'titles': (1.9, 2.8, 10.1, 3.8), 'panels': (1.9, 3.6, 10.1, 5.4), 'verdict_legend': (1.9, 5.0, 10.1, 6.1)}
for k, (x0, y0, x1, y1) in R.items():
    p.get_pixmap(dpi=660, clip=fitz.Rect(x0 * cm, y0 * cm, x1 * cm, y1 * cm)).save(os.path.join(D, 'crops', f'{k}.png'))
