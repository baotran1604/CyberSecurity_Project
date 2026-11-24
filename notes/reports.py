from hashlib import sha256
from importlib import metadata
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


@login_required
def inventory(request):
    if not request.user.is_staff:
        raise PermissionDenied

    packages = [metadata.distribution("Django")]
    # Fix 1: list every installed package, including the ones Django needs.
    # packages = list(metadata.distributions())

    rows = sorted((p.metadata["Name"], p.version) for p in packages)
    return render(request, "notes/inventory.html", {"rows": rows})


GUIDE_FOLDER = Path(__file__).with_name("guides")
# Keep a copy of the checksum for each approved guide.
CHECKSUMS = {
    "reading-plan.txt": "9cd2b383e316abb328bd5af8aa10170194df7721e614caa2dd9efdf62f395fea",
    # Fix 3: add the checksum for the Weekly Review guide.
    # "weekly-review.txt": "8d89e255164871ac64ac5826b98ae12372fcfab6ea2b2ef999a06fb423b1547e",
}


@login_required
def guides(request):
    guides = []
    for path in sorted(GUIDE_FOLDER.glob("*.txt")):
        data = path.read_bytes()
        expected = CHECKSUMS.get(path.name)
        body = ""
        if expected is None:
            status = "This guide is missing its checksum, so we can’t open it yet."
        elif sha256(data).hexdigest() != expected:
            status = "This file differs from the approved release. Check your copy of the guide."
        else:
            status = "Release checksum verified."
            body = data.decode("utf-8")
        guides.append({"name": path.stem.replace("-", " ").title(), "status": status, "body": body})
    return render(request, "notes/guides.html", {"guides": guides})
