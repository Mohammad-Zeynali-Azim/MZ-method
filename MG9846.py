def readfrom_nodelist(nodelist, readcount_fromnodelist, level_count):
    global tasmim
    templist = []
    templist.clear()
    k = len(nodelist) - readcount_fromnodelist
#    print(len(nodelist))
    templist.clear()
 #   print("sdsdsd", k)
 #   print("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",tasmim)
    for i in range(k, len(nodelist)):
        temp = nodelist[i]
        templist.append(temp)
  #  print("temp list", templist)
    level_count = level_count + 1

    if(tasmim==1):
        T1=1
        T2=1
        if(level_count%2==0):
                 readcount_fromnodelist = len(templist)*2
        else:
                 readcount_fromnodelist=int((len(templist)-2)/2)+2
    else:
        readcount_fromnodelist = int(((level_count - 2) / 2) + 2) * ((level_count % 2) + 1)
        T1=0
        T2=2

    if (level_count % 2 == T1 and level_count != T2):
        nodelist.append(templist[0])
        for i in range(1, len(templist) - 2, 2):
            if ((i + 1) > len(templist) - 2):
                break
            nodelist.append(templist[i] + templist[i + 1])
        nodelist.append(templist[len(templist) - 1])
        readfrom_nodelist(nodelist, readcount_fromnodelist, level_count)

        level_count = level_count + 1
        templist.clear()
    else:
        templist.reverse()
        pop_fromTemplist(templist, nodelist, level_count, readcount_fromnodelist)


# =======================================================
def addtolist(num, nodelist):
    global level_count
    num = num / 2
    split_num = str(num).split('.')
    int_part = int(split_num[0])
    decimal_part = int(split_num[1])
    nodelist.append(int_part)
    nodelist.append(decimal_part)


# ========================================================
def pop_fromTemplist(templist, nodelist, level_count, readcount_fromnodelist):
    while True:
        global allow
        temp = 0
        temp = templist.pop()
        #        print("temp in pop_fromlist", temp)
        #      print("temp list after pop", templist)
        addtolist(temp, nodelist)
        if (len(templist) == 0):
            break
    if (level_count < userenteredlevel):
        readfrom_nodelist(nodelist, readcount_fromnodelist, level_count)


# =========================================Special Dimond value Mining ================


# =======================================================================
def Graph_Generate(Root_Value, Root_Value2):
    global userenteredlevel
    global tasmim
    global num
    # num = int(input("Please First Enter Graph Root Number for Generating your graph: "))
    templist1 = []
    readcount_fromnodelist = 1

    readcount_fromnodelist = 1
    nodelist = []
    findnodevale = []
    level_count = 1
    userenteredlevel = 0

    nodelist = []
    findnodevale = []
    level_count = 1
    userenteredlevel = 0
    num = Root_Value
    userenteredlevel = Root_Value2
    #  userenteredlevel=int(input("Please Graph Levels:"))

    if (len(num) == 1):
        tasmim=0
        nodelist.append(num[0])
        readfrom_nodelist(nodelist, readcount_fromnodelist, level_count)

    else:
        tasmim=1
        for i in num:
            nodelist.append(i)
        readcount_fromnodelist = len(nodelist)
        readfrom_nodelist(nodelist, readcount_fromnodelist, level_count)
        # print("Your Graph Noode List is=[",nodelist,"]")
 #   print("sddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd", nodelist)
    templist1 = nodelist
    return templist1


# ==================================================Dimond index Findin====================================

# =========================================dimond value===========================================
def Dimond_value(dif):
    global L1400
    findnodevale = []
    findnodevale.clear()
    L=[]
    L.clear()
    i=0
    f=0
    k = dif
    L = finddimondindex(k)
    print(L)
    for i in L:
        f = i
        findnodevale.append(L1400[f - 1])
    return findnodevale


# =============================================finding same Dimond and its sequence============================

def Same_Domond_sequence(nodelist):
    findnodevale2 = []
    samesequence = []
    print("Enter Base Dimond number to find it same Dimons: ")
    basedimond = int(input())
    findnodevale = Dimond_value(basedimond, nodelist)
    for i in range(1, 100):
        s = finddimondindex(i)
        for i in s:
            h = i
            findnodevale2.append(nodelist[h - 1])

        if (findnodevale2 == findnodevale):
            samesequence.append(i)
        findnodevale2.clear()
    return samesequence


# =============================================node value mining in your level============================

def Node_value_in_Level(k, nodelist):
    level_node_value = []
    # nc_inlevel=int(input("please enter level number if you want know value of Level:"))
    nc_inlevel = k
    x = node_count_in_Level(nc_inlevel)
    y = nodecount(nc_inlevel - 1)
    # print("x is:",x)
    #  print("y is:",y)
    for i in range(y, y + x):
        level_node_value.append(nodelist[i])
    return level_node_value


# =============== Create binary graph from Division by two Graphs====================================

def Binary_graph(nodelist):
    binary_node_list = []
    for i in nodelist:
        if (i%2==1):
            binary_node_list.append(1)
        else:
            binary_node_list.append(0)
    return binary_node_list


