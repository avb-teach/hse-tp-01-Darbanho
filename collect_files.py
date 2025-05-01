import os
import sys
import shutil

def collect_file_dirrs(in_dirr, out_dirr, max_depth=None):
    if not os.path.isdir(in_dirr):
        sys.exit(0)

    for root, dirs, files in os.walk(in_dirr):
        for file in files:
            src = os.path.join(root, file)
            rel_path = os.path.relpath(src, in_dirr)
            parts = rel_path.split(os.sep)

            if max_depth is not None:
                if max_depth <= 1:
                    aim_parts = [file]
                else:
                    aim_parts = parts[-(max_depth - 1):]
                dst = os.path.join(out_dirr, *aim_parts)
            else:
                dst = os.path.join(out_dirr, file)
                name, ext = os.path.splitext(file)
                count = 1
                while os.path.exists(dst):
                    dst = os.path.join(out_dirr, f"{name}_{count}{ext}")
                    count += 1

            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    in_dirr = sys.argv[1]
    out_dirr = sys.argv[2]
    max_depth = None

    if "--max_depth" in sys.argv:
        try:
            idx = sys.argv.index("--max_depth")
            if idx + 1 < len(sys.argv):
                max_depth = int(sys.argv[idx + 1])
        except:
            pass

    collect_file_dirrs(in_dirr, out_dirr, max_depth)