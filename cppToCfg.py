file = open("test.cpp",'r')
file = file.read()
file = file.split("\n")
content=[""]
for item in file:
    content.append(item)
print(content)

graph=[]
for i in range(20):
    temp=[]
    for j in range(20):
        temp.append(0)
    graph.append(temp)

#current line number
line = 1

def func(start,end):
    global line
    while(start <= end):

        #############################################################
        #if else case
        if('if' in content[start]):
            graph[start-1][start]=1
            print("if detected")
            startOfIf=start
            startOfElif= -1
            startOfElse= -1
            endOfIf=0
            endOfElif=[]
            endOfElse=-1

            #find end of if else including elif and else
            temp = startOfIf+2

            inIf=True
            inElse=False
            inElif=False
            stack=["{"]
            while(True):
                #####if statement
                if inIf:
                    if len(stack)==0:
                        inIf=False
                        endOfIf=temp-1
                        func(startOfIf+1,endOfIf)
                        stack.append("{")

                        if "else if" in content[temp]:
                            inElif=True
                            graph[startOfIf][temp]=1
                            startOfElif=temp
                            temp+=2
                        elif "else" in content[temp]:
                            inElse=True
                            startOfElse=temp
                            graph[startOfIf][temp]=1
                            temp+=2
                        else:
                            break

                    elif "{" in content[temp]:
                        stack.append("{")
                        temp+=1
                    elif "}" in content[temp]:
                        stack.pop()
                        temp+=1
                    else:
                         temp+=1

                ##else if statement
                elif inElif:
                    if len(stack)==0:
                        inElif=False
                        stack.append("{")
                        func(startOfElif+1,temp-1)
                        endOfElif.append(temp-1)
                        if "else if" in content[temp]:
                            inElif=True
                            graph[startOfIf][temp]=1
                            startOfElif=temp
                            temp+=2
                        elif "else" in content[temp]:
                            startOfElse=temp
                            graph[startOfIf][temp]=1
                            inElse=True
                            temp+=2
                        else:
                            break

                    elif "{" in content[temp]:
                        stack.append("{")
                        temp+=1
                    elif "}" in content[temp]:
                        stack.pop()
                        temp+=1
                    else :
                        temp+=1

                ###else statement
                elif inElse:
                    if len(stack)==0:
                        inElse=False
                        endOfElse=temp-1
                        func(startOfElse+1,endOfElse)
                        break

                    elif "{" in content[temp]:
                        stack.append("{")
                        temp+=1
                    elif "}" in content[temp]:
                        stack.pop()
                        temp+=1
                    else:
                        temp+=1


            graph[endOfIf][temp]=1

            if startOfElse!=-1:
                graph[endOfElse][temp]=1

            if len(endOfElif)!=0:
                for item in endOfElif:
                    graph[item][temp]=1

            start = temp
            continue

        #############################################################
        #while case
        elif 'while' in content[start]:
            print("while_detected")
            startOfWhile=start
            endOfWhile=0

            #find ending line of for loop
            stack=["{"]
            for i in range(startOfWhile+2,1000):
                if len(stack)==0:
                    endOfWhile=i-1
                    break
                if "{" in content[i]:
                    stack.append("{")
                elif "}" in content[i]:
                    stack.pop()

            graph[start-1][start]=1
            start+=1
            func(start+1,endOfWhile)
            start-=1
            graph[endOfWhile][startOfWhile]=1
            continue

        #############################################################
        #for case
        elif('for' in content[start]):
            print("for_detected")
            startOfFor=start
            endOfFor=0

            #find ending line of for loop
            stack=["{"]
            for i in range(startOfFor+2,1000):
                if len(stack)==0:
                    endOfFor=i-1
                    break
                if "{" in content[i]:
                    stack.append("{")
                elif "}" in content[i]:
                    stack.pop()

            graph[start-1][start]=1
            start+=1
            func(start+1,endOfFor)
            start-=1
            graph[endOfFor][startOfFor]=1
            continue

        #############################################################
        #normal statement
        else:
            print("normal_statement detected")
            graph[start-1][start]=1
            start+=1
            continue
        #############################################################

func(1,19)

for i in range(len(graph)):
    print (i," ",graph[i])