# ===================================================Binary value in special Leval=====================

def Binary_value_in_Level(k,nodelist):
    binary_level_node_value = []
    LNV = Node_value_in_Level(k,nodelist)
    for i in LNV:
        if (i%2==1):
            binary_level_node_value.append(1)
        else:
            binary_level_node_value.append(0)
    return binary_level_node_value


# =============================================dimond index value==========================================

def finddimondindex(di):
    nodeindex_list = []
    dimond_number = di
    global num
    d = len(num)  # digit count
    nodeindex_list = []

    # ----------------------Number of nodes until to level k+3----------------------------------
    sum = 0
    for i in range(1, di + 3):
        sum = sum + (((int((i - 1) / 2)) + d)) * ((i + 1) % 2 + 1)
 #       print("ssssssssssssssssssssssssss", sum)

    # ----------------------Find K level----------------------------------
    dimond_count1 = 0
    L = 1
    j = 1
    while True:
        dimond_count1 = dimond_count1 + (int((j - 1) / 2) + d)
        print(dimond_count1, j)
        if (dimond_count1 >= di):
            break
        j = j + 2
 #   print("K in level:", j)

    # ---------------------------------Dimond Count in level j----------------------------------
    dimond_count1_k_level = 0
    for L in range(1, j, 2):
        dimond_count1_k_level = dimond_count1_k_level + (int((L - 1) / 2) + d)
    #    print("dimond_count1_k_level:", dimond_count1_k_level)

    # ---------------------------------Dimond index in graph----------------------------------
    Dimond_K_index = di - dimond_count1_k_level
    a = (di - dimond_count1_k_level - 1)
    #print("aaaaaaaaaaaaaaaa:", a)
 #   print("Dimond_K_index", Dimond_K_index)

    # ---------------------------------K location in graph----------------------------------
    k_location = 0
    sum = 0
    for L in range(1, j):
        sum = sum + (((int((L - 1) / 2)) + d)) * ((L + 1) % 2 + 1)
    #print("sum:", sum)
    k_location = (Dimond_K_index) + sum
    nodeindex_list.append(k_location)

    print("k_location", k_location)
    # ---------------------------------Second Node of Dimond Location ----------------------------------
    sum1 = 0
    sum1 = sum + (int((j - 1) / 2) + d)
    sec_node_location = a * 2 + sum1 + 1
    nodeindex_list.append(sec_node_location)
    #print("sec_node_location", sec_node_location)

    # ---------------------------------third Node of Dimond Location ----------------------------------
    third_node_location = 0
    third_node_location = sec_node_location + 1
    nodeindex_list.append(third_node_location)
    #print("third_node_location", third_node_location)

    # ---------------------------------fourth Node of Dimond Location ----------------------------------
    fourth_node_location = 0
    sum2 = 0
    sum2 = sum1 + (int((j - 1) / 2) + d) * 2
    fourth_node_location = (a + 1) + sum2
    nodeindex_list.append(fourth_node_location)

    #print("third_node_location", fourth_node_location)

    # ---------------------------------fifth Node of Dimond Location ----------------------------------
    fifth_node_location = 0
    fifth_node_location = fourth_node_location + 1
    nodeindex_list.append(fifth_node_location)

    #print("fifth_node_location", fifth_node_location)

    # ---------------------------------sixth Node of Dimond Location ----------------------------------

    sixth_node_location = 0
    sum3 = 0
    sum3 = sum2 + (int(((j + 2) - 1) / 2) + d)
    sixth_node_location = (a * 2 + 1) + 1 + sum3
    nodeindex_list.append(sixth_node_location)

   # print("sixth_node_location", sixth_node_location)

    # ---------------------------------seventh Node of Dimond Location ----------------------------------
    seventh_node_location = 0
    seventh_node_location = sixth_node_location + 1
    nodeindex_list.append(seventh_node_location)

  #  print("sixth_node_location", seventh_node_location)

    # ---------------------------------eigth Node of Dimond Location ----------------------------------

    eigth_node_location = 0
    sum4 = 0
    sum4 = sum3 + (int(((j + 2) - 1) / 2) + d) * 2
    eigth_node_location = (a + 1) + 1 + sum4
    nodeindex_list.append(eigth_node_location)

 #   print("eigth_node_location", eigth_node_location)
    return nodeindex_list


# ==========================================================================================================
# =================== Dgraph=========================

# ====================================node count in graph========================================
def nodecount(l):
    global tasmim
    sum1 = 0
    k = l
    for i in range(1,k+1):  #ta sathe k benabar in k+1 minevisim
        sum1=sum1+node_count_in_Level(i)
      #  print("i is:",i,node_count_in_Level(i))
    return sum1

# =======================================Sum of node in Level=================================

