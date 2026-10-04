"""Package the fixed public DPLM checkpoint without changing its contents."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
TAG = "dplm2-bit650m-40cf303"
EXPECTED_REVISION = "40cf303d79335c4c8f1b13d08fbc3187e8ba9222"
EXPECTED_WEIGHT = "27d73fca4faf9ed5440ae8952c3711c366686d3e5ee49d188bb36cef9d94ff48"


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def main():
    source = json.loads((ROOT / "model/source.json").read_text(encoding="utf-8-sig"))
    assert source["revision"] == EXPECTED_REVISION
    assert source["sha256"] == EXPECTED_WEIGHT
    expected_url = (
        "https://huggingface.co/airkingbd/dplm2_bit_650m/resolve/"
        + EXPECTED_REVISION + "/pytorch_model.bin?download=true"
    )
    assert source["url"] == expected_url
    seven_zip = shutil.which("7z") or shutil.which("7zz")
    if not seven_zip:
        raise RuntimeError("7-Zip is required to build the distribution.")
    stage = ROOT / "stage"
    model = stage / "dplm2_bit_650m"
    dist = ROOT / "dist"
    verified = ROOT / "verified"
    if any(p.exists() for p in (stage, dist, verified)):
        raise RuntimeError("Build directories must be new.")
    model.mkdir(parents=True)
    dist.mkdir()
    for name in ("config.json", "vocab.txt", "source.json"):
        shutil.copyfile(ROOT / "model" / name, model / name)
    weight = model / "pytorch_model.bin"
    subprocess.run([
        "curl", "--fail", "--location", "--retry", "5", "--retry-all-errors",
        "--connect-timeout", "30", "--max-time", "1800",
        "--output", str(weight), expected_url,
    ], check=True)
    expected = {"pytorch_model.bin": EXPECTED_WEIGHT, **source["companion_sha256"]}
    assert weight.stat().st_size == source["size_bytes"]
    for name, checksum in expected.items():
        if digest(model / name) != checksum:
            raise RuntimeError("Source checksum mismatch: " + name)
    expected["source.json"] = digest(model / "source.json")
    shutil.copyfile(ROOT / "LICENSE", stage / "LICENSE.txt")
    archive = dist / "dplm2_bit_650m.7z"
    subprocess.run([
        seven_zip, "a", "-t7z", "-mx=1", "-mmt=2", "-v1500m",
        str(archive), "dplm2_bit_650m", "LICENSE.txt",
    ], cwd=stage, check=True)
    volumes = sorted(dist.glob("dplm2_bit_650m.7z.*"))
    if len(volumes) != 2 or any(p.stat().st_size >= 2 * 1024**3 for p in volumes):
        raise RuntimeError("Expected 2 volumes, each below GitHub's 2 GiB limit.")
    subprocess.run([seven_zip, "t", str(volumes[0])], check=True)
    subprocess.run([seven_zip, "x", str(volumes[0]), "-o" + str(verified), "-y"], check=True)
    for name, checksum in expected.items():
        if digest(verified / "dplm2_bit_650m" / name) != checksum:
            raise RuntimeError("Extracted checksum mismatch: " + name)
    assets = [{"name":p.name, "bytes":p.stat().st_size, "sha256":digest(p)} for p in volumes]
    (dist / "SHA256SUMS.txt").write_text(
        "".join(a["sha256"] + "  " + a["name"] + "\n" for a in assets), encoding="utf-8")
    report = {"model_id":source["model_id"], "revision":EXPECTED_REVISION,
              "source_file_sha256":expected, "assets":assets,
              "archive_test":"passed", "extracted_checksums":"passed"}
    (dist / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
