"""
Upscale em lote de sprites com IA (Real-ESRGAN), 32x32 -> 128x128, só no processador.
Requisitos:  pip install numpy pillow

Uso:
    python3 upscale_sprites.py ENTRADA SAIDA [opções]

Exemplos:
    python3 upscale_sprites.py sprites32 sprites128 --amostra 12            # amostra comparativa
    python3 upscale_sprites.py sprites32 sprites128                         # lote completo (qualidade)
    python3 upscale_sprites.py sprites32 sprites128 --modelo rapido         # ~8x mais rápido

Opções:
    --modelo qualidade|rapido   qualidade = RealESRGAN_x4plus_anime_6B (padrão)
                                rapido    = realesr-animevideov3 (bem mais leve)
    --processos N               processos em paralelo (padrão: nº de núcleos)
    --lote N                    sprites por passada da rede (padrão 4)
    --colorkey RRGGBB           cor tratada como transparente (opcional)
    --amostra N                 processa só N sprites e gera amostra.png

Acelerações:
  * paralelismo: um processo por núcleo, cada um com BLAS em 1 thread;
  * lotes: vários sprites por passada (matrizes maiores = CPU mais eficiente);
  * sprites totalmente transparentes não passam pela IA;
  * sprites idênticos (comum em sprite sheets) são processados uma vez só e copiados;
  * pode interromper e rodar de novo: o que já existe na saída é pulado.
Cada arquivo é salvo no mesmo formato real do original (PNG ou BMP 32 bits com alfa).
"""
import os
# 1 thread de BLAS por processo: o paralelismo vem dos processos (tem que vir antes do numpy)
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse, collections, hashlib, io, pickle, shutil, struct, sys, time, urllib.request, zipfile
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
MODELS = {
    "qualidade": ("RealESRGAN_x4plus_anime_6B.pth",
                  "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"),
    "rapido": ("realesr-animevideov3.pth",
               "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth"),
}


# ---------------- carrega .pth sem torch ----------------
def load_pth(path):
    zf = zipfile.ZipFile(path)
    prefix = zf.namelist()[0].split("/")[0]
    dtypes = {"FloatStorage": np.float32, "HalfStorage": np.float16}

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == "_rebuild_tensor_v2":
                def rb(storage, offset, size, stride, *a):
                    st = [s * storage.itemsize for s in stride]
                    return np.lib.stride_tricks.as_strided(storage[offset:], size, st).copy()
                return rb
            if mod.startswith("torch") and name.endswith("Storage"):
                return name
            if name == "OrderedDict":
                return collections.OrderedDict
            return super().find_class(mod, name)

        def persistent_load(self, pid):
            _, stype, key, _, _ = pid
            return np.frombuffer(zf.read(f"{prefix}/data/{key}"), dtype=dtypes[stype])

    d = U(zf.open(f"{prefix}/data.pkl")).load()
    sd = d.get("params_ema", d.get("params", d))
    return {k: v.astype(np.float32) for k, v in sd.items()}


# ---------------- camadas (layout C,N,H,W) ----------------
def conv(x, w, b):
    C, N, H, W = x.shape
    p = np.pad(x, ((0, 0), (0, 0), (1, 1), (1, 1)))
    cols = np.empty((C, 9, N, H, W), np.float32)
    k = 0
    for i in range(3):
        for j in range(3):
            cols[:, k] = p[:, :, i:i + H, j:j + W]; k += 1
    out = w.reshape(w.shape[0], -1) @ cols.reshape(C * 9, N * H * W)
    out += b[:, None]
    return out.reshape(-1, N, H, W)


def lrelu(x):
    return np.maximum(x, 0.2 * x)


def up2(x):
    return x.repeat(2, 2).repeat(2, 3)


class RRDBNet:  # RealESRGAN_x4plus_anime_6B
    def __init__(self, p):
        self.p = p
        self.nb = len({k.split(".")[1] for k in p if k.startswith("body.") and "rdb" in k})

    def c(self, n, x):
        return conv(x, self.p[n + ".weight"], self.p[n + ".bias"])

    def rdb(self, pre, x):
        xs = [x]
        for i in range(1, 5):
            xs.append(lrelu(self.c(f"{pre}.conv{i}", np.concatenate(xs))))
        return self.c(f"{pre}.conv5", np.concatenate(xs)) * 0.2 + x

    def __call__(self, x):
        f = self.c("conv_first", x)
        b = f
        for i in range(self.nb):
            o = b
            for r in (1, 2, 3):
                o = self.rdb(f"body.{i}.rdb{r}", o)
            b = o * 0.2 + b
        f = f + self.c("conv_body", b)
        f = lrelu(self.c("conv_up1", up2(f)))
        f = lrelu(self.c("conv_up2", up2(f)))
        return self.c("conv_last", lrelu(self.c("conv_hr", f)))


