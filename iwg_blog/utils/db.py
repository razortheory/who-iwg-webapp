from django.db.models import Func, Value, QuerySet, F
from django.db.models.functions import Concat


class Position(Func):
    """
    Returns position of substring in string
    """
    function = 'POSITION'
    arg_joiner = ' IN '

    def __init__(self, expression1, expression2, **extra):
        super(Position, self).__init__(expression1, expression2, **extra)


class OrderableQuerySet(QuerySet):
    def order_by_array(self, ordering_array):
        return self.annotate(
            element_position=Position(
                Concat(Value(','), F('pk'), Value(',')),
                Value(',%s,' % ','.join(map(str, ordering_array))),
            )
        ).order_by('element_position')
