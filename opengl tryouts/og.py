import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm  # pip install PyGLM
import math

# Vertex shader source code
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
out vec2 TexCoord;
uniform mat4 projection;
uniform mat4 view;
void main()
{
    gl_Position = projection * view * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
void main()
{
    // Render a simple green color for the plane
    FragColor = vec4(0.3, 0.7, 0.3, 1.0);
}
"""

# Plane vertices and indices
plane_vertices = np.array([
    # positions           # texture coords
    -10.0, 0.0, -10.0,    0.0, 0.0,
     10.0, 0.0, -10.0,    1.0, 0.0,
     10.0, 0.0,  10.0,    1.0, 1.0,
    -10.0, 0.0,  10.0,    0.0, 1.0,
], dtype=np.float32)

indices = np.array([
    0, 1, 2,
    2, 3, 0
], dtype=np.uint32)

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

def main():
    global camera_angle, vertical_angle

    # Initialize GLFW
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "OpenGL Plane with Full Rotation Camera", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # Compile shaders and create shader program
    vertex_shader = OpenGL.GL.shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = OpenGL.GL.shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = OpenGL.GL.shaders.compileProgram(vertex_shader, fragment_shader)

    # Generate buffers and arrays
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)
    
    # Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, plane_vertices.nbytes, plane_vertices, GL_STATIC_DRAW)
    
    # Element Buffer Object
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * plane_vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Texture coordinate attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * plane_vertices.itemsize, ctypes.c_void_p(3 * plane_vertices.itemsize))
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)  # Unbind VAO

    glEnable(GL_DEPTH_TEST)

    # Setup projection matrix (constant for now)
    projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)

    # Render loop
    while not glfw.window_should_close(window):
        process_input(window)
        
        # Update camera position based on horizontal and vertical angles
        radius = 15.0
        # Convert angles to radians for math functions
        h_rad = glm.radians(camera_angle)
        v_rad = glm.radians(vertical_angle)
        
        # Calculate position on a sphere around the origin (spherical coordinates)
        camX = radius * math.sin(v_rad) * math.sin(h_rad)
        camY = radius * math.cos(v_rad)
        camZ = radius * math.sin(v_rad) * math.cos(h_rad)
        camera_pos = glm.vec3(camX, camY, camZ)

        # Create view matrix looking at the origin
        view = glm.lookAt(camera_pos, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))

        # Render
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader_program)
        
        # Pass projection and view matrices to the shader
        proj_loc = glGetUniformLocation(shader_program, "projection")
        view_loc = glGetUniformLocation(shader_program, "view")
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        
        # Bind VAO and draw the plane
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Clean up
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteProgram(shader_program)
    glfw.terminate()

if __name__ == "__main__":
    main()
