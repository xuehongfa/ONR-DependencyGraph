from joern.all import JoernSteps
import glob

j=JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data/')

j.connectToDatabase()
check_list = ["ForStatement","IfStatement","WhileStatement","SwitchStatement"]

check_list2= ["ForStatement","WhileStatement"]


def nor_stat_selection(S,f,i):
    query_sta = """g.v("""+str(S)+""").code"""
    query_id = """g.v("""+str(S)+""").astNodes().filter{it.type == "Identifier" }.code"""

    ids = j.runGremlinQuery(query_id)
    #print ids
    sta = j.runGremlinQuery(query_sta)
    if (i in ids) and (ptr in ids):
        #print "check nor"
        f.write(sta+";"+"\n")
        return 1
    else:
        return 0


ptr = ""
for filename in glob.glob('*.txt'):
    #print filename
    with open(filename, 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    #print my_list
    ptr = filename.split("_")[1].split('.txt')[0]
    newfilename = filename.split('.txt')[0]+'.c'
    S_file=open('/home/hongfa/workspace/DependencyGraph/sphinx3_src/'+newfilename,'w+')

    CompoundStatement_query = """g.v("""+filename.split("_")[0]+""").out().filter{it.type == "FunctionDef"}.ithChildren("0").out().id"""
    CompoundStatements =j.runGremlinQuery(CompoundStatement_query)
    #print CompoundStatements
    duplicate = []
    duplicate2 = []
    klee_var = ''
    for S in CompoundStatements:
        query_sta = """g.v("""+str(S)+""").code"""
        query_sta_type = """g.v("""+str(S)+""").type"""
        query_sta_id = """g.v("""+str(S)+""").id"""
        query_id = """g.v("""+str(S)+""").astNodes().filter{it.type == "Identifier" }.code"""
        ids = j.runGremlinQuery(query_id)
        sta = j.runGremlinQuery(query_sta)
        sta_type = j.runGremlinQuery(query_sta_type)
        sta_id=j.runGremlinQuery(query_sta_id)
        lable = 0

        for i in my_list:
            if i in ids:
                lable = 1
                if klee_var not in duplicate2:
                    klee_var = i
                    duplicate2.append(klee_var)

        if lable == 1:
            if sta_type not in check_list:
                if (str(sta_id)) in duplicate:
                    continue
                S_file.write(sta+";"+"\n")
                klee = 'klee_make_symbolic(&'+klee_var+', sizeof('+klee_var+'), "'+klee_var+'");'
                S_file.write(klee+"\n")
                duplicate.append(str(sta_id))

            if sta_type in check_list2:
                if (str(sta_id)) in duplicate:
                    continue
                S_file.write(sta+"\n")
                S_file.write("{"+"\n")
                duplicate.append(str(sta_id))
                CompoundStatement_query = """g.v("""+str(S)+""").astNodes().filter{it.type == "Condition"}.id"""
                CompoundStatements_id = j.runGremlinQuery(CompoundStatement_query)

                for compound in CompoundStatements_id:
                        #print compound
                    query_parent = """g.v("""+str(compound)+""").parents().id"""
                    query_parent_type = """g.v("""+str(compound)+""").parents().type"""
                    p_id = j.runGremlinQuery(query_parent)
                    p_type = j.runGremlinQuery(query_parent_type)
                    #print p_type[0]
                    if p_id[0] == sta_id:
                            #print "yes"
                        query_compound = """g.v("""+str(sta_id)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                        compound_out = j.runGremlinQuery(query_compound)
                        for c in compound_out:
                                #print c

                            type_query = """g.v("""+str(c)+""").type"""
                            type = j.runGremlinQuery(type_query)
                            if type not in check_list:

                                for i in my_list:
                                    if (str(c)) in duplicate:
                                        break
                                    if nor_stat_selection(c,S_file,i) == 1:
                                        duplicate.append(str(c))

                    elif p_type[0] in check_list2:
                        query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                        ids = j.runGremlinQuery(query_id)
                        flag = 0
                        for i in my_list:
                            if (i in ids) and (ptr in ids):
                                flag = 1#print p_id
                        if flag == 1:
                            query_compound = """g.v("""+str(p_id[0])+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                            query_sta = """g.v("""+str(p_id[0])+""").code"""
                            sta= j.runGremlinQuery(query_sta)
                            compound_out = j.runGremlinQuery(query_compound)
                            if (str(p_id[0])) in duplicate:
                                continue
                            S_file.write(sta+"\n")
                            S_file.write("{"+"\n")
                            duplicate.append(str(p_id[0]))
                            for c in compound_out:
                                #print c
                                type_query = """g.v("""+str(c)+""").type"""
                                type = j.runGremlinQuery(type_query)
                                if type not in check_list:
                                    for i in my_list:
                                        if (str(c)) in duplicate:
                                            break
                                        if nor_stat_selection(c,S_file,i) == 1:
                                            duplicate.append(str(c))
                            S_file.write("}"+"\n")
                    elif p_type[0] == "IfStatement":
                        query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                        ids = j.runGremlinQuery(query_id)

                        flag = 0
                        for i in my_list:
                            if (i in ids) and (ptr in ids):
                                flag = 1#print p_id
                        if flag == 1:
                            query_compound = """g.v("""+str(p_id[0])+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                            query_sta = """g.v("""+str(p_id[0])+""").code"""
                            sta= j.runGremlinQuery(query_sta)
                            compound_out = j.runGremlinQuery(query_compound)
                            if (str(p_id[0])) in duplicate:
                                continue
                            S_file.write(sta+"\n")
                            S_file.write("{"+"\n")
                            duplicate.append(str(p_id[0]))
                            query_children_type = """g.v("""+str(p_id[0])+""").ithChildren("1").type"""
                            query_children_id = """g.v("""+str(p_id[0])+""").ithChildren("1").id"""

                            children_type = j.runGremlinQuery(query_children_type)
                            children_id = j.runGremlinQuery(query_children_id)

                            if children_type == "CompoundStatement":
                                query_compound = """g.v("""+str(children_id)+""").out().id"""
                                compound_out = j.runGremlinQuery(query_compound)

                                for c in compound_out:
                                    #print c
                                    type_query = """g.v("""+str(c)+""").type"""
                                    type = j.runGremlinQuery(type_query)
                                    if type not in check_list:
                                        for i in my_list:
                                            if (str(c)) in duplicate:
                                                break
                                            if nor_stat_selection(c,S_file,i) == 1:
                                                duplicate.append(str(c))
                            else:
                                #print children_id
                                if children_type not in check_list:

                                    for i in my_list:
                                        if (str(children_id[0])) in duplicate:
                                            break
                                        if nor_stat_selection(children_id[0],S_file,i) == 1:
                                            #print children_id
                                            duplicate.append(str(children_id[0]))
                            S_file.write("}"+"\n")


                S_file.write("}"+"\n")


            if sta_type == "IfStatement":
                if_flag = 0
                for i in my_list:
                    if i in ids and ptr in ids:
                        if_flag = 1
                if if_flag == 1:
                    if (str(sta_id)) in duplicate:
                        continue
                    S_file.write(sta+"\n")
                    S_file.write("{"+"\n")
                    duplicate.append(str(sta_id))
                    CompoundStatement_query = """g.v("""+str(S)+""").astNodes().filter{it.type == "Condition"}.id"""
                    CompoundStatements_id = j.runGremlinQuery(CompoundStatement_query)
                    #print CompoundStatements_id
                    check_else_query = """g.v("""+str(S)+""").out().filter{it.type == "ElseStatement"}.id"""
                    check_else = j.runGremlinQuery(check_else_query)

                    for compound in CompoundStatements_id:
                            #print compound
                        query_parent = """g.v("""+str(compound)+""").parents().id"""
                        query_parent_type = """g.v("""+str(compound)+""").parents().type"""
                        p_id = j.runGremlinQuery(query_parent)
                        p_type = j.runGremlinQuery(query_parent_type)
                        #print p_type[0]
                        if p_id[0] == sta_id:
                            continue
                        #     print str(p_id[0]) + " "+str(compound)
                        #     query_compound = """g.v("""+str(sta_id)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                        #     compound_out = j.runGremlinQuery(query_compound)
                        #     for c in compound_out:
                        #             #print c
                        #
                        #         type_query = """g.v("""+str(c)+""").type"""
                        #         type = j.runGremlinQuery(type_query)
                        #         if type not in check_list:
                        #
                        #             for i in my_list:
                        #                 if (str(c)) in duplicate:
                        #                     break
                        #                 if nor_stat_selection(c,S_file,i) == 1:
                        #                     duplicate.append(str(c))

                        if p_type[0] in check_list2:
                            query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                            ids = j.runGremlinQuery(query_id)
                            flag = 0
                            print str(p_id[0]) + " "+str(compound)
                            for i in my_list:
                                if (i in ids) and (ptr in ids):
                                    flag = 1#print p_id
                            if flag == 1:
                                query_compound = """g.v("""+str(p_id[0])+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                                query_sta = """g.v("""+str(p_id[0])+""").code"""
                                query_sta_id = """g.v("""+str(p_id[0])+""").id"""
                                query_else_parents = """g.v("""+str(p_id[0])+""").parents().parents().id"""
                                else_parents = j.runGremlinQuery(query_else_parents)
                                sta= j.runGremlinQuery(query_sta)
                                compound_out = j.runGremlinQuery(query_compound)
                                sta_id = j.runGremlinQuery(query_sta_id)
                                #print sta_id
                                #print else_parents[0]
                                if (str(sta_id)) in duplicate:
                                    continue
                                if len(check_else) != 0:
                                    if check_else[0] == else_parents[0]:
                                    #print else_parents[0]
                                        continue
                                S_file.write(sta+"\n")
                                S_file.write("{"+"\n")
                                duplicate.append(str(sta_id))
                                for c in compound_out:
                                    #print c
                                    type_query = """g.v("""+str(c)+""").type"""
                                    type = j.runGremlinQuery(type_query)
                                    if type not in check_list:
                                        for i in my_list:
                                            if (str(c)) in duplicate:
                                                break
                                            if nor_stat_selection(c,S_file,i) == 1:
                                                duplicate.append(str(c))
                                    elif type in check_list2:
                                        query_id = """g.v("""+str(c)+""").astNodes().filter{it.type == "Identifier" }.code"""
                                        ids = j.runGremlinQuery(query_id)
                                        flag = 0
                                        for i in my_list:
                                            if (i in ids) and (ptr in ids):
                                                flag = 1#print p_id
                                        if flag == 1:
                                            query_compound = """g.v("""+str(c)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                                            query_sta = """g.v("""+str(c)+""").code"""
                                            query_sta_id = """g.v("""+str(c)+""").id"""
                                            query_else_parents = """g.v("""+str(c)+""").parents().parents().parents().parents().id"""
                                            else_parents = j.runGremlinQuery(query_else_parents)
                                            sta= j.runGremlinQuery(query_sta)
                                            compound_out = j.runGremlinQuery(query_compound)
                                            sta_id = j.runGremlinQuery(query_sta_id)
                                            #print else_parents[0]
                                            if (str(sta_id)) in duplicate:
                                                continue
                                            if len(check_else) != 0:
                                                if check_else[0] == else_parents[0]:
                                                #print else_parents[0]

                                                    continue
                                            S_file.write(sta+"\n")
                                            S_file.write("{"+"\n")
                                            duplicate.append(str(sta_id))
                                            for c in compound_out:
                                                #print c
                                                type_query = """g.v("""+str(c)+""").type"""
                                                type = j.runGremlinQuery(type_query)
                                                if type not in check_list:
                                                    for i in my_list:
                                                        if (str(c)) in duplicate:
                                                            break
                                                        if nor_stat_selection(c,S_file,i) == 1:
                                                            duplicate.append(str(c))
                                            S_file.write("}"+"\n")
                                #print sta_id
                                S_file.write("}"+"\n")

                        elif p_type[0] == "IfStatement":
                            query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                            ids = j.runGremlinQuery(query_id)
                            query_sta = """g.v("""+str(p_id[0])+""").code"""
                            sta = j.runGremlinQuery(query_sta)
                            query_else_parents = """g.v("""+str(p_id[0])+""").parents().parents().id"""
                            else_parents = j.runGremlinQuery(query_else_parents)
                            flag = 0
                            for i in my_list:
                                if (i in ids) and (ptr in ids):
                                    flag = 1#print p_id
                            if flag == 1:
                                if (str(p_id[0])) in duplicate:
                                    continue
                                if len(check_else) != 0:
                                    if check_else[0] == else_parents[0]:
                                        continue
                                S_file.write(sta+"\n")
                                S_file.write("{"+"\n")
                                duplicate.append(str(p_id[0]))
                                query_children_type = """g.v("""+str(p_id[0])+""").ithChildren("1").type"""
                                query_children_id = """g.v("""+str(p_id[0])+""").ithChildren("1").id"""

                                children_type = j.runGremlinQuery(query_children_type)
                                children_id = j.runGremlinQuery(query_children_id)

                                if children_type[0] == "CompoundStatement":
                                    query_compound = """g.v("""+str(children_id[0])+""").out().id"""
                                    compound_out = j.runGremlinQuery(query_compound)

                                    for c in compound_out:
                                        #print str(c) +"SSS"
                                        type_query = """g.v("""+str(c)+""").type"""
                                        type = j.runGremlinQuery(type_query)
                                        #print type
                                        if type not in check_list:
                                            for i in my_list:
                                                if (str(c)) in duplicate:
                                                    break
                                                if nor_stat_selection(c,S_file,i) == 1:
                                                    duplicate.append(str(c))
                                        elif type in check_list2:
                                            query_id = """g.v("""+str(c)+""").astNodes().filter{it.type == "Identifier" }.code"""
                                            ids = j.runGremlinQuery(query_id)
                                            flag = 0
                                            for i in my_list:
                                                if (i in ids) and (ptr in ids):
                                                    flag = 1#print p_id
                                            if flag == 1:
                                                query_compound = """g.v("""+str(c)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                                                query_sta = """g.v("""+str(c)+""").code"""
                                                query_sta_id = """g.v("""+str(c)+""").id"""
                                                query_else_parents = """g.v("""+str(c)+""").parents().parents().parents().parents().id"""
                                                else_parents = j.runGremlinQuery(query_else_parents)
                                                sta= j.runGremlinQuery(query_sta)
                                                compound_out = j.runGremlinQuery(query_compound)
                                                sta_id = j.runGremlinQuery(query_sta_id)
                                                #print sta_id
                                                #print else_parents[0]
                                                if (str(sta_id)) in duplicate:
                                                    print else_parents[0]

                                                    continue
                                                if len(check_else) != 0:
                                                    if check_else[0] == else_parents[0]:
                                                    #print else_parents[0]
                                                        continue
                                                S_file.write(sta+"\n")
                                                S_file.write("{"+"\n")
                                                #print str(duplicate) + ptr
                                                duplicate.append(str(sta_id))
                                                #print str(duplicate) + ptr
                                                for c in compound_out:
                                                    #print c
                                                    type_query = """g.v("""+str(c)+""").type"""
                                                    type = j.runGremlinQuery(type_query)
                                                    if type not in check_list:
                                                        for i in my_list:
                                                            if (str(c)) in duplicate:
                                                                break
                                                            if nor_stat_selection(c,S_file,i) == 1:
                                                                duplicate.append(str(c))
                                                S_file.write("}"+"\n")
                                            #elif type == "IfStatement":


                                else:
                                    #print children_id
                                    if children_type not in check_list:

                                        for i in my_list:
                                            if (str(children_id[0])) in duplicate:
                                                break
                                            if nor_stat_selection(children_id[0],S_file,i) == 1:
                                                #print children_id
                                                duplicate.append(str(children_id[0]))
                                S_file.write("}"+"\n")
                    S_file.write("}"+"\n")
                    #print "HOngfa"

                    if len(check_else)!= 0:

                        S = check_else[0]
                        #print S
                        query_id = """g.v("""+str(S)+""").astNodes().filter{it.type == "Identifier" }.code"""
                        ids = j.runGremlinQuery(query_id)
                        flag = 0
                        for i in my_list:
                            if (i in ids) and (ptr in ids):
                                flag = 1
                        if flag == 1:

                            S_file.write("else"+"\n")
                            S_file.write("{"+"\n")
                            CompoundStatement_query = """g.v("""+str(S)+""").out().out().id"""
                            CompoundStatements_id = j.runGremlinQuery(CompoundStatement_query)
                            for compound in CompoundStatements_id:
                                    #print compound
                                query_parent = """g.v("""+str(compound)+""").id"""
                                query_parent_type = """g.v("""+str(compound)+""").type"""
                                p_id = j.runGremlinQuery(query_parent)
                                p_type = j.runGremlinQuery(query_parent_type)
                                #print p_type


                                if p_type in check_list2:
                                    query_id = """g.v("""+str(p_id)+""").astNodes().filter{it.type == "Identifier" }.code"""
                                    ids = j.runGremlinQuery(query_id)
                                    flag = 0

                                    for i in my_list:
                                        if (i in ids) and (ptr in ids):
                                            flag = 1
                                            #print p_id
                                    if flag == 1:

                                        query_compound = """g.v("""+str(p_id)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                                        query_sta = """g.v("""+str(p_id)+""").code"""
                                        sta= j.runGremlinQuery(query_sta)
                                        compound_out = j.runGremlinQuery(query_compound)

                                        S_file.write(sta+"\n")
                                        S_file.write("{"+"\n")
                                        for c in compound_out:
                                            #print c
                                            type_query = """g.v("""+str(c)+""").type"""
                                            type = j.runGremlinQuery(type_query)
                                            if type not in check_list:
                                                for i in my_list:
                                                    if (str(c)) in duplicate:
                                                        break
                                                    if nor_stat_selection(c,S_file,i) == 1:
                                                        duplicate.append(str(c))
                                            elif type in check_list2:
                                                query_id = """g.v("""+str(c)+""").astNodes().filter{it.type == "Identifier" }.code"""
                                                ids = j.runGremlinQuery(query_id)
                                                flag = 0
                                                for i in my_list:
                                                    if (i in ids) and (ptr in ids):
                                                        flag = 1#print p_id
                                                if flag == 1:
                                                    query_compound = """g.v("""+str(c)+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                                                    query_sta = """g.v("""+str(c)+""").code"""
                                                    query_sta_id = """g.v("""+str(c)+""").id"""
                                                    query_else_parents = """g.v("""+str(c)+""").parents().parents().id"""
                                                    else_parents = j.runGremlinQuery(query_else_parents)
                                                    sta= j.runGremlinQuery(query_sta)
                                                    compound_out = j.runGremlinQuery(query_compound)
                                                    sta_id = j.runGremlinQuery(query_sta_id)
                                                    #print else_parents[0]
                                                    if (str(sta_id)) in duplicate:
                                                        continue
                                                    if check_else[0] == else_parents[0]:

                                                        continue
                                                    S_file.write(sta+"\n")
                                                    S_file.write("{"+"\n")
                                                    duplicate.append(str(sta_id))
                                                    for c in compound_out:
                                                        #print c
                                                        type_query = """g.v("""+str(c)+""").type"""
                                                        type = j.runGremlinQuery(type_query)
                                                        if type not in check_list:
                                                            for i in my_list:
                                                                if (str(c)) in duplicate:
                                                                    break
                                                                if nor_stat_selection(c,S_file,i) == 1:
                                                                    duplicate.append(str(c))

                                        S_file.write("}"+"\n")

                                elif p_type == "IfStatement":
                                    query_id = """g.v("""+str(p_id)+""").astNodes().filter{it.type == "Identifier" }.code"""
                                    ids = j.runGremlinQuery(query_id)
                                    query_sta = """g.v("""+str(p_id)+""").code"""
                                    sta = j.runGremlinQuery(query_sta)
                                    flag = 0
                                    for i in my_list:
                                        if (i in ids) and (ptr in ids):
                                            flag = 1#print p_id
                                    if flag == 1:
                                        if (str(p_id)) in duplicate:
                                            continue
                                        S_file.write(sta+"\n")
                                        S_file.write("{"+"\n")
                                        duplicate.append(str(sta_id))
                                        query_children_type = """g.v("""+str(p_id)+""").ithChildren("1").type"""
                                        query_children_id = """g.v("""+str(p_id)+""").ithChildren("1").id"""

                                        children_type = j.runGremlinQuery(query_children_type)
                                        children_id = j.runGremlinQuery(query_children_id)

                                        if children_type[0] == "CompoundStatement":
                                            query_compound = """g.v("""+str(children_id[0])+""").out().id"""
                                            compound_out = j.runGremlinQuery(query_compound)

                                            for c in compound_out:
                                                #print c
                                                type_query = """g.v("""+str(c)+""").type"""
                                                type = j.runGremlinQuery(type_query)
                                                if type not in check_list:
                                                    for i in my_list:
                                                        if (str(c)) in duplicate:
                                                            break
                                                        if nor_stat_selection(c,S_file,i) == 1:
                                                            duplicate.append(str(c))
                                        else:
                                            #print children_id
                                            if children_type not in check_list:

                                                for i in my_list:
                                                    if (str(children_id[0])) in duplicate:
                                                        break
                                                    if nor_stat_selection(children_id[0],S_file,i) == 1:
                                                        #print children_id
                                                        duplicate.append(str(children_id[0]))
                                        S_file.write("}"+"\n")
                                S_file.write("}"+"\n")


            if sta_type == "SwitchStatement":
                CompoundStatement_query = """g.v("""+str(S)+""").astNodes().filter{it.type == "Condition"}.id"""
                CompoundStatements_id = j.runGremlinQuery(CompoundStatement_query)

                for compound in CompoundStatements_id:
                        #print compound
                    query_parent = """g.v("""+str(compound)+""").parents().id"""
                    query_parent_type = """g.v("""+str(compound)+""").parents().type"""
                    p_id = j.runGremlinQuery(query_parent)
                    p_type = j.runGremlinQuery(query_parent_type)
                    #print p_type[0]
                    if p_id[0] == sta_id:
                        continue
                    elif p_type[0] in check_list2:
                        query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                        ids = j.runGremlinQuery(query_id)
                        flag = 0
                        for i in my_list:
                            if i in ids:
                                flag = 1#print p_id
                        if flag == 1:
                            query_compound = """g.v("""+str(p_id[0])+""").out().filter{it.type == "CompoundStatement"}.out().id"""
                            query_sta = """g.v("""+str(p_id[0])+""").code"""
                            sta= j.runGremlinQuery(query_sta)
                            compound_out = j.runGremlinQuery(query_compound)
                            S_file.write(sta+"\n")
                            S_file.write("{"+"\n")
                            for c in compound_out:
                                #print c
                                type_query = """g.v("""+str(c)+""").type"""
                                type = j.runGremlinQuery(type_query)
                                if type not in check_list:
                                    for i in my_list:
                                        if (str(c)) in duplicate:
                                            break
                                        if nor_stat_selection(c,S_file,i) == 1:
                                            duplicate.append(str(c))
                            S_file.write("}"+"\n")
                    elif p_type[0] == "IfStatement":
                        query_id = """g.v("""+str(p_id[0])+""").astNodes().filter{it.type == "Identifier" }.code"""
                        ids = j.runGremlinQuery(query_id)
                        flag = 0
                        for i in my_list:
                            if i in ids:
                                flag = 1#print p_id
                        if flag == 1:
                            query_children_type = """g.v("""+str(p_id[0])+""").ithChildren("1").type"""
                            query_children_id = """g.v("""+str(p_id[0])+""").ithChildren("1").id"""

                            children_type = j.runGremlinQuery(query_children_type)
                            children_id = j.runGremlinQuery(query_children_id)

                            if children_type[0] == "CompoundStatement":
                                query_compound = """g.v("""+str(children_id[0])+""").out().id"""
                                compound_out = j.runGremlinQuery(query_compound)

                                for c in compound_out:
                                    #print c
                                    type_query = """g.v("""+str(c)+""").type"""
                                    type = j.runGremlinQuery(type_query)
                                    if type not in check_list:
                                        for i in my_list:
                                            if (str(c)) in duplicate:
                                                break
                                            if nor_stat_selection(c,S_file,i) == 1:
                                                duplicate.append(str(c))
                            else:
                                #print children_id
                                if children_type not in check_list:

                                    for i in my_list:
                                        if (str(children_id[0])) in duplicate:
                                            break
                                        if nor_stat_selection(children_id[0],S_file,i) == 1:
                                            #print children_id
                                            duplicate.append(str(children_id[0]))




