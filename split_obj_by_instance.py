# import os
# import argparse
# import json
# import numpy as np

# def process_folder(folder_path):
#     # Find all .ply files in the folder (excluding already split files)
#     ply_files = [
#         f for f in os.listdir(folder_path)
#         if f.endswith('.ply') and not any(suffix in f.lower() for suffix in ['_trunk.ply', '_branch.ply', '_spur.ply'])
#     ]
    
#     for ply_filename in ply_files:
#         base_name, _ = os.path.splitext(ply_filename)
#         json_filename = f"{base_name}.json"
        
#         ply_path = os.path.join(folder_path, ply_filename)
#         json_path = os.path.join(folder_path, json_filename)
        
#         if not os.path.exists(json_path):
#             print(f"Skipping {ply_filename}: no matching JSON ({json_filename})")
#             continue
        
#         # Load JSON mapping
#         with open(json_path, 'r') as jf:
#             color_to_label = {
#                 tuple(map(int, k.strip('()').split(', '))): v
#                 for k, v in json.load(jf).items()
#             }
        
#         # Read PLY manually
#         with open(ply_path, 'r') as f:
#             vertex_count = face_count = 0
#             # Read header
#             while True:
#                 line = f.readline().strip()
#                 if line.startswith('element vertex'):
#                     vertex_count = int(line.split()[-1])
#                 elif line.startswith('element face'):
#                     face_count = int(line.split()[-1])
#                 elif line == 'end_header':
#                     break

#             # Read vertices
#             vertices = []
#             colors = []
#             for _ in range(vertex_count):
#                 parts = f.readline().strip().split()
#                 x, y, z = map(float, parts[:3])
#                 r, g, b = map(int, parts[3:6])
#                 vertices.append((x, y, z, r, g, b))
#                 colors.append((r, g, b))
#             vertices = np.array(vertices, dtype=[
#                 ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
#                 ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
#             ])
#             colors = np.array(colors)

#             # Read faces (supporting any vertex count per face)
#             faces = []
#             for _ in range(face_count):
#                 parts = f.readline().strip().split()
#                 n = int(parts[0])  # number of vertices in this face
#                 idxs = list(map(int, parts[1:1+n]))
#                 faces.append(tuple(idxs))

#         # Determine category for each vertex
#         vertex_categories = []
#         for color in colors:
#             label = color_to_label.get(tuple(color), '')
#             l = label.lower()
#             if l.startswith('trunk'):
#                 vertex_categories.append('trunk')
#             elif l.startswith('branch'):
#                 vertex_categories.append('branch')
#             elif l.startswith('spur'):
#                 vertex_categories.append('spur')
#             else:
#                 vertex_categories.append('other')
#         vertex_categories = np.array(vertex_categories)

#         # Split into categories
#         for category in ['trunk', 'branch', 'spur']:
#             mask = vertex_categories == category
#             old_to_new = -np.ones(len(vertices), dtype=int)
#             old_to_new[mask] = np.arange(mask.sum())
#             filtered_vertices = vertices[mask]
#             valid_faces = [
#                 tuple(old_to_new[i] for i in face)
#                 for face in faces
#                 if all(mask[i] for i in face)
#             ]
            
#             out_path = os.path.join(folder_path, f"{base_name}_{category.upper()}.ply")
#             with open(out_path, 'w') as out:
#                 # Write header
#                 out.write("ply\n")
#                 out.write("format ascii 1.0\n")
#                 out.write(f"element vertex {len(filtered_vertices)}\n")
#                 out.write("property float x\nproperty float y\nproperty float z\n")
#                 out.write("property uchar diffuse_red\nproperty uchar diffuse_green\nproperty uchar diffuse_blue\n")
#                 out.write(f"element face {len(valid_faces)}\n")
#                 out.write("property list uchar int vertex_indices\n")
#                 out.write("end_header\n")
                
#                 # Write vertices
#                 for v in filtered_vertices:
#                     out.write(f"{v['x']} {v['y']} {v['z']} {v['red']} {v['green']} {v['blue']}\n")
                
#                 # Write faces, preserving original vertex count
#                 for face in valid_faces:
#                     out.write(f"{len(face)} " + " ".join(map(str, face)) + "\n")
            
