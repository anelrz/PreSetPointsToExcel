import math

class M_ID_Collection(object):
    
    def __init__(self, double_ratio, triple_mid_ratio, edge_multiply, double_edge_multiply, prefix):
        
        self.M_IDs=[]        
        self.i = 0
        self.M_ID_count = 0
        self.double_ratio = double_ratio
        self.triple_mid_ratio = triple_mid_ratio
        self.edge_multiply = edge_multiply
        self.double_edge_multiply = double_edge_multiply
        self.prefix = prefix
    
    def findandinsertMID(self,Hi,HiHi,unit1, sensorgroup):
        
        rangematch = False
        unit = self.fixunit(unit1)
                
        if(Hi != None):    
            try:
                test_M_ID = self.findtestrange(Hi, HiHi, unit, sensorgroup)
                
                for M_ID in self.M_IDs:
                    rangematch = self.M_ID_rangetest(M_ID, test_M_ID)
                    if(rangematch):
                        return M_ID
                if(rangematch ==False):
                    self.M_ID_count += 1
                    test_M_ID.name = (self.prefix + ':' + str(self.M_ID_count))
                    self.M_IDs.append(test_M_ID)
                    return test_M_ID
                                              
            except ValueError:
                print(ValueError)
                       
        elif(Hi != None and HiHi == None):
            print()
            
        elif(Hi == None and HiHi == None):
            return None
         
        else:
            return None

            
    def M_ID_rangetest (self, M_ID, rangeMID):
        
        if(M_ID.Rhl != None and M_ID.Rhh != None and rangeMID.Rhl != None and rangeMID.Rhh != None):
            lowoverlap = self.find_overlap(M_ID.Rll, M_ID.Rlh, rangeMID.Rll, rangeMID.Rlh)
            midoverlap = self.find_overlap(M_ID.Rml, M_ID.Rmh, rangeMID.Rml, rangeMID.Rmh)
            highoverlap= self.find_overlap(M_ID.Rhl, M_ID.Rhh, rangeMID.Rhl, rangeMID.Rhh)
                
            if((lowoverlap!= None) and (midoverlap!=None) and (highoverlap!=None) and (M_ID.unit == rangeMID.unit) and (M_ID.sensorgroup == rangeMID.sensorgroup)):
                M_ID.Rll = lowoverlap[0]
                M_ID.Rlh = lowoverlap[1]
                M_ID.Rml = midoverlap[0]
                M_ID.Rmh = midoverlap[1]
                M_ID.Rhl = highoverlap[0]
                M_ID.Rhh = highoverlap[1]
                return True
            else:
                return False
        elif(M_ID.Rhl == None and M_ID.Rhh == None and rangeMID.Rhl == None and rangeMID.Rhh == None):
            lowoverlap = self.find_overlap(M_ID.Rll, M_ID.Rlh, rangeMID.Rll, rangeMID.Rlh)
            midoverlap = self.find_overlap(M_ID.Rml, M_ID.Rmh, rangeMID.Rml, rangeMID.Rmh)
            
            if((lowoverlap!= None) and (midoverlap!=None) and (M_ID.unit == rangeMID.unit) and (M_ID.sensorgroup == rangeMID.sensorgroup)):
                M_ID.Rll = lowoverlap[0]
                M_ID.Rlh = lowoverlap[1]
                M_ID.Rml = midoverlap[0]
                M_ID.Rmh = midoverlap[1]
                M_ID.Rhl = None
                M_ID.Rhh = None
                return True
            else:
                return False
        else:
            return False
            
            
    def find_overlap(self, p1l, p1h, p2l, p2h):
        low = max(p1l, p2l)
        high = min(p1h, p2h)
        overlap = high - low
        if(overlap <= 0):
            return None
        else:
            return [low, high]                  
            
    def findtestrange(self, Hi, HiHi, unit, sensorgroup):
        if((Hi != None) and (HiHi != None)):
            middiff = abs(HiHi-Hi)
            mid = middiff*self.triple_mid_ratio # 0.9
            margin = (middiff - mid)/2
            edgewidth = mid * self.edge_multiply # 3
             
            if((Hi > 0) and (HiHi > 0)):
                return M_ID(Hi-edgewidth-margin, Hi-margin, Hi+margin, Hi+margin+mid, HiHi+margin, HiHi+margin+edgewidth, unit, sensorgroup)
            else:
                return M_ID(HiHi-edgewidth-margin, HiHi-margin, HiHi+margin, HiHi+margin+mid, Hi+margin, Hi+margin+edgewidth, unit, sensorgroup)
            
        elif((Hi != None) and (HiHi == None)):
            mid = abs(Hi*self.double_ratio) #0.7
            margin = (Hi-mid)/2
            return M_ID(Hi-mid-margin, Hi-margin, Hi+margin, Hi+(mid*self.double_edge_multiply)+margin, None, None, unit, sensorgroup)
        
        else:
            pass
        
    def M_ID_Choose_Points(self):
        for MID in self.M_IDs:
            if(MID.Rhl != None and MID.Rhh != None):
                MID.pointLow = MID.Rlh
                MID.pointMid = (MID.Rmh-MID.Rml)/2 + MID.Rml
                MID.pointHigh= MID.Rhl
                MID.cal_testsignals()
            else:
                MID.pointLow = MID.Rlh
                MID.pointMid = MID.Rml
                MID.cal_testsignals()
            
        return self.M_IDs
    
    def fixunit(self, unit1):
        d = str(unit1)
        u = str("μ")
        
        if(ord(d[0]) == 181):
            return (u + d[1:])
        else:
            return unit1
        

