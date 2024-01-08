# projeto-aa-3-Fixed-Probability-Counter-1/16-Space-Saving-Count
## file_processor.py

Para executar o arquivo `file_processor.py`, é necessário passar os seguintes argumentos:

- `-f` ou `--file`: Este é o caminho para o documento que se quer processar.
- `-l` ou `--language`: Esta é o idioma em que o documento está.
## Exemplo de uso


```bash
py file_processor.py -f docs\La_venganza_de_Don_Mendo.txt -l es
```

## run.py

Para executar o arquivo `run.py`, é necessário passar os seguintes argumentos:

- `-f` ou `--file`: Este é o caminho para o documento que se quer ler.
- `-n` ou `--number`: Este é o número máximo de frequências de letras que o programa deve retornar. O valor padrão é 26.
- `-e` ou `--exact`: Se este argumento for passado o contador exato será executado.
- `-a` ou `--approximate`: Se este argumento for passado o contador aproxiamdo será executado.
- `-ds` ou `--data_stream`: Se este argumento for passado o algoritmo de Metwally et al. será executado.
- `-k` ou `--k`: Este é o número de vezes que o algoritmo aproximado é executado. O valor padrão é 1.

## Exemplo de uso

Aqui está um exemplo de como pode executar o programa pela linha de comandos:

```bash
py run.py -e -f docs_processed\The_Tragedy_of_Romeo_and_Juliet.txt -n 10
```

## results.py
Necessário alterar diretamente o código para carregar os ficheiros e produzir os gráficos/resultados desejados