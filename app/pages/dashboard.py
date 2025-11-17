import reflex as rx
from app.states.auth_state import AuthState
from app.states.vessel_state import VesselState
from app.states.dashboard_state import DashboardState
from app.components.connection_indicator import connection_indicator
from app.components.occupancy_display import occupancy_display
from app.components.validation_history import validation_history


def action_buttons() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("qr-code", class_name="h-6 w-6 mr-3"),
            "Escanear QR Code",
            class_name="w-full flex items-center justify-center py-4 px-6 bg-[#2C4A6E] text-white rounded-xl hover:bg-[#203650] transition-all duration-200 font-semibold shadow-lg hover:shadow-xl",
        ),
        rx.el.button(
            rx.icon("search", class_name="h-5 w-5 mr-3"),
            "Busca Manual",
            class_name="w-full flex items-center justify-center py-3 px-6 border border-[#2C4A6E] text-[#2C4A6E] rounded-xl hover:bg-[#2C4A6E] hover:text-white transition-all duration-200 font-semibold mt-3",
        ),
        class_name="space-y-3",
    )


def vessel_info() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("ship", class_name="h-5 w-5 text-[#2C4A6E] mr-2"),
            rx.el.span(
                VesselState.selected_vessel_name, class_name="font-medium text-gray-800"
            ),
            class_name="flex items-center",
        ),
        rx.el.button(
            "Trocar Embarcação",
            class_name="text-sm text-[#2C4A6E] hover:text-[#203650] font-medium",
        ),
        rx.el.div(
            rx.el.span(
                f"Gap de Embarque: {DashboardState.gap_embarque_minutos} minutos",
                class_name="text-sm text-gray-600",
            ),
            class_name="mt-2",
        ),
        class_name="bg-white p-4 rounded-xl shadow-lg border border-gray-200",
    )


def dashboard_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Dashboard de Controle", class_name="text-2xl font-bold text-gray-800"
            ),
            rx.el.p(
                rx.cond(
                    AuthState.logged_in_user,
                    f"Bem-vindo, {AuthState.logged_in_user.nome}!",
                    "Bem-vindo!",
                ),
                class_name="text-gray-600",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            connection_indicator(),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                "Logout",
                on_click=AuthState.logout,
                class_name="flex items-center text-sm text-red-600 hover:text-red-800 font-medium ml-4",
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-start justify-between p-6 bg-gray-100 border-b border-gray-200",
    )


def dashboard_page() -> rx.Component:
    return rx.el.main(
        dashboard_header(),
        rx.el.div(
            rx.el.div(
                vessel_info(),
                occupancy_display(),
                action_buttons(),
                class_name="space-y-6",
            ),
            rx.el.div(validation_history(), class_name="space-y-6"),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 p-6",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
        on_mount=DashboardState.load_initial_data,
    )