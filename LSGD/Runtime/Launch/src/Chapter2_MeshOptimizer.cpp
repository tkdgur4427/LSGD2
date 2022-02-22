#include <glad/gl.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/ext.hpp>

#include <assimp/scene.h>
#include <assimp/postprocess.h>
#include <assimp/cimport.h>
#include <assimp/version.h>

#include <meshoptimizer.h>

#include <stdio.h>
#include <stdlib.h>

#include <vector>

using glm::mat4;
using glm::vec3;

#include "Chapters.h"

namespace MeshOptimizer
{

    static const char *shaderCodeVertex = R"(
#version 460 core
layout(std140, binding=0) uniform PerFrameData
{
    uniform mat4 MVP;
};
layout(location=0) in vec3 pos;
layout(location=0) out vec3 color;
void main()
{
    gl_Position = MVP * vec4(pos, 1.0f);
    color = pos.xyz;
}
)";

    static const char *shaderCodeGeometry = R"(
#version 460 core

layout(triangles) in;
layout(triangle_strip, max_vertices=3) out;

layout(location=0) in vec3 color[];
layout(location=0) out vec3 colors;
layout(location=1) out vec3 barycoords;

void main()
{
    const vec3 bc[3] = vec3[](
        vec3(1.0, 0.0, 1.0),
        vec3(0.0, 1.0, 0.0),
        vec3(0.0, 0.0, 1.0)
    );
    for (int i = 0; i < 3; ++i)
    {
        gl_Position = gl_in[i].gl_Position;
        colors = color[i];
        barycoords = bc[i];
        EmitVertex();
    }
    EndPrimitive();
}
)";

    static const char *shaderCodeFragment = R"(
#version 460 core
layout(location=0) in vec3 colors;
layout(location=1) in vec3 barycoords;
layout(location=0) out vec4 out_FragColor;
float edgeFactor(float thickness)
{
    // fwidth() function calculates the sum of the absolute values of the derivatives in the x and y screen coordinates and is used to determine the thickness of the lines
    vec3 a3 = smoothstep(vec3(0.0), fwidth(barycoords) * thickness, barycoords);
    return min(min(a3.x, a3.y), a3.z);
}

void main()
{
    out_FragColor = vec4(mix(vec3(0.0), colors, edgeFactor(1.0)), 1.0);
}
)";

    struct PerFrameData
    {
        mat4 mvp;
    };
}

