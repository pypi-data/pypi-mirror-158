from typing import Any

import justpy as jp

from .element import Element


class Html(Element):

    def __init__(self, content: str = ''):
        """HTML Element

        Renders arbitrary HTML onto the page. `Tailwind <https://tailwindcss.com/>`_ can be used for styling.

        :param content: the HTML code to be displayed
        """
        view = jp.QDiv(temp=False)
        super().__init__(view)
        self.content = content

    @property
    def content(self) -> str:
        return self.view.inner_html

    @content.setter
    def content(self, content: Any):
        self.set_content(content)

    def set_content(self, content: str):
        self.view.inner_html = content
