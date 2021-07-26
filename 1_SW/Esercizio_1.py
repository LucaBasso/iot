import cherrypy
import json


class Converter(object):
    exposed=True

    def GET(self,*path,**query):
        if len(path)==0:#1 and path[0]=="converter":
            return self.myConverter(float(query["value"]),query["originalUnit"],query["targetUnit"])
        else:
            raise cherrypy.HTTPError(400,"Errore")

    def myConverter(self,value:float,unit1:str,unit2:str):
        valueOut=0.0
        if unit1=="K":
            if value<0:
                raise cherrypy.HTTPError(400, "Kelvin temperatures cannot be lower than 0")
            else:
                if unit2=="F":  #K2F
                    valueOut=((value-273.15)*9/5)+32
                elif unit2=="C":    #K2C
                    valueOut=value-273.15
                elif unit2=="K":    #K2K
                    valueOut=value
        elif unit1=="C":
            if value< -273.15:
                raise cherrypy.HTTPError(400, "Celsius temperatures cannot be lower than -273.15")
            else:
                if unit2=="F":
                    valueOut=(value*9/5)+32
                elif unit2=="C":
                    valueOut=value
                elif unit2=="K":
                    valueOut=value+273.15
        elif unit1=="F":
            if value< -459.67:
                raise cherrypy.HTTPError(400, "Fahrenheit temperatures cannot be lower than -459.67")
            else:
                if unit2=="F":
                    valueOut=value
                elif unit2=="C":
                    valueOut=(value-32)*5/9
                elif unit2=="K":
                    valueOut=((value-32)*5/9)+273.15
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

    cherrypy.config.update({'server.socket_host':'0.0.0.0'})
    cherrypy.config.update({'server.socket_port':8080})

    cherrypy.engine.start()
    cherrypy.engine.block()