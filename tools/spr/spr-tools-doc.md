# Ferramentas de Tibia.spr (unpack/pack)

Scripts para extrair os sprites de um `Tibia.spr` em arquivos BMP e para gerar um novo `Tibia.spr`
a partir de uma pasta de BMPs. Servem para converter o `.spr` original (sprites de 32×32) para o
formato de 64×64 usado por este otclient.

| Arquivo | Função |
|---|---|
| `spr_extract.py` | unpack: `Tibia.spr` → `<id>.bmp` + `spr.json` |
| `spr_compile.py` | pack: pasta com `<id>.bmp` → `Tibia.spr` |
| `sprformat.py` | leitura/escrita do formato `.spr` e de BMP (usado pelos dois scripts) |

Requisito: Python 3, sem dependências externas.

---

## Fluxo completo (32×32 → 64×64)

Use um disco com uns 5 GB livres (não use o `/tmp`, que costuma ser tmpfs): os BMPs em 64
ocupam cerca de 3 GB.

### 1. Extrair o `.spr` original

```bash
python3 tools/spr/spr_extract.py data/things/1098/Tibia.spr ~/sprites32
```

Gera `~/sprites32/1.bmp`, `2.bmp`, … (um arquivo por id; sprites vazios não são gravados) e
`~/sprites32/spr.json`. No 10.98 são 188.096 BMPs, em cerca de 10 segundos.

### 2. Redimensionar em lote

