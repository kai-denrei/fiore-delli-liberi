"""
Fetch all folio images from Getty MS Ludwig XV 13 via IIIF manifest.
Downloads highest resolution JPEGs to data/raw/images/.
"""

import json
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request

MANIFEST_URL = "https://media.getty.edu/iiif/manifest/928f4025-a697-4b9f-b5ee-9a5d7e15a6ff"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "images"
DELAY = 1.5  # seconds between downloads


def fetch_manifest():
    req = Request(MANIFEST_URL, headers={"User-Agent": "FioreTranscription/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def parse_canvases(manifest):
    """Extract (label, image_url) pairs from IIIF v2 manifest."""
    entries = []
    for canvas in manifest.get("sequences", [{}])[0].get("canvases", []):
        label = canvas.get("label", "unknown")
        # Get the image resource URL from the first image annotation
        images = canvas.get("images", [])
        if not images:
            continue
        resource = images[0].get("resource", {})
        service = resource.get("service", {})
        base_url = service.get("@id", "")
        if not base_url:
            # Fall back to resource @id and strip size/rotation/quality
            base_url = resource.get("@id", "")
            base_url = re.sub(r"/full/.*", "", base_url)
        if base_url:
            entries.append((label, f"{base_url}/full/full/0/default.jpg"))
    return entries


def label_to_filename(label):
    """Convert canvas label like 'fol. 1v' to 'fol_01v.jpg'."""
    label = label.strip()
    # Match folio labels
    m = re.match(r"fol\.\s*(\d+)(v|r)?", label, re.IGNORECASE)
    if m:
        num = int(m.group(1))
        side = m.group(2) or "r"
        return f"fol_{num:02d}{side}.jpg"
    # Non-folio images: sanitize the label
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", label).strip("_").lower()
    return f"{safe}.jpg"


def download_image(url, dest):
    req = Request(url, headers={"User-Agent": "FioreTranscription/1.0"})
    with urlopen(req, timeout=60) as resp:
        data = resp.read()
    dest.write_bytes(data)
    return len(data)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching IIIF manifest...")
    manifest = fetch_manifest()

    entries = parse_canvases(manifest)
    print(f"Found {len(entries)} canvases in manifest.\n")

    skipped = 0
    downloaded = 0

    for i, (label, url) in enumerate(entries, 1):
        filename = label_to_filename(label)
        dest = OUTPUT_DIR / filename
        if dest.exists() and dest.stat().st_size > 100_000:
            print(f"  [{i}/{len(entries)}] SKIP (exists): {filename}")
            skipped += 1
            continue

        print(f"  [{i}/{len(entries)}] Downloading: {label} -> {filename} ...", end=" ", flush=True)
        try:
            size = download_image(url, dest)
            print(f"{size / 1_000_000:.1f} MB")
            downloaded += 1
        except Exception as e:
            print(f"FAILED: {e}")

        if i < len(entries):
            time.sleep(DELAY)

    print(f"\nDone. Downloaded: {downloaded}, Skipped: {skipped}, Total: {len(entries)}")
    print(f"Images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