int Chapter2::MeshOptimizer_main()
{
    glfwSetErrorCallback(
        [](int error, const char *description)
        {
            (void)error;
            fprintf(stderr, "Error: %s\n", description);
        });

    if (!glfwInit())
        exit(EXIT_FAILURE);

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *window = glfwCreateWindow(1024, 768, "Simple example", nullptr, nullptr);
    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetKeyCallback(
        window,
        [](GLFWwindow *window, int key, int scancode, int action, int mods)
        {
            (void)scancode;
            (void)mods;
            if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
                glfwSetWindowShouldClose(window, GLFW_TRUE);
        });

    glfwMakeContextCurrent(window);
    gladLoadGL(glfwGetProcAddress);
    glfwSwapInterval(1);

    const GLuint shaderVertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(shaderVertex, 1, &MeshOptimizer::shaderCodeVertex, nullptr);
    glCompileShader(shaderVertex);

    const GLuint shaderGeometry = glCreateShader(GL_GEOMETRY_SHADER);
    glShaderSource(shaderGeometry, 1, &MeshOptimizer::shaderCodeGeometry, nullptr);
    glCompileShader(shaderGeometry);

    const GLuint shaderFragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(shaderFragment, 1, &MeshOptimizer::shaderCodeFragment, nullptr);
    glCompileShader(shaderFragment);

    const GLuint program = glCreateProgram();
    glAttachShader(program, shaderVertex);
    glAttachShader(program, shaderGeometry);
    glAttachShader(program, shaderFragment);
    glLinkProgram(program);
    glUseProgram(program);

    GLuint vao;
    glCreateVertexArrays(1, &vao);
    glBindVertexArray(vao);

    const GLsizeiptr kBufferSize = sizeof(MeshOptimizer::PerFrameData);

    GLuint perFrameDataBuffer;
    glCreateBuffers(1, &perFrameDataBuffer);
    glNamedBufferStorage(perFrameDataBuffer, kBufferSize, nullptr, GL_DYNAMIC_STORAGE_BIT);
    glBindBufferRange(GL_UNIFORM_BUFFER, 0, perFrameDataBuffer, 0, kBufferSize);

    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    glEnable(GL_DEPTH_TEST);

    GLuint meshData;
    glCreateBuffers(1, &meshData);

    const aiScene *scene = aiImportFile("Data/rubber_duck/scene.gltf", aiProcess_Triangulate);
    if (!scene || !scene->HasMeshes())
    {
        printf("Unable to load Data/rubber_duck/scene.gltf\n");
        exit(255);
    }

    // we load our mesh via Assimp, preserve the existing vertices and indices exactly as they were loaded by Assimp
    const aiMesh *mesh = scene->mMeshes[0];
    std::vector<vec3> positions;
    for (unsigned i = 0; i != mesh->mNumVertices; ++i)
    {
        const aiVector3D v = mesh->mVertices[i];
        positions.push_back(vec3(v.x, v.z, v.y));
    }
    std::vector<unsigned int> indices;
    for (unsigned i = 0; i != mesh->mNumFaces; ++i)
    {
        for (unsigned j = 0; j != 3; ++j)
            indices.push_back(mesh->mFaces[i].mIndices[j]);
    }
    aiReleaseImport(scene);

    std::vector<unsigned int> indicesLod;
    {
        // we should generate a remap table for our existing vertex and index data
        // - the MeshOptimizer says:
        // - the remap table is generated based on binary equivalence of the input vertices, so the resulting mesh will be rendered in the same way
        std::vector<unsigned int> remap(indices.size());
        const size_t vertexCount = meshopt_generateVertexRemap(remap.data(), indices.data(), indices.size(), positions.data(), indices.size(), sizeof(vec3));

        // returned 'vertexCount' value correspons to the number of unique vertices that have remained after remapping
        // - allocate space and generate new vertex and index buffers
        // - now we can use other MeshOptimizer algorithm to optimize these buffers even further:
        std::vector<unsigned int> remappedIndices(indices.size());
        std::vector<vec3> remappedVertices(vertexCount);
        meshopt_remapIndexBuffer(remappedIndices.data(), indices.data(), indices.size(), remap.data());
        meshopt_remapVertexBuffer(remappedVertices.data(), positions.data(), positions.size(), sizeof(vec3), remap.data());

        // when we want to render a mesh, the GPU has to transform each vertex via a vertex shader
        // - GPUs can reuse transformed vertices by means of a small built-in cache, usually storing between 16 and 32 vertices inside it
        // - in order to use this small cache effectively, we need to reorder the triangles to maximize the locality of vertex references
        // - pay attention to how only the indices data is being touched here:
        meshopt_optimizeVertexCache(remappedIndices.data(), remappedIndices.data(), indices.size(), vertexCount);

        // transformed vertices from triangles that are sent for rasterization to generate fragments
        // - usually each fragment is run through a depth test first, and fragments that pass the depth test get the fragment shader executed to compute final color
        // - as fragment shaders get more and more expensive, it becomes increasingly important to reduce the number of fragment shader invocations
        // - this can be achieved by reducing pixel overdraw in a mesh, and in general, it requires the use of view-dependent algorithms
        // - however, MeshOptimizer implements heuristics to reorder the triangles and minimize overdraw from all directions!
        // - last parameter, 1.05 is the threshold that determines how much algorithm can compromise the vertex cache hit ratio
        meshopt_optimizeOverdraw(remappedIndices.data(), remappedIndices.data(), indices.size(), glm::value_ptr(remappedVertices[0]), vertexCount, sizeof(vec3), 1.05f);

        // once we have optimized the mesh to reduce pixel overdraw, the vertex buffer access pattern can still be optimized for memory efficiency
        // - the GPU has to fetch specified vertex attributes from the vertex buffer and pass this data into the vertex shader
        // - to speed up this fetch, a memory cache is used, which means optimizing the locality of vertex buffer access is very important
        // - we can use MeshOptimizer to optimize our index and vertex buffers for vertex fetch efficiency as follows
        // - this function will reorder vertices in the vertex buffer and regenerate indices to match the new contents of the vertex buffer
        meshopt_optimizeVertexFetch(remappedVertices.data(), remappedIndices.data(), indices.size(), remappedVertices.data(), vertexCount, sizeof(vec3));

        // the last thing we will do in this recipe is simpify the mesh
        // - MeshOptimizer can generate a new index buffer that uses existing vertices from the vertex buffer with a reduced number of triangles
        // - this new index buffer can be used to render 'Level-of-Detail(LOD)' meshes
        // - multiple LOD meshes can be generated this way by changing the threshold value
        const float threshold = 0.2f;
        const size_t target_index_count = size_t(remappedIndices.size() * threshold);
        const float target_error = 1e-2f;
        indicesLod.resize(remappedIndices.size());
        indicesLod.resize(meshopt_simplify(&indicesLod[0], remappedIndices.data(), remappedIndices.size(), &remappedVertices[0].x, vertexCount, sizeof(vec3), target_index_count, target_error));

        // we copy the remapped data back into the original vectors
        indices = remappedIndices;
        positions = remappedVertices;
    }

    const size_t sizeIndices = sizeof(unsigned int) * indices.size();
    const size_t sizeIndicesLod = sizeof(unsigned int) * indicesLod.size();
    const size_t sizeVertices = sizeof(vec3) * positions.size();

    // with modern OpenGL, we can store vertex and index data inside a single buffer
    glNamedBufferStorage(meshData, sizeIndices + sizeIndicesLod + sizeVertices, nullptr, GL_DYNAMIC_STORAGE_BIT);
    glNamedBufferSubData(meshData, 0, sizeIndices, indices.data());
    glNamedBufferSubData(meshData, sizeIndices, sizeIndicesLod, indicesLod.data());
    glNamedBufferSubData(meshData, sizeIndices + sizeIndicesLod, sizeVertices, positions.data());

    // we should tell OpenGL where to read the vertex and index data from
    // - the starting offset to the vertex data is 'sizeIndices + sizeIndicesLod'
    glVertexArrayElementBuffer(vao, meshData);
    glVertexArrayVertexBuffer(vao, 0, meshData, sizeIndices + sizeIndicesLod, sizeof(vec3));
    glEnableVertexArrayAttrib(vao, 0);
    glVertexArrayAttribFormat(vao, 0, 3, GL_FLOAT, GL_FALSE, 0);
    glVertexArrayAttribBinding(vao, 0, 0);

    while (!glfwWindowShouldClose(window))
    {
        int width, height;
        glfwGetFramebufferSize(window, &width, &height);
        const float ratio = width / (float)height;

        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        const mat4 m1 = glm::rotate(glm::translate(mat4(1.0f), vec3(-0.5f, -0.5f, -1.5f)), (float)glfwGetTime(), vec3(0.0f, 1.0f, 0.0f));
        const mat4 m2 = glm::rotate(glm::translate(mat4(1.0f), vec3(+0.5f, -0.5f, -1.5f)), (float)glfwGetTime(), vec3(0.0f, 1.0f, 0.0f));
        const mat4 p = glm::perspective(45.0f, ratio, 0.1f, 1000.0f);

        const MeshOptimizer::PerFrameData perFrameData1 = {p * m1};
        glNamedBufferSubData(perFrameDataBuffer, 0, kBufferSize, &perFrameData1);
        glDrawElements(GL_TRIANGLES, static_cast<unsigned>(indices.size()), GL_UNSIGNED_INT, nullptr);

        const MeshOptimizer::PerFrameData perFrameData2 = {p * m2};
        glNamedBufferSubData(perFrameDataBuffer, 0, kBufferSize, &perFrameData2);

        // to render the simplified LOD mesh, we use number of indices in LOD and use an offset to where its indices start in the index buffer
        // - we need to skip 'sizeIndices' bytes to do it
        glDrawElements(GL_TRIANGLES, static_cast<unsigned>(indicesLod.size()), GL_UNSIGNED_INT, (void *)sizeIndices);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteBuffers(1, &meshData);
    glDeleteBuffers(1, &perFrameDataBuffer);
    glDeleteProgram(program);
    glDeleteShader(shaderFragment);
    glDeleteShader(shaderVertex);
    glDeleteVertexArrays(1, &vao);

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}