#!/usr/bin/env python3
"""Generate the formula from the latest published pgram release."""

import json
from pathlib import Path
import re
import subprocess


def formula(release, checksums):
    tag = release["tag_name"]
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError(f"unsupported stable release tag: {tag}")
    assets = {asset["name"]: asset["browser_download_url"] for asset in release["assets"]}
    hashes = dict((name, digest) for digest, name in (line.split() for line in checksums.splitlines()))
    lines = [
        'class Pgram < Formula',
        '  desc "Pangram AI-detection CLI with local scan history and a result cache"',
        '  homepage "https://github.com/lucasheriques/pgram"',
        f'  version "{tag[1:]}"',
        '  license "MIT"',
    ]
    for os, scope in (("darwin", "macos"), ("linux", "linux")):
        lines += ["", f"  on_{scope} do"]
        for arch, cpu in (("arm64", "arm"), ("amd64", "intel")):
            name = f"pgram_{tag[1:]}_{os}_{arch}.tar.gz"
            digest = hashes[name]
            url = assets[name]
            if not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError(f"invalid checksum for {name}")
            expected = f"https://github.com/lucasheriques/pgram/releases/download/{tag}/{name}"
            if url != expected:
                raise ValueError(f"unexpected release URL: {url}")
            lines += [f"    on_{cpu} do", f'      url "{url}"', f'      sha256 "{digest}"', "    end"]
        lines += ["  end"]
    lines += ["", "  def install", '    bin.install "pgram"', "  end", "",
              "  test do", '    assert_match version.to_s, shell_output("#{bin}/pgram version")', "  end", "end", ""]
    return "\n".join(lines)


def main():
    release = json.loads(subprocess.check_output([
        "gh", "api", "repos/lucasheriques/pgram/releases/latest",
    ], text=True))
    checksum = next(asset for asset in release["assets"] if asset["name"] == "checksums.txt")
    checksums = subprocess.check_output([
        "gh", "api", f'repos/lucasheriques/pgram/releases/assets/{checksum["id"]}',
        "-H", "Accept: application/octet-stream",
    ], text=True)
    content = formula(release, checksums)
    Path("Formula").mkdir(exist_ok=True)
    Path("Formula/pgram.rb").write_text(content)


if __name__ == "__main__":
    main()
