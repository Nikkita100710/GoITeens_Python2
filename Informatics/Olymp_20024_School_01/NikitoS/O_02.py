k, w = map(int, input().split())
a1, b1, a2, b2, a3, b3 = map(int, input().split())
def can_choose_tents(a, b):
   return a <= w and b >= k
if can_choose_tents(a1, b1) or can_choose_tents(a2, b2) or can_choose_tents(a3, b3)\
        or can_choose_tents(a1 + a2, b1 + b2) or can_choose_tents(a1 + a3, b1 + b3)\
        or can_choose_tents(a2 + a3, b2 + b3) \
        or can_choose_tents(a1 + a2 + a3, b1 + b2 + b3):
   print("YES")
else: print("NO")