#             print(f"Wrote {out_path} with {len(filtered_vertices)} vertices and {len(valid_faces)} faces")

# def main():
#     parser = argparse.ArgumentParser(
#         description="Split PLYs in a folder into trunk, branch, and spur based on matching JSON labels (preserving face vertex counts)."
#     )
#     parser.add_argument(
#         "--folder", required=True,
#         help="Path to the folder containing .ply and .json files"
#     )
#     args = parser.parse_args()
#     process_folder(args.folder)

# if __name__ == "__main__":
#     main()

# Full script: merge_and_export.py
# This script:
# 1. Splits each tree_<id>.ply into instance parts (trunk, branch, spur) with unique colors.
# 2. Saves global_instance_colors.json mapping part -> [r,g,b].
# 3. Creates color_to_part.json mapping "r,g,b" -> part name.
# 4. Merges all instance parts by tree and category into tree_<id>_<category>.ply.
# 5. Zips merged files into merged_by_category_instances.zip.

import os
import json
import colorsys
import numpy as np
import zipfile

# === Full script with cleanup: merge_and_export_cleanup.py ===

GLOBAL_COLOR_MAP = {}
INSTANCE_COLOR_JSON = 'global_instance_colors.json'
COLOR_TO_PART_JSON = 'color_to_part.json'
MERGED_ZIP = 'merged_by_category_instances.zip'

def get_unique_color(key):
    """Assign a reproducible unique color for each key."""
    i = len(GLOBAL_COLOR_MAP)
    hue = (i * 0.618033988749895) % 1.0
    rgb_frac = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
    rgb = tuple(int(255 * c) for c in rgb_frac)
    GLOBAL_COLOR_MAP[key] = rgb
    return rgb

def split_and_color(folder):
    """Split each tree_<id>.ply into labeled parts with unique colors."""
    for fname in os.listdir(folder):
        if not fname.endswith('.ply'):
            continue
        print("Processing:", fname)
        base, _ = os.path.splitext(fname)
        json_path = os.path.join(folder, f"{base}.json")
        if not os.path.isfile(json_path):
            continue

        with open(json_path) as jf:
            ori = {tuple(map(int,k.strip('()').split(', '))):v 
                   for k,v in json.load(jf).items()}

        path = os.path.join(folder, fname)
        with open(path) as f:
            v_count = face_count = 0
            while True:
                line = f.readline().strip()
                if line.startswith('element vertex'):
                    v_count = int(line.split()[-1])
                elif line.startswith('element face'):
                    face_count = int(line.split()[-1])
                elif line == 'end_header':
                    break
            verts=[]; colors=[]; faces=[]
            for _ in range(v_count):
                parts = f.readline().split()
                x,y,z = map(float,parts[:3])
                r,g,b = map(int,parts[3:6])
                verts.append((x,y,z,r,g,b)); colors.append((r,g,b))
            for _ in range(face_count):
                parts = f.readline().split()
                cnt = int(parts[0])
                idxs = list(map(int,parts[1:1+cnt]))
                faces.append(tuple(idxs))

        labels = [ori.get(c,'') for c in colors]
        for lbl in sorted(set(labels)-{''}):
            key = f"{base}_{lbl}"
            rgb = GLOBAL_COLOR_MAP.get(key) or get_unique_color(key)
            mask = [l==lbl for l in labels]
            old2new = -np.ones(len(verts),int)
            old2new[mask]=np.arange(mask.count(True))
            v_sub=[verts[i] for i in range(len(verts)) if mask[i]]
            f_sub=[tuple(old2new[j] for j in face) 
                   for face in faces if all(mask[j] for j in face)]
            out_name = f"{key}_.ply"
            with open(os.path.join(folder,out_name),'w') as out:
                out.write("ply\nformat ascii 1.0\n")
                out.write(f"element vertex {len(v_sub)}\n")
                out.write("property float x\nproperty float y\nproperty float z\n")
                out.write("property uchar diffuse_red\nproperty uchar diffuse_green\nproperty uchar diffuse_blue\n")
                out.write(f"element face {len(f_sub)}\nproperty list uchar int vertex_indices\nend_header\n")
                for v in v_sub:
                    out.write(f"{v[0]} {v[1]} {v[2]} {rgb[0]} {rgb[1]} {rgb[2]}\n")
                for face in f_sub:
                    out.write(f"{len(face)} "+" ".join(map(str,face))+"\n")

