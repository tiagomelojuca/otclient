#!/usr/bin/env python3
"""Builds a Tibia.spr from a directory of <id>.bmp files.

Sprite ids without a BMP are stored as empty sprites. Signature, sprite count and format flags
are read from the spr.json written by spr_extract.py (copy it to the resized directory, or pass
them as arguments).

Example:
    python3 spr_compile.py sprites64/ Tibia.spr --size 64
"""

import argparse
import os
import struct
import sys
import time

import sprformat


def main():
    parser = argparse.ArgumentParser(description="Compile BMP files into a Tibia.spr")
    parser.add_argument("input", help="directory with <id>.bmp files")
    parser.add_argument("spr", help="output Tibia.spr")
    parser.add_argument("--size", type=int, default=64, help="sprite size, every BMP must match it (default: 64)")
    parser.add_argument("--meta", help="spr.json to use (default: <input>/spr.json)")
    parser.add_argument("--signature", type=lambda v: int(v, 0), help="override the spr signature")
    parser.add_argument("--count", type=int, help="override the sprite count")
    parser.add_argument("--extended", choices=["yes", "no"], help="override u32 sprite count")
    parser.add_argument("--alpha", choices=["yes", "no"], help="override alpha channel")
    parser.add_argument("--alpha-threshold", type=int, default=128,
                        help="without alpha channel, pixels with alpha lower than this are transparent (default: 128)")
    args = parser.parse_args()

    if args.meta:
        with open(args.meta) as f:
            meta = sprformat.json.load(f)
    else:
        meta = sprformat.load_meta(args.input)

    signature = args.signature if args.signature is not None else meta.get("signature")
    count = args.count if args.count is not None else meta.get("count")
    extended = (args.extended == "yes") if args.extended else meta.get("extended", True)
    alpha = (args.alpha == "yes") if args.alpha else meta.get("alpha", False)
    if signature is None or count is None:
        parser.error("signature/count unknown: copy spr.json from the extracted directory or pass --signature and --count")
    if not 1 <= args.alpha_threshold <= 255:
        parser.error("--alpha-threshold must be between 1 and 255")
    if not extended and count > 0xFFFF:
        parser.error("%d sprites do not fit in a u16 count, use --extended yes" % count)

    print("signature 0x%08X, %d sprites, %dx%d, %s, %s" % (
        signature, count, args.size, args.size, "u32 count" if extended else "u16 count", "RGBA" if alpha else "RGB"))

    started = time.time()
    header = struct.pack("<I", signature) + (struct.pack("<I", count) if extended else struct.pack("<H", count))
    table_offset = len(header)
    offsets = [0] * count
    errors = 0

    with open(args.spr, "wb") as out:
        out.write(header)
        out.write(bytes(4 * count))
        position = table_offset + 4 * count

        for sprite_id in range(1, count + 1):
            path = os.path.join(args.input, "%d.bmp" % sprite_id)
            if os.path.exists(path):
                try:
                    width, height, bgra = sprformat.read_bmp(path)
                    if (width, height) != (args.size, args.size):
                        raise ValueError("image is %dx%d, expected %dx%d" % (width, height, args.size, args.size))
                    data = sprformat.encode_sprite(bgra, alpha, args.alpha_threshold)
                except ValueError as e:
                    print("error: %s: %s" % (path, e), file=sys.stderr)
                    errors += 1
                    continue

                if position > 0xFFFFFFFF:
                    sys.exit("error: output is larger than 4GB, the spr offsets are only 32 bits")
                offsets[sprite_id - 1] = position
                out.write(sprformat.COLOR_KEY + struct.pack("<H", len(data)) + data)
                position += 5 + len(data)

            if sprite_id % 20000 == 0:
                print("  %d/%d" % (sprite_id, count), flush=True)

        out.seek(table_offset)
        out.write(struct.pack("<%dI" % count, *offsets))

    print("%s written (%.1f MB) in %.1fs" % (args.spr, position / 1048576.0, time.time() - started))
    if errors:
        print("%d sprites failed and were stored as empty" % errors, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
