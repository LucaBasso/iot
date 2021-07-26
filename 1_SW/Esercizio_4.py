import cherrypy
import json
import os


class FreeboardExample(object):
    exposed=True

    def GET(self,*path,**query):
        return open("./freeboard/index.html")

    def POST(self,*path,**query):
        file=open('./freeboard/dashboard/dashboard.json','w')
        #if file==OSError:
        #    file=open('./dashboard/dashboard copy.json','w')
        file.write(query["json_string"])
        file.close()

if __name__=="__main__":
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True,
            'tools.staticdir.root':os.path.abspath(os.getcwd()),
        },
        '/css':{
            'tools.staticdir.on':True,
            'tools.staticdir.dir':'./freeboard/css'
        },
        '/js':{
            'tools.staticdir.on':True,
            'tools.staticdir.dir':'./freeboard/js'
        },
        '/img':{
            'tools.staticdir.on':True,
            'tools.staticdir.dir':'./freeboard/img'
        },
        '/dashboard':{
            'tools.staticdir.on':True,
            'tools.staticdir.dir':'./freeboard/dashboard'
        },
        '/plugins':{
            'tools.staticdir.on':True,
            'tools.staticdir.dir':'./freeboard/plugins'
        }
    }
    cherrypy.tree.mount(FreeboardExample(),'/',conf)

    cherrypy.config.update({'server.socket_host':'127.0.0.1'})
    cherrypy.config.update({'server.socket_port':8080})

    cherrypy.engine.start()
    cherrypy.engine.block()