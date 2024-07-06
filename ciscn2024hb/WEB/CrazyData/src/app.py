from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

server = SimpleJSONRPCServer(('0.0.0.0', 80))
server.register_function(lambda x,y: x+y, 'add')
server.register_function(lambda x: x, 'ping')
server.serve_forever()