class SRVGGCompact:  # realesr-animevideov3
    def __init__(self, p):
        self.p = p
        self.idx = sorted(int(k.split(".")[1]) for k in p if k.endswith(".bias"))

    def __call__(self, x):
        h = x
        for n, i in enumerate(self.idx):
            h = conv(h, self.p[f"body.{i}.weight"], self.p[f"body.{i}.bias"])
            if n < len(self.idx) - 1:
                a = self.p[f"body.{i + 1}.weight"][:, None, None, None]
                h = np.where(h > 0, h, a * h)
        C, N, H, W = h.shape  # pixel shuffle x4
        h = h.reshape(3, 4, 4, N, H, W).transpose(0, 3, 4, 1, 5, 2).reshape(3, N, H * 4, W * 4)
        return h + x.repeat(4, 2).repeat(4, 3)


# ---------------- pré/pós-processamento ----------------
def fill_background(a, empty, passes=4):
    """Espalha as cores do sprite para dentro do fundo transparente (evita halo)."""
    a = a.copy(); known = ~empty
    for _ in range(passes):
        acc = np.zeros_like(a); n = np.zeros(a.shape[:2])
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            acc += np.roll(a * known[..., None], (dy, dx), (0, 1))
            n += np.roll(known, (dy, dx), (0, 1))
        new = (~known) & (n > 0)
        a[new] = acc[new] / n[new][:, None]
        known |= new
    a[~known] = 0
    return a


