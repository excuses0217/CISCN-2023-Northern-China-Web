import logging
import os
import socket
import socketserver
import sys
import traceback
import xmlrpc.server

try:
    import fcntl
except ImportError:
    # For Windows
    fcntl = None

import jsonrpclib
from jsonrpclib import Fault
from jsonrpclib.jsonrpc import USE_UNIX_SOCKETS


def get_version(request):
    # must be a dict
    if 'jsonrpc' in request.keys():
        return 2.0
    if 'id' in request.keys():
        return 1.0
    return None


def validate_request(request):
    if not isinstance(request, dict):
        fault = Fault(
            -32600, 'Request must be {}, not %s.' % type(request)
        )
        return fault
    rpcid = request.get('id', None)
    version = get_version(request)
    if not version:
        fault = Fault(-32600, 'Request %s invalid.' % request, rpcid=rpcid)
        return fault
    request.setdefault('params', [])
    method = request.get('method', None)
    params = request.get('params')
    if not method or not isinstance(method, str) or \
            not isinstance(params, (list, dict, tuple)):
        fault = Fault(
            -32600, 'Invalid request parameters or method.', rpcid=rpcid
        )
        return fault
    return True


class SimpleJSONRPCDispatcher(xmlrpc.server.SimpleXMLRPCDispatcher):

    def __init__(self, encoding=None):
        xmlrpc.server.SimpleXMLRPCDispatcher.__init__(
            self, allow_none=True, encoding=encoding)

    def _marshaled_dispatch(self, data, dispatch_method=None):
        response = None
        try:
            request = jsonrpclib.loads(data)
        except Exception as e:
            fault = Fault(-32700, 'Request %s invalid. (%s)' % (data, e))
            response = fault.response()
            return response
        if not request:
            fault = Fault(-32600, 'Request invalid -- no request data.')
            return fault.response()
        if isinstance(request, list):
            # This SHOULD be a batch, by spec
            responses = []
            for req_entry in request:
                result = validate_request(req_entry)
                if type(result) is Fault:
                    responses.append(result.response())
                    continue
                resp_entry = self._marshaled_single_dispatch(req_entry)
                if resp_entry is not None:
                    responses.append(resp_entry)
            if len(responses) > 0:
                response = '[%s]' % ','.join(responses)
            else:
                response = ''
        else:
            result = validate_request(request)
            if type(result) is Fault:
                return result.response()
            response = self._marshaled_single_dispatch(request)
        return response

    def _marshaled_single_dispatch(self, request):
        # TODO - Use the multiprocessing and skip the response if
        # it is a notification
        # Put in support for custom dispatcher here
        # (See SimpleXMLRPCServer._marshaled_dispatch)
        method = request.get('method')
        params = request.get('params')
        try:
            response = self._dispatch(method, params)
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            fault = Fault(-32603, '%s:%s' % (exc_type, exc_value))
            return fault.response()
        if 'id' not in request.keys() or request['id'] is None:
            # It's a notification
            return None
        try:
            response = jsonrpclib.dumps(response,
                                        version=get_version(request),
                                        methodresponse=True,
                                        rpcid=request['id']
                                        )
            return response
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            fault = Fault(-32603, '%s:%s' % (exc_type, exc_value))
            return fault.response()

    def _dispatch(self, method, params):
        func = None
        try:
            func = self.funcs[method]
        except KeyError:
            if self.instance is not None:
                if hasattr(self.instance, '_dispatch'):
                    return self.instance._dispatch(method, params)
                else:
                    try:
                        func = xmlrpc.server.resolve_dotted_attribute(
                            self.instance,
                            method,
                            True
                            )
                    except AttributeError:
                        pass
        if func is not None:
            try:
                if isinstance(params, list):
                    response = func(*params)
                else:
                    response = func(**params)
                return response
            # except TypeError:
            #     return Fault(-32602, 'Invalid parameters.')
            except Exception:
                err_lines = traceback.format_exc().splitlines()
                trace_string = '%s | %s' % (err_lines[-3], err_lines[-1])
                fault = jsonrpclib.Fault(-32603, 'Server error: %s' %
                                         trace_string)
                return fault
        else:
            return Fault(-32601, 'Method %s not supported.' % method)


