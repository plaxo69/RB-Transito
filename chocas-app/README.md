# CHOCAS — Posto de Trânsito de Estremoz

Aplicação web responsiva construída a partir do livro `CHOCAS POSTO TRÂNSITO DE ESTREMOZ 20265.xlsm`.

## Funcionalidades incluídas nesta primeira versão

- Pesquisa das 245 entradas de infrações importadas da folha **Descrições**, incluindo código, coima, responsabilidade e textos-base.
- Consulta das seis tabelas de velocidades e cálculo da velocidade deduzida para valores que constem das tabelas.
- Consulta indicativa dos escalões de excesso de velocidade com base nos intervalos existentes nas folhas de ligeiros/motociclos e pesados.
- Preparação de texto-base para os modelos de radar importados, com campos variáveis.
- Registo dos elementos de teste simples e contraprova de álcool, sem calcular uma TAS deduzida quando a fonte de dedução externa não está disponível.
- Consulta das 17 folhas extraídas do Excel.
- Histórico local, exportação CSV e impressão.
- Interface adaptável a telemóvel, computador e instalação como PWA.

## Executar localmente

A aplicação é estática. Basta servir esta pasta por HTTP (não abrir `index.html` diretamente, porque os navegadores bloqueiam o carregamento de `data/workbook.json` em `file://`). Por exemplo, com Python instalado:

```bash
python -m http.server 8080
```

Depois abrir `http://localhost:8080`.

## Publicar no Cloudflare Pages

1. Criar um repositório GitHub novo e carregar todos os ficheiros desta pasta, mantendo `data/workbook.json`.
2. No Cloudflare Pages, criar uma aplicação ligada a esse repositório.
3. Como é uma aplicação estática, deixar o comando de build vazio e definir a pasta de saída como `/` (raiz do projeto).
4. Publicar. Não são necessárias variáveis de ambiente nem uma base de dados para esta versão.

## Limitações importantes

- O navegador não executa macros VBA. Os botões, formulários e automatismos das macros do Excel têm de ser recriados individualmente na aplicação.
- Fórmulas que dependem de ficheiros externos (por exemplo, a tabela externa de deduções do álcool) não são recalculadas aqui. A aplicação apresenta os dados que foi possível extrair e evita inventar resultados.
- O histórico desta versão fica no armazenamento local do navegador/dispositivo. Não sincroniza automaticamente entre telemóvel e computador.
- Os textos e cálculos são ferramentas de apoio. Antes de qualquer utilização operacional, confirmar enquadramento legal, tabelas metrológicas, dados do equipamento e redação final.

## Privacidade

Os dados introduzidos e o histórico ficam no dispositivo/navegador. Esta versão não envia autos, identificações ou resultados de testes para um servidor.
