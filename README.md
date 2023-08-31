# Simulação de Ecossistema em Python

#### O projeto consiste em uma simulação onde duas espécies de animais (coelhos e raposas), são simuladas em um campo com o objetivo de criar um ecossistema em que as duas espécies possam coexistir.

#### As raposas se alimentam dos coelhos, que se alimentam de frutas. os dois precisam de água regularmente.
#### Caso as raposas cacem muito os coelhos, acabam os aniquilando e ambos são levados a extinção.

#### O equilibrio acontece quando os coelhos conseguem adiquirir atributos que seperem os da raposa mas não a ponto de extinguilas.

#### Todo os dados do simulação são registrados e uma análise é feita com ferramentas de data science.

__________________________________________________________________________________________________________________________________________

Visão Geral
<img src="https://github.com/Leonardo8133/Ec-Simulation/blob/master/images/Figure_0.png" width=100%>
<img src="https://github.com/Leonardo8133/Ec-Simulation/blob/master/images/Figure_1.png" width=30%>
<img src="https://github.com/Leonardo8133/Ec-Simulation/blob/master/images/Figure_2.png" width=30%>
<img src="https://github.com/Leonardo8133/Ec-Simulation/blob/master/images/Figure_4.png" width=30%>

### Funcionamento:

##### O projeto engloba:
<ol>
    <li>Mapa gerado aleatoriamento usando Perlin Noise</li>
    <li>Técnicas de otimização como Chunk Drawing</li>
    <li>Regressão Logística</li>
    <li>Redes Neurais Genéticas como Inteligencia Artificial</li>
    <li>Dados Salvos em DataFrames (Pandas) e Guardados em arquivos criptografados (pickle)</li>
    <li>Visualizalçao dos Dados em Pandas/Matplotlib/Seaborn/Numpy</li>
</ol>

#### Funcionamento: 
   Cada entidade (animal), precisa de comida, água e descanso para sobreviver. Podem também, se reproduzir quando o nível de "amor" está alto e tem como velocidade o atributo mais importante.
    As entidades também contam com um gene e um multiplicador aleatório de fome, sede, velocidade, amor e descanso. O gene foi resultado de muitas horas de treinamento de uma rede neural genética chamada (NEAT).
 ###### Rede Neural NEAT: 
   O treinamento da rede neural NEAT consiste em colocar uma grande população no mapa, dar um gene unico para cada indivíduo e deixar que eles usem a rede neural como tomador de decisão em como agir (quando comer, beber e etc...).
 Quando toda a população morre ou demora muita para morrer, a simulação é resetada e uma nova população é colocada no mundo, mas dessa vez, os genes dos melhores animais da geração passada estarão mais presentes na geração atual. E assim o treinamento corre por Diversas geraçoes, até que um grupo de indivíduos "Perfeitos" sejam encontrados e estes servem como Modelo para a simulação final.

Todos os Arquivos .txt marcados com [data] podem ser abertos com o data_visu.py, modificando o diretorio de leitura na linha 15.

#### Bibliotecas Necessárias
<ul>
    <li><a href="https://pypi.org/project/pandas/"> Pandas <a></li>
    <li><a href="https://pypi.org/project/numpy/"> Numpy <a></li>
    <li><a href="https://pypi.org/project/matplotlib/"> Matplotlib <a></li>
    <li><a href="https://pypi.org/project/pygame/"> Pygame <a></li>
    <li><a href="https://pypi.org/project/neat-python/"> Neat Python <a></li>  
    <li><a href="https://pypi.org/project/pathfinfing/"> Pathfinfing <a></li>
    <li>Sklearn (if you use Logistic Regression IA.)</li>
</ul>


## Para rodar o código, simplismente de run no simulation.py


    
