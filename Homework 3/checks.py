#!/usr/bin/env python3
import sys
import csv
import math

MISSING = '?'

# ── Stats Helpers ────────────────────────────────────────────────
def mean(xs):
    if not xs: return 0.0
    return sum(xs) / len(xs)

def sd(xs):
    if len(xs) < 1: return 0.0
    mu = mean(xs)
    return math.sqrt(sum((x - mu)**2 for x in xs) / len(xs))

def pearson(xs, ys):
    if len(xs) != len(ys) or len(xs) < 1: return 0.0
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = sum((x - mx)**2 for x in xs)
    dy  = sum((y - my)**2 for y in ys)
    if dx == 0 or dy == 0:
        return 0
    return num / math.sqrt(dx * dy)

def print_res(found_set):
    """Format and print results: length followed by sorted items."""
    res = list(found_set)
    # Ensure numerical sorting for row numbers, alphabetical for columns
    if all(isinstance(x, int) for x in res):
        res.sort()
    else:
        res.sort()
    print(len(res))
    for x in res:
        print(x)

# ── Feature-Level Checks (A-E) ───────────────────────────────────

def check_A(rows):
    """A: Identical features — columns with the same values for every row."""
    headers = list(rows[0].keys())
    cols = {h: [r[h] for r in rows] for h in headers}
    found = set()
    for i in range(len(headers)):
        for j in range(i + 1, len(headers)):
            h1, h2 = headers[i], headers[j]
            if cols[h1] == cols[h2]:
                found.update([h1, h2])
    print_res(found)

def check_B(rows):
    """B: Correlated features — pairs of numeric features with Pearson |r| > 0.95."""
    headers = [h for h in rows[0].keys() if h != 'class!']
    found = set()
    for i in range(len(headers)):
        for j in range(i + 1, len(headers)):
            h1, h2 = headers[i], headers[j]
            xs, ys = [], []
            for r in rows:
                if r[h1] != MISSING and r[h2] != MISSING:
                    xs.append(float(r[h1]))
                    ys.append(float(r[h2]))
            if xs and abs(pearson(xs, ys)) > 0.95:
                found.update([h1, h2])
    print_res(found)

def check_C(rows):
    """C: Outlier features — columns with >=1 value > 3σ from mean."""
    headers = [h for h in rows[0].keys() if h != 'class!']
    found = set()
    for h in headers:
        vals = [float(r[h]) for r in rows if r[h] != MISSING]
        if not vals: continue
        mu, sigma = mean(vals), sd(vals)
        if sigma == 0: continue # Cannot have outliers if variance is 0
        for r in rows:
            if r[h] != MISSING and abs(float(r[h]) - mu) > 3 * sigma:
                found.add(h)
                break
    print_res(found)

def check_D(rows):
    """D: Features with conflicting values — referential integrity violations."""
    found = set()
    for r in rows:
        needed = ['HEIGHT','LENGHT','AREA','ECCEN','P_BLACK','P_AND','BLACKPIX','BLACKAND']
        if any(r[c] == MISSING for c in needed):
            continue
            
        h, l, a, e = float(r['HEIGHT']), float(r['LENGHT']), float(r['AREA']), float(r['ECCEN'])
        pb, pa = float(r['P_BLACK']), float(r['P_AND'])
        bpx, ba = float(r['BLACKPIX']), float(r['BLACKAND'])

        if a != h * l: 
            found.update(['AREA', 'HEIGHT', 'LENGHT'])
        if h > 0 and abs(e - l/h) > 0.01: 
            found.update(['ECCEN', 'LENGHT', 'HEIGHT'])
        if a > 0 and abs(pb - bpx/a) > 0.001: 
            found.update(['P_BLACK', 'BLACKPIX', 'AREA'])
        if a > 0 and abs(pa - ba/a) > 0.001: 
            found.update(['P_AND', 'BLACKAND', 'AREA'])
    print_res(found)

def check_E(rows):
    """E: Features with implausible values."""
    found = set()
    gt_zero = ['HEIGHT', 'LENGHT', 'WIDTH', 'AREA', 'BLACKPIX', 'BLACKAND', 'WB_TRANS', 'MEAN_TR', 'ECCEN']
    prop = ['P_BLACK', 'P_AND']
    
    for r in rows:
        for h in gt_zero:
            if r[h] != MISSING and float(r[h]) <= 0: 
                found.add(h)
        for h in prop:
            if r[h] != MISSING and not (0 <= float(r[h]) <= 1): 
                found.add(h)
        if r['class!'] != MISSING and str(r['class!']) not in ['1','2','3','4','5']: 
            found.add('class!')
    print_res(found)

