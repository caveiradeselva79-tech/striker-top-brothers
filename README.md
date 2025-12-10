# ==========================
# SISTEMA STRIKER TOP BROTHERS
# ==========================

import csv
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Tuple, Optional
from urllib.parse import quote_plus
import calendar

SENHA_SISTEMA = "striker"
NOME_ACADEMIA = "STRIKER TOP BROTHERS"

ARQ_ALUNOS = "aluno.csv"  # mantém o nome que você já usava p/ não quebrar seus dados
ARQ_PAGAMENTOS = "pagamentos.csv"
ARQ_PRESENCAS = "presencas.csv"
ARQ_DESPESAS_FIXAS = "despesas_fixas.csv"
ARQ_REPASSES = "repasses_professores.csv"
ARQ_RELATORIO_LUCRO = "relatorio_lucro.csv"

PIX_CHAVE = "cezarmatosjulio@gmail.com"
PIX_TITULAR = "STRIKER TOP BROTHERS"
PIX_BANCO = "Mercado Pago"

ENDERECO = "Rua Jules Rimet, 60 - Alvorada - Cuiaba - MT"
COORD_LAT = -15.58112
COORD_LON = -56.08718

DDI = "55"
WHATS_ADMIN = "65996920712"
WHATS_DUVIDAS = WHATS_ADMIN

# ---- CAMPOS DO CSV (corrigido: 'telefone' e 'modalidade' separados)
CAMPOS = [
    "nome", "cpf", "rg", "nascimento", "plano", "email",
    "opcao_pagto", "vencimento", "ult_pagamento", "telefone", "modalidade"
]

# ---- PLANOS (chaves curtas, descrições separadas)
PLANOS = {
    "Beginner": 135.00,
    "Intermediate": 150.00,
    "Hard": 165.00,
}
PLANOS_DESC = {
    "Beginner": "2x na semana",
    "Intermediate": "3x na semana",
    "Hard": "5x na semana"
}

alunos: List[Dict[str, str]] = []

def hoje() -> date:
    return date.today()

def fmt_brl(valor: float) -> str:
    s = f"{valor:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")

def _to_float(valor_str: str) -> float:
    if valor_str is None:
        return 0.0
    s = str(valor_str).strip()
    if not s:
        return 0.0
    s = s.replace(" ", "")
    if s.count(",") == 1 and s.count(".") >= 1:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def _parse_date_any(txt: str):
    txt = (txt or "").strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(txt, fmt).date()
        except ValueError:
            pass
    try:
        return datetime.strptime(txt[:7], "%Y-%m").date().replace(day=1)
    except Exception:
        return None

def data_str(d) -> str:
    return d.strftime("%d/%m/%Y") if d else ""

def normalizar_doc(s: str) -> str:
    return "".join(ch for ch in (s or "") if ch.isdigit())

def _end_of_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]

def _due_date_for(month: int, year: int, vencimento_field: str) -> Optional[date]:
    if not vencimento_field:
        return None
    d = _parse_date_any(vencimento_field)
    if d:
        return date(year, month, min(d.day, _end_of_month(year, month)))
    dia = "".join(ch for ch in vencimento_field if ch.isdigit())
    if not dia:
        return None
    try:
        dia = int(dia)
        dia = max(1, min(dia, _end_of_month(year, month)))
        return date(year, month, dia)
    except Exception:
        return None

def confirmar(msg: str) -> bool:
    r = input(msg + " (s/N): ").strip().lower()
    return r in ("s", "sim", "y", "yes")

def _garantir_csv(caminho: str, cabecalhos: List[str]) -> None:
    p = Path(caminho)
    if not p.exists():
        with p.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cabecalhos)

def _ler_csv_dict(caminho: str) -> List[Dict[str, str]]:
    p = Path(caminho)
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]

def maps_link() -> str:
    if COORD_LAT and COORD_LON:
        return f"https://www.google.com/maps?q={COORD_LAT},{COORD_LON}"
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(ENDERECO)}"

def whats_link(numero: str, mensagem: str) -> str:
    numero = normalizar_doc(numero)
    return f"https://wa.me/{DDI}{numero}?text={quote_plus(mensagem)}"

