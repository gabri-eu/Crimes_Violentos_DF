"""
gerar_figuras.py — Gera as figuras do projeto Crimes Violentos DF e as salva
em ../imagens/ para exibição no README do GitHub.

Baseia-se no notebook notebooks/03_analise_descritiva.ipynb (células 1-29),
adicionando savefig() antes de cada plt.show() para que as imagens sejam
persistidas e versionadas.

Uso:
    python scripts/gerar_figuras.py
(rode a partir da raiz do projeto ou de dentro de scripts/)
"""
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
pd.set_option("display.float_format", "{:,.2f}".format)

plt.style.use("default")
sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parent.parent

DADOS_PROCESSADOS = ROOT / "dados_processados"
RESULTADOS = ROOT / "resultados"
IMAGENS = ROOT / "imagens"

RESULTADOS.mkdir(exist_ok=True)
IMAGENS.mkdir(exist_ok=True)


def _save(fig, nome):
    """Salva a figura em imagens/ com nome descritivo e bbox ajustado."""
    caminho = IMAGENS / nome
    fig.savefig(str(caminho), bbox_inches="tight", dpi=120)
    print(f"salvo: {caminho.relative_to(ROOT)}")


# ── Carga da base ─────────────────────────────────────────────────────────
base = pd.read_parquet(DADOS_PROCESSADOS / "base_analitica.parquet")

# ── Assinatura dos gráficos ─────────────────────────────────────────────────
ANO = datetime.now().year
GITHUB = "https://github.com/gabri-eu"


def assinatura_figura(fig):
    fig.text(
        0.99,
        0.01,
        (
            f"Elaboração: Gabriel Santana ({ANO}) | "
            f"GitHub: {GITHUB}"
        ),
        ha="right",
        va="bottom",
        fontsize=9,
        style="italic",
        color="dimgray",
    )


# ── Bases analíticas ────────────────────────────────────────────────────────
base_ra = base.query("nivel_geografico == 'Região Administrativa'").copy()
base_ra_territorial = base_ra.query(
    "regiao_administrativa != 'Unidades Prisionais'"
).copy()
base_unidades_prisionais = base_ra.query(
    "regiao_administrativa == 'Unidades Prisionais'"
).copy()
base_df = base.query("nivel_geografico == 'Distrito Federal'").copy()

