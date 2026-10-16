import math
import sys
import glfw

from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GL.shaders import compileProgram, compileShader


VERTEX_SHADER = """
#version 120

varying vec3 vPosition;
varying vec3 vNormal;

void main()
{
    vec4 eyePosition = gl_ModelViewMatrix * gl_Vertex;

    vPosition = eyePosition.xyz;
    vNormal = normalize(gl_NormalMatrix * gl_Normal);

    gl_Position = gl_ProjectionMatrix * eyePosition;
}
"""


FRAGMENT_SHADER = """
#version 120

varying vec3 vPosition;
varying vec3 vNormal;

uniform vec3 uObjectColor;
uniform vec3 uLightColor;
uniform vec3 uLightPosition;

uniform float uKa;
uniform float uKd;
uniform float uKs;
uniform float uShininess;

void main()
{
    vec3 N = normalize(vNormal);
    vec3 L = normalize(uLightPosition - vPosition);
    vec3 V = normalize(-vPosition);
    vec3 R = reflect(-L, N);

    // Ambient component
    vec3 ambient = uKa * uLightColor * uObjectColor;

    // Diffuse component
    float diff = max(dot(N, L), 0.0);
    vec3 diffuse = uKd * diff * uLightColor * uObjectColor;

    // Specular component
    float spec = 0.0;

    if (diff > 0.0)
    {
        spec = pow(max(dot(R, V), 0.0), uShininess);
    }

    vec3 specular = uKs * spec * uLightColor;

    // Final Phong illumination
    vec3 result = ambient + diffuse + specular;

    gl_FragColor = vec4(clamp(result, 0.0, 1.0), 1.0);
}
"""


MATERIALS = {
    glfw.KEY_1: (0.90, 0.16, 0.12),
    glfw.KEY_2: (0.15, 0.78, 0.28),
    glfw.KEY_3: (0.16, 0.38, 0.95),
}


state = {
    "color": MATERIALS[glfw.KEY_1],
    "rotating": True,
}


def key_callback(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_SPACE:
        state["rotating"] = not state["rotating"]
        print("Rotation:", "ON" if state["rotating"] else "PAUSED")

    elif key in MATERIALS:
        state["color"] = MATERIALS[key]
        print("Material color changed.")


def sphere_vertex(latitude, longitude):
    x = math.cos(latitude) * math.sin(longitude)
    y = math.sin(latitude)
    z = math.cos(latitude) * math.cos(longitude)

    return x, y, z


def emit_vertex(latitude, longitude):
    x, y, z = sphere_vertex(latitude, longitude)

    glNormal3f(x, y, z)
    glVertex3f(x, y, z)


def draw_sphere(stacks=48, slices=64):
    glBegin(GL_TRIANGLES)

    for i in range(stacks):
        lat0 = -math.pi / 2 + math.pi * i / stacks
        lat1 = -math.pi / 2 + math.pi * (i + 1) / stacks

        for j in range(slices):
            lon0 = 2 * math.pi * j / slices
            lon1 = 2 * math.pi * (j + 1) / slices

            emit_vertex(lat0, lon0)
            emit_vertex(lat1, lon0)
            emit_vertex(lat1, lon1)

            emit_vertex(lat0, lon0)
            emit_vertex(lat1, lon1)
            emit_vertex(lat0, lon1)

    glEnd()


def set_uniforms(program):
    glUniform3f(
        glGetUniformLocation(program, "uObjectColor"),
        *state["color"]
    )

    glUniform3f(
        glGetUniformLocation(program, "uLightColor"),
        1.0, 1.0, 1.0
    )

    glUniform3f(
        glGetUniformLocation(program, "uLightPosition"),
        -2.5, 3.0, 3.0
    )

    glUniform1f(
        glGetUniformLocation(program, "uKa"), 0.18
    )

    glUniform1f(
        glGetUniformLocation(program, "uKd"), 0.78
    )

    glUniform1f(
        glGetUniformLocation(program, "uKs"), 0.65
    )

    glUniform1f(
        glGetUniformLocation(program, "uShininess"), 48.0
    )


def main():
    if not glfw.init():
        print("Error: GLFW initialization failed.")
        return 1

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.DEPTH_BITS, 24)
    glfw.window_hint(glfw.DOUBLEBUFFER, glfw.TRUE)

    window = glfw.create_window(
        900, 650,
        "Experiment 7 - Phong Illumination Model",
        None, None
    )

    if not window:
        glfw.terminate()
        print("Error: Could not create OpenGL window.")
        return 1

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    glfw.set_key_callback(window, key_callback)

    try:
        program = compileProgram(
            compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )
    except Exception as error:
        glfw.destroy_window(window)
        glfw.terminate()
        print("Shader compilation failed:")
        print(error)
        return 1

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glClearColor(0.035, 0.045, 0.075, 1.0)

    print("Experiment 7: Phong Illumination Model")
    print("1: Red sphere")
    print("2: Green sphere")
    print("3: Blue sphere")
    print("SPACE: Pause/resume rotation")
    print("ESC: Exit")

    previous_time = glfw.get_time()
    rotation_angle = 0.0

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = min(current_time - previous_time, 0.1)
        previous_time = current_time

        if state["rotating"]:
            rotation_angle = (
                rotation_angle + 24.0 * delta_time
            ) % 360.0

        width, height = glfw.get_framebuffer_size(window)
        width = max(width, 1)
        height = max(height, 1)

        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(
            45.0,
            width / float(height),
            0.1,
            100.0
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluLookAt(
            0.0, 0.0, 3.2,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0
        )

        glRotatef(rotation_angle, 0.0, 1.0, 0.0)
        glRotatef(-12.0, 1.0, 0.0, 0.0)

        glUseProgram(program)
        set_uniforms(program)
        draw_sphere()
        glUseProgram(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteProgram(program)
    glfw.destroy_window(window)
    glfw.terminate()

    return 0


if __name__ == "__main__":
    sys.exit(main())