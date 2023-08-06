# IC-ToolKit-EDD

<img src="https://user-images.githubusercontent.com/71731452/177205395-ffe34180-5a7d-41f5-aba2-31ccc5b31031.gif" alt="exemplo imagem">

> Esse projeto tem como objetivo facilitar a resolução de problemas da equipe de transformação.

### Ajustes e melhorias

É possivel implementar qualquer tipo de script nesse projeto

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:
<!---Estes são apenas requisitos de exemplo. Adicionar, duplicar ou remover conforme necessário--->
* Você instalou uma versão do Python superior a 3.7
* Você tem uma máquina `<Windows / Linux>`.

## 🚀 Instalando IC-ToolKit-EDD

Para instalar o IC-ToolKit-EDD, siga estas etapas:

Linux:
```
pip3 install ic-toolkit-edd
```

Windows:
```
pip install ic-toolkit-edd
```

Windows / Linux:

Use o comando abaixo para informar as credencias do seu banco MySQL.
```
ic config
```
> Obs: Isso vai gerar um arquivo .credentials em uma pasta .intuitivecare

<img src="https://user-images.githubusercontent.com/71731452/177249673-6373a5e5-8d13-4c70-8d2b-fefab60002db.svg" width=500>

## ☕ Comandos IC-ToolKit-EDD

Use o comando abaixo para gerar um query com as hashs do diretorio atual

```
ic gethash
```
> Obs: Um editor de texto ira abrir apos a execução do comando com a query gerada

<img src="https://user-images.githubusercontent.com/71731452/177250804-c6833e17-9ec4-45a1-a166-6e07397f08d7.png" width=600>

---
Use o comando abaixo para baixar um ou mais arquivos da Amazon S3

```
ic downorig <>
```
> Obs: Tambem é possivel baixar parseados e padronizados utilizando os comandos downpars ou downpadr

<img src="https://user-images.githubusercontent.com/71731452/177250567-1464f5fa-292b-4b60-963c-f0892867780d.svg" width=600>

## 🤝 Contribuindo

### Adicionando novas funções

Para adicionar novas funcionalidades basta seguir o exemplo do codigo abaixo
  
<img src="https://user-images.githubusercontent.com/71731452/177251543-1293882c-c50c-4492-b683-00d4005f6e10.svg" width=600>
  
> @app.command() possibilita a função ser chamada via CLI
  
