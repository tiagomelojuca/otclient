"""
Reduz os sprites já gerados (128x128) para 64x64, sem rodar a IA de novo.
Usa Lanczos com transparência, igual ao modo --tamanho 64 do upscale_sprites.py,
então o resultado é o mesmo que você teria rodando a rede direto para 64.

Requisitos:  pip install numpy pillow
Uso:
    python3 reduzir_sprites.py sprites128 sprites64
    python3 reduzir_sprites.py sprites128 sprites64 --tamanho 64 --processos 4

Mantém nome e formato real de cada arquivo (PNG ou BMP 32 bits com alfa).
Pode interromper e rodar de novo: o que já existe na saída é pulado.
"""
import argparse, os, struct, sys, time
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from PIL import Image

ARGS = {}


def save_bmp_rgba(im, path):
    """BMP 32 bits com canal alfa (cabeçalho V5)."""
    w, h = im.size
    px = np.asarray(im.convert("RGBA"))[::-1][..., [2, 1, 0, 3]].tobytes()
    info = struct.pack("<IiiHHIIiiII", 124, w, h, 1, 32, 3, len(px), 2835, 2835, 0, 0)
    info += struct.pack("<IIII", 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    info += struct.pack("<I", 0x73524742) + b"\0" * 48 + struct.pack("<IIII", 4, 0, 0, 0)
    head = struct.pack("<2sIHHI", b"BM", 14 + len(info) + len(px), 0, 0, 14 + len(info))
    tmp = Path(str(path) + ".tmp")
    tmp.write_bytes(head + info + px)
    tmp.replace(path)


def work(src):
    dst = ARGS["saida"] / src.name
    try:
        im = Image.open(src)
        fmt = im.format
        out = im.convert("RGBA").resize((ARGS["tamanho"], ARGS["tamanho"]), Image.LANCZOS)
        if fmt == "BMP":
            save_bmp_rgba(out, dst)
        else:
            tmp = dst.with_name(dst.name + ".tmp")
            out.save(tmp, format=fmt or "PNG")
            tmp.replace(dst)
        return None
    except Exception as e:
        return f"{src}: {e}"


def init(saida, tamanho):
    ARGS["saida"], ARGS["tamanho"] = saida, tamanho


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--tamanho", type=int, default=64)
    ap.add_argument("--processos", type=int, default=os.cpu_count() or 1)
    a = ap.parse_args()

    a.saida.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in a.entrada.iterdir()
                   if p.is_file() and p.suffix.lower() in (".bmp", ".png") and p.name != "amostra.png"
                   and not (a.saida / p.name).exists())
    if not files:
        sys.exit("Nada a fazer (pasta vazia ou tudo já convertido).")
    print(f"{len(files)} arquivos -> {a.tamanho}x{a.tamanho}, {a.processos} processos")

    t0, erros = time.time(), []
    with Pool(a.processos, initializer=init, initargs=(a.saida, a.tamanho)) as pool:
        for i, err in enumerate(pool.imap_unordered(work, files, chunksize=64), 1):
            if err:
                erros.append(err)
            if i % 500 == 0 or i == len(files):
                print(f"\r{i}/{len(files)}  {i / (time.time() - t0):.0f} sprites/s", end="", flush=True)
    print(f"\nPronto em {(time.time() - t0) / 60:.1f} min.")
    if erros:
        (a.saida / "erros.txt").write_text("\n".join(erros))
        print(f"{len(erros)} erros (ver erros.txt)")


if __name__ == "__main__":
    main()