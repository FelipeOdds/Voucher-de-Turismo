import reflex as rx
from app.states.dashboard_state import DashboardState


def validation_item(validation: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    rx.cond(
                        validation["tipo"] == "embarque",
                        "arrow-up",
                        rx.cond(
                            validation["tipo"] == "desembarque",
                            "arrow-down",
                            "alert-circle",
                        ),
                    ),
                    class_name=rx.cond(
                        validation["tipo"] == "embarque",
                        "h-4 w-4 text-green-600",
                        rx.cond(
                            validation["tipo"] == "desembarque",
                            "h-4 w-4 text-blue-600",
                            "h-4 w-4 text-yellow-600",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        validation["passageiro_nome"],
                        class_name="text-sm font-medium text-gray-800",
                    ),
                    rx.el.p(
                        validation["voucher_numero"], class_name="text-xs text-gray-500"
                    ),
                    class_name="ml-3",
                ),
                class_name="flex items-start",
            ),
            rx.el.div(
                rx.el.p(
                    validation["tipo"].title(),
                    class_name=rx.cond(
                        validation["tipo"] == "embarque",
                        "text-xs font-medium px-2 py-1 bg-green-100 text-green-800 rounded-full w-fit",
                        rx.cond(
                            validation["tipo"] == "desembarque",
                            "text-xs font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded-full w-fit",
                            "text-xs font-medium px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full w-fit",
                        ),
                    ),
                ),
                rx.el.p(
                    validation["data_validacao"].to_string(),
                    class_name="text-xs text-gray-500 mt-1",
                ),
                class_name="text-right",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name="p-3 bg-gray-50 rounded-lg border border-gray-100 hover:bg-gray-100 transition-colors duration-200",
    )


def validation_history() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Últimas Validações", class_name="text-lg font-semibold text-gray-800 mb-4"
        ),
        rx.el.div(
            rx.cond(
                DashboardState.validation_history.length() > 0,
                rx.el.div(
                    rx.foreach(DashboardState.validation_history, validation_item),
                    class_name="space-y-3 max-h-64 overflow-y-auto",
                ),
                rx.el.div(
                    rx.el.p(
                        "Nenhuma validação recente",
                        class_name="text-sm text-gray-500 text-center py-8",
                    ),
                    class_name="bg-gray-50 rounded-lg border border-gray-100",
                ),
            )
        ),
        class_name="bg-white p-6 rounded-xl shadow-lg border border-gray-200",
    )