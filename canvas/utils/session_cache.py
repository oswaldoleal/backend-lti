

class PyLTISessionCache:

    requests = {}

    @classmethod
    def add_request(cls, request, launch_id):
        cls.requests[launch_id] = request

    @classmethod
    def get_request(cls, launch_id):
        return cls.requests[launch_id]
    
    launchs = {}

    @classmethod
    def add_launch(cls, launch, launch_id):
        cls.launchs[launch_id] = launch

    @classmethod
    def get_launch(cls, launch_id):
        return cls.launchs[launch_id]
