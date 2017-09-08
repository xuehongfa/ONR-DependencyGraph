from joern.all import JoernSteps
import glob
import sys
import pickle
import os
j=JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data/')

# j.addStepsDir('Use this to inject utility traversals')

j.connectToDatabase()

FunctionName_query = """queryNodeIndex("type:File").out().filter{it.type == "Function"}.name"""
FunctionName = j.runGremlinQuery(FunctionName_query)
ori_duplicate = []

functionlist = []
import glob

for filename in glob.glob('/home/hongfa/workspace/DependencyGraph/lbm_or_src/*'):
    #print filename

    nameid = filename.split(".c")[0].split("/home/hongfa/workspace/DependencyGraph/lbm_or_src/")[1]
    print nameid


    command =' echo id:"'+str(nameid)+'" | joern-lookup -a name >>/home/hongfa/workspace/DependencyGraph/lbmx_or_src/list_or.txt'

    os.system(command)

with open('/home/hongfa/workspace/DependencyGraph/lbm_or_src/list_or.txt','r,' ) as f:
    names = f.readlines()
    for name in names:
        n = name.split(':')[1]
        with open('/home/hongfa/workspace/DependencyGraph/lbm_or_src/list.txt','a+') as f2:
            f2.write("fun:"+n)
