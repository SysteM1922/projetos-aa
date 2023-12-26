# projeto-aa-2-Randomized-Max-Weight-Cut
## graph_generator.py

Para executar o arquivo `graph_generator.py`, é necessário passar os seguintes argumentos:

- `-min_v` ou `--minimum_vertices`: Este é o número mínimo de vértices. O valor padrão é 2.
- `-max_v` ou `--maximum_vertices`: Este é o número máximo de vértices. Não existe um valor padrão para este e é mandatório atribuir-lhe um valor para gerar grafos.
- `-p` ou `--percentage`: Este é a percentagem de probabilidade para a geração de arestas. O valor padrão é 4, que corresponde às percentagens [12.5%, 25%, 50%, 75%]
- `-s` ou `--save`: Se este argumento for passado, o gráfico gerado será guardado
- `-n` ou `--name`: Este é o nome do gráfico a ser carregado. Não há valor padrão para isso.
- `-l` ou `--load`: Se este argumento for passado, o gráfico com o nome fornecido será carregado.

## Exemplo de uso


```bash
python graph_generator.py  -max_v 10 --save
```

## run.py

Para executar o arquivo `run.py`, é necessário passar os seguintes argumentos:

- `-min_v` ou `--minimum_vertices`: Este é o número mínimo de vértices. O valor padrão é 2.
- `-max_v` ou `--maximum_vertices`: Este é o número máximo de vértices. Não existe um valor padrão para este e é mandatório atribuir-lhe um valor para gerar grafos.
- `-p` ou `--percentage`: Este é o percentual de probabilidade para a geração de arestas. O valor padrão é 4, que corresponde às percentagens [12.5%, 25%, 50%, 75%]
- `-e_s` ou `--exhaustive`: Se este argumento for passado, a pesquisa exaustiva será executada.
- `-g_sg3` ou `--sg3_greedy`: Se este argumento for passado, a pesquisa greedy Sahni-Gonzalez-3 será executada.
- `-m_c` ou `--monte_carlo_random`: Se este argumento for passado, a pesquisa randomizada de Monte Carlo será executada.
- `-b_e` ou `--random_node_choose_best_edge`: Se este argumento for passado, a pesquisa randomizada Nó Aleatório escolhe Melhor Aresta será executada.
- `-max_tries` ou `--max_tries`: Este é a percentagem do número máximo de tentativas que um algoritmo randomizado pode testar. O valor padrão é 100
- `-max_time` ou `--max_time`: Este é o tempo máximo que um algoritmo randomizado pode demorar a pesquisar cada grafo. O valor padrão é infinito

## Exemplo de uso

Aqui está um exemplo de como pode executar o programa pela linha de comandos:

```bash
python run.py -min_v 2 -max_v 50 -m_c -max_time 2 -max_tries 10
```
Para guardar os resultados em ficheiros é necessário descomentar algumas linhas na main()

## file_loader.py
Necessário alterar diretamente o código para carregar os ficheiros e produzir os gráficos desejados

## graph_converter.py
Utilizado para converter o grafo .txt SW10000EWD em formato .gml