Redimensione cada BMP de 32×32 para 64×64, salvando em `~/sprites64` com o **mesmo nome**
(`<id>.bmp`). Ver [Redimensionamento](#redimensionamento) para escolher o filtro.

### 3. Copiar o `spr.json`

```bash
cp ~/sprites32/spr.json ~/sprites64/
```

Ele guarda a assinatura, a quantidade de sprites e as flags de formato do `.spr` original, que o
compilador precisa para gerar um arquivo compatível.

### 4. Fazer backup do `.spr` atual

```bash
cp data/things/1098/Tibia.spr data/things/1098/Tibia.spr.32
```

### 5. Gerar o novo `Tibia.spr`

```bash
python3 tools/spr/spr_compile.py ~/sprites64 data/things/1098/Tibia.spr --size 64
```

O progresso é mostrado a cada 20.000 sprites. O arquivo final deve ter entre 2,6 e 3,8 GB e leva
alguns minutos para ser gerado.

### Verificação opcional: ida e volta em 32

Para conferir que os scripts não alteram nada, recompile a extração em 32. O resultado é idêntico
ao original byte a byte:

```bash
python3 tools/spr/spr_compile.py ~/sprites32 /caminho/roundtrip.spr --size 32
```

```bash
cmp data/things/1098/Tibia.spr /caminho/roundtrip.spr && echo IDENTICO
```

---

## Referência

### `spr_extract.py`

```
spr_extract.py <spr> <saida> [--size N] [--no-extended] [--alpha] [--magenta]
```

| Opção | Padrão | Descrição |
|---|---|---|
| `<spr>` | — | `Tibia.spr` de entrada |
| `<saida>` | — | pasta de saída (criada se não existir) |
| `--size N` | `32` | tamanho dos sprites gravados no `.spr` |
| `--no-extended` | desligado | quantidade de sprites em u16 (clients anteriores ao 9.60) |
| `--alpha` | desligado | os sprites têm canal alpha (`GameSpritesAlphaChannel`) |
| `--magenta` | desligado | grava BMP 24 bits com fundo `ff00ff` em vez de BMP 32 bits com alpha |

### `spr_compile.py`

```
spr_compile.py <pasta> <spr> [--size N] [--meta ARQ] [--signature S] [--count N]
               [--extended yes|no] [--alpha yes|no] [--alpha-threshold N]
```

| Opção | Padrão | Descrição |
|---|---|---|
| `<pasta>` | — | pasta com os `<id>.bmp` |
| `<spr>` | — | `Tibia.spr` de saída |
| `--size N` | `64` | tamanho dos sprites; todo BMP precisa ser exatamente N×N |
| `--meta ARQ` | `<pasta>/spr.json` | `spr.json` a usar |
| `--signature S` | do `spr.json` | sobrescreve a assinatura (aceita `0x...`) |
| `--count N` | do `spr.json` | sobrescreve a quantidade de sprites |
| `--extended yes\|no` | do `spr.json` | quantidade de sprites em u32 (`yes`) ou u16 (`no`) |
| `--alpha yes\|no` | do `spr.json` | grava os pixels em RGBA (`yes`) ou RGB (`no`) |
| `--alpha-threshold N` | `128` | sem canal alpha, pixels com alpha menor que N viram transparentes |

Comportamento:

- Ids sem BMP correspondente viram sprite vazio.
- Um BMP com erro (tamanho errado, formato não suportado, sprite grande demais) é listado no final,
  gravado como vazio, e o script termina com código de saída 1.
- BMPs aceitos: não comprimidos, de 24 bits (fundo `ff00ff` = transparente) ou 32 bits (canal
  alpha), de cima para baixo ou de baixo para cima.

### `spr.json`

```json
{
  "signature": 1471927811,
  "count": 338944,
  "extended": true,
  "alpha": false,
  "size": 32
}
```

`size` é só informativo: o tamanho do `.spr` gerado é definido por `--size` no compilador.

---

## Redimensionamento

Por padrão a extração gera BMP de **32 bits com canal alpha**: os pixels transparentes têm alpha 0.

- **Nearest neighbor** (pixel art ampliada 4×): o resultado fica idêntico ao original, só que maior.
  Funciona com qualquer opção.
- **Filtros suaves** (bilinear, bicúbico, upscalers com IA): as bordas ficam semitransparentes. Como
  o `.spr` do 10.98 não guarda alpha, o compilador decide pixel a pixel: alpha < `--alpha-threshold`
  vira transparente, o resto vira opaco. Ajuste o valor se as bordas ficarem ruins:
  `--alpha-threshold 64` mantém mais borda e `--alpha-threshold 200` corta mais.
- Se a ferramenta de redimensionamento não lida bem com alpha, extraia com `--magenta` (BMP 24 bits
  com fundo `ff00ff`). Nesse caso use **nearest neighbor**: a interpolação mistura o magenta nas
  bordas e deixa um contorno rosado.

Salve sempre em BMP de 24 ou 32 bits sem compressão.

---

## Erros comuns

| Mensagem | Causa | Solução |
|---|---|---|
| `image is 63x64, expected 64x64` | o redimensionamento não gerou exatamente 64×64 | redimensione para o tamanho exato |
| `unsupported BMP with 8 bits per pixel` | BMP com paleta | salve em 24 ou 32 bits |
| `compressed BMP files are not supported` | BMP com compressão RLE | salve sem compressão |
| `unsupported BMP channel masks` | ordem de canais incomum | salve em 24 bits ou em 32 bits BGRA padrão |
| `encoded sprite has N bytes...` | sprite maior que 65.535 bytes (só acontece com `--alpha yes`) | ver [Limites](#limites) |
| `signature/count unknown` | falta o `spr.json` na pasta | copie o `spr.json` ou use `--signature` e `--count` |
| `output is larger than 4GB` | o `.spr` passou do limite de 32 bits | ver [Limites](#limites) |

---

## Como o Tibia.spr funciona

Todos os números são little endian.

```
u32        assinatura (0x57BBD603 no 10.98)
u32        quantidade de sprites (u16 em clients anteriores ao 9.60)
u32[N]     tabela com a posição de cada sprite no arquivo; 0 = sprite vazio
...        dados dos sprites
```

Cada sprite:

```
u8[3]   ff 00 ff          color key (ignorado pelo client)
u16     tamanho dos dados a seguir
repetir até acabar os dados:
  u16   quantidade de pixels transparentes
  u16   quantidade de pixels coloridos
  RGB × coloridos         (RGBA quando o client usa GameSpritesAlphaChannel)
```

Os pixels são percorridos linha a linha, a partir do canto superior esquerdo. É uma compressão RLE
simples: uma sequência de pixels transparentes ocupa só 2 bytes, e os pixels transparentes do final
não são gravados.

O arquivo **não guarda o tamanho do sprite**: o client simplesmente assume um tamanho fixo. Por isso
quem muda para 64 é o otclient (`Otc::SPRITE_PIXELS = 64` em `src/client/const.h`), e o formato
do `.spr` continua o mesmo.

O `Tibia.dat` não muda: ele aponta para os ids dos sprites e guarda deslocamentos em unidades de 32,
e a lógica do client continua em 32 por tile.

## Diferenças entre o `.spr` original e o de 64

O formato é exatamente o mesmo; muda só a quantidade de pixels por sprite (16.384 em vez de 1.024).

- **Não há compatibilidade entre as versões:** este otclient não lê um `.spr` de 32, e o Tibia
  original e os editores de `.spr` não leem o de 64. O tamanho do `.spr` precisa ser sempre igual
  ao `SPRITE_PIXELS` do client, que só muda recompilando.
- **Tamanho de cada sprite:** é guardado em 16 bits, no máximo 65.535 bytes. Sem alpha (caso do
  10.98), um sprite de 64 ocupa no máximo cerca de 12 KB, e com alpha cerca de 16 KB: sempre cabe.
  Em 128 com alpha, um sprite totalmente opaco passaria do limite.

## Limites

- **Tamanho do arquivo:** um `.spr` de 64 do 10.98 fica com cerca de 650 MB (o original tem 164 MB;
  em 128 ficou com 2,5 GB). As posições na tabela são de 32 bits, então o máximo é 4 GB.
- **Memória RAM:** o client não carrega mais o `.spr` inteiro na RAM; cada sprite é lido do disco
  quando sua textura é criada.
- **Memória de vídeo:** as texturas ocupam 4× mais que com sprites de 32 (seriam 16× em 128).
- **Imagens customizadas:** coisas com `image:` nos `.otml` precisam de PNGs na escala de 64.
