from enum import Enum

from qfluentwidgets import Theme, FluentIconBase, getIconColor


class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    PREVIOUS = 'previous'
    NEXT = 'next'
    FIRST = 'first'
    LAST = 'last'
    CHIP = 'chip'
    GRID = 'grid'

    def path(self, theme=Theme.AUTO):
        return f':/icon/{self.value}_{getIconColor()}.svg'
