import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.h2(
                "Bem-vindo de volta",
                class_name="text-2xl font-bold text-gray-800 text-center",
            ),
            rx.el.p(
                "Acesse sua conta para gerenciar a operação.",
                class_name="text-sm text-gray-500 text-center mb-6",
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
                    placeholder="tripulante@liberta.com",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#2C4A6E] focus:border-[#2C4A6E] sm:text-sm",
                    required=True,
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Senha",
                    html_for="password",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    id="password",
                    name="password",
                    type="password",
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#2C4A6E] focus:border-[#2C4A6E] sm:text-sm",
                    required=True,
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.login_error_message != "",
                rx.el.div(
                    rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                    rx.el.span(AuthState.login_error_message),
                    class_name="flex items-center bg-red-100 text-red-700 text-sm font-medium p-3 rounded-md mb-4",
                ),
                None,
            ),
            rx.el.button(
                rx.cond(
                    AuthState.is_loading, rx.el.p("Entrando..."), rx.el.p("Entrar")
                ),
                type="submit",
                disabled=AuthState.is_loading,
                class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#2C4A6E] hover:bg-[#203650] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#2C4A6E] disabled:opacity-50 disabled:cursor-not-allowed",
            ),
            class_name="",
        ),
        on_submit=AuthState.login,
        class_name="w-full max-w-md",
    )


def login_page() -> rx.Component:
    return rx.el.main(
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                rx.el.p("Redirecionando..."),
                class_name="flex items-center justify-center h-screen",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("ship", class_name="h-12 w-12 text-[#2C4A6E] mx-auto mb-4"),
                    rx.el.h1(
                        "Liberta Turismo",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.el.p(
                        "App de Controle da Tripulação",
                        class_name="text-md text-gray-600 text-center mb-10",
                    ),
                    login_form(),
                ),
                class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-lg border border-gray-200",
            ),
        ),
        class_name="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4 font-['Inter']",
    )