def obter_valor_plano(tipo_plano: str) -> float:
    chave = (tipo_plano or "").strip().capitalize()
    return PLANOS.get(chave, 0.0)

def carregar_alunos():
    alunos.clear()
    p = Path(ARQ_ALUNOS)
    if not p.exists():
        return
    with p.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            for c in CAMPOS:
                row.setdefault(c, "")
            alunos.append(row)

def salvar_alunos():
    with open(ARQ_ALUNOS, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for a in alunos:
            w.writerow(a)

def cadastrar_aluno():
    print("\n=== Cadastro de Aluno ===")
    nome = input("Nome: ").strip()
    cpf = normalizar_doc(input("CPF: ").strip())
    rg = input("RG: ").strip()
    nasc = input("Nascimento - (DD/MM/AAAA): ").strip()
    plano = input("Plano - (Beginner/Intermediate/Hard): ").strip().capitalize()
    email = input("Email: ").strip()
    opcao_pagto = input("Opçao de pagamento - (PIX/Cartao/Outro): ").strip()
    venc = input("Vencimento (DD/MM/AAAA) ou dia (1-31): ").strip()
    ult_pag = ""
    telefone = normalizar_doc(input("Telefone - (somente numeros, com DDD): ").strip())
    modalidade = input("Modalidade - (Jiu-Jitsu, Muay Thai, Kickboxing, Boxe): ").strip()

    if plano not in PLANOS:
        print("Plano invalido. Use Beginner/Intermediate/Hard.")
        return

    nasc_date = _parse_date_any(nasc)
    venc_date = _parse_date_any(venc)
    aluno = {
        "nome": nome, "cpf": cpf, "rg": rg, "nascimento": data_str(nasc_date),
        "plano": plano, "email": email, "opcao_pagto": opcao_pagto,
        "vencimento": data_str(venc_date) if venc_date else (venc if venc.isdigit() else ""),
        "ult_pagamento": ult_pag, "telefone": telefone, "modalidade": modalidade
    }
    alunos.append(aluno)
    salvar_alunos()
    print(f"Aluno cadastrado: {nome} ({plano} - {fmt_brl(PLANOS[plano])})")

def registrar_presenca():
    print("\n=== Registrar Presenca ===")
    cpf = normalizar_doc(input("CPF do aluno: ").strip())
    if not cpf:
        print("CPF invalido.")
        return
    with open(ARQ_PRESENCAS, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([hoje().isoformat(), cpf])
    print("Presenca registrada.")

def listar_presencas_do_cpf():
    print("\n=== Listar Presencas por CPF ===")
    cpf = normalizar_doc(input("CPF: ").strip())
    out = []
    p = Path(ARQ_PRESENCAS)
    if p.exists():
        with p.open("r", encoding="utf-8", newline="") as f:
            r = csv.reader(f)
            for linha in r:
                if len(linha) >= 2 and normalizar_doc(linha[1]) == cpf:
                    out.append(linha[0])
    if not out:
        print("Sem presencas registradas.")
    else:
        print("Datas:")
        for d in out:
            print(" -", d)

def listar_planos():
    print("\n===== PLANOS DISPONIVEIS =====")
    for nome, preco in PLANOS.items():
        desc = PLANOS_DESC.get(nome, "")
        rotulo = f"{nome} - {desc}" if desc else nome
        print(f"{rotulo:<28} -> {fmt_brl(preco)}")
    print("=" * 36)

def registrar_pagamento():
    print("\n=== Registrar Pagamento por Plano ===")
    aluno = input("Nome do aluno: ").strip()
    plano = input("Plano do aluno (Beginner/Intermediate/Hard): ").strip().capitalize()
    if plano not in PLANOS:
        print("Plano invalido.")
        return
    data_pag = input("Data do pagamento (DD/MM/AAAA) - Enter p/ hoje: ").strip()
    if not data_pag:
        data_pag = date.today().strftime("%d/%m/%Y")

    _garantir_csv(ARQ_PAGAMENTOS, ["aluno", "valor", "data_pagamento"])
    with open(ARQ_PAGAMENTOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["aluno", "valor", "data_pagamento"])
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({"aluno": aluno, "valor": "{:.2f}".format(PLANOS[plano]), "data_pagamento": data_pag})

    for a in alunos:
        if a["nome"].strip().lower() == aluno.strip().lower():
            a["ult_pagamento"] = data_pag
            salvar_alunos()
            break

    print(f"Pagamento registrado: {aluno} - {plano} ({fmt_brl(PLANOS[plano])}) em {data_pag}")

def listar_alunos():
    print("\n=== Alunos Cadastrados ===")
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    print("{:<25} {:<11} {:<14} {:<12} {:<12} {:<12} {:<14}".format(
        "Nome","CPF","Plano","Telefone","Venc.","Ult.Pag.","Modalidade"))
    print("-" * 105)
    for a in alunos:
        print("{:<25} {:<11} {:<14} {:<12} {:<12} {:<12} {:<14}".format(
            a.get("nome",""), a.get("cpf",""), a.get("plano",""),
            a.get("telefone",""), a.get("vencimento",""),
            a.get("ult_pagamento",""), a.get("modalidade","")
        ))

def buscar_alunos_por_plano():
    print("\n=== Procurar Alunos por Plano ===")
    plano = input("Plano (Beginner/Intermediate/Hard): ").strip().capitalize()
    if plano not in PLANOS:
        print("Plano invalido.")
        return
    filtrados = [a for a in alunos if (a.get('plano','').strip().capitalize() == plano)]
    if not filtrados:
        print("Nenhum aluno encontrado no plano", plano)
        return
    print(f"Encontrados {len(filtrados)} aluno(s) no plano {plano}:")
    print("{:<25} {:<11} {:<28} {:<12} {:<14}".format("Nome","CPF","Email","Telefone","Modalidade"))
    print("-" * 95)
    for a in filtrados:
        print("{:<25} {:<11} {:<28} {:<12} {:<14}".format(
            a.get("nome",""), a.get("cpf",""), a.get("email",""),
            a.get("telefone",""), a.get("modalidade","")
        ))

def editar_aluno():
    print("\n=== Editar Aluno por CPF ===")
    cpf = normalizar_doc(input("Digite o CPF do aluno: ").strip())
    if not cpf:
        print("CPF invalido.")
        return
    idx = None
    for i, a in enumerate(alunos):
        if normalizar_doc(a.get("cpf","")) == cpf:
            idx = i
            break
    if idx is None:
        print("Aluno nao encontrado.")
        return
    a = alunos[idx]
    print("Pressione ENTER para manter o valor atual.\n")

    def ask(label, key, transform=lambda x: x, validator=None):
        atual = a.get(key, "")
        novo = input(f"{label} [{atual}]: ").strip()
        if not novo:
            return atual
        if validator and not validator(novo):
            print("Valor invalido. Mantendo atual.")
            return atual
        return transform(novo)

    a["nome"] = ask("Nome", "nome")
    a["rg"] = ask("RG", "rg")
    a["nascimento"] = ask("Nascimento (DD/MM/AAAA)", "nascimento",
                          transform=lambda s: data_str(_parse_date_any(s)) or s)
    a["plano"] = ask("Plano (Beginner/Intermediate/Hard)", "plano",
                     transform=lambda s: s.capitalize(),
                     validator=lambda s: s.capitalize() in PLANOS)
    a["email"] = ask("Email", "email")
    a["opcao_pagto"] = ask("Opcao de Pagamento", "opcao_pagto")
    a["vencimento"] = ask("Vencimento (DD/MM/AAAA ou dia 1-31)", "vencimento",
                          transform=lambda s: (data_str(_parse_date_any(s)) if _parse_date_any(s) else (s if s.isdigit() else a["vencimento"])))
    a["ult_pagamento"] = ask("Ultimo Pagamento (DD/MM/AAAA)", "ult_pagamento",
                             transform=lambda s: data_str(_parse_date_any(s)) or s)
    a["telefone"] = ask("Telefone (somente numeros, com DDD)", "telefone",
                        transform=lambda s: normalizar_doc(s))
    a["modalidade"] = ask("Modalidade (texto livre)", "modalidade")

    print(f"CPF permanece: {a['cpf']}")
    alunos[idx] = a
    salvar_alunos()
    print("Aluno atualizado com sucesso.")

def excluir_aluno():
    print("\n=== Excluir Aluno por CPF ===")
    cpf = normalizar_doc(input("Digite o CPF do aluno: ").strip())
    if not cpf:
        print("CPF invalido.")
        return
    idx = None
    for i, a in enumerate(alunos):
        if normalizar_doc(a.get("cpf","")) == cpf:
            idx = i
            break
    if idx is None:
        print("Aluno nao encontrado.")
        return
    a = alunos[idx]
    print(f"Encontrado: {a.get('nome','')} (Plano {a.get('plano','')})")
    if not confirmar("Confirma excluir este aluno?"):
        print("Operacao cancelada.")
        return

    nome_aluno = a.get("nome","").strip().lower()
    alunos.pop(idx)
    salvar_alunos()
    print("Aluno removido do cadastro.")

    if confirmar("Remover presencas relacionadas?"):
        p = Path(ARQ_PRESENCAS)
        if p.exists():
            linhas = []
            with p.open("r", encoding="utf-8", newline="") as f:
                r = csv.reader(f)
                for linha in r:
                    if len(linha) >= 2 and normalizar_doc(linha[1]) == cpf:
                        continue
                    linhas.append(linha)
            with p.open("w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerows(linhas)
        print("Presencas removidas.")

    if confirmar("Remover pagamentos relacionados por NOME?"):
        p = Path(ARQ_PAGAMENTOS)
        if p.exists():
            rows = _ler_csv_dict(ARQ_PAGAMENTOS)
            restantes = [row for row in rows if row.get("aluno", "").strip().lower() != nome_aluno]
            with p.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["aluno","valor","data_pagamento"])
                writer.writeheader()
                writer.writerows(restantes)
        print("Pagamentos removidos (match por nome).")

def _is_overdue_for_month(a: Dict[str,str], month: int, year: int, today: date) -> Tuple[bool, Optional[int], Optional[date]]:
    due = _due_date_for(month, year, a.get("vencimento",""))
    if not due:
        return (False, None, None)
    if today <= due:
        return (False, None, due)
    last_pay = _parse_date_any(a.get("ult_pagamento",""))
    if (not last_pay) or (last_pay < due):
        days = (today - due).days
        return (True, days, due)
    return (False, None, due)

def listar_alunos_em_atraso():
    print("\n=== Alunos em Atraso na Mensalidade ===")
    ref = input("Mes/Ano (MM/AAAA) - Enter para mes atual: ").strip()
    today = hoje()
    if ref:
        try:
            month = int(ref[:2])
            year = int(ref[-4:])
        except Exception:
            print("Formato invalido. Use MM/AAAA.")
            return
    else:
        month, year = today.month, today.year

    atrasados = []
    for a in alunos:
        overdue, days, due = _is_overdue_for_month(a, month, year, today)
        if overdue:
            atrasados.append((a, days, due))

    if not atrasados:
        print("Nenhum aluno em atraso para", f"{month:02d}/{year:04d}")
        return

    print("{:<25} {:<11} {:<14} {:<12} {:<12} {:<12}".format(
        "Nome","CPF","Plano","Venc.","Dias Atraso","Telefone"))
    print("-" * 95)
    for a, days, due in atrasados:
        print("{:<25} {:<11} {:<14} {:<12} {:<12} {:<12}".format(
            a.get("nome",""), a.get("cpf",""), a.get("plano",""),
            data_str(due), days, a.get("telefone","")
        ))

    if confirmar("Gerar links de cobranca (WhatsApp) para todos em atraso?"):
        for a, days, due in atrasados:
            valor = PLANOS.get(a.get("plano","").capitalize(), 0.0)
            msg = "Ola {}! Sua mensalidade {} ({}) esta em atraso desde {}. Chave PIX: {}. {} - {}".format(
                a.get("nome",""), a.get("plano",""), fmt_brl(valor),
                data_str(due), PIX_CHAVE, NOME_ACADEMIA, maps_link()
            )
            url = whats_link(a.get("telefone",""), msg)
            print(f"- {a.get('nome','')}: {url}")

def somar_pagamentos_mes(ano: int, mes: int) -> float:
    linhas = _ler_csv_dict(ARQ_PAGAMENTOS)
    total = 0.0
    for row in linhas:
        valor = _to_float(row.get("valor"))
        data = _parse_date_any(row.get("data_pagamento", ""))
        if data and data.year == ano and data.month == mes:
            total += valor
    return total

def somar_despesas_fixas() -> float:
    _garantir_csv(ARQ_DESPESAS_FIXAS, ["nome", "valor_mensal"])
    linhas = _ler_csv_dict(ARQ_DESPESAS_FIXAS)
    return sum(_to_float(row.get("valor_mensal")) for row in linhas)

def somar_repasses_mes(ano: int, mes: int) -> float:
    _garantir_csv(ARQ_REPASSES, ["professor", "mes", "ano", "valor"])
    linhas = _ler_csv_dict(ARQ_REPASSES)
    total = 0.0
    for row in linhas:
        try:
            r_mes = int(str(row.get("mes", "")).strip() or 0)
            r_ano = int(str(row.get("ano", "")).strip() or 0)
        except ValueError:
            r_mes, r_ano = 0, 0
        if r_mes == mes and r_ano == ano:
            total += _to_float(row.get("valor"))
    return total

def calcular_lucro_mensal(ano: int, mes: int) -> Tuple[float, float, float, float]:
    total_pagamentos = somar_pagamentos_mes(ano, mes)
    despesas = somar_despesas_fixas()
    repasses = somar_repasses_mes(ano, mes)
    lucro = total_pagamentos - despesas - repasses
    return total_pagamentos, despesas, repasses, lucro

def _salvar_relatorio_lucro(ano: int, mes: int, total_pagamentos: float, despesas: float, repasses: float, lucro: float) -> None:
    campos = ["ano", "mes", "total_pagamentos", "despesas_fixas", "repasses", "lucro"]
    _garantir_csv(ARQ_RELATORIO_LUCRO, campos)
    dados = _ler_csv_dict(ARQ_RELATORIO_LUCRO)
    chave = (str(ano), str(mes))
    atualizou = False
    for row in dados:
        if (row.get("ano"), row.get("mes")) == chave:
            row["total_pagamentos"] = "{:.2f}".format(total_pagamentos)
            row["despesas_fixas"] = "{:.2f}".format(despesas)
            row["repasses"] = "{:.2f}".format(repasses)
            row["lucro"] = "{:.2f}".format(lucro)
            atualizou = True
            break
    if not atualizou:
        dados.append({
            "ano": str(ano),
            "mes": str(mes),
            "total_pagamentos": "{:.2f}".format(total_pagamentos),
            "despesas_fixas": "{:.2f}".format(despesas),
            "repasses": "{:.2f}".format(repasses),
            "lucro": "{:.2f}".format(lucro),
        })
    with open(ARQ_RELATORIO_LUCRO, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

def gerar_relatorio_lucro():
    try:
        print("\n=== Relatorio de Lucro Mensal ===")
        mes = int(input("Mes (1-12): ").strip())
        ano = int(input("Ano (ex.: 2025): ").strip())
        total_pagamentos, despesas, repasses, lucro = calcular_lucro_mensal(ano, mes)
        print("-" * 54)
        print("Total de Pagamentos dos Alunos  : {}".format(fmt_brl(total_pagamentos)))
        print("Despesas Fixas (mensais)         : {}".format(fmt_brl(despesas)))
        print("Repasses a Professores (mes)     : {}".format(fmt_brl(repasses)))
        print("-" * 54)
        print("LUCRO DO MES                     : {}".format(fmt_brl(lucro)))
        print("-" * 54)
        _salvar_relatorio_lucro(ano, mes, total_pagamentos, despesas, repasses, lucro)
        print(f"Relatorio salvo/atualizado em '{ARQ_RELATORIO_LUCRO}'.")
    except Exception as e:
        print("Erro ao gerar relatorio de lucro:", e)

def mostrar_pix():
    try:
        print("\n=== PIX ===")
        print(f"Chave  : {PIX_CHAVE}")
        print(f"Titular: {PIX_TITULAR}")
        print(f"Banco  : {PIX_BANCO}")
        print("\nLink Google Maps:", maps_link())
    except Exception as e:
        print("Erro ao exibir PIX/Maps:", e)

def link_cobranca_whatsapp():
    try:
        print("\n=== Link de Cobranca (WhatsApp) ===")
        nome = input("Nome do aluno: ").strip()
        telefone = normalizar_doc(input("Telefone do aluno (somente numeros, com DDD): ").strip())
        plano = input("Plano (Beginner/Intermediate/Hard): ").strip().capitalize()
        valor = PLANOS.get(plano, 0.0)
        if valor <= 0:
            print("Plano invalido.")
            return
        msg = "Ola {}! Sua mensalidade {} e {}. Chave PIX: {}. {} - {}".format(
            nome, plano, fmt_brl(valor), PIX_CHAVE, NOME_ACADEMIA, maps_link()
        )
        url = whats_link(telefone, msg)
        print("Envie este link no WhatsApp:\n", url)
    except Exception as e:
        print("Erro ao gerar link de cobranca:", e)

def link_duvidas_whatsapp():
    try:
        print("\n=== Link de Duvidas (WhatsApp) ===")
        msg = "Ola! Aqui e o {}. Como podemos ajudar?".format(NOME_ACADEMIA)
        url = whats_link(WHATS_DUVIDAS, msg)
        print("Link para duvidas (admin):\n", url)
    except Exception as e:
        print("Erro ao gerar link de duvidas:", e)

def _login():
    tentativas = 3
    while tentativas > 0:
        senha = input("Senha do sistema: ").strip()
        if senha == SENHA_SISTEMA:
            print("Acesso liberado!\n")
            return True
        tentativas -= 1
        print("Senha incorreta. Tentativas restantes: {}".format(tentativas))
    print("Acesso bloqueado.")
    return False

def _menu():
    print("\n=== SISTEMA STRIKER v6 ASCII ===")
    print("1) Listar planos")
    print("2) Cadastrar aluno")
    print("3) Registrar presenca")
    print("4) Listar presencas por CPF")
    print("5) Registrar pagamento por plano")
    print("6) Mostrar PIX / Maps")
    print("7) Gerar link de cobranca (WhatsApp)")
    print("8) Gerar link de duvidas (WhatsApp)")
    print("9) Gerar relatorio de lucro mensal")
    print("10) Listar alunos cadastrados")
    print("11) Procurar alunos por plano")
    print("12) Editar aluno cadastrado (por CPF)")
    print("13) Excluir aluno (por CPF)")
    print("14) Listar alunos em atraso na mensalidade")
    print("0) Sair")

def _bootstrap_csvs():
    _garantir_csv(ARQ_ALUNOS, CAMPOS)
    _garantir_csv(ARQ_PAGAMENTOS, ["aluno", "valor", "data_pagamento"])
    _garantir_csv(ARQ_PRESENCAS, ["data_iso", "cpf"])
    _garantir_csv(ARQ_DESPESAS_FIXAS, ["nome", "valor_mensal"])
    _garantir_csv(ARQ_REPASSES, ["professor", "mes", "ano", "valor"])
    _garantir_csv(ARQ_RELATORIO_LUCRO, ["ano", "mes", "total_pagamentos", "despesas_fixas", "repasses", "lucro"])

def main():
    _bootstrap_csvs()
    carregar_alunos()
    if not _login():
        return
    while True:
        _menu()
        opc = input("Escolha uma opcao: ").strip()
        if opc == "1":
            listar_planos()
        elif opc == "2":
            cadastrar_aluno()
        elif opc == "3":
            registrar_presenca()
        elif opc == "4":
            listar_presencas_do_cpf()
        elif opc == "5":
            registrar_pagamento()
        elif opc == "6":
            mostrar_pix()
        elif opc == "7":
            link_cobranca_whatsapp()
        elif opc == "8":
            link_duvidas_whatsapp()
        elif opc == "9":
            gerar_relatorio_lucro()
        elif opc == "10":
            listar_alunos()
        elif opc == "11":
            buscar_alunos_por_plano()
        elif opc == "12":
            editar_aluno()
        elif opc == "13":
            excluir_aluno()
        elif opc == "14":
            listar_alunos_em_atraso()
        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opcao invalida. Tente novamente.")

if _name_ == "_main_":
    main()
