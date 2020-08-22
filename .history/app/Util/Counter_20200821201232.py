import os

cur = dir(os)
latest_ID = 1
for i in cur:
    latest_ID += 1
    print(latest_ID,i)

