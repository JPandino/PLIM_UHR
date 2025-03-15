# PLIM-UHR
MODELO DE PROGRAMAÇÃO LINEAR INTEIRA MISTA PARA USINAS HIDRELÉTRICAS REVERSÍVEIS - PLIM-UHR

## Descrição
Uma Usina Hidrelétrica Reversível (UHR) funciona como um Sistemas de Armazenamento de Energia (SAE) que trabalha com dois reservatórios, um superior e um inferior, juntamente com turbinas reversíveis, para armazenar energia potencial gravitacional. O presente modelo foi desenvolvido buscando maximizar o lucro de uma UHR por meio da arbitragem de preços no mercado spot (curto prazo), através da operação de curto prazo.
Este é um modelo de programação linear inteira mista, orientado a objetos, que considera partidas e paradas de unidades geradoras da UHR. É modelado com a linguagem de programação Python, em conjunto com a biblioteca Pyomo, fazendo uso de uma linguagem de programação de otimização de alto nível, que pode ser usada junto com os solucionadores Gurobi, GLPK, SCIP e IPOPT.
O modelo é capaz de obter a melhor resposta final da otimização do lucro expressando o planejamento operacional **mensal** para isso.

## Modelo Linear
As funções de geração e consumo hidráulicas, utilizadas dentro do modelo, tem comportamento não linear. A não linearidade está relacionada à altura de queda utilizada nas funções de geração e consumo hidráulicas.

## Dependências
- Pandas
- Numpy
- Pyomo
- Gurobi (Solver)
## Entradas
### Parâmetros da UHR (Exemplo)
  - "unit": ["A", "B", "C", "D"]
  - "vsmax": 5779
  - "vsmin": 1974
  - "vimax": 2950
  - "vimin": 2562
  - "qsmax": 10030
  - "qimax": 16200
  - "pmax": {"A": 372, "B": 372, "C": 372, "D": 372}
  - "pwmax": {"A": 372, "B": 372, "C": 372, "D": 372}
  - "pmin": {"A": 50, "B": 50, "C": 50, "D": 50}
  - "pwmin": {"A": 50, "B": 50, "C": 50, "D": 50}
  - "e_p": {"A": 1.15*0.95, "B": 1.15*0.98, "C": 1.15*0.95, "D": 1.15*0.98}
  - "e_pw": {"A": 1.15/0.90, "B": 1.15/0.92, "C": 1.15/0.90, "D": 1.15/0.92}
  - "rp": 0.8
  - "VIs": 3876.5
  - "VIi": 2756
  - "C": 0.0036
  - "k1": 8.00
  - "k2": 1000.
  - "k3": 1000.
  - "M_acl": 300.0
  - "P_acl": 141.58

### Cenários de **Preço** e **Vazão** em escala horária (Séries Temporais)
  - Vazão afluente do reservatório superior [m³/s]
  - Vazão afluente do reservatório inferior [m³/s]
  - Preço da energia no mercado de curto prazo (PLD) [R$/MWh]
  **Nota:**
## Saídas


## Visualização
Gráficos
