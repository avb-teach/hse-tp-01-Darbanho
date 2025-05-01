import os
import sys
import shutil

def gather_dirrs(in_dirr, out_dirr, max_depth=None):
    if not os.path.isdir(in_dirr):
        sys.exit(0)

    for rt, dirs, files in os.walk(in_dirr):
        for file in files:
            src = os.path.join(rt, file)
            rel_pt = os.path.relpath(src, in_dirr)
            path_parts = rel_pt.split(os.sep)

            if max_depth is not None:

                aim_marks = path_parts[-(max_depth - 1):] if max_depth > 1 else [file]
                dst = os.path.join(out_dirr, *aim_marks)
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

    gather_dirrs(in_dirr, out_dirr, max_depth)