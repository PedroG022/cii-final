import base64
from typing import Optional

import flet as ft
import pandas as pd
import requests
from flet_core import Control
from fletrt import Route

from src.loader import get_recommendations


class Index(Route):
    def __init__(self):
        super().__init__()

        self.list: Optional[ft.Column] = None
        self.frame = pd.read_json('./livros.json')

    def on_click(self, e):
        self.list.controls.clear()

        try:
            original = self.frame[self.frame['ISBN'] == int(e)]
            itens = original.to_dict(orient='records')[0]

            self.list.controls.append(ft.Text('Original'))
            self.list.controls.append(ft.Row(
                [
                    ft.Image(src_base64=download_image_to_base64(itens['imagem']), fit=ft.ImageFit.FILL, height=100,
                             width=100, ),
                    ft.Column(
                        [
                            ft.Text(itens['nome']),
                            ft.Text(itens['autor'])
                        ]
                    )
                ]
            ))

            self.list.controls.append(ft.Text('Recomendações'))

            recommendations = get_recommendations(e)

            for id in recommendations:
                recommendation = self.frame[self.frame['ISBN'] == int(id)]
                book = recommendation.to_dict(orient='records')[0]

                img = download_image_to_base64(book['imagem'])

                cont = ft.Row(
                    [
                        ft.Image(src_base64=img, fit=ft.ImageFit.FILL, height=100,
                                 width=100, ),
                        ft.Column(
                            [
                                ft.Text(book['nome']),
                                ft.Text(book['autor'])
                            ]
                        )
                    ]
                )

                self.list.controls.append(cont)
                self.page.update()

        except Exception as e:
            self.page.views[-1].controls.append(ft.Text(f"Error: {e}", color=ft.colors.ERROR))
            self.page.update()

    def body(self) -> Control:
        prompt = ft.TextField(hint_text='Insert a book\'s ISBN', width=200)

        confirm = ft.ElevatedButton(text='Confirm', height=50, width=200,
                                    on_click=lambda _: self.on_click(prompt.value))

        self.list = ft.Column()

        return ft.Column([prompt, confirm, self.list], scroll=ft.ScrollMode.ALWAYS, expand=True)

    def view(self):
        base = super().view()

        base.vertical_alignment = ft.MainAxisAlignment.CENTER
        base.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        base.padding = 64

        return base


def download_image_to_base64(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'})
    if response.status_code == 200:
        image_bytes = response.content
        encoded_string = base64.b64encode(image_bytes).decode('utf-8')
        return encoded_string
    else:
        raise Exception("Error fetching image from URL")
