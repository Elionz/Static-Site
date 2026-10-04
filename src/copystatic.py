import os
import shutil


def copy_static(source_dir, dest_dir):
    # Start clean: delete the destination if it exists
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    copy_contents(source_dir, dest_dir)


def copy_contents(source_dir, dest_dir):
    for name in os.listdir(source_dir):
        source_path = os.path.join(source_dir, name)
        dest_path = os.path.join(dest_dir, name)
        print(f" * {source_path} -> {dest_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_contents(source_path, dest_path)