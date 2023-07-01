

class RequestCache:

    requests = {}

    @classmethod
    def add_request(cls, request, launch_id):
        cls.requests[launch_id] = request

    @classmethod
    def get_request(cls, launch_id):
        return cls.requests[launch_id]
