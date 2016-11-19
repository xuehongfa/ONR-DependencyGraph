from joern.all import JoernSteps
import glob
import sys
import pickle

j=JoernSteps()

j.setGraphDbURL('http://localhost:7474/db/data/')

# j.addStepsDir('Use this to inject utility traversals')

j.connectToDatabase()


#function_query= """getFunctionsByName("""+sys.argv[1]+""").id"""
function_query= """getFunctionsByName("mainGtU").id"""
functionID = j.runGremlinQuery(function_query)
#print functionID[0]
nodes_query = """g.v("""+str(functionID[0])+""").out().filter{it.type == "FunctionDef"}.ithChildren("0").astNodes().filter{it.type=="Identifier" }"""
nodes = j.runGremlinQuery(nodes_query)
#print nodes
duplicate = []
for node in nodes:

    Expression = 0
    Assignment = 0
    edge = []
    #print node
    nodeID = str(node).split(" {childNum")[0].split("(n")[1]
    query_statement_id = """g.v("""+nodeID+""").statements().id"""
    query_statement_code = """g.v("""+nodeID+""").statements().code"""

    check_call_query = """g.v("""+nodeID+""").parents().type"""
    check_call = j.runGremlinQuery(check_call_query)
    #it should be check_call[0]
    if check_call[0] == "Callee":
        continue

    statementID = j.runGremlinQuery(query_statement_id)
    #print statementID
    statementCode = j.runGremlinQuery(query_statement_code)
    #print statementCode
    query_statementType = """g.v("""+str(statementID[0])+""").type"""
    statementType = j.runGremlinQuery(query_statementType)
    #print statementType
    query_code = """g.v("""+nodeID+""").code"""
    query_childnum = """g.v("""+nodeID+""").childNum"""
    nodeCode = j.runGremlinQuery(query_code)
    #print nodeCode
    nodeChildnum = j.runGremlinQuery(query_childnum)
    #print nodeChildnum
    D_file = open(str(functionID[0])+'_'+nodeCode,'a')
    if statementType == 'ExpressionStatement':
        #print "yes"

        if "=" in statementCode[0] and nodeChildnum == '0':
            #print "yes"
            Expression = 1
            related_nodes_query =  """g.v("""+str(statementID[0])+""").out().astNodes().filter{it.type=="Identifier"}.code"""
            related_nodes = j.runGremlinQuery(related_nodes_query)
            related_nodesIDs_query = """g.v("""+str(statementID[0])+""").out().astNodes().filter{it.type=="Identifier"}.id"""
            related_nodesIDs = j.runGremlinQuery(related_nodesIDs_query)
            #print related_nodesIDs
            i = 0
            for related_node in related_nodes:
                related_nodeID = related_nodesIDs[i]
                #print related_nodeID
                check_call_query="""g.v("""+str(related_nodeID)+""").parents().type"""
                check_call = j.runGremlinQuery(check_call_query)
                #print check_call
                if related_node != nodeCode and related_node not in edge and check_call[0] != "Callee":
                    edge.append(str(related_node))
                i += 1
        statement_childrenType_query = """g.v("""+str(statementID[0])+""").ithChildren("0").type"""
        statement_childrenID_query = """g.v("""+str(statementID[0])+""").ithChildren("0").id"""
        statement_children_type = j.runGremlinQuery(statement_childrenType_query)
        #print statement_children_type[0]
        statement_Children_ID = j.runGremlinQuery(statement_childrenID_query)
        #print statement_Children_ID
        if statement_children_type[0] == "CallExpression":
            #print "yes"
            arguments_query = """g.v("""+str(statementID[0])+""").ithChildren("0").astNodes().filter{it.type == "Argument"}.out().astNodes().filter{it.type == "Identifier"}.code"""
            arguments = j.runGremlinQuery(arguments_query)

            for argument in arguments:
                #print argument
                if argument != nodeCode and argument not in edge:
                    edge.append(str(argument))




    if statementType == "IdentifierDeclStatement":

        check_assignment_query = """g.v("""+str(statementID[0])+""").ithChildren("0").out().type"""
        check_assignment = j.runGremlinQuery(check_assignment_query)
        #print check_assignment
        if "AssignmentExpr" in check_assignment:
            #print "yes"

            assignment_nodes_query = """g.v("""+str(statementID[0])+""").ithChildren("0").out().filter{it.type == "AssignmentExpr"}.astNodes().filter{it.type == "Identifier"}.id"""
            assignment_nodes = j.runGremlinQuery(assignment_nodes_query)
            for assignment_node in assignment_nodes :
                #print assignment_node
                query = """g.v("""+str(assignment_node)+""").parents().type"""
                query2 = """g.v("""+str(assignment_node)+""").code"""
                assignment_type = j.runGremlinQuery(query)
                assignment_code = j.runGremlinQuery(query2)
                #print assignment_type
                if assignment_type != "Callee" and nodeChildnum == '0' and assignment_code != nodeCode and assignment_code not in edge:
                    Assignment=1
                    edge.append(str(assignment_code[0]))





    #For Loop Count

    Loop_query = """g.v("""+str(functionID[0])+""").out().filter{it.type == "FunctionDef"}.ithChildren("0").astNodes().filter{it.type=="DoStatement" || it.type == "ForStatement"}.id"""
    Loop_statements = j.runGremlinQuery(Loop_query)

    i = 0
    for Loop in Loop_statements:
        Loop_inside_query = """g.v("""+str(Loop)+""").out().astNodes().filter{it.type == "Identifier"}.code"""
        Loop_inside = j.runGremlinQuery(Loop_inside_query)
        #print Loop_inside
        if nodeCode in Loop_inside and (Assignment == 1 or Expression == 1) and "TC"+str(i) not in edge:
            edge.append("TC"+str(i))
        i += 1

    #For Branch Count:
    Branch_query = """g.v("""+str(functionID[0])+""").out().filter{it.type == "FunctionDef"}.ithChildren("0").astNodes().filter{it.type=="IfStatement"}.id"""
    Branch_statements = j.runGremlinQuery(Branch_query)

    i = 0

    for Branch in Branch_statements:
        print Branch
        Branch_inside_query = """g.v("""+str(Branch)+""").out().astNodes().filter{it.type == "Identifier"}.code"""
        Branch_inside = j.runGremlinQuery(Branch_inside_query)

        if nodeCode in Branch_inside and (Assignment == 1 or Expression == 1) and "BC"+str(i) not in edge:
            edge.append("BC"+str(i))
        i += 1


    #
    # if statementType == "UnaryExpression":
    #
    # if statementType == "IncDecOp":

    #
    #print edge
    if len(edge) == 0:
        continue
    D_file.write(str(edge)+'\n')
    D_file.close()
