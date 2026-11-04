"""
Upscale em lote de sprites com IA (Real-ESRGAN anime 6B), 32x32 -> 128x128.
Roda SÓ NO PROCESSADOR (sem placa de vídeo, sem PyTorch). Precisa apenas de:
    pip install numpy pillow

Uso:
    python3 upscale_sprites.py ENTRADA SAIDA [--colorkey ff00ff] [--amostra 12]

Exemplo:
    cd /home/tiago/Projetos/tibia64/otclient/data/things/1098
    python3 upscale_sprites.py sprites32 sprites128 --colorkey ff00ff --amostra 12

O modelo (~17 MB) é baixado automaticamente na primeira execução.
--amostra N processa só N sprites espalhados e gera "amostra.png" (original x IA).
"""
import argparse, collections, pickle, sys, urllib.request, zipfile
from pathlib import Path
import numpy as np
from PIL import Image

MODEL_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
MODEL = Path(__file__).with_name("RealESRGAN_x4plus_anime_6B.pth")


# ---------- carrega .pth sem torch ----------
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
    return d.get("params_ema", d.get("params", d))


# ---------- RRDBNet em numpy ----------
def conv(x, w, b):
    C, H, W = x.shape
    p = np.pad(x, ((0, 0), (1, 1), (1, 1)))
    cols = np.empty((C, 9, H, W), np.float32)
    k = 0
    for i in range(3):
        for j in range(3):
            cols[:, k] = p[:, i:i + H, j:j + W]; k += 1
    out = w.reshape(w.shape[0], -1) @ cols.reshape(C * 9, H * W)
    return (out + b[:, None]).reshape(-1, H, W)


lrelu = lambda x: np.where(x > 0, x, 0.2 * x)
up2 = lambda x: x.repeat(2, 1).repeat(2, 2)


class RRDBNet:
    def __init__(self, sd):
        self.p = {k: v.astype(np.float32) for k, v in sd.items()}
        self.nb = len({k.split(".")[1] for k in sd if k.startswith("body.") and "rdb" in k})

    def c(self, n, x):
        return conv(x, self.p[n + ".weight"], self.p[n + ".bias"])

    def rdb(self, pre, x):
        xs = [x]
        for i in range(1, 5):
            xs.append(lrelu(self.c(f"{pre}.conv{i}", np.concatenate(xs))))
        return self.c(f"{pre}.conv5", np.concatenate(xs)) * 0.2 + x

    def __call__(self, img):
        f = self.c("conv_first", img.transpose(2, 0, 1).astype(np.float32))
        b = f
        for i in range(self.nb):
            o = b
            for r in (1, 2, 3):
                o = self.rdb(f"body.{i}.rdb{r}", o)
            b = o * 0.2 + b
        f = f + self.c("conv_body", b)
        f = lrelu(self.c("conv_up1", up2(f)))
        f = lrelu(self.c("conv_up2", up2(f)))
        out = self.c("conv_last", lrelu(self.c("conv_hr", f)))
        return np.clip(out.transpose(1, 2, 0), 0, 1)


# ---------- transparência por cor-chave ----------
def fill_background(a, keymask, passes=4):
    """Espalha as cores do sprite para dentro do fundo (evita halo da cor-chave)."""
    a = a.copy(); known = ~keymask
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


def run_net(net, a, pad=4):
    a = np.pad(a / 255, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
    return net(a)[pad * 4:-pad * 4, pad * 4:-pad * 4] * 255


def process(net, im, key):
    """Retorna RGBA 4x. A cor e o canal alfa passam pela IA separadamente."""
    rgba = np.asarray(im.convert("RGBA"), np.float32)
    rgb, alpha = rgba[..., :3], rgba[..., 3].copy()
    if key is not None:
        alpha[np.all(rgb == key, axis=2)] = 0
    rgb = fill_background(rgb, alpha == 0)  # sem halo preto/rosa nas bordas
    o_rgb = run_net(net, rgb)
    if alpha.min() == 255:
        o_a = np.full(o_rgb.shape[:2], 255.0)
    else:
        o_a = run_net(net, np.repeat(alpha[..., None], 3, 2)).mean(2)
        o_a[o_a < 12] = 0
        o_a[o_a > 243] = 255
    out = np.dstack([o_rgb, o_a])
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8), "RGBA")