# ── Figura 1 — Distribuição das Ocorrências ────────────────────────────────
limite = 100
dados = base_ra_territorial.loc[base_ra_territorial["ocorrencias"] <= limite, "ocorrencias"]

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
ax.hist(dados, bins=25, color="#7A1628", edgecolor="white", linewidth=0.8, alpha=0.90)
ax.set_xlim(0, limite)
ax.set_title("Distribuição das Ocorrências", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Número de ocorrências", fontsize=12)
ax.set_ylabel("Frequência", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.01, -0.03,
    "Figura 1. Distribuição do número de ocorrências registradas entre 2015 e 2024 por observação da base analítica. "
    "Os valores foram limitados a 100 ocorrências para melhorar a visualização da distribuição central "
    "e reduzir a influência de valores extremos.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.22, top=0.90)
_save(fig, "figura_01_distribuicao_ocorrencias.png")
plt.show()

# ── Figura 2 — Distribuição das Taxas de Crimes Violentos ───────────────────
limite = base_ra_territorial["taxa_10mil"].quantile(0.99)
dados = base_ra_territorial.loc[base_ra_territorial["taxa_10mil"] <= limite, "taxa_10mil"]

fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
ax.hist(dados, bins=30, color="#A61C2F", edgecolor="white", linewidth=0.8, alpha=0.90)
ax.set_title("Distribuição das Taxas de Crimes Violentos por 10 mil Habitantes",
             fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Taxa por 10 mil habitantes", fontsize=12)
ax.set_ylabel("Frequência", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.01, -0.03,
    "Figura 2. Distribuição das taxas de crimes violentos por 10 mil habitantes nas "
    "Regiões Administrativas do Distrito Federal, entre 2015 e 2024. Para facilitar a visualização da "
    "distribuição principal, foram excluídos os 1% maiores valores (percentil 99).",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.22, top=0.90)
_save(fig, "figura_02_distribuicao_taxas.png")
plt.show()

# ── Figura 3 — Ocorrências por Tipo de Crime ────────────────────────────────
crime = base_ra_territorial.groupby("tipo_crime")["ocorrencias"].sum().sort_values(ascending=True)
total_df = base_df["ocorrencias"].sum()

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=120)
ax.barh(crime.index, crime.values, color="#6D071A", edgecolor="white", linewidth=0.8)
ax.set_title("Ocorrências por Tipo de Crime", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Número de ocorrências", fontsize=12)
ax.set_ylabel("")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.text(0.98, 0.05, f"Total no DF\n{total_df:,} ocorrências",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=10,
        bbox=dict(facecolor="#F5F5F5", edgecolor="gray", boxstyle="round,pad=0.4"))
fig.text(0.01, -0.03,
    "Figura 3. Total de ocorrências registradas por tipo de crime entre 2015 e 2024. "
    "O quadro destaca o número total de ocorrências contabilizadas para o Distrito Federal "
    "no período analisado.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.22, top=0.90)
_save(fig, "figura_03_ocorrencias_tipo_crime.png")
plt.show()

# ── Figura 4 — Distribuição das Taxas por Tipo de Crime (boxplot) ────────────
fig, ax = plt.subplots(figsize=(11, 6), dpi=120)
sns.boxplot(data=base_ra_territorial, x="tipo_crime", y="taxa_10mil", showfliers=False,
            width=0.6, color="#A61C2F",
            medianprops={"color": "black", "linewidth": 2},
            whiskerprops={"linewidth": 1.2}, capprops={"linewidth": 1.2},
            boxprops={"edgecolor": "black"}, ax=ax)
ax.set_title("Distribuição das Taxas de Crimes Violentos por Tipo de Crime",
             fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("")
ax.set_ylabel("Taxa por 10 mil habitantes", fontsize=12)
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xticks(rotation=15)
fig.text(0.01, -0.03,
    "Figura 4. Distribuição das taxas anuais de crimes violentos por 10 mil habitantes "
    "segundo o tipo de crime, entre 2015 e 2024. As caixas representam o intervalo interquartílico (Q1–Q3), "
    "a linha central indica a mediana e os valores extremos foram omitidos para facilitar a comparação entre as distribuições.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.22, top=0.90)
_save(fig, "figura_04_boxplot_tipo_crime.png")
plt.show()

# ── Figura 5 — Ocorrências por Região Administrativa ────────────────────────
ranking = base_ra_territorial.groupby("regiao_administrativa")["ocorrencias"].sum().sort_values(ascending=True)
media_df = ranking.mean()

fig, ax = plt.subplots(figsize=(11, 12), dpi=120)
ax.barh(ranking.index, ranking.values, color="#6D071A", edgecolor="white", linewidth=0.7)
ax.axvline(media_df, color="black", linestyle="--", linewidth=2, label=f"Média das RAs ({media_df:.0f})")
ax.set_title("Número de Ocorrências por Região Administrativa", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Número de ocorrências", fontsize=12)
ax.set_ylabel("")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.text(0.01, -0.02,
    "Figura 5. Total de ocorrências registradas por Região Administrativa entre 2015 e 2024. "
    "A linha tracejada representa a média de ocorrências entre as Regiões Administrativas, "
    "permitindo identificar quais regiões apresentam valores acima ou abaixo do comportamento médio.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(left=0.28, bottom=0.15, top=0.92)
_save(fig, "figura_05_ocorrencias_ra.png")
plt.show()

# ── Figura 6 — Taxa Média por Região Administrativa ─────────────────────────
ranking = base_ra_territorial.loc[base_ra_territorial["regiao_administrativa"] != "Unidades Prisionais"] \
    .groupby("regiao_administrativa")["taxa_10mil"].mean().sort_values()
media_ra = ranking.mean()

fig, ax = plt.subplots(figsize=(11, 12), dpi=120)
ax.barh(ranking.index, ranking.values, color="#A61C2F", edgecolor="white", linewidth=0.7)
ax.axvline(media_ra, color="black", linestyle="--", linewidth=2, label=f"Média das RAs ({media_ra:.2f})")
ax.set_title("Taxa Média de Crimes Violentos por Região Administrativa", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Taxa por 10 mil habitantes", fontsize=12)
ax.set_ylabel("")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.text(0.01, -0.02,
    "Figura 6. Taxa média de crimes violentos por 10 mil habitantes entre 2015 e 2024 nas Regiões "
    "Administrativas do Distrito Federal. A linha tracejada representa a média das "
    "taxas observadas entre as Regiões Administrativas, permitindo identificar quais "
    "localidades apresentam níveis de criminalidade superiores ou inferiores ao padrão médio.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(left=0.30, bottom=0.15, top=0.92)
_save(fig, "figura_06_taxa_ra.png")
plt.show()

# ── Figura 7 — População por Região Administrativa ──────────────────────────
ranking = base_ra_territorial.loc[base_ra["regiao_administrativa"] != "Unidades Prisionais"] \
    .groupby("regiao_administrativa")["populacao"].mean().sort_values()
media_ra = ranking.mean()

fig, ax = plt.subplots(figsize=(11, 12), dpi=120)
ax.barh(ranking.index, ranking.values, color="#4A4A4A", edgecolor="white", linewidth=0.7)
ax.axvline(media_ra, color="black", linestyle="--", linewidth=2, label=f"Média das RAs ({media_ra:,.0f} hab.)")
ax.set_title("População Média por Região Administrativa", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Habitantes", fontsize=12)
ax.set_ylabel("")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.text(0.01, -0.02,
    "Figura 7. População média das Regiões Administrativas do Distrito Federal, "
    "utilizada como denominador no cálculo das taxas de crimes violentos por "
    "10 mil habitantes, entre 2015 e 2024. A linha tracejada representa a população média entre as "
    "Regiões Administrativas.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(left=0.30, bottom=0.15, top=0.92)
_save(fig, "figura_07_populacao_ra.png")
plt.show()

# ── Figura 8 — Renda Domiciliar per Capita por Região Administrativa ─────────
ranking = base_ra_territorial.loc[base_ra["regiao_administrativa"] != "Unidades Prisionais"] \
    .groupby("regiao_administrativa")["renda_per_capita"].mean().sort_values()
media_ra = ranking.mean()

fig, ax = plt.subplots(figsize=(11, 12), dpi=120)
ax.barh(ranking.index, ranking.values, color="#4A4A4A", edgecolor="white", linewidth=0.7)
ax.axvline(media_ra, color="black", linestyle="--", linewidth=2, label=f"Média das RAs (R$ {media_ra:,.0f})")
ax.set_title("Renda Domiciliar per Capita por Região Administrativa", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Renda domiciliar per capita (R$)", fontsize=12)
ax.set_ylabel("")
ax.grid(axis="x", linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.text(0.01, -0.02,
    "Figura 8. Renda domiciliar per capita média das Regiões Administrativas do "
    "Distrito Federal. A linha tracejada representa a renda média observada entre "
    "as Regiões Administrativas, permitindo identificar localidades com níveis "
    "socioeconômicos acima ou abaixo da média.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(left=0.30, bottom=0.15, top=0.92)
_save(fig, "figura_08_renda_ra.png")
plt.show()

# ── Figura 9 — População e Ocorrências (regplot) ────────────────────────────
dados = base_ra_territorial.loc[base_ra["regiao_administrativa"] != "Unidades Prisionais"] \
    .groupby("regiao_administrativa", as_index=False).agg(
        populacao=("populacao", "mean"), ocorrencias=("ocorrencias", "sum"))

fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
sns.regplot(data=dados, x="populacao", y="ocorrencias",
            scatter_kws={"s": 60, "color": "#6D071A", "alpha": 0.80},
            line_kws={"color": "black", "linewidth": 2}, ax=ax)
ax.set_title("População e Número de Ocorrências", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("População")
ax.set_ylabel("Número de ocorrências")
ax.grid(linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.01, -0.03,
    "Figura 9. Relação entre a população das Regiões Administrativas e o número "
    "total de ocorrências de crimes violentos registradas entre 2015 e 2024. "
    "A linha representa o ajuste linear estimado.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.18)
_save(fig, "figura_09_populacao_ocorrencias.png")
plt.show()

# ── Figura 10 — Renda per Capita e Taxa de Crimes Violentos (regplot) ───────
dados = base_ra_territorial.loc[base_ra_territorial["regiao_administrativa"] != "Unidades Prisionais"] \
    .groupby("regiao_administrativa", as_index=False).agg(
        renda=("renda_per_capita", "mean"), taxa=("taxa_10mil", "mean"))

fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
sns.regplot(data=dados, x="renda", y="taxa",
            scatter_kws={"s": 60, "color": "#A61C2F", "alpha": 0.80},
            line_kws={"color": "black", "linewidth": 2}, ax=ax)
ax.set_title("Renda Domiciliar per Capita e Taxa de Crimes Violentos", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Renda domiciliar per capita (R$)")
ax.set_ylabel("Taxa por 10 mil habitantes")
ax.grid(linestyle="--", alpha=0.35)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.01, -0.03,
    "Figura 10. Relação entre a renda domiciliar per capita das Regiões "
    "Administrativas e a taxa média de crimes violentos por 10 mil habitantes, entre 2015 e 2024. "
    "A linha representa o ajuste linear estimado.",
    ha="left", va="top", fontsize=9, style="italic", wrap=True)
assinatura_figura(fig)
plt.subplots_adjust(bottom=0.18)
_save(fig, "figura_10_renda_taxa.png")
plt.show()

print("Concluído: 10 figuras salvas em imagens/")
