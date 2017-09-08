from joern.all import JoernSteps
import glob
count = 0
with open('/home/hongfa/workspace/SPEC2006/CFP2006/sphinx3/Source/checks.txt') as file:
    pairs=file.readlines()
    s = "total checks : "
    for p in pairs:
        if s in p:
            c = p.split("total checks : ")[1]
            count = count + int(c)

with open("/home/hongfa/workspace/SPEC2006/CFP2006/sphinx3/Source/totalchecks_after.txt", 'a') as f:

    f.write(str(count)+'\n')