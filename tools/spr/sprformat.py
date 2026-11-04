"""Shared helpers for reading/writing Tibia.spr files and the BMP files used to edit them.

Tibia.spr layout (little endian):

    u32         signature
    u16 | u32   sprite count            (u32 when GameSpritesU32 is enabled, client >= 9.60)
    u32[count]  absolute offset of each sprite, 0 means "no sprite"
    ...sprite data...

Each sprite:

    u8[3]  color key (always ff 00 ff, ignored by the client)
    u16    size of the pixel data that follows
    repeat until the pixel data ends:
        u16  number of transparent pixels
        u16  number of colored pixels
        u8[colored * channels]  RGB (or RGBA when GameSpritesAlphaChannel is enabled)

Pixels are walked row by row from the top-left corner; trailing transparent pixels are not stored.
"""

import json
import os
import re
import struct

COLOR_KEY = b"\xff\x00\xff"
MAX_RUN = 0xFFFF
MAX_DATA_SIZE = 0xFFFF
META_FILE = "spr.json"

# runs of magenta pixels vs runs of anything else, always aligned to 3 byte BGR pixels
_MAGENTA_RUNS = re.compile(rb"(?s)((?:\xff\x00\xff)+)|((?:(?!\xff\x00\xff)...)+)")
_run_patterns = {}


def _alpha_runs(threshold):
    """Regex splitting a BGRA buffer into (transparent, colored) runs, aligned to 4 byte pixels.

    A pixel is transparent when its alpha is lower than threshold (1..255).
    """
    pattern = _run_patterns.get(threshold)
    if pattern is None:
        low = re.escape(bytes([threshold - 1]))
        high = re.escape(bytes([threshold]))
        pattern = re.compile(rb"(?s)((?:...[\x00-" + low + rb"])+)|((?:...[" + high + rb"-\xff])+)")
        _run_patterns[threshold] = pattern
    return pattern


class SprFile:
    def __init__(self, path, extended=True, alpha=False):
        with open(path, "rb") as f:
            self.data = f.read()
        self.extended = extended
        self.alpha = alpha
        self.signature = struct.unpack_from("<I", self.data, 0)[0]
        if extended:
            self.count = struct.unpack_from("<I", self.data, 4)[0]
            table = 8
        else:
            self.count = struct.unpack_from("<H", self.data, 4)[0]
            table = 6
        self.offsets = struct.unpack_from("<%dI" % self.count, self.data, table)

    def read_bgra(self, sprite_id, size):
        """Decodes sprite_id (1 based) into a top-down BGRA buffer, or None when the sprite is empty."""
        offset = self.offsets[sprite_id - 1]
        if offset == 0:
            return None

        channels = 4 if self.alpha else 3
        data = self.data
        data_size = struct.unpack_from("<H", data, offset + 3)[0]
        pos = offset + 5
        end = pos + data_size
        total = size * size
        out = bytearray(total * 4)
        pixel = 0
        while pos < end and pixel < total:
            transparent, colored = struct.unpack_from("<HH", data, pos)
            pos += 4
            pixel += transparent
            colored = min(colored, total - pixel)
            if colored > 0:
                src = data[pos:pos + colored * channels]
                dst = pixel * 4
                block = bytearray(colored * 4)
                block[0::4] = src[2::channels]
                block[1::4] = src[1::channels]
                block[2::4] = src[0::channels]
                block[3::4] = src[3::channels] if self.alpha else b"\xff" * colored
                out[dst:dst + colored * 4] = block
            pos += colored * channels
            pixel += colored
        return out


def encode_sprite(bgra, alpha, threshold):
    """Encodes a top-down BGRA buffer into the sprite pixel data (without color key/size header)."""
    out = bytearray()
    transparent = 0
    for match in _alpha_runs(1 if alpha else threshold).finditer(bgra):
        if match.group(1) is not None:
            transparent += (match.end() - match.start()) // 4
            continue

        run = match.group(2)
        colored = len(run) // 4
        if transparent > MAX_RUN or colored > MAX_RUN:
            raise ValueError("pixel run too long for the spr format")

        pixels = bytearray(colored * (4 if alpha else 3))
        channels = 4 if alpha else 3
        pixels[0::channels] = run[2::4]
        pixels[1::channels] = run[1::4]
        pixels[2::channels] = run[0::4]
        if alpha:
            pixels[3::4] = run[3::4]

        out += struct.pack("<HH", transparent, colored)
        out += pixels
        transparent = 0

    if len(out) > MAX_DATA_SIZE:
        raise ValueError("encoded sprite has %d bytes, the spr format allows at most %d" % (len(out), MAX_DATA_SIZE))
    return bytes(out)