# ── Case-Level Checks (G-K) ──────────────────────────────────────

def check_G(rows):
    """G: Outlier cases — rows with >=1 value > 3σ from column mean."""
    headers = [h for h in rows[0].keys() if h != 'class!']
    stats = {}
    for h in headers:
        vals = [float(r[h]) for r in rows if r[h] != MISSING]
        stats[h] = (mean(vals), sd(vals))
        
    found = set()
    for i, r in enumerate(rows):
        for h in headers:
            if r[h] != MISSING:
                mu, sigma = stats[h]
                if sigma > 0 and abs(float(r[h]) - mu) > 3 * sigma:
                    found.add(i + 2) # i+2 maps exactly to file line number
                    break
    print_res(found)

def check_H(rows):
    """H: Inconsistent cases — rows identical on features but different class!"""
    headers = [h for h in rows[0].keys() if h != 'class!']
    groups = {}
    for i, r in enumerate(rows):
        feats = tuple(r[h] for h in headers)
        if feats not in groups: 
            groups[feats] = []
        groups[feats].append((i + 2, r['class!']))
        
    found = set()
    for feats, items in groups.items():
        classes = set(c for idx, c in items)
        if len(classes) > 1:
            for idx, c in items: 
                found.add(idx)
    print_res(found)

def check_I(rows):
    """I: Class-conditional outlier cases."""
    headers = [h for h in rows[0].keys() if h != 'class!']
    valid_classes = set(r['class!'] for r in rows if r['class!'] != MISSING and r['class!'] in ['1','2','3','4','5'])
    
    found = set()
    for c in valid_classes:
        c_rows = [(i + 2, r) for i, r in enumerate(rows) if r['class!'] == c]
        stats = {}
        for h in headers:
            vals = [float(r[h]) for idx, r in c_rows if r[h] != MISSING]
            stats[h] = (mean(vals), sd(vals))
            
        for idx, r in c_rows:
            for h in headers:
                if r[h] != MISSING:
                    mu, sigma = stats[h]
                    if sigma > 0 and abs(float(r[h]) - mu) > 3 * sigma:
                        found.add(idx)
                        break
    print_res(found)

def check_J(rows):
    """J: Cases with conflicting values (Referential Integrity)."""
    found = set()
    for i, r in enumerate(rows):
        needed = ['HEIGHT','LENGHT','AREA','ECCEN','P_BLACK','P_AND','BLACKPIX','BLACKAND']
        if any(r[c] == MISSING for c in needed): 
            continue
        
        h, l, a, e = float(r['HEIGHT']), float(r['LENGHT']), float(r['AREA']), float(r['ECCEN'])
        pb, pa = float(r['P_BLACK']), float(r['P_AND'])
        bpx, ba = float(r['BLACKPIX']), float(r['BLACKAND'])
        
        if (a != h * l or
            (h > 0 and abs(e - l/h) > 0.01) or
            (a > 0 and abs(pb - bpx/a) > 0.001) or
            (a > 0 and abs(pa - ba/a) > 0.001)):
            found.add(i + 2)
    print_res(found)

def check_K(rows):
    """K: Cases with implausible values."""
    found = set()
    gt_zero = ['HEIGHT', 'LENGHT', 'WIDTH', 'AREA', 'BLACKPIX', 'BLACKAND', 'WB_TRANS', 'MEAN_TR', 'ECCEN']
    prop = ['P_BLACK', 'P_AND']
    
    for i, r in enumerate(rows):
        bad = False
        for h in gt_zero:
            if r[h] != MISSING and float(r[h]) <= 0: bad = True
        for h in prop:
            if r[h] != MISSING and not (0 <= float(r[h]) <= 1): bad = True
        if r['class!'] != MISSING and str(r['class!']) not in ['1','2','3','4','5']: bad = True
        
        if bad: 
            found.add(i + 2)
    print_res(found)

# ── Dispatcher ───────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    action = sys.argv[1]
    path = sys.argv[2]
    
    with open(path, 'r') as f:
        data = list(csv.DictReader(f))
        
    dispatch = {
        'A': check_A, 'B': check_B, 'C': check_C, 'D': check_D, 'E': check_E,
        'G': check_G, 'H': check_H, 'I': check_I, 'J': check_J, 'K': check_K
    }
    
    if action in dispatch:
        dispatch[action](data)