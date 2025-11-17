import reflex as rx
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.pages.select_vessel import select_vessel_page
from app.pages.register import register_page
from app.pages.forgot_password import forgot_password_page
from app.pages.reset_password import reset_password_page
from app.states.init_state import InitState
from app.states.auth_state import AuthState


class RootState(rx.State):
    @rx.event
    async def on_load(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield auth_state.check_login()
            return
        init_state = await self.get_state(InitState)
        if not init_state.db_initialized:
            yield InitState.initialize_database()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin="anonymous"
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(forgot_password_page, route="/forgot-password")
app.add_page(reset_password_page, route="/reset-password")
app.add_page(dashboard_page, route="/", on_load=RootState.on_load)
app.add_page(select_vessel_page, route="/select-vessel", on_load=RootState.on_load)