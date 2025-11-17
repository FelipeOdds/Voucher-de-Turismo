import reflex as rx
from app.states.dashboard_state import DashboardState


def connection_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.cond(
                DashboardState.is_offline,
                "w-2 h-2 bg-red-500 rounded-full animate-pulse",
                "w-2 h-2 bg-green-500 rounded-full",
            )
        ),
        rx.el.span(
            DashboardState.connection_status_text,
            class_name=rx.cond(
                DashboardState.is_offline,
                "text-xs font-medium text-red-700",
                "text-xs font-medium text-green-700",
            ),
        ),
        class_name=rx.cond(
            DashboardState.is_offline,
            "flex items-center gap-2 px-3 py-1 bg-red-100 rounded-full border border-red-200",
            "flex items-center gap-2 px-3 py-1 bg-green-100 rounded-full border border-green-200",
        ),
    )