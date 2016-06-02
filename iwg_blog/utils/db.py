from django.db.models import Func


class Position(Func):
    """
    Returns position of substring in string
    """
    function = 'POSITION'
    arg_joiner = ' IN '

    def __init__(self, expression1, expression2, **extra):
        super(Position, self).__init__(expression1, expression2, **extra)
