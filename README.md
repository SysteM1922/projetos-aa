# projeto-aa-1-Max-Weight-Cut
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
- `-g_s` ou `--simple_greedy`: Se este argumento for passado, a pesquisa simple greedy será executada.
- `-g_s_sorted` ou `--simple_greedy_sorted`: Se este argumento for passado, a pesquisa simple greedy sorted será executada.
- `-g_sg3` ou `--sg3_greedy`: Se este argumento for passado, a pesquisa greedy Sahni-Gonzalez-3 será executada.

## Exemplo de uso

Aqui está um exemplo de como você pode executar o arquivo:

```bash
python run.py -min_v 2 -max_v 50 -g_sg3
```
Para guardar os resultados em ficheiros é necessário descomentar algumas linhas na main()

## file_loader.py
Necessário alterar diretamente o código para carregar os ficheiros e produzir os gráficos desejados