![](https://img.shields.io/badge/graph-heuristics-orange)
![](https://img.shields.io/badge/vehicle_routing-blue)
![](https://img.shields.io/badge/graph-database-yellow)
![](https://img.shields.io/badge/AI-Machine_Learning-purple)
![](https://img.shields.io/badge/OpenStreetMap-green)
![](https://img.shields.io/badge/Ortools-red)
![](https://img.shields.io/badge/NetworkX-blue)
![](https://img.shields.io/badge/Folium-green)
![](https://img.shields.io/badge/Streamlit-brightgreen)
![](https://img.shields.io/badge/Neo4j-yellow)
![](https://img.shields.io/badge/PostgreSQL-blue)
![](https://img.shields.io/badge/DBeaver-brown)

# Roteamento de Veículos

### [Main](#roteamento-de-veiculos) | [Installation](#installation) | [Architecture](#architecture) | [Contributors](#contributors) | [Licence](#licence)

Trabalho final de Algoritmos e Estruturas de Dados 2 e Banco de dados. Resolução do problema de roteamento de veículos.

![graph_from_ufg](images/ufg_graph.png)
*UFG - Campus samambaia e proximidades*

Nos modelamos a cidade por meio de um grafo, sendo as ruas as arestas, e os nós as intersecções das ruas. Nesse grafo, rodamos os algoritmos como de Djistraka e A*.

## Sobre o Problema

O problema de roteamento de veículos (VRP - Vehicle Routing Problem) é um dos desafios mais significativos na área de logística e transporte. Ele envolve a determinação das rotas mais eficientes para um conjunto de veículos que devem realizar entregas ou serviços em diversos locais. O objetivo principal é minimizar o custo total, que pode incluir a distância percorrida, o tempo de viagem ou o consumo de combustível, enquanto se atende a todas as restrições operacionais, como capacidade dos veículos e janelas de tempo para as entregas.

### Subvariações do Problema de Roteamento de Veículos

1. **VRP Básico:** Otimização das rotas de veículos sem nenhuma restrição adicional, focando apenas na minimização da distância total percorrida. Nossa solução.
2. **VRP com Janelas de Tempo (VRPTW):** As entregas devem ser feitas dentro de intervalos de tempo específicos para cada local.
3. **VRP com Capacidades (CVRP):** Considera a capacidade limitada de carga dos veículos.
4. **VRP com Múltiplos Depósitos (MDVRP):** Envolve múltiplos pontos de partida e chegada para os veículos.
5. **VRP com Frota Heterogênea:** Considera veículos com diferentes capacidades e custos operacionais.
6. **Problema do Caixeiro Viajante (TSP):** Um caso especial do VRP, onde um único veículo deve visitar todos os locais exatamente uma vez e retornar ao ponto de partida.

## Ferramentas Utilizadas

- **OpenStreetMap:** Fonte de dados geográficos.
- **Ortools:** Ferramenta de otimização do Google para resolver problemas combinatórios, incluindo VRP.
- **NetworkX:** Biblioteca Python para a criação, manipulação e estudo da estrutura, dinâmica e funções de grafos complexos.
- **Folium:** Biblioteca Python para visualização de dados geoespaciais.
- **Streamlit:** Ferramenta de compartilhamento de dados que facilita a criação de aplicações web interativas.
- **Neo4j:** Banco de dados de grafos para salvar a modelagem de grafos da cidade.
- **PostgreSQL:** Banco de dados relacional para gerencia das informações das entregas
- **DBeaver:** Para se conectar e trabalhar com os bancos de dados de maneira mais facil.

## Installation

Siga estes passos para instalar corretamente e contribuir:

```bash
python3 -m venv <name_you_want> # Criar ambiente virtual

git clone https://github.com/guilhermefrazao/AED2_roteamento_de_veiculos.git # Clonar repositório

source <name_you_want>/bin/activate # Ativar ambiente virtual

cd AED2_roteamento_de_veiculos

pip install -r requirements.txt # Instalar dependências Python

code . # Abrir VSCode (opcional)

streamlit run app.py
```


Tenha certeza de ter git e python instalado. Recomendamos baixar [DBeaver](https://dbeaver.io/download/) para trabalhar com o PostgreSQL. 

Baixe o PostgreSQL e crie um banco de dados, coloque as informações de dbname, user, localhost e etc nos parametros do [banco_de_daos.py](entregaai/banco_de_dados.py). Caso opte pelo uso do DBeaver, faça a conexão e importe os csv em `/data`.

*NOTA*: Os csv foram gerados com dados falsos, por meio de scripts em Python.

## Modelagem de Dados
#### Modelagem do Banco de Dados Relacional (PostgreSQL)

![Relational Database](images/relational-bd.png)

#### Modelagem com Banco de Dados de Grafos (Neo4j)

![Graph Database](images/graph-bd.png)

## Info, Links and Others:

### Architecture

    .
    ├── code        #code and tests
    ├── data        # data used in PostgreSQL
    ├── docs        # Reports
    ├── entregaai   #streamlit application
    │   └── static
    │       ├── images  #images used on streamlit
    │       └── maps    #maps generated
    └── images      #images used
    └── LICENCE.md 
    └── README.md
    └── requirements.txt

### Contributors:

- Carlos Henrique Goncalves Batista
- Guilherme Frazão Fernandes
- Pedro Antonio Maciel Saraiva

### LICENCE: 

**Creative Commons Attribution-NonCommercial (CC BY-NC)**

You can see the licence [here](https://www.creativecommons.org/licenses/by-nc/4.0/deed.en)