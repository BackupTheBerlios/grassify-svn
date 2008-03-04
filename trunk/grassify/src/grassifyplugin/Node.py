class Node:

        def __init__(self, unitname, unitclass, unittype=None, description=None, phase=None, later=None, earlier=None, concurrent=None):
                self.__unitname = unitname
                self.__unitclass = unitclass
                self.__unittype = unittype or ""
                self.__description = description or ""
                self.__phase = phase or ""
                self.__later = later or set()
                self.__earlier = earlier or set()
                self.__concurrent = concurrent or set()
                
        def addLater(self, n):
                self.__later.add(n)

        def addEarlier(self, n):
                self.__earlier.add(n)

        def addConcurrent(self, n):
                self.__concurrent.add(n)

        # getters and setters
        def getUnitname(self):
                return self.__unitname

        def setUnitname(self, unitname):
                self.__unitname = __unitname

        def getLater(self):
                return self.__later

        def setLater(self, later):
                self.__later = __later

        def getEarlier(self):
                return self.__earlier

        def setEarlier(self, earlier):
                self.__earlier = __earlier

        def getConcurrent(self):
                return self.__concurrent

        def setConcurrent(self, concurrent):
                self.__concurrent = __concurrent

        # properties
        unitname = property(getUnitname, setUnitname)
        later = property(getLater, setLater)
        earlier = property(getEarlier, setEarlier)
        concurrent = property(getConcurrent, setConcurrent)
        