def save_bmp_rgba(im, path):
    """BMP 32 bits com canal alfa (cabeçalho V5)."""
    w, h = im.size
    px = np.asarray(im.convert("RGBA"))[::-1][..., [2, 1, 0, 3]].tobytes()
    info = struct.pack("<IiiHHIIiiII", 124, w, h, 1, 32, 3, len(px), 2835, 2835, 0, 0)
    info += struct.pack("<IIII", 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    info += struct.pack("<I", 0x73524742) + b"\0" * 48 + struct.pack("<IIII", 4, 0, 0, 0)
    head = struct.pack("<2sIHHI", b"BM", 14 + len(info) + len(px), 0, 0, 14 + len(info))
    Path(path).write_bytes(head + info + px)


def save_like(out, dst, fmt):
    if fmt == "BMP":
        save_bmp_rgba(out, dst)
    else:
        out.save(dst, format=fmt or "PNG")


PAD = 4
G = {}


def init_worker(modelo, key):
    p = load_pth(HERE / MODELS[modelo][0])
    G["net"] = RRDBNet(p) if modelo == "qualidade" else SRVGGCompact(p)
    # o canal alfa é uma máscara simples: o modelo leve basta e custa ~1/8
    G["anet"] = SRVGGCompact(load_pth(HERE / MODELS["rapido"][0]))
    G["key"] = key


def run_net(imgs, net="net"):
    """imgs: lista de arrays H,W,3 (0..255) do mesmo tamanho -> lista de H*4,W*4,3."""
    x = np.stack([np.pad(a / 255, ((PAD, PAD), (PAD, PAD), (0, 0)), mode="edge") for a in imgs])
    x = x.transpose(3, 0, 1, 2).astype(np.float32)          # C,N,H,W
    y = G[net](x).transpose(1, 2, 3, 0)                    # N,H,W,C
    s = PAD * 4
    return [np.clip(o[s:-s, s:-s], 0, 1) * 255 for o in y]


def work(batch):
    """batch: lista de (src, dst). Retorna lista de (src, dst, ok, msg)."""
    key = G["key"]
    res, jobs = [], []
    for src, dst in batch:
        try:
            im = Image.open(src); fmt = im.format
            rgba = np.asarray(im.convert("RGBA"), np.float32)
            rgb, alpha = rgba[..., :3], rgba[..., 3].copy()
            if key is not None:
                alpha[np.all(rgb == key, axis=2)] = 0
            h, w = alpha.shape
            if alpha.max() == 0:  # vazio: não precisa de IA
                save_like(Image.new("RGBA", (w * 4, h * 4), (0, 0, 0, 0)), dst, fmt)
                res.append((src, dst, True, "vazio")); continue
            jobs.append((src, dst, fmt, fill_background(rgb, alpha == 0), alpha))
        except Exception as e:
            res.append((src, dst, False, str(e)))

    # agrupa por tamanho para poder empilhar num lote só
    by_size = collections.defaultdict(list)
    for j in jobs:
        by_size[j[4].shape].append(j)
    for group in by_size.values():
        outs = run_net([j[3] for j in group])
        need_a = [j for j in group if j[4].min() < 255]
        a_res = run_net([np.repeat(j[4][..., None], 3, 2) for j in need_a], "anet") if need_a else []
        a_out = {id(j): r.mean(2) for j, r in zip(need_a, a_res)}
        for i, (src, dst, fmt, _, alpha) in enumerate(group):
            o_rgb = outs[i]
            if id(group[i]) in a_out:
                o_a = a_out[id(group[i])]
                o_a[o_a < 12] = 0; o_a[o_a > 243] = 255
            else:
                o_a = np.full(o_rgb.shape[:2], 255.0)
            out = Image.fromarray(np.clip(np.dstack([o_rgb, o_a]) + 0.5, 0, 255).astype(np.uint8), "RGBA")
            try:
                save_like(out, dst, fmt); res.append((src, dst, True, ""))
            except Exception as e:
                res.append((src, dst, False, str(e)))
    return res


def checker(size, s=8):
    y, x = np.mgrid[:size[1], :size[0]]
    c = np.where(((x // s) + (y // s)) % 2, 200, 150).astype(np.uint8)
    return Image.fromarray(np.dstack([c, c, c]), "RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--modelo", choices=list(MODELS), default="qualidade")
    ap.add_argument("--processos", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--lote", type=int, default=4)
    ap.add_argument("--colorkey")
    ap.add_argument("--amostra", type=int, default=0)
    a = ap.parse_args()

    for m in {a.modelo, "rapido"}:
        fname, url = MODELS[m]
        if not (HERE / fname).exists():
            print("Baixando modelo", fname, "...")
            urllib.request.urlretrieve(url, HERE / fname)
    key = np.array(list(bytes.fromhex(a.colorkey.lstrip("#"))), np.float32) if a.colorkey else None

    files = sorted(p for p in a.entrada.iterdir() if p.suffix.lower() in (".bmp", ".png") and p.is_file())
    if not files:
        sys.exit(f"Nenhum .bmp/.png em {a.entrada}")
    if a.amostra:
        step = max(1, len(files) // a.amostra)
        files = files[::step][:a.amostra]
    a.saida.mkdir(parents=True, exist_ok=True)

    # pula o que já existe e agrupa arquivos idênticos
    print(f"{len(files)} arquivos. Verificando duplicados...")
    groups = collections.OrderedDict()
    for f in files:
        if not a.amostra and (a.saida / f.name).exists():
            continue
        groups.setdefault(hashlib.md5(f.read_bytes()).digest(), []).append(f)
    todo = [(str(g[0]), str(a.saida / g[0].name)) for g in groups.values()]
    copies = {str(g[0]): g[1:] for g in groups.values() if len(g) > 1}
    n_pend = sum(len(g) for g in groups.values())
    print(f"Pendentes: {n_pend}  |  únicos p/ IA: {len(todo)}  |  processos: {a.processos}  |  modelo: {a.modelo}")

    batches = [todo[i:i + a.lote] for i in range(0, len(todo), a.lote)]
    t0, done, erros = time.time(), 0, []
    with Pool(a.processos, initializer=init_worker, initargs=(a.modelo, key)) as pool:
        for res in pool.imap_unordered(work, batches):
            for src, dst, ok, msg in res:
                if not ok:
                    erros.append(f"{src}: {msg}"); continue
                for dup in copies.get(src, []):
                    shutil.copyfile(dst, a.saida / dup.name)
                done += 1
            el = time.time() - t0
            eta = el / done * (len(todo) - done) if done else 0
            print(f"\r{done}/{len(todo)}  {done / el:.1f} sprites/s  restante ~{eta / 3600:.1f} h   ",
                  end="", flush=True)
    print(f"\nPronto em {(time.time() - t0) / 60:.1f} min.")
    if erros:
        (a.saida / "erros.txt").write_text("\n".join(erros))
        print(f"{len(erros)} erros (ver erros.txt)")

    if a.amostra:
        W = 128 * 2 + 12
        sheet = Image.new("RGB", (W * min(4, len(files)), 140 * ((len(files) + 3) // 4)), (40, 40, 40))
        for k, f in enumerate(files):
            o, u = Image.open(f).convert("RGBA"), Image.open(a.saida / f.name).convert("RGBA")
            x, y = (k % 4) * W, (k // 4) * 140
            for img, dx in ((o.resize((128, 128), Image.NEAREST), 0), (u.resize((128, 128)), 132)):
                bg = checker((128, 128)); bg.paste(img, (0, 0), img); sheet.paste(bg, (x + dx, y))
        sheet.save(a.saida / "amostra.png")
        print("Comparação salva em", a.saida / "amostra.png")


if __name__ == "__main__":
    main()
    