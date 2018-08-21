
from country import Country #import the class country from country.py

#sets some standard lists that will be used in the program, its outside the class because I found it easier this way
countryCatCountry = []
countryCatPopulation = []
countryCatArea = []
countryCatContinent = []

class CountryCatalogue:

    def __init__(self, continentFile, dataFile): #setting the parameters to be of any name
        self._countryCat = {} #initializing the two dictionaries
        self._cDictionary = {} #initializing the two dictionaries

        with open(continentFile) as f: #opens file and create self._cDictionary with the right key and value
            for line in f: #runs through the file
                line = line.strip()
                (key,val) = line.split(",")
                self._cDictionary[(key)] = val
            del self._cDictionary["Country"] #deletes header key and value

        with open(dataFile) as f: #reading the file to get a clean country name for each country
            for line in f: #runs through the file
                split = line.split("|")
                countryCatCountry.append(split[0]) #the area values lies on the zeroth index of the line
            countryCatCountry.pop(0)

        with open(dataFile) as f: #reading the file to get a clean population value for each country
            for line in f: #runs through the file
                line = line.strip()
                line = line.strip(",")
                line = line.replace(",","")
                split = line.split("|")
                countryCatPopulation.append(split[1]) #the area values lies on the first index of the line
            countryCatPopulation.pop(0)

        with open(dataFile) as f: #reading the file to get a clean area value for each country
            for line in f: #runs through the file
                line = line.strip() #removes \n
                line = line.strip(",")
                line = line.replace(",","")
                line = line.split("|") #splits at the |
                countryCatArea.append((line[2])) #the area values lies on the second index of the line
            countryCatArea.pop(0)

        with open(continentFile) as f:#reads through another file to get the
            for line in f:
                line = line.strip()
                line = line.split(",")
                countryCatContinent.append(line[1])  #the area values lies on the first index of the line (this is a different file than those above)
            countryCatContinent.pop(0)

        #this portion is important, this is were the collection store objects of type Country.
        for i in range(0,len(countryCatArea)):
            self._countryCat[countryCatCountry[i]] = Country(countryCatCountry[i],countryCatPopulation[i],countryCatArea[i],countryCatContinent[i])

    #if the name of the country is in the file, and returns all the data about the country if successful
    def findCountry(self, name):
        if name in self._countryCat:
            return self._countryCat[name]
        else:
            return None

    def setPopulationOfCountry(self, name, pop): #sets the population of a country, updating it if country exists
        if name in self._countryCat:
            self._countryCat[name].setPopulation(pop)
            return True
        else:
            return False

    def setAreaOfCountry(self, name, area): #same as above but just for area
        if name in self._countryCat:
            self._countryCat[name].setArea(area)
            return True
        else:
            return False

    def addCountry(self, name, pop, area, continent): #adds country, taking in all the new parameters and updated cDictionary and countryCat
        if name not in self._countryCat:
            countryCatCountry.append(name)
            countryCatPopulation.append(pop)
            countryCatArea.append(area)
            countryCatContinent.append(continent)
            self._cDictionary[name] = continent
            self._countryCat[name] = Country(name, pop, area, continent)
            return True
        else:
            return False

    def deleteCountry(self, name): #deletes country if it already exsits, and updated cDic and countryCat accordingly
        if name in self._countryCat:
            indexOfCountry = countryCatCountry.index(name)
            indexOfCountry = indexOfCountry - 1
            print(indexOfCountry)
            self._countryCat.pop(name)
            self._cDictionary.pop(name)
            countryCatCountry.pop(indexOfCountry)
            countryCatPopulation.pop(indexOfCountry)
            countryCatArea.pop(indexOfCountry)
            countryCatPopulation.pop(indexOfCountry)

    def printCountryCatalogue(self): #prints the entire catalogue for a country
        for name in self._countryCat:
            print(self._countryCat[name])

    def getCountriesByContinent(self, continent): #returns list of countries on a continent
        if continent in countryCatContinent: #checks if continent even exists
            countriesInGivenContinent = []
            for el in self._countryCat:
                if self._countryCat[el].getContinent() == continent:
                    countriesInGivenContinent.append(self._countryCat[el]) #appends to list
            return countriesInGivenContinent
        else:
            return [] #return empty string if contient doesnt exist

    def getCountriesByPopulation(self, continent):
        listOfPopulations = [] #intializes lists
        listOfCountries = []
        if continent.isalnum() is True or " " in continent: #checks if continent exists
            element = [el for el, x in enumerate(countryCatContinent) if x == continent] #finds all occurrences of an element in a list
            for x in element:
                listOfPopulations.append(self._countryCat[countryCatCountry[x]].getPopulation()) #appends to list the pop
                listOfCountries.append(countryCatCountry[x]) #appends to list the country for which pop was added
            tuple = list(zip(listOfCountries, listOfPopulations)) #converts the tuples into a list and combines the seperate tuples
            return tuple
        else:
            return []

    def getCountriesByArea(self, continent): #same thing as above but instead of outputing a list of populations its a list of areas.
        listOfAreas = []
        listOfCountries = []
        if continent.isalnum() is True or " " in continent:
            element = [el for el, x in enumerate(countryCatContinent) if x == continent]
            for x in element:
                listOfAreas.append(self._countryCat[countryCatCountry[x]].getArea())
                listOfCountries.append(countryCatCountry[x])
            tuple= list(zip(listOfCountries, listOfAreas))
            return tuple
        else:
            return []

    def findMostPopulousContinent(self):
        listOfContinents = []
        for country in self._countryCat :
            # iterates through continents in countryCat and appends any unique continents
            if self._countryCat[country].getContinent() not in listOfContinents :
                listOfContinents.append(self._countryCat[country].getContinent())
        continentPopulations = []

        for continent in listOfContinents : #returns a list of country objects that are in continent
            population = 0
            countryList = self.getCountriesByContinent(continent)
            for country in countryList :
                population = population + int(country.getPopulation()) #keeps a running total of the population in that continent
            continentPopulations.append([continent, population]) #creates a list with continents and their populations
        #below: this was one of the methods I did first, getting stuck on the others with this sorting tuples idea so this portion of the code
        #how inefficent this is
        i = 0
        largestPopulation = -1
        largestContinent = ""
        while i < len(continentPopulations): #loops until the end of continentPopulations list
            if continentPopulations[i][1] > largestPopulation :
                largestPopulation = continentPopulations[i][1] #updates largestPopulation value
                largestContinent = continentPopulations[i][0] #stores the continent that has the largest population
            i = i + 1 #next position in list
            tuple = (largestContinent, largestPopulation)
        return tuple #returns the continent with the largest population

    def filterCountriesByPopDensity(self, lowerBound, upperBound): #chekcs for popdensities within a given range
        listOfPoputionDensity = []
        listOfCountry =[]
        for name in self._countryCat: #for names in the catalogue
            if self._countryCat[name].getPopDensity() >= lowerBound and self._countryCat[name].getPopDensity() <= upperBound: #checks bounds
                listOfCountry.append(self._countryCat[name].getName()) #add to list
                listOfPoputionDensity.append(self._countryCat[name].getPopDensity())
                tuple = list(zip(listOfCountry,listOfPoputionDensity))
                tuple = sorted(tuple , key=lambda x: x[1], reverse=True)  #sorts tuple by population instead of country name
        if listOfPoputionDensity == []:
            return []
        else:
            return tuple

    def saveCountryCatalogue(self, outputFileName): #writes code to output file
        file = open(outputFileName,'w') #wasnt sure how to use write method with the (with open() as f) method.
        count = 0
        for i in sorted(self._countryCat): #each country
            output = self._countryCat[i].getName()+"|"+ self._countryCat[i].getContinent()+"|"+ str(self._countryCat[i].getPopulation())+"|"+ str(self._countryCat[i].getArea())+"|"+ str(self._countryCat[i].getPopDensity()) +"\n"
            file.write(output) #adds the output to the desire doc
            count = count + 1
        file.close() #close file
        if count == len(self._countryCat):
            return count
        else:
            return -1























