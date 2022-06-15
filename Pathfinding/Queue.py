from ast import Delete
from heapq import heapify



class Queue:
    __max = True
    __type = ""
    __arr =[]
    def __init__(self, type, max=True):
        self.__arr = []
        if type != "FIFO" and type !="LIFO" and type !="PRIO":
            raise RuntimeError("Please provide a valid type")
        self.__type = type
        self.__max = max

    def __contains__(self, item):
        for element in self.__arr:
            if element == item:
                return True
        return False

    def print(self):
        print(self.__arr)

    def is_empty(self):
        return len(self.__arr)==0
    
    def __heapify(self, n , i):
        if self.__max:
            largest = i
            l = 2* i +1
            r = 2* i +2
            if l<n  and self.__arr[i]<self.__arr[l]:
                largest = l
            if r<n  and self.__arr[i]<self.__arr[r]:
                largest = r 
            
            if largest != i:
                self.__arr[i], self.__arr[largest] = self.__arr[largest], self.__arr[i]
                self.__heapify(n, largest)
        else:
            smallest = i
            l = 2* i +1
            r = 2* i +2
            if l<n  and self.__arr[i]>self.__arr[l]:
                smallest = l
            if r<n  and self.__arr[i]>self.__arr[r]:
                smallest = r 
            
            if smallest != i:
                self.__arr[i], self.__arr[smallest] = self.__arr[smallest], self.__arr[i]
                self.__heapify(n, smallest)

    def push(self, number):
        if self.__type == "PRIO": 
            size = len(self.__arr)
            if size==0:
                self.__arr.append(number)
            else:
                self.__arr.append(number)
                for i in range((len(self.__arr)//2) -1, -1, -1):
                    self.__heapify(len(self.__arr), i)
        elif self.__type == "FIFO" or self.__type == "LIFO":
            self.__arr.append(number)
    
    def pop(self):
        if self.__type == "PRIO":
            max = self.__arr[0]
            self.__arr.pop(0)
            self.__heapify(len(self.__arr), 0)
            return max
        elif self.__type == "FIFO":
            element= self.__arr[0]
            self.__arr.pop(0)
            return element
        elif self.__type == "LIFO":
            element = self.__arr[len(self.__arr)-1]
            self.__arr.pop()
            return element
