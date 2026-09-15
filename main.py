# Student ID:
import openpyxl
from datetime import time

# Needed to go back and add a format function to account for discrepancies in the WGUPS data files
def norm(address):
    address = str(address).lower().replace(".", "").replace(",", "").strip()
    address = address.split("#")[0].strip()
    rep = {"south": "s", "north": "n", "east": "e", "west": "w"}
    parts = [rep.get(p, p) for p in address.split()]
    return " ".join(parts)

# defined constants listed in the project outline
HASH = 100; CAP = 16; MPH = 18.0; PKG = "WGUPS Package File.xlsx"; DST = "WGUPS Distance Table.xlsx"

# Created hash table data structure with list and buckets
def ht_new(): return [[] for _ in range(HASH)]

def _h(id):
    return id % HASH

# record layout to set all package information
def ht_put(HASH_T, id, addr, deadline, city, zip, weight):
    bucket = HASH_T[_h(id)]
    record = [id, addr, deadline, city, zip, weight, "At Hub", None, None, None]
    # instituded for loop to satisfy task B requirements
    for i, r in enumerate(bucket):
        if r[0] == id:
            bucket[i] = record
            return
    bucket.append(record)

def ht_get(HASH_T, id):
    for r in HASH_T[_h(id)]:
        if r[0] == id:
            return r

# Time conversion
def tmin(time): return time.hour * 60 + time.minute + time.second / 60

