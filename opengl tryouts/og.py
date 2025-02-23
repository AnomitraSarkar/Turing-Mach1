import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm  # pip install PyGLM
import math

# Vertex shader source code (shared by plane and cube)
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
out vec2 TexCoord;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;
void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
"""

# Fragment shader source code (shared by plane and cube)
fragment_shader_source = """
#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
uniform vec4 color;
void main()
{
    FragColor = color;
}
"""

# Plane vertices and indices (a large quad on the XZ plane)
plane_vertices = np.array([
    # positions           # texture coords
    -10.0, 0.0, -10.0,    0.0, 0.0,
     10.0, 0.0, -10.0,    1.0, 0.0,
     10.0, 0.0,  10.0,    1.0, 1.0,
    -10.0, 0.0,  10.0,    0.0, 1.0,
], dtype=np.float32)

plane_indices = np.array([
    0, 1, 2,
    2, 3, 0
], dtype=np.uint32)

# Cube vertex data (36 vertices, with position and texture coords)
# This cube is centered at the origin with side length 1.
cube_vertices = np.array([
    # Back face
    -0.5, -0.5, -0.5,   0.0, 0.0,
     0.5,  0.5, -0.5,   1.0, 1.0,
     0.5, -0.5, -0.5,   1.0, 0.0,
     0.5,  0.5, -0.5,   1.0, 1.0,
    -0.5, -0.5, -0.5,   0.0, 0.0,
    -0.5,  0.5, -0.5,   0.0, 1.0,

    # Front face
    -0.5, -0.5,  0.5,   0.0, 0.0,
     0.5, -0.5,  0.5,   1.0, 0.0,
     0.5,  0.5,  0.5,   1.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 1.0,
    -0.5,  0.5,  0.5,   0.0, 1.0,
    -0.5, -0.5,  0.5,   0.0, 0.0,

    # Left face
    -0.5,  0.5,  0.5,   1.0, 0.0,
    -0.5,  0.5, -0.5,   1.0, 1.0,
    -0.5, -0.5, -0.5,   0.0, 1.0,
    -0.5, -0.5, -0.5,   0.0, 1.0,
    -0.5, -0.5,  0.5,   0.0, 0.0,
    -0.5,  0.5,  0.5,   1.0, 0.0,

    # Right face
     0.5,  0.5,  0.5,   1.0, 0.0,
     0.5, -0.5, -0.5,   0.0, 1.0,
     0.5,  0.5, -0.5,   1.0, 1.0,
     0.5, -0.5, -0.5,   0.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 0.0,
     0.5, -0.5,  0.5,   0.0, 0.0,

    # Bottom face
    -0.5, -0.5, -0.5,   0.0, 1.0,
     0.5, -0.5, -0.5,   1.0, 1.0,
     0.5, -0.5,  0.5,   1.0, 0.0,
     0.5, -0.5,  0.5,   1.0, 0.0,
    -0.5, -0.5,  0.5,   0.0, 0.0,
    -0.5, -0.5, -0.5,   0.0, 1.0,

    # Top face
    -0.5,  0.5, -0.5,   0.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 0.0,
     0.5,  0.5, -0.5,   1.0, 1.0,
     0.5,  0.5,  0.5,   1.0, 0.0,
    -0.5,  0.5, -0.5,   0.0, 1.0,
    -0.5,  0.5,  0.5,   0.0, 0.0,
], dtype=np.float32)

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

# Global camera angles (in degrees)
camera_angle = 45.0   # Horizontal rotation
vertical_angle = 45.0 # Vertical rotation

def process_input(window):
    global camera_angle, vertical_angle

    # Horizontal rotation
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        camera_angle -= 0.25
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        camera_angle += 0.25

    # Vertical rotation (full rotation allowed)
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        vertical_angle -= 0.25
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        vertical_angle += 0.25

    # Escape key closes the window
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def init_indexed_object(vertices, indices):
    """Initialize buffers for an indexed object (VAO, VBO, EBO) and return VAO and index count."""
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    # Setup VBO
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Setup EBO
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Vertex attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    return VAO, len(indices)

def init_object_array(vertices):
    """Initialize buffers for a non-indexed object using glDrawArrays, and return VAO and vertex count."""
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    vertex_count = int(len(vertices) / 5)
    return VAO, vertex_count

def main():
    global camera_angle, vertical_angle

    # Initialize GLFW
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "OpenGL Plane with Cube", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # Compile shaders and create shader program
    vertex_shader = OpenGL.GL.shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = OpenGL.GL.shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)

    # Initialize plane using indexed drawing
    plane_VAO, plane_index_count = init_indexed_object(plane_vertices, plane_indices)
    # Initialize cube using array drawing (non-indexed)
    cube_VAO, cube_vertex_count = init_object_array(cube_vertices)

    glEnable(GL_DEPTH_TEST)

    # Setup projection matrix (constant)
    projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)

    while not glfw.window_should_close(window):
        process_input(window)
        
        # Update camera position based on angles
        radius = 15.0
        h_rad = glm.radians(camera_angle)
        v_rad = glm.radians(vertical_angle)
        
        camX = radius * math.sin(v_rad) * math.sin(h_rad)
        camY = radius * math.cos(v_rad)
        camZ = radius * math.sin(v_rad) * math.cos(h_rad)
        camera_pos = glm.vec3(camX, camY, camZ)
        view = glm.lookAt(camera_pos, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shader_program)
        
        # Set the shared projection and view matrices
        proj_loc = glGetUniformLocation(shader_program, "projection")
        view_loc = glGetUniformLocation(shader_program, "view")
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        
        model_loc = glGetUniformLocation(shader_program, "model")
        color_loc = glGetUniformLocation(shader_program, "color")
        
        # Render the plane with an identity model matrix (green)
        model = glm.mat4(1.0)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        glUniform4f(color_loc, 0.3, 0.7, 0.3, 1.0)
        glBindVertexArray(plane_VAO)
        glDrawElements(GL_TRIANGLES, plane_index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        # Render the cube on top of the plane.
        # Translate the cube upward so its bottom is at y = 0.
        # Since the cube is centered at origin with side length 1, translating by 0.5 in Y positions it on the plane.
        model = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.5, 0.0))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        # Set cube color (e.g., blue)
        glUniform4f(color_loc, 0.0, 0.0, 1.0, 1.0)
        glBindVertexArray(cube_VAO)
        glDrawArrays(GL_TRIANGLES, 0, cube_vertex_count)
        glBindVertexArray(0)
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Cleanup: Deleting VAOs (and associated buffers will be cleaned up by context deletion)
    glDeleteVertexArrays(1, [plane_VAO])
    glDeleteVertexArrays(1, [cube_VAO])
    glfw.terminate()

if __name__ == "__main__":
    main()