class M_ID(object):

    def __init__(self, Rll, Rlh, Rml, Rmh, Rhl, Rhh, unit, sensorgroup):
        self.Rll = Rll
        self.Rlh = Rlh
        self.Rml = Rml
        self.Rmh = Rmh
        self.Rhl = Rhl
        self.Rhh = Rhh
        self.unit = unit
        self.name = None
        self.pointLow = None
        self.pointMid= None
        self.pointHigh = None
        self.testsignals=[]
        self.testlevels=[]
        self.testlevelunit = None
        self.sensorgroup = sensorgroup
    
    def print_point(self):
        if(self.Rhl != None and self.Rhh != None):
            print("%-5s: %8.2f %8.2f %8.2f %s"  % (self.name, self.pointLow, self.pointMid, self.pointHigh, self.unit.replace(u"\u03bc", chr(181))))
        else:
            print("%-5s: %8.2f %8.2f          %s"  % (self.name, self.pointLow, self.pointMid, self.unit.replace(u"\u03bc", chr(181))))
        
        
    def cal_testsignals(self):
        if(self.Rhl != None and self.Rhh != None):
            self.testsignals.append(self.convert(self.pointLow, self.unit, self.sensorgroup))
            self.testsignals.append(self.convert(self.pointMid, self.unit, self.sensorgroup))
            self.testsignals.append(self.convert(self.pointHigh, self.unit, self.sensorgroup))
            self.testlevels.append(self.pointLow)
            self.testlevels.append(self.pointMid)
            self.testlevels.append(self.pointHigh)
            
        else:
            self.testsignals.append(self.convert(self.pointLow, self.unit, self.sensorgroup))
            self.testsignals.append(self.convert(self.pointMid, self.unit, self.sensorgroup))
            self.testlevels.append(self.pointLow)
            self.testlevels.append(self.pointMid)
        
        
    def convert(self, value, unit, sensorgroup):
        if(unit == "mm" and sensorgroup == "group 3"):
            self.testlevelunit = "V"
            return (-value*7.87)-10
        
        elif(unit == "μmPP" and sensorgroup == "group 3"):
            self.testlevelunit = "mV@80Hz"
            return ((value * 7.87) / 2) / math.sqrt(2)

        elif(unit == "mm/s rms" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return (value * 2 * math.pi * 80 * 10.2 /1000)
        
        elif(unit == "mm/s rms" and sensorgroup == "group 2"):
            self.testlevelunit = "mV@160Hz"
            return (value * 2 * math.pi * 160 * 1.02 /1000)

        elif(unit == "mm/s rms" and sensorgroup == "group 4"):
            self.testlevelunit = "mV@80Hz"
            return (value * 100)
        
        elif(unit == "rpm" and sensorgroup == "group 3"):
            self.testlevelunit = "Hz ~1V"
            return value/60
        
        elif(unit == "m/s² rms" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return value * 10.2

        elif(unit == "m/s² rms" and sensorgroup == "group 2"):
            self.testlevelunit = "mV@80Hz"
            return value * 1.02
        
        elif(unit == "μm" and sensorgroup == "group 3"):
            self.testlevelunit = "V"
            return ((-value*7.87)-10000)/1000
        
        elif(unit == "g rms" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return value * 100
        
        elif(unit == "μm pp" and sensorgroup == "group 3"):
            self.testlevelunit = "mV@80Hz"
            return ((value * 7.87) / 2) / math.sqrt(2)
        
        elif(unit == "g PP" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"    
            return value *100 / math.sqrt(2) / 2
        
        elif(unit == "mm/s PP" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return (value * 2 * math.pi * 80 * 10.2 /1000 / 2 / math.sqrt(2))
        
        elif(unit == "inch/s rms" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return (value * 2 * math.pi * 80 * 10.2 /1000 / 25.4)
        
        elif(unit == "g pp" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return (value / 2 / math.sqrt(2))

        elif(unit == "mm/s 0-PK" and sensorgroup == "group 2"):
            self.testlevelunit = "mV@160Hz"
            return (value * 2 * math.pi * 160 * 1.02 /1000/ math.sqrt(2))

        elif(unit == "m/s² 0-PK" and sensorgroup == "group 2"):
            self.testlevelunit = "mV@80Hz"
            return value * 1.02 / math.sqrt(2)

        elif(unit == "mm/s 0-PK" and sensorgroup == "group 1"):
            self.testlevelunit = "mV@80Hz"
            return (value * 2 * math.pi * 80 * 10.2 /1000/ math.sqrt(2))

        elif(unit == "inch/s rms" and sensorgroup == "group 5"):
            self.testlevelunit = "mV@80Hz"
            return (value * 145)
        
        else:
            print("No unit match: " + str(unit) + ". No sensorgroup match: " + str(sensorgroup))
            return None
