from copy import deepcopy


class BaseScan:
    attack_vectors = []
    @classmethod
    def load_param(cls, param_name: str):
        payloads = []
        template = {
            "method": "GET",
            "params": {param_name: ""}
        }
        for v in cls.attack_vectors:
            template["params"][param_name] = v
            payloads.append(deepcopy(template))

        return payloads

    @classmethod
    def load_body(cls, param_name):
        payloads = []
        template = {
            "method": "POST",
            "data": {param_name: ""}
        }
        for v in cls.attack_vectors:
            template["data"][param_name] = v
            payloads.append(deepcopy(template))

        return payloads

    @classmethod
    def load_json(cls, param_name):
        payloads = []
        template = {
            "method": "POST",
            "json": {param_name: ""}
        }
        for v in cls.attack_vectors:
            template["json"][param_name] = v
            payloads.append(deepcopy(template))

        return payloads


