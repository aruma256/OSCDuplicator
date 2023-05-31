from flet import Page, app

from prototype_app import PrototypeApp


def main(page: Page):
    page.title = "OSC Duplicator"
    page.horizontal_alignment = "center"
    page.window_width, page.window_height = 600, 800
    page.update()

    app = PrototypeApp()

    page.add(app)


if __name__ == "__main__":
    app(target=main)
