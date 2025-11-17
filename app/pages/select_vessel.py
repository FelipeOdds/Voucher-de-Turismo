import reflex as rx
from app.states.vessel_state import VesselState
from app.states.auth_state import AuthState


def vessel_card(vessel: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("ship", class_name="h-8 w-8 text-[#2C4A6E]"),
            rx.el.h3(vessel["nome"], class_name="text-lg font-semibold text-gray-800"),
            rx.el.p(
                f"Capacidade: {vessel['capacidade_maxima']} passageiros",
                class_name="text-sm text-gray-600",
            ),
            class_name="flex flex-col items-center gap-2",
        ),
        rx.el.button(
            "Selecionar",
            on_click=lambda: VesselState.select_vessel(vessel["id"]),
            class_name="mt-4 w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#2C4A6E] hover:bg-[#203650] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#2C4A6E]",
        ),
        class_name="p-6 bg-white rounded-xl shadow-lg border border-gray-200 transform hover:-translate-y-1 transition-transform duration-300",
    )


def select_vessel_page() -> rx.Component:
    return rx.el.main(
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        rx.cond(
                            AuthState.logged_in_user,
                            f"Bem-vindo, {AuthState.logged_in_user.nome}!",
                            "Bem-vindo!",
                        )
                    ),
                    rx.el.button(
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="bg-red-500 text-white p-2 rounded",
                    ),
                    class_name="flex justify-between items-center p-4 bg-gray-100",
                ),
                rx.el.h1(
                    "Selecione a Embarcação",
                    class_name="text-3xl font-bold text-gray-800 my-6 text-center",
                ),
                rx.cond(
                    VesselState.is_loading,
                    rx.el.div(
                        rx.el.p("Carregando embarcações..."),
                        class_name="flex justify-center",
                    ),
                    rx.el.div(
                        rx.foreach(VesselState.vessels, vessel_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6",
                    ),
                ),
            ),
            rx.el.div(
                rx.el.p("Acesso negado. Redirecionando para login..."),
                class_name="flex items-center justify-center h-screen",
            ),
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
        on_mount=VesselState.fetch_vessels,
    )