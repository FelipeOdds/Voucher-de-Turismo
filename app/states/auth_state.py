import reflex as rx
import bcrypt
import uuid
import datetime
from typing import TypedDict, Optional
from app.models import Tripulante
from app.db import get_session


class AuthState(rx.State):
    logged_in_user: Tripulante | None = None
    is_authenticated: bool = False
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    token: str | None = rx.Cookie(name="token")

    @rx.event
    async def login(self, form_data: dict):
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Email e senha são obrigatórios."
            self.is_loading = False
            return
        async with get_session() as session:
            result = await session.execute(
                rx.text("SELECT * FROM tripulante WHERE email = :email"),
                {"email": email},
            )
            user_data = result.first()
        if user_data and bcrypt.checkpw(
            password.encode("utf-8"), user_data.senha_hash.encode("utf-8")
        ):
            user_dict = {
                c.name: getattr(user_data, c.name) for c in user_data.cursor.description
            }
            self.is_authenticated = True
            self.logged_in_user = Tripulante(**user_dict)
            self.token = self.logged_in_user["token"]
            from app.states.vessel_state import VesselState

            vessel_state = await self.get_state(VesselState)
            if vessel_state.selected_vessel_id:
                yield rx.redirect("/")
            else:
                yield rx.redirect("/select-vessel")
        else:
            self.error_message = "Email ou senha inválidos."
        self.is_loading = False

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.logged_in_user = None
        self.token = None
        return rx.redirect("/login")

    @rx.event
    async def check_login(self):
        if self.token:
            async with get_session() as session:
                result = await session.execute(
                    rx.text("SELECT * FROM tripulante WHERE token = :token"),
                    {"token": self.token},
                )
                user_data = result.first()
            if user_data:
                user_dict = {
                    c.name: getattr(user_data, c.name)
                    for c in user_data.cursor.description
                }
                self.is_authenticated = True
                self.logged_in_user = Tripulante(**user_dict)
                current_path = self.router.page.path
                if current_path == "/login":
                    from app.states.vessel_state import VesselState

                    vessel_state = await self.get_state(VesselState)
                    if vessel_state.selected_vessel_id:
                        return rx.redirect("/")
                    else:
                        return rx.redirect("/select-vessel")
                return
        self.is_authenticated = False
        current_path = self.router.page.path
        if current_path not in [
            "/login",
            "/register",
            "/forgot-password",
            "/reset-password",
        ]:
            return rx.redirect("/login")

    @rx.event
    async def register(self, form_data: dict):
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""
        nome = form_data.get("nome")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        if not all([nome, email, password, confirm_password]):
            self.error_message = "Todos os campos são obrigatórios."
            self.is_loading = False
            return
        if password != confirm_password:
            self.error_message = "As senhas não coincidem."
            self.is_loading = False
            return
        if len(password) < 8:
            self.error_message = "A senha deve ter no mínimo 8 caracteres."
            self.is_loading = False
            return
        async with get_session() as session:
            result = await session.execute(
                rx.text("SELECT id FROM tripulante WHERE email = :email"),
                {"email": email},
            )
            if result.first():
                self.error_message = "Este email já está em uso."
                self.is_loading = False
                return
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            new_token = str(uuid.uuid4())
            await session.execute(
                rx.text(
                    "INSERT INTO tripulante (nome, email, senha_hash, token, created_at, email_verified) VALUES (:nome, :email, :senha_hash, :token, :created_at, :email_verified)"
                ),
                params={
                    "nome": nome,
                    "email": email,
                    "senha_hash": hashed_password,
                    "token": new_token,
                    "created_at": datetime.datetime.utcnow(),
                    "email_verified": False,
                },
            )
            await session.commit()
        self.success_message = "Conta criada com sucesso! Você já pode fazer login."
        self.is_loading = False
        yield rx.redirect("/login")

    @rx.event
    async def forgot_password(self, form_data: dict):
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""
        email = form_data.get("email")
        if not email:
            self.error_message = "O campo de email é obrigatório."
            self.is_loading = False
            return
        async with get_session() as session:
            result = await session.execute(
                rx.text("SELECT id FROM tripulante WHERE email = :email"),
                {"email": email},
            )
            user = result.first()
            if not user:
                self.error_message = "Nenhum usuário encontrado com este email."
                self.is_loading = False
                return
            reset_token = str(uuid.uuid4())
            expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            await session.execute(
                rx.text(
                    "UPDATE tripulante SET reset_token = :token, reset_token_expires = :expires WHERE email = :email"
                ),
                params={"token": reset_token, "expires": expires, "email": email},
            )
            await session.commit()
        print(
            f"FAKE EMAIL: Link de recuperação para {email}: /reset-password?token={reset_token}"
        )
        self.success_message = "Se o email estiver correto, você receberá instruções para redefinir sua senha."
        self.is_loading = False

    @rx.event
    async def reset_password(self, form_data: dict):
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        token = self.router.page.params.get("token", "")
        if not all([password, confirm_password, token]):
            self.error_message = "Token inválido ou senhas não fornecidas."
            self.is_loading = False
            return
        if password != confirm_password:
            self.error_message = "As senhas não coincidem."
            self.is_loading = False
            return
        if len(password) < 8:
            self.error_message = "A senha deve ter no mínimo 8 caracteres."
            self.is_loading = False
            return
        async with get_session() as session:
            result = await session.execute(
                rx.text(
                    "SELECT id, reset_token_expires FROM tripulante WHERE reset_token = :token"
                ),
                {"token": token},
            )
            user = result.first()
            if not user or user.reset_token_expires < datetime.datetime.utcnow():
                self.error_message = "Token inválido ou expirado. Por favor, solicite a redefinição novamente."
                self.is_loading = False
                return
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            await session.execute(
                rx.text(
                    "UPDATE tripulante SET senha_hash = :hash, reset_token = NULL, reset_token_expires = NULL WHERE id = :id"
                ),
                {"hash": hashed_password, "id": user.id},
            )
            await session.commit()
        self.success_message = "Sua senha foi redefinida com sucesso!"
        self.is_loading = False
        yield rx.redirect("/login")