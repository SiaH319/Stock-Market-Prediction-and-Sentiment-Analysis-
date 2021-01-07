'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''



def BinarySearch(List, item):
    first = 0
    last = len(List)-1
    found = False

    while first <= last and not found:
        midpoint = (first + last)//2
        if List[midpoint] == item:
            found = True
        else:
            if item < List[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found

