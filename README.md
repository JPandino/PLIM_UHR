# PLIM-UHR
MODELO DE PROGRAMAÇÃO LINEAR INTEIRA MISTA PARA USINAS HIDRELÉTRICAS REVERSÍVEIS - PLIM-UHR

## Descrição
Uma Usina Hidrelétrica Reversível (UHR) funciona como um Sistemas de Armazenamento de Energia (SAE) que trabalha com dois reservatórios, um superior e um inferior, juntamente com turbinas reversíveis, para armazenar energia potencial gravitacional. O presente modelo foi desenvolvido buscando maximizar o lucro de uma UHR por meio da arbitragem de preços no mercado spot (curto prazo), através da operação de curto prazo.
Este é um modelo de programação linear inteira mista, orientado a objetos, que considera partidas e paradas de unidades geradoras da UHR. É modelado com a linguagem de programação Python, em conjunto com a biblioteca Pyomo, fazendo uso de uma linguagem de programação de otimização de alto nível, que pode ser usada junto com os solucionadores CPLEX, Gurobi, GLPK, SCIP e IPOPT.
O modelo é capaz de obter a melhor resposta final da otimização do lucro expressando o planejamento operacional **diário** para isso.

**Nota:** Embora seja possível expandir o horizonte de planejamento para além de 24 horas, a elevada complexidade inerente a problemas com variáveis inteiras mistas e múltiplos estágios frequentemente torna inviável a obtenção de uma solução ótima utilizando solucionadores comerciais.

## Modelo Linear
As funções de geração e consumo hidráulicas, utilizadas dentro do modelo, tem comportamento não linear. A não linearidade está relacionada à altura de queda utilizada nas funções de geração e consumo hidráulicas.

## Dependências
- Pandas
- Pyomo
- CPLEX (Solver)

## Entradas
### Parâmetros da UHR (Hipotético)
  - Unidades Geradoras UG (unit): ["A", "B", "C", "D"]
  - Volume Máximo do R. Superior (vsmax): 5779 hm³
  - Volume Mínimo do R. Superior (vsmin): 1974 hm³
  - Volume Máximo do R. Inferior (vimax): 2950 hm³
  - Volume Mínimo do R. Inferior (vimin): 2562 hm³
  - Vazão Defluente Máxima (qsmax): 10030 m³/s
  - Vazão Defluente Mínima (qimax): 16200 m³/s
  - Vazão Máxima em Modo Turbina (pmax): {"A": 372, "B": 372, "C": 372, "D": 372} m³/s
  - Vazão Máxima em Modo Bomba (pwmax): {"A": 372, "B": 372, "C": 372, "D": 372} m³/s
  - Vazão Mínima em Modo Turbina (pmin): {"A": 50, "B": 50, "C": 50, "D": 50} m³/s
  - Vazão Mínima em Modo Bomba (pwmin): {"A": 50, "B": 50, "C": 50, "D": 50} m³/s
  - Rendimento em Modo Turbina (e_p): {"A": 1.0925, "B": 1.127, "C": 1.0925, "D": 1.127} adimensional
  - Rendimento em Modo Bomba (e_pw): {"A": 1.27, "B": 1.25, "C": 1.27, "D": 1.25} adimensional
  - Rampa de Subida/Descida (rp): 0.8 adimensional
  - Volume Inicial do R. Superior (VIs): 3876.5 hm³
  - Volume Inicial do R. Inferior (VIi): 2756 hm³
  - Volume Final do R. Superior (VFs): 3876.5 hm³
  - Volume Final do R. Inferior (VFi): 2756 hm³
  - Custo de O&M (k1): 8.00 R$/MWh
  - Custo de Partida de uma UG (k2): 1000.0 R$
  - Custo de Parada de uma UG (k3): 1000.0 R$
  - Montante Contratado no Mercado Livre (M_acl): 300.0 MWmédio
  - Preço da Energia Contratada no Mercado Livre (P_acl): 141.58 R$/MWh

### Cenários de Preço e Vazão em escala horária (Séries Temporais)
  - Vazão afluente do reservatório superior [m³/s]
  - Vazão afluente do reservatório inferior [m³/s]
  - Preço da energia no mercado de curto prazo (PLD) [R$/MWh]

  **Nota:** No caso da UHR trabalhar como um sistema fechado, sem afluência nos dois reservatórios ou em somente um deles, a base de dados referente a essa informação deve ser passada com valores iguais a 0 (zero).
  
  **Nota:** Arquivo em formato .csv
## Saídas
  - Vazão Turbinada e Bombeada
  - Partidas e Paradas
  - Mudanças no Modo de Operação (turbina e bomba)
  - Volume Vertido
  - Custos
  - Receitas

