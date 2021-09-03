"""Project invoke developer tasks"""
import invoke


@invoke.task
def sort(ctx, path=".", check=False):
    """Sort module imports"""
    print("  sorting imports ...")
    args = ["isort", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))


@invoke.task
def fmt(ctx, path=".", check=False, sort_=True):
    """Format code and sort imports"""
    if sort_:
        sort(ctx, path=path, check=check)
    print("  formatting ...")
    args = ["black", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))


@invoke.task
def check_style(ctx):
    print("  checking style ...")
    for cmd in ["sort", "fmt"]:
        ctx.run(f"invoke {cmd} --check")


@invoke.task
def lint(ctx, path="."):
    print("  linting ...")
    print("linting noop")
    # ctx.run(f"prospector {path}")
