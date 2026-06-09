# Análise Estatística do Sensor Espacial AMT00102

Este projeto realiza uma análise estatística aprofundada sobre dados reais coletados pelo **AMT00102**, um magnetômetro embarcado em uma missão espacial experimental. O conjunto de dados cobre o período de **abril de 2009 a outubro de 2013**.

===================

## O que é um Magnetômetro?

Um magnetômetro é um sensor que mede a intensidade e a direção do campo magnético ao redor dele, utilizando a unidade **nanoTesla (nT)**. No contexto aeroespacial, ele é fundamental para:
* **Orientação de Satélites:** Determinar para onde o satélite está apontando usando o campo magnético da Terra.
* **Clima Espacial:** Detectar anomalias, perturbações magnéticas e monitorar tempestades solares.
* **Navegação:** Apoiar os sistemas de navegação de bordo.

===================

## O que foi feito?

A base de dados original conta com mais de **8,6 milhões de leituras brutas**. Para tornar visível esta análise, foi utilizado um arquivo de estatísticas agregadas em **janelas de 6 horas** (totalizando 6.425 registros).

O projeto aplica conceitos fundamentais de **Estatística Descritiva** e **Visualização de Dados** utilizando Python, englobando:
* Tabelas de distribuição de frequências.
* Gráficos de histograma e séries temporais.
* Cálculo de medidas de tendência central (média, mediana).
* Medidas de dispersão (variância, desvio padrão) e quartis.

===================

## Aplicação na Vida Real

Na engenharia aeroespacial, as análises desenvolvidas neste projeto são aplicadas para:
1.  **Monitoramento de Saúde (Telemetry Health):** Identificar quedas anômalas no volume de leituras, o que pode indicar falhas de comunicação ou desligamento do equipamento.
2.  **Segurança da Missão:** Detectar valores extremos do campo magnético que sinalizam tempestades geomagnéticas capazes de afetar a operação do satélite.
3.  **Calibração:** Analisar a série temporal para revelar padrões orbitais cíclicos, ajudando a calibrar o sensor e validar sua precisão ao longo dos anos de missão.

===================

## Tecnologias Utilizadas

* **Python** (Pandas, NumPy)
* **Matplotlib / Seaborn** (Visualização de dados)
* **Visual Studio Code** (Ambiente de desenvolvimento)
