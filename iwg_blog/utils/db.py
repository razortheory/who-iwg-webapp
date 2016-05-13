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
    def order_by_array(self, ordering_array, field_name=None, separator='\a'):
        field_name = field_name or 'pk'
        return self.annotate(
            element_position=Position(
                Concat(Value(separator), F(field_name), Value(separator)),
                Value(separator + separator.join(map(str, ordering_array)) + separator),
            )
        ).order_by('element_position')
