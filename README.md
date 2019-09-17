# Social Network

**Número da Lista**: 2<br>
**Conteúdo da Disciplina**: Grafos 2<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 16/0000840  |  Alexandre Miguel |
| 16/0121612  |  Gabriela Guedes |

## Sobre 
Estudo do Grafo montado a partir de quem o usuário segue no Twitter e, quais desses, se seguem entre si. O projeto tem o objetivo de indentificar nucleos mais conectados e análisar o grafo a partir dos métodos estudados.

<!-- ## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento. -->

## Instalação 
**Linguagem**: Python 3<br>
É necessário ter python 3 instalado e as seguintes bibliotecas:
- plotly
- networkx
- requests
- json

## Uso 
Para rodar o projeto é necessário ter uma conta no twitter cadastrada como [desenvolvedor](https://developer.twitter.com). No site do twitter developer é necessário criar um App e gerar os tokens: API key e API secret key.
Crie um arquivo `tokens.py` seguindo o exemplo de `example_tokens.py` e coloque os tokens criados nos locais indicados.

**Para rodar o projeto:**
```sh
python twitterGraph.py
```




