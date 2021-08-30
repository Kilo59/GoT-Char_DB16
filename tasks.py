"""Project invoke developer tasks"""
import invoke


@invoke.task
def sort(ctx, path=".", check=False):
    print("  sorting imports ...")
    args = ["isort", path]
    if check:
        args.append("--check")
    ctx.run(" ".join(args))


@invoke.task(pre=[sort])
def fmt(ctx, path=".", check=False):
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
