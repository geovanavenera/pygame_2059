# 2059 — Survive the Chrome City

Jogo 2D shooter desenvolvido em Python com pygame.
Atividade prática — Linguagem de Programação Aplicada — UNINTER 2026.

## Como jogar

| Tecla | Ação |
|-------|------|
| ← → ou A D | Mover o personagem |
| SPACE / W / ↑ | Pular |
| CTRL (esq. ou dir.) | Atirar |
| ESC | Voltar ao menu / Sair |
| ENTER | Confirmar / Iniciar |

## Objetivo
- Elimine **15 inimigos** para vencer.
- Não deixe sua **vida chegar a zero** (você tem 5 pontos de vida).
- Os inimigos ficam mais rápidos a cada 5 eliminações (waves).

## Como rodar (código-fonte)

```bash
pip install pygame
python main.py
```

## Como gerar o executável (.exe)

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole main.py
```

O `.exe` será gerado na pasta `dist/`. Copie todos os arquivos `.py` para junto do executável (ou use `--add-data` para empacotar assets).

## Estrutura do projeto

```
2059/
├── main.py       # Loop principal e tela de fim de jogo
├── menu.py       # Tela de menu
├── player.py     # Jogador
├── enemy.py      # Inimigos androides
├── bullet.py     # Projéteis
├── hud.py        # Interface (vida, kills, wave)
└── settings.py   # Configurações e constantes globais
```

## Tecnologias
- Python 3.x
- pygame 2.x

  <div align="right">
  <img src="https://raw.githubusercontent.com/geovanavenera/assets/main/2059_pygame.png" width="250"/>
</div>
  <div align="right">
  <img src="https://raw.githubusercontent.com/geovanavenera/assets/main/2059_.png" width="250"/>
</div>
  <div align="right">
  <img src="https://raw.githubusercontent.com/geovanavenera/assets/main/2059_GAMEOVER.png" width="250"/>
</div>

