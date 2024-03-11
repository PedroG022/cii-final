import flet as ft
from fletrt import Router

from src.pages.index import Index


def main(page: ft.Page):
    router = Router(page, routes={
        '/': Index(),
    })

    router.install()


if __name__ == '__main__':
    ft.app(target=main, port=40444)