def node_count_in_Level(k):
    i = k
    global num
    l=len(num)
 #   print("erer",l)
    levelnodecount = 0
    if(l!=1):
            if(((i%2)==1)):
                #print("fard")
                if (i == 1):
                    levelnodecount =l
                else:
                    te = ((int((i - 1) / 2)))
                    for j in range(1,te+1):
                       l=l+1
                    levelnodecount=l
            else:
                 if(i==2):
                     levelnodecount=l*2
                 else:
                     te = ((int((i - 1) / 2)))
                     for j in range(1, te +1):
                         l = l + 1
                     levelnodecount = l*2

    else:
        if (i == 1):
            levelnodecount =l
        else:
            levelnodecount = ((int((i - 2) / 2)) + 2) * (((i % 2) + 1))

    return levelnodecount


# ==========================================find Dimond count=======================================

def findDimondCount(lb, le):
    L_b = lb
    L = L_b
    L_end = le
    dimond_count = 0
    setlevel = []
    if (L_end - L < 4):
        print("There is not Dimond")
    else:
        if (L % 2 == 1):
            L = L + 1
            while True:
                setlevel.append(L)
                L = L + 2
                if (L_end - L < 4):
                    break
    print(setlevel)
    for l in setlevel:
        dimond_count = dimond_count + (int((l - 1) / 2) + 2)
    # print("Dimond Count from(", L_b, "to", L_end, ") is:", dimond_count)
    return dimond_count


# ============================================node position==================================================

def nodelocation(nodenumber):
    sum = 0
    k = nodenumber
    i = 2
    while True:
        sum = sum + (((int((i - 2) / 2)) + 2) * ((i % 2) + 1))
        if (sum > k):
            node_locatin_level = i - 1
            break
        i = i + 1
    print("node_locatin_level=", node_locatin_level)

    sum1 = 0
    for i in range(2, node_locatin_level):
        sum1 = sum1 + (((int((i - 2) / 2)) + 2) * ((i % 2) + 1))
    sum1 = sum1 + 1
    print("node location in level L=", k - sum1)


# =================================Find Index of Dimond====================================================
# ==================================Writing Graph value in File========================================================================


# ============================================Level to Level Print graph value

def Level_to_Levl_value(nodelist):
    level_node_value = []
    R_level_node_value = []
    for i in range(1, 100):
        x = node_count_in_Level(i)
        y = nodecount(i - 1)
        for j in range(y, y + x):
            level_node_value.append(nodelist[j])
        print(level_node_value)
        R_level_node_value.append(level_node_value)
        level_node_value.clear()
        print("\n")


# return R_level_node_value

# ===================================================================================================

def Binary_Level_to_Levl_value(nodelist):
    level_node_value = []
    Binary_level_node_value = []
    r = []
    for k in range(1, 102):
        x = node_count_in_Level(k)
        y = nodecount(k - 1)
        # print("x is:",x)
        #  print("y is:",y)
        for j in range(y, y + x):
            level_node_value.append(nodelist[j])

        for i in level_node_value:
            if (i%2==1):
                Binary_level_node_value.append(1)
            else:
                Binary_level_node_value.append(0)
        level_node_value.clear()
        print("kkkkkkkkkk",k,"a",Binary_level_node_value)
        print("list1:", r)
        Binary_level_node_value.clear()

# ===================================================chap=======================
list1 = []
list1.clear()


def chap(k):
    list1.append(k)
    print(list1)
    print(list1[0])


# ======================================Compare Two  Graph=================================================================

def Compare_Graph(nodelist1, nodelist2):
    Equal_Levels = []
    level_node_value1 = []
    level_node_value2 = []
    for i in range(1, 200):
        x = node_count_in_Level(i)
        y = nodecount(i - 1)
        # print("x is:",x)
        #  print("y is:",y)
        for j in range(y, y + x):
            level_node_value1.append(nodelist1[j])
            level_node_value2.append(nodelist2[j])
        if (level_node_value1 == level_node_value2):
            Equal_Levels.append(i)
        level_node_value1.clear()
        level_node_value2.clear()
  #      print("\n")
    return Equal_Levels


# ==========================================================================================================

def Compare_Binary_Graph(nodelist1, nodelist2):
    Equal_Levels = []
    level_node_value1 = []
    level_node_value2 = []
    B_level_node_value1 = []
    B_level_node_value2 = []
    for k in range(1, 17):
        x = node_count_in_Level(k)
        y = nodecount(k - 1)
        # print("x is:",x)
        #  print("y is:",y)
        for j in range(y, y + x):
            level_node_value1.append(nodelist1[j])
            level_node_value2.append(nodelist2[j])
            for l in level_node_value1:
                if (l % 2 == 1):
                    B_level_node_value1.append(1)
                else:
                    B_level_node_value1.append(0)
            for m in level_node_value2:
                if (m % 2 == 1):
                    B_level_node_value2.append(1)
                else:
                    B_level_node_value2.append(0)
            level_node_value1.clear()
            level_node_value2.clear()

        if (B_level_node_value1 == B_level_node_value2):
            Equal_Levels.append(k)
        B_level_node_value1.clear()
        B_level_node_value2.clear()
      #  print("\n")
    return Equal_Levels

# ==============================================After constructing=============================================================

def After_constructing(L1):
    global L1400
    L1400=L1









