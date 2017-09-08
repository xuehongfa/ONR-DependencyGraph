from joern.all import JoernSteps
import glob

for filename in glob.glob('/home/hongfa/workspace/Deckard-parallel1.3/scripts/clonedetect/clusters/*'):
    print filename
    count = 0
    count2 = 0
    with open(filename, 'r') as f:


        pairs=f.readlines()
        for p in pairs:
            count2 = count2 +1
            if p == "\n":
                count = count +1

        count2 = count2 - count
    with open("/home/hongfa/workspace/Deckard-parallel1.3/scripts/clonedetect/clusters/CountPairs.txt", 'a') as f:

        f.write(filename +" "+str(count)+" "+str(count2)+'\n')