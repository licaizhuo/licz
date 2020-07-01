from rest_framework import status
from rest_framework.response import Response


class MyResponse(Response):

    def __init__(self, data_status=status.HTTP_200_OK, data_message=0,
                 results=None, headers=None, exception=False, **kwargs):
        data = {
            "status": data_status,
            "message": data_message
        }
        # print(results)
        if results:
            data['results'] = results

        data.update(kwargs)
        super().__init__(data=data, status=data_status,
                         headers=headers, exception=exception)