def save_bmp_rgba(im, path):
    """BMP 32 bits com canal alfa (cabeçalho V5), como GIMP/Photoshop gravam."""
    import struct
    w, h = im.size
    px = np.asarray(im.convert("RGBA"))[::-1][..., [2, 1, 0, 3]].tobytes()  # BGRA, de baixo p/ cima
    info = struct.pack("<IiiHHIIiiII", 124, w, h, 1, 32, 3, len(px), 2835, 2835, 0, 0)
    info += struct.pack("<IIII", 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    info += struct.pack("<I", 0x73524742) + b"\0" * 36 + b"\0" * 12  # sRGB, endpoints, gamma
    info += struct.pack("<IIII", 4, 0, 0, 0)  # intent, profile data/size, reserved
    head = struct.pack("<2sIHHI", b"BM", 14 + len(info) + len(px), 0, 0, 14 + len(info))
    Path(path).write_bytes(head + info + px)


def save_like(out, dst, fmt):
    """Grava no mesmo formato real do arquivo original (mesmo nome)."""
    if fmt == "BMP":
        save_bmp_rgba(out, dst)
    else:
        out.save(dst, format=fmt or "PNG")


def checker(size, s=8):
    y, x = np.mgrid[:size[1], :size[0]]
    c = np.where(((x // s) + (y // s)) % 2, 200, 150).astype(np.uint8)
    return Image.fromarray(np.dstack([c, c, c]), "RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada", type=Path)
    ap.add_argument("saida", type=Path)
    ap.add_argument("--colorkey", help="cor de transparência em hex, ex: ff00ff")
    ap.add_argument("--amostra", type=int, default=0)
    a = ap.parse_args()

    files = sorted(p for p in a.entrada.iterdir()
                   if p.suffix.lower() in (".bmp", ".png") and p.is_file())
    if not files:
        sys.exit(f"Nenhum .bmp/.png em {a.entrada}")
    if a.amostra:
        step = max(1, len(files) // a.amostra)
        files = files[::step][:a.amostra]

    if not MODEL.exists():
        print("Baixando modelo...")
        urllib.request.urlretrieve(MODEL_URL, MODEL)
    net = RRDBNet(load_pth(MODEL))
    key = np.array(list(bytes.fromhex(a.colorkey.lstrip("#"))), np.float32) if a.colorkey else None

    a.saida.mkdir(parents=True, exist_ok=True)
    pares = []
    for i, f in enumerate(files, 1):
        dst = a.saida / f.name
        if dst.exists() and not a.amostra:
            continue  # permite retomar o lote
        im = Image.open(f)
        fmt = im.format
        if i == 1:
            print(f"Formato real: {fmt}, modo: {im.mode}")
        out = process(net, im, key)
        save_like(out, dst, fmt)
        pares.append((im.convert("RGBA"), out))
        print(f"[{i}/{len(files)}] {f.name}")

    if a.amostra and pares:
        W = 128 * 2 + 12
        sheet = Image.new("RGB", (W * min(4, len(pares)), 140 * ((len(pares) + 3) // 4)), (40, 40, 40))
        for k, (o, u) in enumerate(pares):
            x, y = (k % 4) * W, (k // 4) * 140
            for img, dx in ((o.resize((128, 128), Image.NEAREST), 0), (u, 132)):
                bg = checker((128, 128))
                bg.paste(img, (0, 0), img)
                sheet.paste(bg, (x + dx, y))
        sheet.save(a.saida / "amostra.png")
        print("Comparação salva em", a.saida / "amostra.png")


if __name__ == "__main__":
    main()