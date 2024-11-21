a, b = map(int, input().split())
finish = 0
for b_range in range(1, b+1):
    a_for = b_range*a #a_for = скільки монет у текуший день
    if a_for % b == 0:
        finish += 1
print(finish)