def save_mappings(folder):
    """Save JSONs mapping parts↔colors."""
    with open(os.path.join(folder, INSTANCE_COLOR_JSON),'w') as f:
        json.dump(GLOBAL_COLOR_MAP, f, indent=2)
    inv = {','.join(map(str,v)):k for k,v in GLOBAL_COLOR_MAP.items()}
    with open(os.path.join(folder, COLOR_TO_PART_JSON),'w') as f:
        json.dump(inv, f, indent=2)

def merge_by_category(folder):
    """Merge instance PLYs by tree and category, zip them, then remove instances."""
    cats=['Trunk','Branch','Spur']
    trees = sorted({ '_'.join(f.split('_')[:2]) 
                     for f in os.listdir(folder) if f.startswith('tree_') and f.endswith('.ply') })
    print("Trees found:", trees)
    merged=[]
    for tree in trees:
        for cat in cats:
            insts=[f for f in os.listdir(folder)
                   if f.startswith(f"{tree}_{cat}_") and f.endswith('.ply')]
    
            print(f"Processing {tree} category {cat}, found {len(insts)} instances", f"{tree}_{cat}_")
            if not insts: continue
            verts=[]; faces=[]; off=0
            for inst in insts:
                print("Merging:", inst)
                with open(os.path.join(folder,inst)) as f:
                    vc=fc=0
                    while True:
                        l=f.readline().strip()
                        if l.startswith('element vertex'): vc=int(l.split()[-1])
                        elif l.startswith('element face'): fc=int(l.split()[-1])
                        elif l=='end_header': break
                    for _ in range(vc):
                        x,y,z,r,g,b = f.readline().split()
                        verts.append((float(x),float(y),float(z),int(r),int(g),int(b)))
                        #Use only 3 decimal places for colors
                        
                    for _ in range(fc):
                        parts=f.readline().split()
                        cnt=int(parts[0]); idxs=list(map(int,parts[1:1+cnt]))
                        faces.append([i+off for i in idxs])
                off+=vc
            out=f"{tree}_{cat.upper()}.ply"
            with open(os.path.join(folder,out),'w') as w:
                w.write("ply\nformat ascii 1.0\n")
                w.write(f"element vertex {len(verts)}\n")
                w.write("property float x\nproperty float y\nproperty float z\n")
                w.write("property uchar diffuse_red\nproperty uchar diffuse_green\nproperty uchar diffuse_blue\n")
                w.write(f"element face {len(faces)}\nproperty list uchar int vertex_indices\nend_header\n")
                for v in verts: w.write(f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]}\n")
                for fc_ in faces: w.write(f"{len(fc_)} "+" ".join(map(str,fc_))+"\n")
            merged.append(out)

    # Zip merged PLYs
    # zip_path=os.path.join(folder,MERGED_ZIP)
    # with zipfile.ZipFile(zip_path,'w') as z:
    #     for m in merged: z.write(os.path.join(folder,m),arcname=m)
    # Remove instance-level PLYs (underscore count > 2)
    for f in os.listdir(folder):
        if f.endswith('.ply') and f.count('_') > 3:
            os.remove(os.path.join(folder,f))
    # return merged, zip_path
    return merged, None  # No zipping in this version


if __name__=="__main__":
    import argparse
    args = argparse.ArgumentParser(
        description="Split PLY files by instance, save color mappings, and merge by category."
    )
    args.add_argument('--folder', required=True, help="Path to the folder containing .ply and .json files")
    args = args.parse_args()
    data_folder = args.folder
    split_and_color(data_folder)
    save_mappings(data_folder)
    merged, zipfile_path = merge_by_category(data_folder)

    print("Done. Created:")
    print(" -", INSTANCE_COLOR_JSON)
    print(" -", COLOR_TO_PART_JSON)
    print(" -", ZIPfile_path if (ZIPfile_path:=zipfile_path) else zipfile_path)

    # List final directory
    print("\nFinal directory contents:")
    for fname in sorted(os.listdir(data_folder)):
        print(" ", fname)

