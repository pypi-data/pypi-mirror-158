"""Query pools let a query run in the background when it
doesn't return within a given timeout. In that case the
result of the previous query is returned or raised. If
there is no result, the default value is returned.
"""

try:
    import gevent  # noqa F401
except ImportError:
    from .native import QueryPool

    CooperativeQueryPool = QueryPool
    NonCooperativeQueryPool = QueryPool
else:
    from .cooperative import CooperativeQueryPool  # noqa F401
    from .noncooperative import NonCooperativeQueryPool  # noqa F401
