# Sistema de Trading Automático

Este é um sistema de trading automático em Python que utiliza a API da Alpaca para executar ordens de compra e venda com base em análises técnicas. A aplicação é equipada com uma interface gráfica desenvolvida com Tkinter, permitindo a configuração de parâmetros de trading e monitoramento em tempo real.

## Funcionalidades

- **Integração com API de Corretora:** Executa ordens de compra e venda utilizando a API da Alpaca.
- **Análise Técnica:** Calcula indicadores técnicos como SMA (Média Móvel Simples), RSI (Índice de Força Relativa) e MACD (Convergência/Divergência de Médias Móveis) para tomada de decisões de trading.
- **Interface Gráfica:** Permite a configuração de tickers, quantidade de ações, stop loss e take profit através de uma interface gráfica interativa.
- **Loop de Trading:** Executa operações automaticamente a cada minuto enquanto o sistema está em execução.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `yfinance` para obter dados de mercado
  - `ta` para cálculos de indicadores técnicos
  - `alpaca-trade-api` para integração com a API da Alpaca
  - `tkinter` para a interface gráfica

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio

   Instale as dependências: bash Copiar código pip install yfinance ta
   alpaca-trade-api


## Configure suas credenciais da API:

- Substitua SUA_API_KEY e SEU_SECRET_KEY pelas suas credenciais da API Alpaca no código.
Uso
Execute o script:

bash
Copiar código
python seu_script.py
Configuração na Interface Gráfica:

- Ticker: Insira o(s) símbolo(s) do ativo(s) que deseja monitorar e negociar. Exemplo: AAPL, GOOGL, TSLA.
Quantidade: Defina a quantidade de ações para comprar ou vender.
- Stop Loss %: Ajuste o percentual de stop loss (preço mínimo para venda).
- Take Profit %: Ajuste o percentual de take profit (preço máximo para venda).
- Indicadores Técnicos: Selecione se deseja usar RSI e/ou MACD na análise.
Iniciar/Parar Trading:

- Clique em "Iniciar Trading" para começar a monitorar e executar ordens.
- Clique em "Parar Trading" para interromper o processo.
Estrutura do Código
- TradingApp: Classe que define a interface gráfica e controla a lógica de trading.
obter_dados(ticker): Função para obter dados históricos do ativo.
- executar_ordem(ticker, quantidade, tipo_ordem, price): Função para enviar ordens de compra e venda para a API da Alpaca.
- analisar_e_investir(ticker): Função que analisa os dados do ativo e decide se deve comprar ou vender.
trading_loop(): Função que executa o loop de trading, chamando a análise e execução de ordens.
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork do repositório e enviar pull requests com melhorias ou correções.

Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

Nota: Este código é para fins educacionais e de demonstração. Antes de usar em um ambiente real, teste e ajuste a estratégia conforme necessário e verifique as políticas da corretora utilizada.

Este `README.md` fornece uma visão geral clara do propósito, funcionamento e requisitos do sistema de trading automático, além de instruções detalhadas para instalação, uso e contribuição. Adapte o texto conforme necessário para refletir qualquer detalhe específico do seu projeto ou configuração.

##Principais modificações:
- Painel de Indicadores: Um painel foi adicionado à interface para exibir os valores de SMA, RSI, MACD e Signal.
- Função update_indicators: Atualiza os valores no painel com base nos cálculos de indicadores.
- Exibição gráfica: Agora, ao invés de exibir os valores no terminal, eles aparecem na interface gráfica.
Esse código permitirá que você visualize os indicadores de análise técnica diretamente na interface gráfica, atualizando-os à medida que os dados são processados.

