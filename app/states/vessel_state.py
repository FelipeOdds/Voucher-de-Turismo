import reflex as rx
from app.models import Embarcacao


class VesselState(rx.State):
    vessels: list[Embarcacao] = []
    is_loading: bool = False
    selected_vessel_id: int | None = rx.LocalStorage(None)
    selected_vessel_name: str = ""

    @rx.event
    async def fetch_vessels(self):
        self.is_loading = True
        async with rx.asession() as session:
            result = await session.execute(
                rx.text(
                    "SELECT id, nome, capacidade_maxima, gap_embarque_minutos FROM embarcacao"
                )
            )
            self.vessels = [
                Embarcacao(
                    id=row[0],
                    nome=row[1],
                    capacidade_maxima=row[2],
                    gap_embarque_minutos=row[3],
                )
                for row in result.fetchall()
            ]
        self.is_loading = False

    @rx.event
    def select_vessel(self, vessel_id: int):
        self.selected_vessel_id = vessel_id
        for vessel in self.vessels:
            if vessel["id"] == vessel_id:
                self.selected_vessel_name = vessel["nome"]
                break
        return rx.redirect("/")