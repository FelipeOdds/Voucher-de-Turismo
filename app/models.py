import reflex as rx
import datetime
import bcrypt
import uuid
from typing import TypedDict


class Tripulante(TypedDict):
    id: int
    nome: str
    email: str
    senha_hash: str
    token: str | None
    created_at: datetime.datetime
    last_login: datetime.datetime | None
    reset_token: str | None
    reset_token_expires: datetime.datetime | None
    email_verified: bool


class Embarcacao(TypedDict):
    id: int
    nome: str
    capacidade_maxima: int
    gap_embarque_minutos: int


class Voucher(TypedDict):
    id: int
    numero_voucher: str
    qr_code_hash: str
    nome_passageiro: str
    cpf: str | None
    status: str
    data_criacao: datetime.datetime
    data_primeira_validacao: datetime.datetime | None


class Validacao(TypedDict):
    id: int
    voucher_id: int
    tripulante_id: int
    embarcacao_id: int
    data_validacao: datetime.datetime
    tipo: str
    sincronizado: bool


class LogTrocaEmbarcacao(TypedDict):
    id: int
    tripulante_id: int
    embarcacao_anterior_id: int
    embarcacao_nova_id: int
    data_troca: datetime.datetime


from app.db import get_session
from sqlalchemy import text


async def init_db():
    async with get_session() as session:
        if "sqlite" in str(session.bind.url):
            await session.execute(text("PRAGMA foreign_keys=ON"))
        result = await session.execute(text("SELECT 1 FROM tripulante LIMIT 1"))
        if result.first() is None:
            print("Criando dados iniciais...")
            password = "liberta123"
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            await session.execute(
                text("""INSERT INTO tripulante (nome, email, senha_hash, created_at, email_verified)
                       VALUES (:nome, :email, :senha_hash, :created_at, :email_verified)"""),
                params={
                    "nome": "Tripulante Padrão",
                    "email": "tripulante@liberta.com",
                    "senha_hash": hashed_password,
                    "created_at": datetime.datetime.utcnow(),
                    "email_verified": True,
                },
            )
            embarcacao1 = Embarcacao(
                id=1, nome="Lancha Azul", capacidade_maxima=50, gap_embarque_minutos=15
            )
            embarcacao2 = Embarcacao(
                id=2,
                nome="Saveiro Branco",
                capacidade_maxima=100,
                gap_embarque_minutos=20,
            )
            await session.execute(
                text(
                    "INSERT INTO embarcacao (nome, capacidade_maxima, gap_embarque_minutos) VALUES (:nome, :capacidade, :gap)"
                ),
                params=[
                    {
                        "nome": e["nome"],
                        "capacidade": e["capacidade_maxima"],
                        "gap": e["gap_embarque_minutos"],
                    }
                    for e in [embarcacao1, embarcacao2]
                ],
            )
            voucher1 = Voucher(
                id=1,
                numero_voucher="LT12345",
                qr_code_hash=str(uuid.uuid4()),
                nome_passageiro="John Doe",
                cpf="111.222.333-44",
                status="ativo",
                data_criacao=datetime.datetime.utcnow(),
                data_primeira_validacao=None,
            )
            voucher2 = Voucher(
                id=2,
                numero_voucher="LT67890",
                qr_code_hash=str(uuid.uuid4()),
                nome_passageiro="Jane Smith",
                cpf="555.666.777-88",
                status="ativo",
                data_criacao=datetime.datetime.utcnow(),
                data_primeira_validacao=None,
            )
            await session.execute(
                text(
                    "INSERT INTO voucher (numero_voucher, qr_code_hash, nome_passageiro, cpf, status) VALUES (:num, :qr, :nome, :cpf, :status)"
                ),
                params=[
                    {
                        "num": v["numero_voucher"],
                        "qr": v["qr_code_hash"],
                        "nome": v["nome_passageiro"],
                        "cpf": v["cpf"],
                        "status": v["status"],
                    }
                    for v in [voucher1, voucher2]
                ],
            )
            await session.commit()
            print("Dados iniciais criados com sucesso!")
        else:
            print("Banco de dados já populado.")