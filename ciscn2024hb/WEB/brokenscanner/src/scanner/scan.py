from scanner.plugins import *
from scanner.core.requester import Requester
import asyncio


async def scan(url, module: str, pos: list, param_name: str):

    Requester.init_sess()
    module_list = module.split('.')
    try:
        current_module = globals()[module_list[0]]
        current_module = getattr(current_module, module_list[1])
        if len(module_list) > 2:
            current_module = getattr(current_module, module_list[2])

        request_struct_list = []

        for p in pos:
            func_name = 'load'
            if p:
                func_name = func_name + '_' + p
            try:
                request_struct_list += getattr(current_module, func_name)(param_name)
            except Exception as e:
                continue

        task_list = []
        for request_struct in request_struct_list:
            task_list.append(Requester.request(url=url, **request_struct))

        result = await asyncio.gather(*task_list)

        await Requester.sess_close()
        return result
    except Exception as e:
        await Requester.sess_close()
        return [str(e)]

