README

 DOCUMENTO DE REQUISITOS

Sistema de Gerenciamento de Biblioteca

1.1 Objetivo

Desenvolver um sistema desktop para gerenciamento de biblioteca com controle de:

Usuários

Funcionários

Livros

Empréstimos

Multas

O sistema será implementado em Python com interface Tkinter e banco de dados MySQL.

1.2 Requisitos Funcionais
RF01 – Cadastro de Usuário

O sistema deve permitir que novos usuários se cadastrem informando:

Nome

Email

Senha

RF02 – Login

O sistema deve permitir autenticação por:

Email

Senha

Opção de entrada como funcionário

RF03 – Diferenciação de Perfil

O sistema deve diferenciar:

Usuário comum

Funcionário

Usuários comuns acessam o painel de empréstimos.
Funcionários acessam o painel administrativo.

RF04 – Visualização de Livros

Usuários devem poder:

Visualizar livros disponíveis

Ver quantidade disponível

RF05 – Empréstimo de Livro

Usuário pode:

Selecionar livro

Emprestar por 7 dias

Ter o estoque reduzido automaticamente

RF06 – Devolução de Livro

Usuário pode:

Devolver livro

Sistema calcula multa automaticamente (R$2 por dia de atraso)

RF07 – Pagamento de Multa

Usuário pode:

Pagar multa

Sistema zera valor da multa

RF08 – Limpeza de Histórico

Usuário pode apagar histórico de empréstimos devolvidos.

RF09 – Gerenciamento de Livros (Funcionário)

Funcionário pode:

Adicionar livros

Editar livros

Remover livros

Visualizar livros

RF10 – Visualização de Multas (Funcionário)

Funcionário pode visualizar:

Usuários com multa

Valor da multa

RF11 – Visualização de Livros Devolvidos

Funcionário pode visualizar histórico completo de devoluções.

1.3 Requisitos Não Funcionais

RNF01 – Sistema Desktop em Python

RNF02 – Banco MySQL

RNF03 – Interface gráfica amigável

RNF04 – Controle de integridade referencial

RNF05 – Sistema deve impedir empréstimo sem estoque