import reflex as rx
from app.states.auth_state import AuthState
from app.states.init_state import InitState
from app.pages.login import login_page
from app.pages.select_vessel import select_vessel_page
from app.pages.dashboard import dashboard_page


def protected_page(content: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_authenticated,
            content,
            rx.el.div(
                rx.el.h1("Acesso Negado", class_name="text-2xl font-bold"),
                rx.el.p("Você precisa estar logado para acessar esta página."),
                rx.el.a("Ir para Login", href="/login"),
                class_name="flex flex-col items-center justify-center h-screen",
            ),
        )
    )


def index() -> rx.Component:
    return protected_page(dashboard_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index, route="/", on_load=[AuthState.check_login, InitState.initialize_database]
)
app.add_page(login_page, route="/login", on_load=AuthState.check_login)
app.add_page(select_vessel_page, route="/select-vessel", on_load=AuthState.check_login)