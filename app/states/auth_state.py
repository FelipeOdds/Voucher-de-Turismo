import reflex as rx
import bcrypt
import secrets
from app.models import Tripulante


class AuthState(rx.State):
    token: str = rx.Cookie("")
    logged_in_user: Tripulante = {
        "id": 0,
        "nome": "",
        "email": "",
        "senha_hash": "",
        "token": None,
    }
    is_loading: bool = False
    login_error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.token != ""

    @rx.event
    async def check_login(self):
        if not self.is_authenticated:
            if self.router.page.path not in ["/login", "/404"]:
                return rx.redirect("/login")
        else:
            async with rx.asession() as session:
                result = await session.execute(
                    rx.text(
                        "SELECT id, nome, email, senha_hash, token FROM tripulante WHERE token = :token"
                    ),
                    {"token": self.token},
                )
                user_data = result.first()
                if user_data:
                    self.logged_in_user = Tripulante(
                        id=user_data[0],
                        nome=user_data[1],
                        email=user_data[2],
                        senha_hash=user_data[3],
                        token=user_data[4],
                    )
                    if self.router.page.path == "/login":
                        return rx.redirect("/select-vessel")
                else:
                    self.logout()

    @rx.event
    async def login(self, form_data: dict):
        self.is_loading = True
        self.login_error_message = ""
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        if not email or not password:
            self.login_error_message = "Email e senha são obrigatórios."
            self.is_loading = False
            return
        async with rx.asession() as session:
            result = await session.execute(
                rx.text(
                    "SELECT id, nome, email, senha_hash, token FROM tripulante WHERE email = :email"
                ),
                {"email": email},
            )
            user_data = result.first()
            if user_data and bcrypt.checkpw(
                password.encode("utf-8"), user_data[3].encode("utf-8")
            ):
                new_token = secrets.token_hex(32)
                await session.execute(
                    rx.text("UPDATE tripulante SET token = :token WHERE id = :id"),
                    {"token": new_token, "id": user_data[0]},
                )
                await session.commit()
                self.token = new_token
                self.logged_in_user = Tripulante(
                    id=user_data[0],
                    nome=user_data[1],
                    email=user_data[2],
                    senha_hash=user_data[3],
                    token=new_token,
                )
                self.is_loading = False
                return rx.redirect("/select-vessel")
            else:
                self.login_error_message = "Credenciais inválidas."
                self.is_loading = False

    @rx.event
    def logout(self):
        self.token = ""
        self.logged_in_user = {
            "id": 0,
            "nome": "",
            "email": "",
            "senha_hash": "",
            "token": None,
        }
        return rx.redirect("/login")