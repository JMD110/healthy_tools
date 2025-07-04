import reflex as rx

from rxconfig import config
from typing import List
import random
import time
from .generate_data_deepseek import generate_data


class State(rx.State):
    """The app state."""

    yami: str = "you are the best!"
    is_dark: bool = True
    is_loading: bool = False
    is_show: bool = True
    for_what: str = "代码写的好"
    show_input_box: bool = False
    show_text_box: bool = True
    data: List[str] = ["you are the best!"]

    @rx.event
    async def change_data(self) -> None:
        self.show_input_box = not self.show_input_box
        self.show_text_box = not self.show_text_box
        self.is_loading = True
        self.is_show = False
        yield
        if self.show_text_box:
            self.set_new_data()
        self.is_loading = False
        self.is_show = True
        yield

    @rx.event
    def get_data(self):
        self.yami = self.data.pop(0)
        self.data.append(self.yami)

    def set_new_data(self) -> None:
        self.data = generate_data(self.for_what)
        self.get_data()


def index() -> rx.Component:
    return rx.box(
        rx.cond(
            State.is_loading,
            rx.center(
                rx.spinner(size="1", color="green"),
                position="relative",
                height="100vh",
                width="100vw",
                z_index=9999,
            ),
        ),
        rx.box(
                rx.image(
                    src=rx.asset("refresh.svg"),
                    on_click=State.change_data,
                    width="30px",
                ),
                position="absolute",
                top="10px",
                right="10px",
                z_index=1000,
            ),
        rx.cond(
            ~State.is_loading,
            rx.center(
                rx.vstack(
                    rx.cond(
                        State.show_input_box,
                        rx.vstack(
                            rx.input(
                                value=State.for_what,
                                on_change=State.set_for_what,
                                max_length=10,
                            ),
                        ),
                    ),
                    rx.cond(
                        State.show_text_box,
                        rx.text(
                            State.yami,
                            font_size="2em",
                            color="green",
                            on_click=State.get_data,
                            margin="20px",
                        ),
                    ),
                    spacing="1",
                ),
                height="100vh",
                position="relative",
                width="100vw",
            ),
        ),
        height="100vh",
        position="relative",
        width="100vw",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
    )
)
app.add_page(index)
