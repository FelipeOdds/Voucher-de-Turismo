import reflex as rx
import datetime
from typing import TypedDict
from app.models import Validacao
from app.db import get_session


class ValidationHistory(TypedDict):
    id: int
    voucher_numero: str
    passageiro_nome: str
    tipo: str
    data_validacao: datetime.datetime


class DashboardState(rx.State):
    current_occupancy: int = 0
    max_capacity: int = 100
    gap_embarque_minutos: int = 15
    is_offline: bool = False
    validation_history: list[ValidationHistory] = []

    @rx.var
    def occupancy_percentage(self) -> int:
        if self.max_capacity == 0:
            return 0
        return int(self.current_occupancy / self.max_capacity * 100)

    @rx.var
    def occupancy_status(self) -> str:
        percentage = self.occupancy_percentage
        if percentage >= 90:
            return "critical"
        elif percentage >= 70:
            return "high"
        elif percentage >= 40:
            return "medium"
        else:
            return "low"

    @rx.var
    def connection_status_text(self) -> str:
        return "Offline" if self.is_offline else "Online"

    @rx.var
    def connection_status_color(self) -> str:
        return "bg-red-500" if self.is_offline else "bg-green-500"

    @rx.event
    async def load_initial_data(self):
        from app.states.vessel_state import VesselState

        vessel_state = await self.get_state(VesselState)
        vessel_id = vessel_state.selected_vessel_id
        if not vessel_id:
            yield rx.redirect("/select-vessel")
            return
        async with get_session() as session:
            result = await session.execute(
                rx.text(
                    "SELECT capacidade_maxima, gap_embarque_minutos FROM embarcacao WHERE id = :id"
                ),
                {"id": vessel_id},
            )
            vessel_data = result.first()
            if vessel_data:
                self.max_capacity = vessel_data.capacidade_maxima
                self.gap_embarque_minutos = vessel_data.gap_embarque_minutos
            else:
                self.max_capacity = 100
                self.gap_embarque_minutos = 15
        self.current_occupancy = 23
        self.validation_history = [
            {
                "id": 1,
                "voucher_numero": "LT12345",
                "passageiro_nome": "João Silva",
                "tipo": "embarque",
                "data_validacao": datetime.datetime.now()
                - datetime.timedelta(minutes=5),
            },
            {
                "id": 2,
                "voucher_numero": "LT67890",
                "passageiro_nome": "Maria Santos",
                "tipo": "embarque",
                "data_validacao": datetime.datetime.now()
                - datetime.timedelta(minutes=12),
            },
            {
                "id": 3,
                "voucher_numero": "LT54321",
                "passageiro_nome": "Pedro Oliveira",
                "tipo": "desembarque",
                "data_validacao": datetime.datetime.now()
                - datetime.timedelta(minutes=18),
            },
        ]
        yield