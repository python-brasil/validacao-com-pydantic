#!/usr/bin/env python3
"""Valida dados antes que eles entrem no banco.

    pip install pydantic
    python main.py

Pydantic transforma um dicionário vindo de fora (JSON, formulário, planilha)
num objeto com tipos garantidos — ou levanta erro dizendo exatamente qual
campo está errado e por quê.
"""
from datetime import date

from pydantic import BaseModel, Field, ValidationError, field_validator


class Inscricao(BaseModel):
    nome: str = Field(min_length=2, max_length=80)
    email: str
    idade: int = Field(ge=16, le=120)
    nascimento: date
    cupom: str | None = None

    @field_validator("nome")
    @classmethod
    def nome_tem_sobrenome(cls, v: str) -> str:
        if len(v.split()) < 2:
            raise ValueError("informe nome e sobrenome")
        return v.title()

    @field_validator("email")
    @classmethod
    def email_parece_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("e-mail inválido")
        return v.lower()


ENTRADAS = [
    {"nome": "ana souza", "email": "ANA@Exemplo.COM", "idade": "28",
     "nascimento": "1998-03-14"},
    {"nome": "jo", "email": "jo#exemplo", "idade": 12, "nascimento": "ontem"},
]


def main():
    for i, bruto in enumerate(ENTRADAS, 1):
        print(f"\n--- entrada {i}: {bruto}")
        try:
            ok = Inscricao(**bruto)
        except ValidationError as e:
            # `e.errors()` é uma lista de dicionários, não um texto: dá para
            # devolver campo a campo numa API em vez de um erro genérico.
            for erro in e.errors():
                campo = ".".join(str(p) for p in erro["loc"])
                print(f"    REJEITADO  {campo}: {erro['msg']}")
            continue
        print(f"    OK  {ok.nome} | {ok.email} | {ok.idade} anos")
        print(f"        tipos: idade={type(ok.idade).__name__}, "
              f"nascimento={type(ok.nascimento).__name__}")


if __name__ == "__main__":
    main()
