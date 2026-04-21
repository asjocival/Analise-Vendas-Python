import pandas as pd

# ler arquivo
df = pd.read_csv("vendas.csv", sep=';', encoding='latin-1')

# limpar nomes das colunas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# remover colunas vazias
df = df.loc[:, ~df.columns.str.contains('unnamed', case=False)]

# visualizar dados
print(df.head())
print(df.info())

# Remover coluna duplicada
df = df.drop(columns=['produtoid.1'])

# Converter números corretamente
df['receita'] = (
    df['receita']
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df['custo'] = (
    df['custo']
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df['lucro'] = (
    df['lucro']
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

df['valor_perda'] = (
    df['valor_perda']
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# Converter data
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')

# Conferir tudo
print(df.info())

# ------------------------------------------------------------------------------------------
# Análises

# Receita Total
print("Receita total:", df['receita'].sum())

# Lucro Total
print("Lucro total:", df['lucro'].sum())

# Margem de Lucro
margem = df['lucro'].sum() / df['receita'].sum() * 100
print(f"Margem de lucro: {margem:.2f}%")

# Top 5 Vendedores
top_vendedores = df.groupby('vendedor')['receita'].sum().sort_values(ascending=False)
print(top_vendedores.head(5))

# Produtos mais Lucrativos
top_produtos = df.groupby('produtos')['lucro'].sum().sort_values(ascending=False)
print(top_produtos.head(5))

# Receita por Região
regiao = df.groupby('regiao')['receita'].sum().sort_values(ascending=False)
print(regiao)

# Lucro por Região
print(df.groupby('regiao')['lucro'].sum())

# Análise de Perdas
print("Total de perdas:", df['valor_perda'].sum())

# Onde Está o Problema?
perdas_tipo = df.groupby('tipo_perda')['valor_perda'].sum().sort_values(ascending=False)
print(perdas_tipo)

# margem por vendedor
margem_vendedor = df.groupby('vendedor').apply(
    lambda x: x['lucro'].sum() / x['receita'].sum() * 100
).sort_values(ascending=False)

print(margem_vendedor.head(5))

# prejuízo por produto
prejuizo_produtos = df.groupby('produtos')['lucro'].sum().sort_values()
print(prejuizo_produtos.head(5))

# perdas por região
perdas_regiao = df.groupby('regiao')['valor_perda'].sum().sort_values(ascending=False)
print(perdas_regiao)

# ------------------------------------------------------------------------
# Gráficos

import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 2, figsize=(12,5))

# gráfico 1 - Top 5 Vendedores
top_vendedores.head(5).plot(kind='bar', ax=axs[0])
axs[0].set_title("Top Vendedores")

# gráfico 2 - Receita por região
regiao.plot(kind='bar', ax=axs[1])
axs[1].set_title("Receita por Região")

plt.tight_layout()
plt.show()