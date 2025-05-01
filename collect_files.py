import os
import sys
import shutil

def gather_dirrs(in_dirr, out_dirr, max_m_depth=None):
    if not os.path.isdir(in_dirr):
        sys.exit(1)

    os.makedirs(out_dirr, exist_ok=True)
    name_counts = {}

    for current_root, dirs, files in os.walk(in_dirr):
        rel_path = os.path.relpath(current_root, in_dirr)
        depth = rel_path.count(os.sep) if rel_path != '.' else 0
        
        if max_m_depth is not None and depth >= max_m_depth:
            continue

        for file in files:
            src_path = os.path.join(current_root, file)
            
            if max_m_depth is None:
                dst_file = file
                if dst_file in name_counts:
                    name, ext = os.path.splitext(file)
                    count = name_counts[file] + 1
                    dst_file = f"{name}_{count}{ext}"
                    name_counts[file] = count
                else:
                    name_counts[file] = 0
                dst_path = os.path.join(out_dirr, dst_file)
            else:
                path_parts = rel_path.split(os.sep)[:max_m_depth-1] if max_m_depth > 1 else []
                dst_dir = os.path.join(out_dirr, *path_parts)
                os.makedirs(dst_dir, exist_ok=True)
                dst_path = os.path.join(dst_dir, file)

            shutil.copy2(src_path, dst_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    in_d = sys.argv[1]
    out_d = sys.argv[2]
    m_depth = None

    if "--max_depth" in sys.argv:
        try:
            idx = sys.argv.index("--max_depth")
            if idx + 1 < len(sys.argv):
                m_depth = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            pass

    gather_dirrs(in_d, out_d, m_depth)