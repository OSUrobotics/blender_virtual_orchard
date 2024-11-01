import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pywavefront
from collections import defaultdict
# from pruning_sb3.pruning_gym import label



def parse_labelled_tree(file_path):
    scene = pywavefront.Wavefront(file_path, collect_faces=True)
    vertices = scene.vertices
    vertices = [vertex[:3] for vertex in vertices]
    faces = scene.mesh_list[0].faces
    vertex_colors = []

    for line in open(file_path, 'r'):
        if line.startswith('v '):
            color = line.split()[4:]
            vertex_colors.append(tuple(map(float, color)))

    return vertices, faces, vertex_colors, scene


def group_by_color(vertices, faces, vertex_colors):
    """Group vertices and faces by color."""
    color_groups = defaultdict(lambda: {'vertices': [], 'faces': []})

    for i, (vertex, color) in enumerate(zip(vertices, vertex_colors)):
        color_groups[color]['vertices'].append((i, vertex))

    for face in faces:
        face_colors = set(vertex_colors[vi] for vi in face)
        if len(face_colors) == 1:
            color = face_colors.pop()
            color_groups[color]['faces'].append(face)
    print(color_groups.keys())

    return color_groups


def create_mesh_data(color_groups):
    """Create mesh data for each color group."""
    mesh_data = {}

    for color, group in color_groups.items():
        vertices = []
        indices = []
        vertex_map = {}

        for i, (index, vertex) in enumerate(group['vertices']):
            vertex_map[index] = i
            vertices.append(vertex)

        for face in group['faces']:
            indices.append([vertex_map[vi] for vi in face])

        mesh_data[color] = (vertices, indices)
        # if self.verbose > 1:
        print(f"Color: {color}, Vertices: {len(vertices)}, Faces: {len(indices)}")

    return mesh_data


def split_obj_by_color(input_file):
    vertices, faces, vertex_colors, _ = parse_labelled_tree(input_file)
    color_groups = group_by_color(vertices, faces, vertex_colors)
    mesh_data = create_mesh_data(color_groups)
    return mesh_data


def save_as_obj(vertices, indices, output_folder, output_file, label, color):
    print(output_folder, output_file, label)
    save_file = os.path.join(output_folder, output_file+'_'+label + '.obj')
    print(f"Saving to {save_file}")
    #Add vertex colors too
    with open(save_file, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]} {color[0]} {color[1]} {color[2]}\n")

        for face in indices:
            f.write(f"f {' '.join(str(i + 1) for i in face)}\n")

import glob
import os


label = {
    (1.0, 0.0, 0.0): "TRUNK",
    (0.0, 1.0, 0.0): "SPUR",
    (1.000000, 0.588235, 0.000000): "BRANCH",
    # (0.235294, 0.000000, 0.000000): "WATER_BRANCH",
}
input_folder = 'tree_dataset/dataset_envy'
output_folder = 'tree_dataset/dataset_envy_split'
#If output folder does not exist, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
print(glob.glob(os.path.join(input_folder, '*.obj')))
# output_folder = '/Users/abhinav/Desktop/gradstuff/research/pruning_sb3/meshes_and_urdf/meshes/trees/envy/train_labelled'
for input_file in glob.glob(os.path.join(input_folder, '*.obj')):
    #get just the file name
    output_file = os.path.basename(input_file).split('.')[0]
    mesh_data = split_obj_by_color(input_file)
    for color, (vertices, indices) in mesh_data.items():
        print(color)
        save_as_obj(vertices, indices, output_folder, output_file, label[color], color)
