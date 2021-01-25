# Ceos

Ceos é uma demostração de script que calcula determinados indicadores técnicos a partir de uma série temporal (histórica) representando as variações de preço de um determinado ativo financeiro. 

## Instalação do ambiente

Recomendamos criar uma _virtualenv_ para o projeto. Para instruções de como fazer isso, você pode acessar o link [aqui](https://www.treinaweb.com.br/blog/criando-ambientes-virtuais-para-projetos-python-com-o-virtualenv/).

Com a _virtualenv_ ativada, você pode executar o seguinte comando para instalar as dependências:

```sh
    $ pip install -r requirements.txt
```

## Organização dos arquivos

**indicators.py** : este arquivo armazena a lógica para calcular determinado indicador técnico a partir de uma _dataset_. 

Os indicadores disponíveis são:

* ema (_Exponential Moving Average_ ou Média Móvel Exponencial): calcula a média de preço nos últimos N períodos dando maior importância, peso, para os valores mais recentes. 

* rsi (_Relative Strength Index_ ou Índice de Força Relativa): permite observar o enfraquecimento de uma tendência e pode sinalizar o rompimento de um suporte ou resistência. 

A fórmula do indicador é **100 - (100/(1 + U/D))**, onde U é a média das contações nos últimos _n_ dias considerando apenas os dias em que o ativo subiu de valor, e D é a média das cotações nos últimos _n_ dias considerando os diasem que o ativo perdeu valor. 

A estratégia para calcular esse indicador, foi, dado uma janela de tempo _n_, zerar os dias conforme a variável que estava sendo calculada. No caso U, ou _up_, zerar os dias em que houve perdas, e no caso de D, ou _down_, zerar os dias que houve ganho. 

A função _rolling_ da biblioteca _Pandas_ permite calcular determinado valor, como a média, em uma janela móvel (_window_) de tamanho pré-estabelecido (_span_).

Para evitar valores nulos ao início da série, podemos utilizar a flag _offset_, que por _default_ é _True_, para que seja considerado os _n_ períodos anteriores ao primeiro dia (_begin\_date_).

* bollinger_bands (Bandas de Bollinger): utiliza o desvio padrão, normalmente multiplicado por 2, para calcular linhas superior e inferior baseado na média móvel simples. 

Utilizamos a mesma estratégia anterior para evitar valores negativos ao início da série resultante.

**assets.py** : As funções do módulo _indicators_ podem ser utilizadas com qualquer _dataset_ (que seja um _pandas.DataFrame_) indexado pelo _Timestamp_. Todavia, criamos uma classe _AssetTimeSeries_ para manipular e calcular os indicadores de forma mais intuitiva dado o registro histórico de um determinado ativo armazenado em _csv_. O arquivo, tabela,precisa ter uma coluna _Timestamp_ e um campo _Close_ indicando o preço de fechamento de determinado ativo financeiro.

A classe pode ser indexada da seguinte forma: 

` AssetTimeSeries(path="< CAMINHO DO ARQUIVO CONTENDO SERIE HISTÓRICA EM FORMATO CSV >") `

Dado uma instância de _AssetTimeSeries_, é possível calcular o valor de um indicador através da função _result\_set_. Essa funcão recebe como pâmetro _indicator_, algum indicador de _indicators.py_, _begin\_date_, data de início do _set_ desejado no formato "YYYY-mm-dd HH:MM:SS", e _end_date_, data final no mesmo formato. 

**indicators_script.py** o script gera um csv com todos os indicadores, média móvel exponencial, índice de força relativa e bandas de bollinger. Para executar o script, os arquivos _indicators.py_ e _assets.py_ necessitam estar no mesmo diretório. 

Exemplo de como o script é chamado: 

` python indicators_script.py -file bitstampUSD_1-min_data_2012-01-01_to_2020-12-31.csv -begin_date '2020-01-01 00:00:00' -end_date '2020-12-30 23:55:00' `

o arquivo resultante possui as seguintes colunas: 

* _Timestamp_

* ema (Média Móvel Exponencial)

* rsi (índice de Força Relativa)

* sma (Média Móvel Simples)

* down_band (Banda de Bollinger Inferior)

* up_band (Banda de Bollinger Superior)

## Pandas

É um dos frameworks mais populares para análise e manipulação de dados, ele foi desenvolvido para lidar de forma eficiente e prática com grandes tabelas.
