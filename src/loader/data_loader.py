import pandas as pd
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def selecionar_planilha():
    root = tk.Tk()
    root.withdraw()

    arquivo = filedialog.askopenfilename(
        title="Selecione uma planilha",
        filetypes=[
            ("Arquivos Excel", "*.xlsx *.xls"),
            ("Arquivos CSV", "*.csv"),
            ("Todos os arquivos", "*.*")
        ]
    )

    root.destroy()
    return arquivo


def carregar_dados(caminho_arquivo):
    if not caminho_arquivo:
        raise ValueError("Nenhum arquivo foi selecionado.")

    caminho = Path(caminho_arquivo)
    extensao = caminho.suffix.lower()

    if extensao in [".xlsx", ".xls"]:
        df = pd.read_excel(caminho)

    elif extensao == ".csv":
        try:
            df = pd.read_csv(caminho, sep=None, engine="python")
        except Exception:
            df = pd.read_csv(caminho, sep=";", engine="python")

    else:
        raise ValueError(f"Formato não suportado: {extensao}")

    if df.empty:
        raise ValueError("A planilha está vazia.")

    return df


def resumo_inicial(df):
    print("\n" + "=" * 70)
    print("ATHENA ANALYTICS - SMART DATA IMPORTER")
    print("=" * 70)

    print(f"\nLinhas: {df.shape[0]}")
    print(f"Colunas: {df.shape[1]}")

    print("\nCOLUNAS IDENTIFICADAS:")
    for coluna in df.columns:
        print(f"- {coluna}")

    print("\nTIPOS DE DADOS:")
    print(df.dtypes)

    print("\nVALORES AUSENTES POR COLUNA:")
    print(df.isnull().sum())

    print("\nPRIMEIRAS 5 LINHAS:")
    print(df.head())


def executar_importacao():
    print("\nATHENA ANALYTICS")
    print("Inicializando Smart Data Importer...\n")

    try:
        caminho = selecionar_planilha()

        if not caminho:
            print("Nenhuma planilha selecionada.")
            return None

        print(f"Arquivo selecionado:\n{caminho}")

        df = carregar_dados(caminho)
        resumo_inicial(df)

        return df

    except Exception as erro:
        print("\nERRO DURANTE A IMPORTAÇÃO:")
        print(erro)
        return None
