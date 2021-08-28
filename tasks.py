"""Project invoke developer tasks"""
import invoke


@invoke.task
def sort(ctx, path="."):
    print("  sorting imports ...")
    ctx.run(f"isort {path}")


@invoke.task(pre=[sort])
def fmt(ctx, path="."):
    print("  formatting ...")
    ctx.run(f"black {path}")
