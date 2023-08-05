import justpy as jp

from .group import Group


class Menu(Group):

    def __init__(self, *, value: bool = False):
        """Menu

        Creates a menu.

        :param value: whether the menu is already opened (default: `False`)
        """
        view = jp.QMenu(value=value, temp=False)

        super().__init__(view)

    def open(self):
        self.view.value = True

    def close(self):
        self.view.value = False
