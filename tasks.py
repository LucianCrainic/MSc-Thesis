"""Build tasks for the MSc thesis repository.

Every document is compiled with Tectonic into ``build/``; nothing is written
back into the source tree.  Run ``inv --list`` for the available tasks.
"""

from pathlib import Path
from shutil import rmtree

from invoke import Exit, task

ROOT = Path(__file__).parent.resolve()
BUILD = ROOT / "build"

#: Single-document targets, keyed by task name.
DOCUMENTS = {
    "thesis": ROOT / "thesis" / "thesis.tex",
    "slides": ROOT / "slides" / "slides.tex",
    "analysis": ROOT / "research" / "analysis" / "research-gap-analysis.tex",
}


def compile_document(c, source: Path) -> Path:
    """Compile one ``.tex`` file and return the path of the resulting PDF."""
    if not source.exists():
        raise Exit(f"no such document: {source.relative_to(ROOT)}", code=1)

    BUILD.mkdir(exist_ok=True)
    c.run(
        f"tectonic --keep-logs --reruns 2 "
        f'--outdir "{BUILD}" "{source}"',
        pty=True,
    )

    pdf = BUILD / f"{source.stem}.pdf"
    print(f"-> {pdf.relative_to(ROOT)}")
    return pdf


@task(help={"open_pdf": "Open the PDF when the build succeeds."})
def thesis(c, open_pdf=False):
    """Build the thesis."""
    pdf = compile_document(c, DOCUMENTS["thesis"])
    if open_pdf:
        c.run(f'open "{pdf}"')


@task(help={"open_pdf": "Open the PDF when the build succeeds."})
def slides(c, open_pdf=False):
    """Build the presentation slides."""
    pdf = compile_document(c, DOCUMENTS["slides"])
    if open_pdf:
        c.run(f'open "{pdf}"')


@task(help={"open_pdf": "Open the PDF when the build succeeds."})
def analysis(c, open_pdf=False):
    """Build the critical review and research-gap analysis."""
    pdf = compile_document(c, DOCUMENTS["analysis"])
    if open_pdf:
        c.run(f'open "{pdf}"')


@task(name="list")
def list_documents(c):
    """List every buildable document and its source path."""
    for name, source in DOCUMENTS.items():
        print(f"{name:<10} {source.relative_to(ROOT)}")


@task
def all(c):
    """Build every document in the repository."""
    for source in DOCUMENTS.values():
        compile_document(c, source)


@task
def clean(c):
    """Remove the build directory."""
    if BUILD.exists():
        rmtree(BUILD)
        print(f"removed {BUILD.relative_to(ROOT)}/")
    else:
        print("nothing to clean")
