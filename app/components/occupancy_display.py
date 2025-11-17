import reflex as rx
from app.states.dashboard_state import DashboardState


def occupancy_display() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Lotação Atual", class_name="text-lg font-semibold text-gray-800 mb-2"
            ),
            rx.el.div(
                rx.el.span(
                    DashboardState.current_occupancy,
                    class_name="text-3xl font-bold text-[#2C4A6E]",
                ),
                rx.el.span(
                    f" / {DashboardState.max_capacity}",
                    class_name="text-xl text-gray-600",
                ),
                class_name="flex items-end",
            ),
            class_name="text-center",
        ),
        rx.el.div(
            rx.el.div(
                class_name=rx.cond(
                    DashboardState.occupancy_status == "critical",
                    "h-2 bg-red-500 rounded-full transition-all duration-300",
                    rx.cond(
                        DashboardState.occupancy_status == "high",
                        "h-2 bg-yellow-500 rounded-full transition-all duration-300",
                        rx.cond(
                            DashboardState.occupancy_status == "medium",
                            "h-2 bg-blue-500 rounded-full transition-all duration-300",
                            "h-2 bg-green-500 rounded-full transition-all duration-300",
                        ),
                    ),
                ),
                style={"width": f"{DashboardState.occupancy_percentage}%"},
            ),
            class_name="w-full bg-gray-200 rounded-full overflow-hidden",
        ),
        rx.el.p(
            f"{DashboardState.occupancy_percentage}% da capacidade",
            class_name="text-sm text-gray-600 text-center mt-2",
        ),
        class_name="bg-white p-6 rounded-xl shadow-lg border border-gray-200",
    )