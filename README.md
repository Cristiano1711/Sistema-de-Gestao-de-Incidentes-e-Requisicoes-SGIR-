# Sistema de Gestão de Incidentes e Requisições (SGIR)
**Desenvolvimento de uma Aplicação Web para Gerenciamento de Workflow de Suporte Técnico**

---

## 1. Resumo (Abstract)
Este projeto descreve a implementação de um sistema de gerenciamento de tickets de suporte técnico utilizando o micro-framework **Flask** e o sistema de gerenciamento de banco de dados relacional (SGBDR) **MySQL**. O objetivo principal é a orquestração de fluxos de trabalho (workflows) e a manutenção da integridade referencial em estados de chamados técnicos, permitindo a colaboração entre usuários solicitantes e técnicos responsáveis através de uma interface web dinâmica e persistência de dados semi-estruturados.

## 2. Introdução
No cenário da Engenharia de Software voltada para infraestrutura de TI, a rastreabilidade de incidentes é um requisito não-funcional crítico. Este sistema propõe uma solução robusta para a captura, triagem e resolução de tickets, focando na separação de responsabilidades e na flexibilidade do armazenamento de logs de interação.

## 3. Arquitetura do Sistema

### 3.1 Camada de Persistência (Database Layer)
O modelo de dados foi projetado para garantir a atomicidade e durabilidade. Diferente de abordagens tradicionais de normalização excessiva para logs de comentários, foi implementada a utilização do tipo de dado **JSON nativo do MySQL**.

- **Vantagem:** Redução da latência de *JOINs* complexos e flexibilidade para armazenar metadados de comentários sem alterar o esquema da tabela principal.

### 3.2 Camada de Lógica (Back-end)
Baseada no padrão **MVC (Model-View-Controller)** simplificado, a aplicação utiliza:
- **Rotas RESTful:** Para operações de CRUD (Create, Read, Update, Delete).
- **Gerenciamento de Estado:** Transições controladas entre os estados `Aberto`, `Em Andamento` e `Fechado`.

### 3.3 Camada de Interface (Front-end)
Implementação de um front-end desacoplado utilizando:
- **Jinja2 Engine:** Para renderização de templates no servidor.
- **CSS Modular:** Utilização de variáveis globais e sistemas de *Grid* e *Flexbox* para garantir a responsividade e manutenção visual.

## 4. Metodologia de Implementação

### 4.1 Persistência de Dados Semi-Estruturados
O sistema armazena o histórico de interações dentro da coluna `comentarios`. A lógica em Python (biblioteca `json`) serializa e desserializa esses objetos, permitindo um crescimento dinâmico do histórico sem a necessidade de tabelas associativas pesadas para este escopo.

### 4.2 Fluxo de Atribuição de Técnicos
O sistema implementa uma lógica de "ownership" (propriedade), onde um agente técnico pode assumir a responsabilidade por um chamado. Esta transição de estado é refletida instantaneamente na interface de monitoramento (Dashboard).

## 5. Especificações Técnicas

| Requisito | Tecnologia |
| :--- | :--- |
| **Linguagem de Programação** | Python  |
| **Framework Web** | Flask (WSGI compliant) |
| **SGBD** | MySQL 8.0 |
| **Comunicação de Dados** | JSON / SQL |
| **Paradigma** | Desenvolvimento Orientado a Objetos e Funcional |

## 6. Configuração do Ambiente de Pesquisa/Desenvolvimento

### 6.1 Pré-requisitos
- Python instalado em ambiente local.
- Instância do MySQL Server ativa.

### 6.2 Instalação de Dependências
```bash
pip install flask mysql-connector-python
```

### 6.3 Inicialização da Estrutura de Dados
Execute o script `database.sql` para instanciar o esquema de banco de dados e as tabelas necessárias.

### 6.4 Variáveis de Conexão
As credenciais de acesso ao banco de dados devem ser configuradas na função `conectar_db` no arquivo `app.py`.

## 7. Conclusão
O sistema demonstra a viabilidade da integração entre tecnologias Python e MySQL para a resolução de problemas de fluxo de trabalho empresarial. A utilização de campos JSON em bancos relacionais destaca-se como uma técnica moderna para lidar com a evolução de dados sem sacrificar a robustez do SQL.

---

**Desenvolvido por:** Cristiano Cardoso Cavalcante Lima.
