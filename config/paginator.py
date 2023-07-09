from rest_framework.pagination import LimitOffsetPagination
class Pagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 2
    limit_query_param = "limit"
    offset_query_param = "offset"
