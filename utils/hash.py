# stdlib imports
import string
import random


def random_base36_string(
        size=10, chars=string.ascii_uppercase + string.digits):
    """creates a random base 36 string.
    Not the best way to avoid collision. But good enough for this situation
    """
    return ''.join(random.choice(chars) for _ in xrange(size))
