from joern.all import JoernSteps
import glob

filename = '/home/hongfa/workspace/links-ACSAC/links-2.14/links_results'
print filename
count = 0
final = 0
with open(filename, 'r') as f:


    overheads=f.readlines()
    for overhead in overheads:
        overhead = overhead.split("CPU time = ")[1].split(" nanoseconds")[0];
        count = count + int(overhead);


final = count / 50
with open("/home/hongfa/workspace/links-ACSAC/links-2.14/overheads", 'a') as f:

    f.write(str(final)+'\n')