class SimpleJSONRPCRequestHandler(
        xmlrpc.server.SimpleXMLRPCRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        response = """
        
<!DOCTYPE html>
<html lang="zh">
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RPC API</title>

<style type="text/css">
	.wrapper {
	  text-align: center;
	  padding: 2rem;
	  background-size: 100%;
	  background-repeat: no-repeat;
	  height: 600px;
	  box-sizing: border-box;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  position: absolute;
	  top: 0;
	  right: 0;
	  bottom: 0;
	  left: 0;
	  overflow: auto;
	}

	.content {
	  font-family: 'Rubik';
	  font-size: 6rem;
	  font-weight: 900;
	  letter-spacing: .04em;
	  display: block;
	  word-spacing: 3rem;
	  line-height: 1.4;
	  text-transform: uppercase;
	}
	.content div {
	  display: inline;
	}
	.content span {
	  display: inline-block;
	}
	.content span:hover {
	  animation: wobble 200ms;
	}
	.content span:nth-child(1n) {
	  color: #F18829;
	  text-shadow: #ef7b11 1px 1px, #f7bd89 -1px -1px, #f37841 -2px -2px 6px, #f49d4f -2px -2px, #f49d4f -1px -2px, #f49d4f -1px -3px, #f49d4f -2px -4px, #f49d4f -2px -5px, #f49d4f -3px -6px, #F18829 -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(-3deg);
	}
	.content span:nth-child(2n) {
	  color: #00B9ED;
	  text-shadow: #00a5d4 1px 1px, #54d9ff -1px -1px, #08f2ff -2px -2px 6px, #17ccff -2px -2px, #17ccff -1px -2px, #17ccff -1px -3px, #17ccff -2px -4px, #17ccff -2px -5px, #17ccff -3px -6px, #00B9ED -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(3deg) translateY(4%);
	}
	.content span:nth-child(3n) {
	  color: #ED5053;
	  text-shadow: #eb393c 1px 1px, #f7acae -1px -1px, #ef6780 -2px -2px 6px, #f17577 -2px -2px, #f17577 -1px -2px, #f17577 -1px -3px, #f17577 -2px -4px, #f17577 -2px -5px, #f17577 -3px -6px, #ED5053 -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(-3deg);
	}
	.content span:nth-child(4n) {
	  color: #00AF4F;
	  text-shadow: #009643 1px 1px, #16ff7f -1px -1px, #00c939 -2px -2px 6px, #00d861 -2px -2px, #00d861 -1px -2px, #00d861 -1px -3px, #00d861 -2px -4px, #00d861 -2px -5px, #00d861 -3px -6px, #00AF4F -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(-2deg);
	}
	.content span:nth-child(5n) {
	  color: #8E509F;
	  text-shadow: #7f478e 1px 1px, #ba8fc6 -1px -1px, #8e5cad -2px -2px 6px, #a266b2 -2px -2px, #a266b2 -1px -2px, #a266b2 -1px -3px, #a266b2 -2px -4px, #a266b2 -2px -5px, #a266b2 -3px -6px, #8E509F -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(3deg) translateY(-2%);
	}
	.content span:nth-child(6n) {
	  color: #F9DE00;
	  text-shadow: #e0c700 1px 1px, #ffee60 -1px -1px, #ffbe14 -2px -2px 6px, #ffe723 -2px -2px, #ffe723 -1px -2px, #ffe723 -1px -3px, #ffe723 -2px -4px, #ffe723 -2px -5px, #ffe723 -3px -6px, #F9DE00 -4px -7px, rgba(0, 0, 5, 0.4) 3px 4px 5px, rgba(0, 0, 5, 0.2) -3px -4px 5px;
	  transform: rotate(5deg) translateY(1%);
	}

	@keyframes wobble {
	  50% {
		transform: translate(2%, 2%);
	  }
	}
</style>

</head>
<body>

<div class="wrapper">
  <div class="content">xx集团内部测试接口</div>
</div>

</body>
</html>
        """

        self.send_header("Content-type", "text/html;charset=UTF-8;")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode())
        self.wfile.flush()
        self.connection.shutdown(1)
        return


    def do_POST(self):
        if not self.is_rpc_path_valid():
            self.report_404()
            return
        try:
            max_chunk_size = 10*1024*1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                chunk = self.rfile.read(chunk_size).decode()
                L.append(chunk)
                size_remaining -= len(L[-1])
            data = ''.join(L)
            response = self.server._marshaled_dispatch(data)
            self.send_response(200)
        except Exception:
            self.send_response(500)
            err_lines = traceback.format_exc().splitlines()
            trace_string = '%s | %s' % (err_lines[-3], err_lines[-1])
            fault = jsonrpclib.Fault(-32603, 'Server error: %s' % trace_string)
            response = fault.response()
        if response is None:
            response = ''
        self.send_header("Content-type", "application/json-rpc")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        if isinstance(response, bytes):
            self.wfile.write(response)
        else:
            self.wfile.write(response.encode())
        self.wfile.flush()
        self.connection.shutdown(1)


class SimpleJSONRPCUnixRequestHandler(SimpleJSONRPCRequestHandler):

    disable_nagle_algorithm = False

#socketserver.TCPServer
class SimpleJSONRPCServer(socketserver.ThreadingTCPServer, SimpleJSONRPCDispatcher):

    allow_reuse_address = True

    def __init__(self, addr, requestHandler=SimpleJSONRPCRequestHandler,
                 logRequests=True, encoding=None, bind_and_activate=True,
                 address_family=socket.AF_INET):
        self.logRequests = logRequests
        SimpleJSONRPCDispatcher.__init__(self, encoding)
        self.address_family = address_family

        if USE_UNIX_SOCKETS and address_family == socket.AF_UNIX:
            # Unix sockets can't be bound if they already exist in the
            # filesystem. The convention of e.g. X11 is to unlink
            # before binding again.
            if os.path.exists(addr):
                try:
                    os.unlink(addr)
                except OSError:
                    logging.warning("Could not unlink socket %s", addr)

            if requestHandler == SimpleJSONRPCRequestHandler:
                requestHandler = SimpleJSONRPCUnixRequestHandler

        socketserver.TCPServer.__init__(
            self, addr, requestHandler, bind_and_activate)
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)


class CGIJSONRPCRequestHandler(SimpleJSONRPCDispatcher):

    def __init__(self, encoding=None):
        SimpleJSONRPCDispatcher.__init__(self, encoding)

    def handle_jsonrpc(self, request_text):
        response = self._marshaled_dispatch(request_text)
        print('Content-Type: application/json-rpc')
        print('Content-Length: %d' % len(response))
        print()
        sys.stdout.write(response)

    handle_xmlrpc = handle_jsonrpc
