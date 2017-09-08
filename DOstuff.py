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
ptrlist_file=open('/home/hongfa/workspace/links_test/ptrList','r')
ptrs=ptrlist_file.readlines()
ptrlist = []
for ptr in ptrs:


    ori_functionId = ptr.split("functionId:")[1].split("\n")[0]
        #print ori_functionId
    if ori_functionId not in ori_duplicate:

        ori_duplicate.append(ori_functionId)
        command =' echo "'+str(ori_functionId)+'" | joern-location | joern-code > /home/hongfa/workspace/DependencyGraph/links_or_src/'+ori_functionId+'.c '

        os.system(command)