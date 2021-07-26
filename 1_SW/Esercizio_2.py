import cherrypy
import json


class Converter(object):
    exposed=True

    def GET(self,*path,**query):
        if len(path)==3:#1 and path[0]=="converter":
            return self.myConverter(float(path[0]),path[1],path[2])
        else:
            raise cherrypy.HTTPError(400,"Errore")

    def PUT(self,*path,**query):
        stringIn=cherrypy.request.body.read()
        dictIn=json.loads(stringIn)
        return self.myConverter(dictIn["values"], dictIn["originalUnit"], dictIn["targetUnit"])

    def myConverter(self,value,unit1:str,unit2:str):
        """Converts a list of values from a temperature unit to another one

        :param value: list of temperatures to convert
        :param unit1: temperature unit to convert from
        :param unit2: temperature unit to convert to"""
        valueOut=[]
        if unit1=="K":
            if unit2=="F":  #K2F
                for i in range(len(value)-1):
                    if value[i] < 0:
                        raise cherrypy.HTTPError(400, "Kelvin temperatures cannot be lower than 0")
                    else:
                        valueOut.append(((value[i] - 273.15) * 9 / 5) + 32)
            elif unit2=="C":    #K2C
                for i in range(len(value) - 1):
                    if value[i] < 0:
                        raise cherrypy.HTTPError(400, "Kelvin temperatures cannot be lower than 0")
                    else:
                        valueOut.append(value[i]-273.15)
            elif unit2=="K":    #K2K
                for i in range(len(value) - 1):
                    if value[i] < 0:
                        raise cherrypy.HTTPError(400, "Kelvin temperatures cannot be lower than 0")
                    else:
                        valueOut.append(value[i])
            else:
                raise cherrypy.HTTPError(400, "Second unit must be k, C or F")
        elif unit1=="C":
            if unit2=="F":
                for i in range(len(value) - 1):
                    if value[i] < -273.15:
                        raise cherrypy.HTTPError(400, "Celsius temperatures cannot be lower than -273.15")
                    else:
                        valueOut.append((value[i]*9/5)+32)
            elif unit2=="C":
                for i in range(len(value) - 1):
                    if value[i] < -273.15:
                        raise cherrypy.HTTPError(400, "Celsius temperatures cannot be lower than -273.15")
                    else:
                        valueOut.append(value[i])
            elif unit2=="K":
                for i in range(len(value) - 1):
                    if value[i] < -273.15:
                        raise cherrypy.HTTPError(400, "Celsius temperatures cannot be lower than -273.15")
                    else:
                        valueOut.append(value[i]+273.15)
            else:
                raise cherrypy.HTTPError(400, "Second unit must be k, C or F")
        elif unit1=="F":
            if unit2=="F":
                for i in range(len(value) - 1):
                    if value[i] < -459.67:
                        raise cherrypy.HTTPError(400, "Fahrenheit temperatures cannot be lower than -459.67")
                    else:
                        valueOut.append(value[i])
            elif unit2=="C":
                for i in range(len(value) - 1):
                    if value[i] < -459.67:
                        raise cherrypy.HTTPError(400, "Fahrenheit temperatures cannot be lower than -459.67")
                    else:
                        valueOut.append((value[i]-32)*5/9)
            elif unit2=="K":
                for i in range(len(value) - 1):
                    if value[i] < -459.67:
                        raise cherrypy.HTTPError(400, "Fahrenheit temperatures cannot be lower than -459.67")
                    else:
                        valueOut.append(((value[i]-32)*5/9)+273.15)
            else:
                raise cherrypy.HTTPError(400, "Second unit must be k, C or F")
        else:
            raise cherrypy.HTTPError(400,"First unit must be k, C or F")

        dict={}
        dict.update({"value":value})
        dict.update({"originalUnit":unit1})
        dict.update({"convertedValue":valueOut})
        dict.update({"targetUnit":unit2})

        return json.dumps(dict)

if __name__ == "__main__":
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True,
        }
    }
    cherrypy.tree.mount(Converter(),'/converter',conf)

    cherrypy.config.update({'server.socket_host':'127.0.0.1'})
    cherrypy.config.update({'server.socket_port':8080})

    cherrypy.engine.start()
    cherrypy.engine.block()