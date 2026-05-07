# 🃏 Klondike Python | Jogo de Paciência Clássico

<p align="center">
  [<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
</p>

---

## 📝 Sobre o Projeto

O **V-ERP** é uma solução robusta para o Planejamento de Recursos Empresariais. Este sistema foi projetado para centralizar operações, oferecendo uma interface amigável e um backend eficiente para o controle de dados em tempo real.

> **Status do Projeto:** 🛠️ Em desenvolvimento (Fase de Implementação de APIs)

---

## ✨ Funcionalidades Principais

* **🔐 Controle de Acesso:** Sistema de login com autenticação via PHP e MySQL.
* **📊 Dashboard Dinâmico:** Visualização clara das métricas do sistema.
* **📂 Organização Modular:** Código separado em diretórios específicos para facilitar a escalabilidade.
* **⚡ Respostas em Tempo Real:** Integração de JavaScript para uma experiência de usuário fluida.

---

## ⚙️ Tecnologias Utilizadas

O projeto utiliza o que há de melhor na stack web clássica:
1.  **Front-end:** Estruturação com HTML5 e estilização moderna com CSS3.
2.  **Lógica de Client-side:** JavaScript para manipulação do DOM e requisições.
3.  **Back-end:** PHP para processamento de lógica de negócio e segurança.
4.  **Banco de Dados:** MySQL para persistência de dados.

---

## 🚀 Como Configurar o Ambiente

Para rodar o V-ERP localmente, siga estes passos:

### 1. Preparação do Servidor
Certifique-se de ter o **XAMPP** ou similar instalado. Inicie os módulos **Apache** e **MySQL**.

### 2. Instalação do Código
Clone este repositório dentro da pasta `htdocs`:
```bash
git clone [https://github.com/vinicius200019/v_erp.git](https://github.com/vinicius200019/v_erp.git)
```

---

## 📈 Fluxo do Sistema

[ADMIN] cadastra produto novo no estoque

   ↓
   
[ADMIN] registra compra do fornecedor (estoque sobe)
   
   ↓
   
[CLIENTE] entra na tela de loja, escolhe o produto, compra
   
   ↓
   
[SISTEMA] registra venda automaticamente, estoque desce
   
   ↓
   
[ADMIN] vê tudo no dashboard

---

## 📂 Estrutura do Projeto

Abaixo está a organização dos arquivos e pastas do repositório:

```text
v_erp/

├── 📄 index.html

├── 📁 css/

│ └── 📄 style.css

├── 📁 js/

│ ├──📄 auth.js

│ ├──📄 dashboard.js

│ ├──📄 compras.js

│ ├──📄 login.js

│ ├──📄 produtos.js

│ ├──📄 sidebar.js

│ └──📄 usuarios.js

├── 📁 pages/

│ ├── 📄compras.html

│ ├── 📄 dashboard.html

│ ├── 📄 login.html

│ ├── 📄 produtos.html

│ ├── 📄 sidebar.html

│ └── 📄 usuarios.html

├── 📁 php/

│ ├── 📁 db/

│ │ ├── 📄compras_db.php

│ │ ├── 📄 dashboard_db.php

│ │ ├── 📄 login_db.php

│ │ ├── 📄 produtos_db.php

│ │ ├── 📄 sidebar_db.php

│ │ └── 📄 usuarios_db.php

│ └── 📁 api/

│ │ ├── 📄api_compras.php

│ │ ├── 📄api_dashboard.php

│ │ ├── 📄api_login.php

│ │ ├── 📄api_produtos.php

│ │ ├── 📄api_sidebar.php

│ │ └── 📄api_usuarios.php

│ ├──  📁 sql/
│ └── 📄 database.sql
```
---
## 🚀 Como Rodar na Sua Máquina

Siga o guia passo a passo para configurar o ambiente local de forma correta:

### 1. Pré-requisitos

Certifique-se de ter instalado um ambiente de servidor local que suporte PHP e MySQL:

XAMPP (Recomendado)

WampServer

### 2. Download do Projeto

Navegue até a pasta raiz do seu servidor local (geralmente C:/xampp/htdocs/) e execute o comando abaixo no terminal:

```bash
git clone [https://github.com/vinicius200019/v_erp.git](https://github.com/vinicius200019/v_erp.git)
```
### 3. Configuração do Banco de Dados

1 - Abra o painel de controle do seu servidor e inicie os módulos Apache e MySQL.

2 - Acesse o gerenciador de banco de dados no seu navegador: http://localhost/phpmyadmin/.

3 - Crie um novo banco de dados chamado v_erp_db.

4 - Clique na aba Importar, selecione o arquivo .sql que está dentro da pasta /sql do projeto e confirme.

### 4. Execução do Sistema

Com tudo configurado, basta acessar o endereço abaixo no seu navegador:

```bash
http://localhost/v_erp/index.html
```

## ⌨️ Desenvolvedores



<strong>Vinícius</strong>
























