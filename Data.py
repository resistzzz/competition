#-*-coding:utf-8
import datetime

class Data(object):
    '''
        input:
            ecs_lines: a list of original train data
            n: the corelation number
        output:
            self.data: 一个列表包括台数和当期时刻
            self.divData: 根据n划分的数据
            self.divLabel: 根据n划分的标签
    '''
    def __init__(self, ecs_lines, n=13):
        self.lastFlavorNum = 18
        self.oriData = []
        self._clearLineFeed(ecs_lines)
        self.n = n
        self.data = []
        self.divData = []
        self.divLabel = []
        self._processOriData()
        self._initData()
        self._countData()
        # self.rmNoise()
        # self.unitf_data()
        self.adjustData()

    def _clearLineFeed(self, ecs_lines):
        for i in range(len(ecs_lines)):
            if ecs_lines[i] != '\r\n':
                self.oriData.append(ecs_lines[i])

    def _processOriData(self):
        for i in range(len(self.oriData)):
            self.oriData[i] = self.oriData[i].split('\t')[1:]
            self.oriData[i][1] = self.oriData[i][1].split(' ')[0]
            if i == 0:
                temp0 = self.oriData[0][1].split('-')
                temp0 = [int(j) for j in temp0]
                d0 = datetime.datetime(temp0[0], temp0[1], temp0[2])
            temp = self.oriData[i][1].split('-')
            temp = [int(j) for j in temp]
            d1 = datetime.datetime(temp[0], temp[1], temp[2])
            if temp[0] > temp0[0] or temp[1] - temp0[1] >= 10:
                self.oriData[i][1] = (d1 - d0).days - 92
            else:
                self.oriData[i][1] = (d1 - d0).days

    def _initData(self):
        num = self.oriData[-1][1] + 1
        self.data = [0] * num

    def _countData(self):
        for elem in self.oriData:
            t = int(elem[0].split('r')[1])
            if t <= self.lastFlavorNum:
                self.data[elem[1]] += 1
        for i in range(len(self.data)):
            self.data[i] = 1.0 * self.data[i]/self.lastFlavorNum

    def _divideData(self, vector):
        dataLen = len(vector)
        i = 0
        j = 0
        temp = []
        x = []
        label = []
        while i != dataLen:
            if (i - j) != self.n:
                temp.append(vector[i])
                i = i + 1
            else:
                x.append(temp)
                label.append(vector[i])
                j = j + 1
                i = j
                temp = []
        return x, label

    def adjustData(self):
        self.divData, self.divLabel = self._divideData(self.data)

    def unitf_data(self):
        print min(self.data), max(self.data)
        for i in range(len(self.data)):
            self.data[i] = 1.0 * (self.data[i] - min(self.data))/(max(self.data) - min(self.data))

    def rmNoise(self):
        for i in range(len(self.data)):
            data_mean = 1.0 * sum(self.data)/len(self.data)
            if self.data[i] > data_mean * 5 and i != 0:
                self.data[i] = self.data[i-1]
            if self.data[i] > data_mean * 5 and i == 0:
                self.data[i] = 0

class Data_flavor(object):
    def __init__(self, oriData, n=13):
        self.lastFlavorNum = 18
        self.data = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': [],
            'flavor16': [], 'flavor17': [], 'flavor18': []
        }
        self.n = n
        self.oriData = []
        self._clearLineFeed(oriData)
        self.divData = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': [],
            'flavor16': [], 'flavor17': [], 'flavor18': []
        }
        self.divLabel = {
            'flavor1': [], 'flavor2': [], 'flavor3': [],
            'flavor4': [], 'flavor5': [], 'flavor6': [],
            'flavor7': [], 'flavor8': [], 'flavor9': [],
            'flavor10': [], 'flavor11': [], 'flavor12': [],
            'flavor13': [], 'flavor14': [], 'flavor15': [],
            'flavor16': [], 'flavor17': [], 'flavor18': []
        }
        self._readOriData()
        self._initData()
        self._countData()
        # self.rmNoise()
        self.adjustData()

    def _clearLineFeed(self, ecs_lines):
        for i in range(len(ecs_lines)):
            if ecs_lines[i] != '\r\n':
                self.oriData.append(ecs_lines[i])

    def _readOriData(self):
        for i in range(len(self.oriData)):
            self.oriData[i] = self.oriData[i].split('\t')[1:]
            self.oriData[i][1] = self.oriData[i][1].split(' ')[0]
            if i == 0:
                temp0 = self.oriData[0][1].split('-')
                temp0 = [int(j) for j in temp0]
                d0 = datetime.datetime(temp0[0], temp0[1], temp0[2])
            temp = self.oriData[i][1].split('-')
            temp = [int(j) for j in temp]
            d1 = datetime.datetime(temp[0], temp[1], temp[2])
            self.oriData[i][1] = (d1 - d0).days

    def _initData(self):
        num = self.oriData[-1][1] + 1
        for elem in self.data:
            self.data[elem] = [0] * num

    def _countData(self):
        for elem in self.oriData:
            t = int(elem[0].split('r')[1])
            if t <= self.lastFlavorNum:
                self.data[elem[0]][elem[1]] += 1

    def rmNoise(self):
        for elem in self.data:
            if elem != 'flavor4' and elem != 'flavor10':
                data_mean = 1.0 * sum(self.data[elem])/len(self.data[elem])
                for i in range(len(self.data[elem])):
                    if self.data[elem][i] > data_mean * 5 and i != 0:
                        self.data[elem][i] = self.data[elem][i-1]
                    if self.data[elem][i] > data_mean * 5 and i == 0:
                        self.data[elem][i] = 0

    def _divideData(self, vector):
        dataLen = len(vector)
        i = 0
        j = 0
        temp = []
        x = []
        label = []
        while i != dataLen:
            if (i - j) != self.n:
                temp.append(vector[i])
                i = i + 1
            else:
                x.append(temp)
                label.append(vector[i])
                j = j + 1
                i = j
                temp = []
        return x, label

    def adjustData(self):
        for elem in self.data:
            self.divData[elem] = self._divideData(self.data[elem])[0]
            self.divLabel[elem] = self._divideData(self.data[elem])[1]

class InputMessage(object):
    def __init__(self, inputArray):
        self.inputArray = []
        self.clearLineFeed(inputArray)
        self.phSeverKind = int(self.inputArray[0].strip())
        self.serverCPU = {}
        self.serverMEM = {}
        self.serverDisk = {}
        for i in range(self.phSeverKind):
            t = self.inputArray[i+1].split(' ')
            self.serverCPU[t[0]] = int(t[1])
            self.serverMEM[t[0]] = int(t[2])
            self.serverDisk[t[0]] = int(t[3])
        self.flavorNum = int(self.inputArray[self.phSeverKind+1])
        self.flavor = []
        for item in self.inputArray[self.phSeverKind+2:self.flavorNum+self.phSeverKind+2]:
            self.flavor.append(item.split(' ')[0])
        self.startTime = self.inputArray[self.flavorNum+self.phSeverKind+2].split(' ')[0].strip()
        self.endTime = self.inputArray[self.flavorNum+self.phSeverKind+3].split(' ')[0].strip()

    def clearLineFeed(self, inputArray):
        for i in range(len(inputArray)):
            if inputArray[i] != '\r\n':
               self.inputArray.append(inputArray[i])