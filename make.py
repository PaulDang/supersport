# make.py
import subprocess

targets = {
    "full": [
        "migrate",
        "runserver",
    ],
}


def run_target(target):
    command_list = targets.get(target)

    if command_list:
        if target == "full":
            subprocess.run(["pipenv", "install"])
        for command in command_list:
            subprocess.run(["pipenv", "run", "python", "manage.py", command])
    else:
        print(f"Target '{target}' not found.")


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "run"
    run_target(target)
