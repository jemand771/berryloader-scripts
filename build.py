# Example build script for mods. Feel free to comment out all sections you dont want

import shutil
import subprocess
import time
import os
from pathlib import Path

import psutil

# Section: build mod
start_time = time.time()

p = subprocess.Popen("dotnet build", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = p.communicate()
if p.returncode != 0:
    print(stdout.decode())
    exit(p.returncode)

print(f"built in {time.time() - start_time:.2f}s")

# Section: kill stacklands process
for proc in psutil.process_iter(["name", "pid"]):
    if proc.name() == "Stacklands.exe":
        proc.kill()
        proc.wait()
        
# Section: copy dll
dll = "./bin/Debug/netstandard2.0/YourMod.dll" # UPDATE PATH
shutil.copyfile(dll, "../../Game/mods/YourMod/YourMod.dll") # UPDATE PATH

def sync_folder(src: Path, dst: Path):
    for file in dst.glob("**/*"):
        file_in_src = src / file.relative_to(dst)
        if file.is_dir() and not file_in_src.exists():
            shutil.rmtree(file)
        elif file.is_file() and (not file_in_src.exists() or file.stat().st_mtime < file_in_src.stat().st_mtime):
            os.remove(file)
    for file in src.glob("**/*"):
        file_in_dst = dst / file.relative_to(src)
        if not file_in_dst.exists():
            file_in_dst.parent.mkdir(parents=True, exist_ok=True)
            if file.is_file():
                shutil.copy(file, file_in_dst)
            elif file.is_dir():
                shutil.copytree(file, file_in_dst)
                
# Section: copy content paths
game = Path("../../Game/mods/YourMod").resolve() # UPDATE PATH
print("syncing folders..")
sync_folder(Path("Blueprints"), game / "Blueprints")
sync_folder(Path("Boosterpacks"), game / "Boosterpacks")
sync_folder(Path("Cards"), game / "Cards")
sync_folder(Path("Images"), game / "Images")
sync_folder(Path("Sounds"), game / "Sounds")

# Section: launch the game
subprocess.Popen("..\..\Game\Stacklands") # UPDATE PATH
