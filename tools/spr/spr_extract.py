#!/usr/bin/env python3
"""Extracts every sprite of a Tibia.spr into <output>/<id>.bmp.

Empty sprites are not written. A spr.json file is saved next to the images with the signature,
sprite count and format flags, so spr_compile.py can rebuild a compatible file.

Example:
    python3 spr_extract.py data/things/1098/Tibia.spr sprites32/
"""

import argparse
import os
import sys
import time

import sprformat


def main():
    parser = argparse.ArgumentParser(description="Extract Tibia.spr sprites to BMP files")
    parser.add_argument("spr", help="input Tibia.spr")
    parser.add_argument("output", help="output directory")
    parser.add_argument("--size", type=int, default=32, help="sprite size stored in the spr (default: 32)")
    parser.add_argument("--no-extended", dest="extended", action="store_false",
                        help="sprite count is u16 (clients older than 9.60)")
    parser.add_argument("--alpha", action="store_true",
                        help="sprites have an alpha channel (GameSpritesAlphaChannel)")
    parser.add_argument("--magenta", action="store_true",
                        help="write 24 bit BMPs using ff00ff as transparency instead of 32 bit BMPs with alpha")
    args = parser.parse_args()

    spr = sprformat.SprFile(args.spr, args.extended, args.alpha)
    os.makedirs(args.output, exist_ok=True)

    print("signature 0x%08X, %d sprites" % (spr.signature, spr.count))
    started = time.time()
    written = 0
    for sprite_id in range(1, spr.count + 1):
        bgra = spr.read_bgra(sprite_id, args.size)
        if bgra is not None:
            sprformat.write_bmp(os.path.join(args.output, "%d.bmp" % sprite_id), bgra, args.size, args.magenta)
            written += 1
        if sprite_id % 20000 == 0:
            print("  %d/%d" % (sprite_id, spr.count), flush=True)

    sprformat.save_meta(args.output, {
        "signature": spr.signature,
        "count": spr.count,
        "extended": spr.extended,
        "alpha": spr.alpha,
        "size": args.size,
    })
    print("%d sprites written to %s in %.1fs" % (written, args.output, time.time() - started))


if __name__ == "__main__":
    sys.exit(main())
