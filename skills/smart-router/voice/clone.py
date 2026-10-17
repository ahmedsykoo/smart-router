"""Arabic TTS in a cloned voice with Chatterbox Multilingual.

Usage:
  py -3.11 -m pip install "chatterbox-tts @ git+https://github.com/resemble-ai/chatterbox@5de7a54aa4e5e2baadb0182dde554908b48b85c2"        (once)
  py -3.11 clone.py --ref my_ref.wav --text lines.txt --out out

lines.txt: UTF-8, one sentence per line. Output: out/01.wav, out/02.wav, ... + out/all.wav
"""
import argparse
from pathlib import Path

import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ref", required=True, help="10-20s clean recording of the voice to clone")
    p.add_argument("--text", required=True, help="UTF-8 text file, one sentence per line")
    p.add_argument("--out", default="out")
    p.add_argument("--lang", default="ar")
    p.add_argument("--exaggeration", type=float, default=0.5, help="0.7+ = more expressive")
    p.add_argument("--cfg", type=float, default=0.5, help="~0.3 = slower, more deliberate pacing")
    p.add_argument("--pause", type=float, default=0.35, help="silence between lines in all.wav (s)")
    a = p.parse_args()

    ref, txt = Path(a.ref), Path(a.text)
    if not ref.is_file():
        raise SystemExit(f"Reference audio not found: {ref}")
    lines = [l.strip() for l in txt.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        raise SystemExit(f"No text lines in {txt}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device} | lines: {len(lines)}")
    model = ChatterboxMultilingualTTS.from_pretrained(device=device, t3_model="v3")
    model.prepare_conditionals(str(ref), exaggeration=a.exaggeration)  # encode the voice once, not per line

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    gap = torch.zeros(1, int(model.sr * a.pause))
    parts = []
    for i, line in enumerate(lines, 1):
        wav = model.generate(line, language_id=a.lang,
                             exaggeration=a.exaggeration, cfg_weight=a.cfg).cpu()
        ta.save(str(out / f"{i:02d}.wav"), wav, model.sr)
        parts += [wav, gap]
        print(f"[{i}/{len(lines)}] {line[:50]}")

    ta.save(str(out / "all.wav"), torch.cat(parts[:-1], dim=1), model.sr)
    print(f"Done: {out / 'all.wav'}")


if __name__ == "__main__":
    main()