def write_bmp(path, bgra, size, magenta=False):
    """Writes a top-down BGRA buffer as a bottom-up BMP.

    By default a 32 bit BMP with alpha channel is written. With magenta=True a 24 bit BMP is written
    instead, using ff00ff for transparent pixels, like most Tibia sprite editors do.
    """
    if magenta:
        bgr = bytearray(size * size * 3)
        bgr[0::3] = bgra[0::4]
        bgr[1::3] = bgra[1::4]
        bgr[2::3] = bgra[2::4]
        for match in _alpha_runs(1).finditer(bgra):
            if match.group(1) is not None:
                start, end = match.start() // 4 * 3, match.end() // 4 * 3
                bgr[start:end] = COLOR_KEY * ((end - start) // 3)
        row = size * 3
        padding = b"\x00" * ((4 - row % 4) % 4)
        pixels = b"".join(bgr[y * row:(y + 1) * row] + padding for y in range(size - 1, -1, -1))
        header = struct.pack("<IiiHHIIiiII", 40, size, size, 1, 24, 0, len(pixels), 2835, 2835, 0, 0)
    else:
        row = size * 4
        pixels = b"".join(bgra[y * row:(y + 1) * row] for y in range(size - 1, -1, -1))
        # BITMAPV4HEADER with BI_BITFIELDS so image tools keep the alpha channel
        header = struct.pack("<IiiHHIIiiII", 108, size, size, 1, 32, 3, len(pixels), 2835, 2835, 0, 0)
        header += struct.pack("<IIII", 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
        header += b"BGRs" + b"\x00" * 36 + b"\x00" * 12

    offset = 14 + len(header)
    with open(path, "wb") as f:
        f.write(b"BM" + struct.pack("<IHHI", offset + len(pixels), 0, 0, offset))
        f.write(header)
        f.write(pixels)


def read_bmp(path):
    """Reads an uncompressed 24 or 32 bit BMP, returning (width, height, top-down BGRA buffer).

    24 bit images use ff00ff as transparent color. 32 bit images use their alpha channel when the
    header declares an alpha mask; otherwise (or when every pixel has alpha 0, as some tools write
    32 bit BMPs without alpha) ff00ff is used as well.
    """
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"BM":
        raise ValueError("not a BMP file")

    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    header_size, width, height, _, bpp, compression = struct.unpack_from("<IiiHHI", data, 14)
    if bpp not in (24, 32):
        raise ValueError("unsupported BMP with %d bits per pixel (use 24 or 32 bits)" % bpp)

    if compression == 3 or compression == 6:
        if header_size >= 56 or compression == 6:
            masks = struct.unpack_from("<IIII", data, 14 + 40)
        else:
            masks = struct.unpack_from("<III", data, 14 + 40) + (0,)
        expected = (0x00FF0000, 0x0000FF00, 0x000000FF)
        if bpp != 32 or masks[:3] != expected or masks[3] not in (0, 0xFF000000):
            raise ValueError("unsupported BMP channel masks %s" % [hex(m) for m in masks])
    elif compression != 0:
        raise ValueError("compressed BMP files are not supported")
    else:
        masks = (0, 0, 0, 0)
    has_alpha_mask = masks[3] == 0xFF000000

    top_down = height < 0
    height = abs(height)
    channels = bpp // 8
    stride = (width * channels + 3) & ~3

    rows = []
    for y in range(height):
        start = pixel_offset + y * stride
        rows.append(data[start:start + width * channels])
    if not top_down:
        rows.reverse()
    raw = b"".join(rows)

    n = width * height
    bgra = bytearray(n * 4)
    if channels == 4:
        bgra[:] = raw
        if has_alpha_mask or any(bgra[3::4]):
            return width, height, bgra
        raw = bytearray(n * 3)
        raw[0::3] = bgra[0::4]
        raw[1::3] = bgra[1::4]
        raw[2::3] = bgra[2::4]
    else:
        bgra[0::4] = raw[0::3]
        bgra[1::4] = raw[1::3]
        bgra[2::4] = raw[2::3]

    alpha = bytearray(b"\xff") * n
    for match in _MAGENTA_RUNS.finditer(raw):
        if match.group(1) is not None:
            alpha[match.start() // 3:match.end() // 3] = bytes((match.end() - match.start()) // 3)
    bgra[3::4] = alpha
    return width, height, bgra


def save_meta(directory, meta):
    with open(os.path.join(directory, META_FILE), "w") as f:
        json.dump(meta, f, indent=2)


def load_meta(directory):
    path = os.path.join(directory, META_FILE)
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)
