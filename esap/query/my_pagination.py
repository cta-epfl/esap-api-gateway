from rest_framework import pagination
from rest_framework.response import Response


# Custom Pagination is used to be able to set the page_size from the client.
# And to return extra information in the response that can be used by the client.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'  # this indicates that the client can control page_size with this parameter
    max_page_size = 500

    # nv:24jul2017
    # function to fill the custom 'pages' property in the response
    def get_number_of_pages(self):
        count = self.page.paginator.count
        page_size = self.request.query_params.get('page_size')
        if page_size is None:
            page_size = self.page_size

        number_of_pages = int(count) / int(page_size)
        return round(number_of_pages + 0.5)

    # nv:24jul2017
    # overriding 'get_paginated_response' to return custom properties in the response
    # Note how properties from the request are also returned,
    # this mechanism could perhaps also be used to handshake id's and guarantee correct order of execution.
    def get_paginated_response(self, data):
        return Response({
            'description': 'ESAP API Gateway',
            'version': '18 aug 2020',
            'requested_page': self.request.query_params.get('page', '1'),
            'requested_page_size': self.request.query_params.get('page_size'),
            'default_page_size': self.page_size,
            'max_page_size': self.max_page_size,
            'count': self.page.paginator.count,
            'pages': self.get_number_of_pages(),
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data,
        })
