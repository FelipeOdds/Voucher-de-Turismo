import reflex as rx
from app.states.auth_state import AuthState


def forgot_password_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.h2(
                "Esqueceu a Senha?",
                class_name="text-2xl font-bold text-gray-800 text-center",
            ),
            rx.el.p(
                "Insira seu email para receber instruções de recuperação.",
                class_name="text-sm text-gray-500 text-center mb-6",
            ),
            rx.cond(
                AuthState.success_message != "",
                rx.el.div(
                    rx.icon("check_check", class_name="h-4 w-4 mr-2"),
                    rx.el.span(AuthState.success_message),
                    class_name="flex items-center bg-green-100 text-green-700 text-sm font-medium p-3 rounded-md mb-4",
                ),
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.div(
                    rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                    rx.el.span(AuthState.error_message),
                    class_name="flex items-center bg-red-100 text-red-700 text-sm font-medium p-3 rounded-md mb-4",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    "Email",
                    html_for="email",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    id="email",
                    name="email",
                    type="email",
                    placeholder="seu.email@exemplo.com",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#2C4A6E] focus:border-[#2C4A6E] sm:text-sm",
                    required=True,
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.el.div(
                        rx.spinner(class_name="h-4 w-4 border-2"),
                        "Enviando...",
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p("Enviar Instruções"),
                ),
                type="submit",
                disabled=AuthState.is_loading,
                class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#2C4A6E] hover:bg-[#203650] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#2C4A6E] disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            rx.el.div(
                rx.el.a(
                    "Voltar para o Login",
                    href="/login",
                    class_name="font-semibold text-[#2C4A6E] hover:underline",
                ),
                class_name="text-center text-sm text-gray-600 mt-6",
            ),
        ),
        on_submit=AuthState.forgot_password,
        class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200",
    )


def forgot_password_page() -> rx.Component:
    return rx.el.main(
        forgot_password_form(),
        class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4 font-['Inter']",
        on_mount=[AuthState.set_error_message(""), AuthState.set_success_message("")],
    )