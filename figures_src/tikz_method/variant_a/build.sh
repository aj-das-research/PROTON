#!/bin/bash
# usage: ./build.sh [name]   (default fig_method) -> name.pdf, name.png (330 dpi)
set -e
cd "$(dirname "$0")"
n=${1:-fig_method}
~/.local/bin/tectonic -X compile --keep-logs $n.tex > build_$n.log 2>&1 || { tail -30 build_$n.log; exit 1; }
grep -E "^(! |.*Overfull|.*Underfull)" $n.log || true
python3 -c "
import fitz,sys; d=fitz.open('$n.pdf'); r=d[0].rect; print('size cm: %.2f x %.2f'%(r.width/72*2.54, r.height/72*2.54)); d[0].get_pixmap(dpi=330).save('$n.png')"
