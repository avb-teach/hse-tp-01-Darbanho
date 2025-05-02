import os
import sys
import shutil

def gather_files(in_dirr, out_dirr, max_depth):
    os.makedirs(out_dirr, exist_ok=True)

    for rt, dirs, filenames in os.walk(in_dirr):
        for fname in filenames:
            istoc = os.path.join(rt, fname)
            rel = os.path.relpath(istoc, in_dirr)
            marks = rel.split(os.sep)
            marks = marks[-max_depth:] if len(marks) > max_depth else marks

            aim_p = os.path.join(out_dirr, *marks)    
            os.makedirs(os.path.dirname(aim_p), exist_ok=True)
            shutil.copy2(istoc, aim_p)

if __name__ == "__main__":
    depth = 1
    params = sys.argv[1:]

    if "--max_depth" in params:
        try:
            idx = params.index("--max_depth")
            depth = int(params[idx + 1])
            params = params[:idx]
        except:
            sys.exit(1)

    if len(params) != 2:
        sys.exit(1)
    in_dirr, out_dirr = params
    if not os.path.isdir(in_dirr):
        sys.exit(1)

    gather_files(in_dirr, out_dirr, depth)


