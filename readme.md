# Suportado apenas no Windows

### Como rodar o projeto

Recomendado uso do Pyenv-Win para controle das versões do Python [Link do repositório](https://github.com/pyenv-win/pyenv-win)

## Requisitos
Python 3.9.13

WPILib 2025 (para simulação)
## Dependências

<!-- Início das dependências Python -->
<!-- Sem CUDA Core  -->
<details>
  <summary>CPU (sem CUDA)</summary>
  Passo 1: Crie um ambiente virtual (venv) para instalar as dependências do projeto
  
  `python -m venv .venv`

  Passo 2:
  Se seu computador não tiver uma placa de vídeo com CUDA Core, rode o comando 

  `pip install -r requirements_cpu.txt`
</details>

<!-- Com CUDA Core -->
<details> 
  <summary>CUDA Core</summary>
  Passo 1: Crie um ambiente virtual (venv) para instalar as dependências do projeto
  
  `python -m venv .venv`

  Passo 2: Ative o ambiente virtual com o comando
  ```
  .\.venv\Scripts\Activate.ps1 # Para Powershell
  .\.venv\Scripts\activate.bat # Para CMD
  ```

  Passo 2:
  Se seu computador tiver uma placa de vídeo com CUDA Core, rode o comando 

  `pip install -r requirements-cuda.txt`
</details>

<!-- Fim das dependências Python -->

## Como rodar o modelo de IA
<details> 
  <summary>Criação do modelo de IA</summary>
Passo 1: Abra o arquivo "criar_modelo.py" em um editor de texto  

Passo 2: Altere o valor da variável "AI_MODEL" para o modelo do Yolo desejado

Passo 3: Altere o valor da variável "AI_MODEL_WITHOUT_ARCHIVE_EXTENSION" para o modelo desejado sem o ".pt" no final

Passo 4: Execute o arquivo "criar_modelo.py"
</details>  

<details>
  <summary>Executando o modelo de IA</summary>
Passo 1: Abra o arquivo "vision.py" em algum editor de texto

Passo 2: Selecione o framework de IA que você deseja rodar, alterando o valor da váriavel "AI_FRAMEWORK". 
```
AI_FRAMEWORK = "tf" # Para TensorFlow Lite
AI_FRAMEWORK = "torch" # Para Torch
```  
Passo 3:
Selecione o modelo desejado do TensorFlow ou do Torch, alterando o valor da variável "AI_MODEL".
```
# Substitua o "n" no "yolov8" para alterar o modelo do yolo

AI_MODEL = "yolov8n_quantização_escolhida.tflite" # Para TensorFlow Lite 
AI_MODEL = "yolov8n.pt" # Para Torch
```

Passo 4: Execute o arquivo "vision.py"
</details>

<!-- Inicio conexão ao robô  -->
## Simualção do código do Robô
Passo 1: Crie um projeto de código em qualquer linguagem de programação (Java, C++, Python)

Passo 2: Aperta Ctrl + Shift + P no 2025 WPILib VS Code, e escreva "Simulate Robot Code", espere buildar o código, selecione as opções desejadas, e clique em OK

Passo 3: No arquivo "vision.py", altere o valor da váriavel RoboRIOIP para "localhost" (linha 19)

## Robô em situação real
Passo 1: Crie um projeto de código em qualquer linguagem de Programação (Java, C++, Python)

Passo 2: Aperta Ctrl + Shift + P no 2025 WPILib VS Code, e escreva "Deploy Robot Code" ou aperte Shift + F5, espere buildar o código e ser carregado a RoboRIO.

Passo 3: 
No arquivo "vision.py", altere o valor da váriavel RoboRIOIP para "10.TE.AM.1" ou "roborio-9485-frc.local" (linha 19)

- Equipe 1234 -> 10.12.34.1
- Equipe 123 -> 10.1.23.1
- Equipe 12 -> 10.0.12.1

<!-- Fim conexão ao robô  -->