def frommin(t_min):
    hour = int(t_min // 60); min = int(t_min % 60); sec = int(round((t_min - hour * 60 - min) * 60))
    if sec == 60: sec = 0; min += 1
    if min == 60: min = 0; hour += 1
    return time(hour, min, sec)

def slmin(miles): return miles / MPH * 60

def dlmin(deadline): return deadline.hour * 60 + deadline.minute if isinstance(deadline, time) else 1440

def parse(hhmm): a, b = hhmm.split(":"); return time(int(a), int(b), 0)

# Reads package information before insertion into the hash table
def load_pkgs():
    wrksht = openpyxl.load_workbook(PKG)[openpyxl.load_workbook(PKG).sheetnames[0]]
    out = []
    for row in range(9, wrksht.max_row + 1):  # started at row 9 because other information contained in previous rows was not real input for the project
        pid = wrksht.cell(row, 1).value
        if isinstance(pid, int):
            out.append((pid, wrksht.cell(row, 2).value, wrksht.cell(row, 6).value, wrksht.cell(row, 3).value, wrksht.cell(row, 5).value, wrksht.cell(row, 7).value))
    return out

# Created distance conversion for greedy algorithm determination of best choice
def load_dst():
    wrkbk = openpyxl.load_workbook(DST); wrksht = wrkbk[wrkbk.sheetnames[0]]
    location = []
    for row in range(9, wrksht.max_row + 1):
        value = wrksht.cell(row, 2).value
        if value:
            address = str(value).split("\n")[0].strip()
            location.append("4001 South 700 East" if address.upper() == "HUB" else address)
    loctions = len(location); dist = [[0.0] * loctions for _ in range(loctions)]
    for i in range(loctions):
        matrix = 9 + i
        for j in range(loctions):
            value = wrksht.cell(matrix, 3 + j).value
            if value is not None:
                dist[i][j] = float(value); dist[j][i] = float(value)
    idx = {norm(location[i]): i for i in range(loctions)}; return idx, idx[norm("4001 South 700 East")], dist

# Created starting state for trucks and packages
def route(HASH_T, ids, start, idx, hub, dist, earliest=None):
    earliest = earliest or {}; cur = hub; tm = tmin(start); miles = 0.0; rem = set(ids); delivered = {}
    # Main while loop for determining earliest availability "Nearest Neighbor Greedy Algorithm"
    while rem:
        av = [p for p in rem if tm >= earliest.get(p, -1)]
        if not av: tm = min(earliest[p] for p in rem); av = [p for p in rem if tm >= earliest.get(p, -1)]
        def sc(p):
            r = ht_get(HASH_T, p); return (dlmin(r[2]), dist[cur][idx[norm(r[1])]])
        p = min(av, key=sc); nxt = idx[norm(ht_get(HASH_T, p)[1])]; dd = dist[cur][nxt]
        miles += dd; tm += slmin(dd); delivered[p] = tm; cur = nxt; rem.remove(p)
    miles += dist[cur][hub]; tm += slmin(dist[cur][hub]); return miles, delivered, tm

# Determine package Status
def stat(dep, deliv, qt):
    qt = tmin(qt); dt = tmin(dep)
    if qt < dt: return "At Hub"
    if deliv is None or qt < tmin(deliv): return "En Route"
    return "Delivered"

# Main Program!!!
def main():
    pkgs = load_pkgs(); idx, hub, dist = load_dst(); HASH_T = ht_new()
    for pid, addr, dl, city, z, w in pkgs: ht_put(HASH_T, pid, addr, dl, city, z, w)
#Added necessary addition of package 30 to package group to ensure ontime delivery
    delayed = {6, 25, 28, 32}; t2only = {3, 18, 36, 38}; grouped = {13, 14, 15, 16, 19, 20, 30}; wrong = {9}
    allids = set(pid for pid, _, _, _, _, _ in pkgs)
    delayed_arrival = time(9, 5)

    t1 = set(grouped)
    cand = sorted([p for p in allids if p not in t1 | delayed | t2only | wrong], key=lambda p: dlmin(ht_get(HASH_T, p)[2]))
    wrong_fix_time = time(10, 20)
    wrong_fix_addr = "410 S State St"
    wrong_start_addr = None

    t2 = set(delayed) | set(t2only)
    cand2 = sorted([p for p in allids if p not in t1 | t2 | wrong], key=lambda p: dlmin(ht_get(HASH_T, p)[2]))
    for p in cand2:
        if len(t2) >= CAP: break
        t2.add(p)

    # Set departure times for trucks
    t3 = allids - t1 - t2
    dep1, dep2 = time(8, 0), time(9, 5)
    for p in t1: r = ht_get(HASH_T, p); r[8] = 1; r[9] = dep1
    for p in t2: r = ht_get(HASH_T, p); r[8] = 2; r[9] = dep2

    m1, d1, e1 = route(HASH_T, t1, dep1, idx, hub, dist); m2, d2, e2 = route(HASH_T, t2, dep2, idx, hub, dist)
    dep3 = frommin(max(min(e1, e2), tmin(time(10, 20))))
    for p in t3: r = ht_get(HASH_T, p); r[8] = 3; r[9] = dep3
    if 9 in t3:
        wrong_start_addr = ht_get(HASH_T, 9)[1]
        ht_get(HASH_T, 9)[1] = wrong_fix_addr
        earliest = {9: tmin(wrong_fix_time)}
    else:
        earliest = {}
    m3, d3, _ = route(HASH_T, t3, dep3, idx, hub, dist, earliest)

    for p, tm in {**d1, **d2, **d3}.items():
        r = ht_get(HASH_T, p); r[6] = "Delivered"; r[7] = frommin(tm)
    total = m1 + m2 + m3
    print(f"\nTotal mileage: {total:.2f}\n")

    # Satisfies requirement D with user interface.
    while True:
        print("1) Package@time  2) Trucks@time  3) Mileage  4) Exit")
        c = input(">").strip()
        if c == "1":
            pid = int(input("ID: ")); qt = parse(input("HH:MM: "))
            r = ht_get(HASH_T, pid)
            print(f"Pkg {pid:2d} {s:9s} Del:{dt} {r[1]}")

            dt = r[7] if s == "Delivered" else "-"

            print(f"Pkg {pid} | Truck {r[8]} | {s} | Delivered: {dt}")
            print(f"Address: {addr_show}")
            print(f"Deadline: {r[2]} | City: {r[3]} | Zip: {r[4]} | Weight: {r[5]}\n")
        elif c == "2":
            qt = parse(input("HH:MM: "))
            for tid in (1, 2, 3):
                print(f"\nTruck {tid} @ {qt}")
                for pid in range(1, 41):
                    r = ht_get(HASH_T, pid)
                    if r[8] == tid:
                        s = stat(r[9], r[7], qt); dt = r[7] if s == "Delivered" else "-"
                        # I had to go back and make additions to this section. Packages were showing "at Hub" not "Delayed".
                        addr_show = r[1]
                        if pid == 9 and wrong_start_addr is not None and qt < wrong_fix_time:
                            addr_show = wrong_start_addr
                        if pid in delayed and qt < delayed_arrival:
                            s = "DELAYED"
                            dt = "-"
                        print(f"Pkg {pid:2d} {s:9s} Del:{dt} DL:{r[2]} {addr_show}")
            print()
        elif c == "3":
            print(f"Total mileage: {total:.2f}\n")
        elif c == "4":
            break

if __name__ == "__main__":
    main()