
class sensorgroup(object):

    def __init__(self):
        pass

    def getgroup(self, sensor):
        if(sensor == "ASA-062"):
            return "group 1"
        
        elif(sensor == "ASA-063"):
            return "group 1"
        
        elif(sensor == "ASA-069"):
            return "group 2"
        
        elif(sensor == "DS-1051"):
            return "group 3"
        
        elif(sensor == "DS-1053"):
            return "group 3"
        
        elif(sensor == "DS-105x"):
            return "group 3"
        
        elif(sensor == "DS-822"):
            return "group 3"
        
        elif(sensor == "VS-0169"):
            return "group 4"

        elif(sensor == "330901"):
            return "group 3"

        elif(sensor == "3300XL NSV"):
            return "group 3"

        elif(sensor == "DS-821"):
            return "group 3"

        elif(sensor == "BN3500"):
            return "group 3"

        elif(sensor == "5485C-004"):
            return "group 5"

        elif(sensor == "330400"):
            return "group 1"
      
        else:
            print("Sensor not found: " + sensor)
            return None


        
