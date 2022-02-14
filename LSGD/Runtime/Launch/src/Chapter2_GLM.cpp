#include <glad/gl.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/ext.hpp>

#include <stdio.h>
#include <stdlib.h>

#include "Chapters.h"

using glm::mat4;
using glm::vec3;

static const char *Chapter2_GLM_shaderCodeVertex = R"(
#version 460 core

// notice how the 'PerFrameData' input structure in the following vertex shader reflects the PerFrameData structure in C++ code
layout(std140, binding=0) uniform PerFrameData
{
    uniform mat4 MVP;
    uniform int isWireframe;
};
layout(location=0) out vec3 color;
const vec3 pos[8] = vec3[8](
	vec3(-1.0,-1.0, 1.0),
	vec3( 1.0,-1.0, 1.0),
	vec3( 1.0, 1.0, 1.0),
	vec3(-1.0, 1.0, 1.0),
	vec3(-1.0,-1.0,-1.0),
	vec3( 1.0,-1.0,-1.0),
	vec3( 1.0, 1.0,-1.0),
	vec3(-1.0, 1.0,-1.0)
);
const vec3 col[8] = vec3[8](
	vec3( 1.0, 0.0, 0.0),
	vec3( 0.0, 1.0, 0.0),
	vec3( 0.0, 0.0, 1.0),
	vec3( 1.0, 1.0, 0.0),
	vec3( 1.0, 1.0, 0.0),
	vec3( 0.0, 0.0, 1.0),
	vec3( 0.0, 1.0, 0.0),
	vec3( 1.0, 0.0, 0.0)
);
const int indices[36] = int[36](
	// front
	0, 1, 2, 2, 3, 0,
	// right
	1, 5, 6, 6, 2, 1,
	// back
	7, 6, 5, 5, 4, 7,
	// left
	4, 0, 3, 3, 7, 4,
	// bottom
	4, 5, 1, 1, 0, 4,
	// top
	3, 2, 6, 6, 7, 3
);
void main()
{
    // gl_VertexID input variable is used to retrieve an index from indices[], which is used to get corresponding values for the position and color
    int idx = indices[gl_VertexID];
    gl_Position = MVP * vec4(pos[idx], 1.0);
    color = isWireframe > 0 ? vec3(0.0) : col[idx];
}
)";

static const char *Chapter2_GLM_shaderCodeFragment = R"(
#version 460 core
layout(location=0) in vec3 color;
layout(location=0) out vec4 out_FragColor;
void main()
{
    out_FragColor = vec4(color, 1.0);
}
)";

struct PerFrameData
{
    mat4 mvp;
    int isWireframe;
};

int Chapter2::GLM_main(void)
{
    // set GLFW error callback
    glfwSetErrorCallback(
        [](int error, const char *description)
        {
            (void)(error);
            fprintf(stderr, "Error: %s\n", description);
        });

    // init GLFW library
    if (!glfwInit())
        exit(EXIT_FAILURE);

    // tell GLFW which version of OpenGL, we want to use [OpenGL 4.6 Core]
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *window = glfwCreateWindow(1024, 768, "Simple example", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    // set callback to get any input event
    glfwSetKeyCallback(
        window,
        [](GLFWwindow *window, int key, int scancode, int action, int mods)
        {
            (void)scancode;
            (void)mods;
            if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
                glfwSetWindowShouldClose(window, GLFW_TRUE);
        });

    // prepare OpenGL context
    glfwMakeContextCurrent(window);
    // we use glad library from here to import all OpenGL entry points and extensions
    gladLoadGL(glfwGetProcAddress);
    glfwSwapInterval(1);

    const GLuint shaderVertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(shaderVertex, 1, &Chapter2_GLM_shaderCodeVertex, nullptr);
    glCompileShader(shaderVertex);

    const GLuint shaderFragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(shaderFragment, 1, &Chapter2_GLM_shaderCodeFragment, nullptr);
    glCompileShader(shaderFragment);

    const GLuint program = glCreateProgram();
    glAttachShader(program, shaderVertex);
    glAttachShader(program, shaderFragment);
    glLinkProgram(program);
    glUseProgram(program);

    GLuint vao;
    glCreateVertexArrays(1, &vao);
    glBindVertexArray(vao);

    /**
     * the buffer object to hold data can be allocated as follow;
     * * use **Direct-State-Access(DSA)** functions from OpenGL 4.6 instead of classic methods
     */
    GLuint perFrameDataBuffer;
    const GLsizeiptr kBufferSize = sizeof(PerFrameData);
    glCreateBuffers(1, &perFrameDataBuffer);

    // GL_DYNAMIC_STORAGE_BIT parameter tells the OpenGL implementation that the content of data store might be updated after creation through calls to 'glBufferSubData'
    glNamedBufferStorage(perFrameDataBuffer, kBufferSize, nullptr, GL_DYNAMIC_STORAGE_BIT);

    // glBindBufferRange() function binds a range within a buffer object to an indexed buffer target
    // the buffer is bound to the indexed target of 0; this value should be used in the shader code to read data from the buffer
    glBindBufferRange(GL_UNIFORM_BUFFER, 0, perFrameDataBuffer, 0, kBufferSize);

    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);

    /**
     * to render 3D cube, need depth test to render image correctly
     * * polygon offset is needed to render a wireframe image of the cube on top of the solid image without Z-fighting
     * * * the value of -1.0 will move the wireframe rendering slightly toward the camera
     */
    glEnable(GL_DEPTH_TEST);

    // note that we set PolygonOffset only for line rendering!
    glEnable(GL_POLYGON_OFFSET_LINE);
    glPolygonOffset(-1.0f, -1.0f);

    while (!glfwWindowShouldClose(window))
    {
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);

        // to calculate ratio for perspective projection matrix
        const float ratio = width / (float)height;

        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // to rotate the cube, the model matrix is calculated as a rotation around the diagonal (1, 1, 1) axis
        // angle of rotation is derived from 'glfwGetTime()'
        const mat4 m = glm::rotate(glm::translate(mat4(1.0f), vec3(0.0f, 0.0f, -3.5f)), (float)glfwGetTime(), vec3(1.0f, 1.0f, 1.0f));
        const mat4 p = glm::perspective(45.0f, ratio, 0.1f, 1000.0f);

        PerFrameData perFrameData = {
            // MVP is calculated like below
            p * m,
            false};

        glNamedBufferSubData(perFrameDataBuffer, 0, kBufferSize, &perFrameData);

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        glDrawArrays(GL_TRIANGLES, 0, 36);

        perFrameData.isWireframe = true;
        glNamedBufferSubData(perFrameDataBuffer, 0, kBufferSize, &perFrameData);

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        glDrawArrays(GL_TRIANGLES, 0, 36);

        // the fragment shader output was rendered into the backbuffer
        // let's swap the front and back buffers to make the triangle visible
        glfwSwapBuffers(window);

        // to conclude the main loop, do NOT forget to poll events with glfwPollEvents
        glfwPollEvents();
    }

    glDeleteBuffers(1, &perFrameDataBuffer);
    glDeleteProgram(program);
    glDeleteShader(shaderFragment);
    glDeleteShader(shaderVertex);
    glDeleteVertexArrays(1, &vao);

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}