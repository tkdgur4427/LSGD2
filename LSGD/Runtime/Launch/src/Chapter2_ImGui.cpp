#include <glad/gl.h>
#include <GLFW/glfw3.h>
#include <imgui.h>
#include <glm/glm.hpp>
#include <glm/ext.hpp>

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include "Chapters.h"

// imgui wrapper
#if defined(_MSC_VER)
#pragma warning(push)
#pragma warning(disable : 4099) // type name first seen using 'class' now seen using 'struct'
#pragma warning(disable : 4244) // 'argument': conversion from 'float' to 'int', possible loss of data
#pragma warning(disable : 4267) // conversion from 'size_t' to 'int', possible loss of data
#pragma warning(disable : 4305) // 'argument': truncation from 'double' to 'float'
#endif

#define NOMINMAX

#include "imgui.cpp"
#include "imgui_demo.cpp"
#include "imgui_draw.cpp"
#include "imgui_tables.cpp"
#include "imgui_widgets.cpp"

#if defined(_MSC_VER)
#pragma warning(pop)
#endif // _MSC_VER

using glm::mat4;

int Chapter2::ImGui_main()
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

    GLFWwindow *window = glfwCreateWindow(1280, 720, "simple example", nullptr, nullptr);
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

    glfwSetCursorPosCallback(
        window,
        [](auto *window, double x, double y)
        {
            // install a cursor position callbck for ImGui
            (void)window;
            ImGui::GetIO().MousePos = ImVec2((float)x, (float)y);
        });

    glfwSetMouseButtonCallback(
        window,
        [](auto *window, int button, int action, int mods)
        {
            (void)mods;
            (void)window;

            // bring our UI to life is to set the mouse button callback and route the mouse button events into ImGui
            auto &io = ImGui::GetIO();
            const int idx = button == GLFW_MOUSE_BUTTON_LEFT ? 0 : button == GLFW_MOUSE_BUTTON_RIGHT ? 2
                                                                                                     : 1;
            io.MouseDown[idx] = action == GLFW_PRESS;
        });

    glfwMakeContextCurrent(window);
    gladLoadGL(glfwGetProcAddress);
    glfwSwapInterval(1);

    // to render geometry data coming from ImGui, we need a VAO with vertex and index buffers
    // * we will use an upper limit of 256 kilobytes for the indices and vertices data
    GLuint vao;
    glCreateVertexArrays(1, &vao);

    GLuint handleVBO;
    glCreateBuffers(1, &handleVBO);
    glNamedBufferStorage(handleVBO, 128 * 1024, nullptr, GL_DYNAMIC_STORAGE_BIT);

    GLuint handleElements;
    glCreateBuffers(1, &handleElements);
    glNamedBufferStorage(handleElements, 256 * 1024, nullptr, GL_DYNAMIC_STORAGE_BIT);

    // the geometry data consist of 2D vertex positions, texture coordinates and RGBA colors, so we should configure the vertex attributes as follows:
    /**
     * struct ImDrawVert {
     *  ImVec2 pos;
     *  ImVec2 uv;
     *  ImU32 col;
     * };
     */
    glVertexArrayElementBuffer(vao, handleElements);
    glVertexArrayVertexBuffer(vao, 0, handleVBO, 0, sizeof(ImDrawVert));

    glEnableVertexArrayAttrib(vao, 0);
    glEnableVertexArrayAttrib(vao, 1);
    glEnableVertexArrayAttrib(vao, 2);

    // vertex attributes corresponding to the positions, texture coordinates, and colors are stored in an interleaved format
    glVertexArrayAttribFormat(vao, 0, 2, GL_FLOAT, GL_FALSE, IM_OFFSETOF(ImDrawVert, pos));
    glVertexArrayAttribFormat(vao, 1, 2, GL_FLOAT, GL_FALSE, IM_OFFSETOF(ImDrawVert, uv));
    glVertexArrayAttribFormat(vao, 2, 4, GL_UNSIGNED_BYTE, GL_TRUE, IM_OFFSETOF(ImDrawVert, col));

    // the final touch to the VAO is to tell OpenGL that every vertex stream should be read from the same buffer bound to the binding point with an index of 0
    glVertexArrayAttribBinding(vao, 0, 0);
    glVertexArrayAttribBinding(vao, 1, 0);
    glVertexArrayAttribBinding(vao, 2, 0);

    glBindVertexArray(vao);

    const GLchar *shaderCodeVertex = R"(
        #version 460 core
        layout(location=0) in vec2 Position;
        layout(location=1) in vec2 UV;
        layout(location=2) in vec4 Color;
        layout(std140, binding=0) uniform PerFrameData
        {
            uniform mat4 MVP;
        };
        out vec2 Frag_UV;
        out vec4 Frag_Color;
        void main()
        {
            Frag_UV = UV;
            Frag_Color = Color;
            gl_Position = MVP * vec4(Position.xy, 0, 1);
        }
    )";

    const GLchar *shaderCodeFragment = R"(
        #version 460 core
        in vec2 Frag_UV;
        in vec4 Frag_Color;
        layout(binding=0) uniform sampler2D Texture;
        layout(location=0) out vec4 Out_Color;
        void main()
        {
            Out_Color = Frag_Color * texture(Texture, Frag_UV.st);
        }
    )";

    const GLuint handleVertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(handleVertex, 1, &shaderCodeVertex, nullptr);
    glCompileShader(handleVertex);

    const GLuint handleFragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(handleFragment, 1, &shaderCodeFragment, nullptr);
    glCompileShader(handleFragment);

    const GLuint program = glCreateProgram();
    glAttachShader(program, handleVertex);
    glAttachShader(program, handleFragment);
    glLinkProgram(program);
    glUseProgram(program);

    GLuint perFrameDataBuffer;
    glCreateBuffers(1, &perFrameDataBuffer);
    glNamedBufferStorage(perFrameDataBuffer, sizeof(mat4), nullptr, GL_DYNAMIC_STORAGE_BIT);
    glBindBufferBase(GL_UNIFORM_BUFFER, 0, perFrameDataBuffer);

    // set up the data structures that are needed to sustain an ImGui context
    ImGui::CreateContext();

    // since we are using glDrawElementBaseVertex() for rendering, which has a vertex offset parameter of baseVertex,
    // we can tell ImGui to output meshes with more than 65535 vertices that can be indexed with 16-bit indices
    // * this is generally good for performance, as it allows you to render the UI with fewer buffer updates
    ImGuiIO &io = ImGui::GetIO();
    io.BackendFlags |= ImGuiBackendFlags_RendererHasVtxOffset;

    // build texture atlas for font rendering with .tff font file
    ImFontConfig cfg = ImFontConfig();
    // * tell ImGui that we are going to manage the memory ourselves
    cfg.FontDataOwnedByAtlas = false;
    // brighten up the font a little bit (the default value is 1.0f)
    // * brightening up small fonts is good trick to make them more readable
    cfg.RasterizerMultiply = 1.0f; // 1.5f;
    // calculate the pixel height of the font;
    // * we take our default window height of 768 and divide it by the desired number of text lines to be fit in the window
    cfg.SizePixels = 768.0f / 32.0f;
    // align every glyph to the pixel boundary and rasterize them at a higher quality for sub-pixel positioning
    // * this will improve the appearance of the text on the screen
    cfg.PixelSnapH = true;
    cfg.OversampleH = 4;
    cfg.OversampleV = 4;

    // load a .tff font from a file
    ImFont *Font = io.Fonts->AddFontFromFileTTF("Data/OpenSans-Light.ttf", cfg.SizePixels, &cfg);

    // let's take the font atlas bitmap data from ImGui in 32-bit RGBA format and upload it to OpenGL
    unsigned char *pixels = nullptr;
    int width, height;
    io.Fonts->GetTexDataAsRGBA32(&pixels, &width, &height);

    // texture creation
    GLuint texture;
    glCreateTextures(GL_TEXTURE_2D, 1, &texture);
    glTextureParameteri(texture, GL_TEXTURE_MAX_LEVEL, 0);
    glTextureParameteri(texture, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTextureParameteri(texture, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTextureStorage2D(texture, 1, GL_RGBA8, width, height);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glTextureSubImage2D(texture, 0, 0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
    glBindTextures(0, 1, &texture);

    // scanlines in the ImGui bitmap are not padded; disable the pixel unpack alignment in OpenGL by setting its value to 1 byte to handle this correctly
    io.Fonts->TexID = (ImTextureID)(intptr_t)texture;
    io.FontDefault = Font;
    io.DisplayFramebufferScale = ImVec2(1, 1);

    // we are ready to proceed with the OpenGL state setup for rendering
    // * All ImGui graphics should be rendered with blending and the scissor test turned on and the depth test and backface culling disabled
    glEnable(GL_BLEND);
    glBlendEquation(GL_FUNC_ADD);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glDisable(GL_CULL_FACE);
    glDisable(GL_DEPTH_TEST);
    glEnable(GL_SCISSOR_TEST);
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f);

    while (!glfwWindowShouldClose(window))
    {
        glfwGetFramebufferSize(window, &width, &height);

        glViewport(0, 0, width, height);
        glClear(GL_COLOR_BUFFER_BIT);

        // start a new frame
        // * ShadowDemoWindow() is test demo
        io = ImGui::GetIO();
        io.DisplaySize = ImVec2((float)width, (float)height);
        ImGui::NewFrame();
        ImGui::ShowDemoWindow();
        ImGui::Render();

        // the geometry data is generated in the ImGui::Render() function and can be retrieved via ImGui::GetDrawData()
        const ImDrawData *draw_data = ImGui::GetDrawData();

        // construct a proper orthographic projection matrix based on the left, right, top, and bottom clipping planes provided by ImGui
        const float L = draw_data->DisplayPos.x;
        const float R = draw_data->DisplayPos.x + draw_data->DisplaySize.x;
        const float T = draw_data->DisplayPos.y;
        const float B = draw_data->DisplayPos.y + draw_data->DisplaySize.y;
        const mat4 orthoProjection = glm::ortho(L, R, B, T);

        glNamedBufferSubData(perFrameDataBuffer, 0, sizeof(mat4), glm::value_ptr(orthoProjection));

        // need to go through all of the ImGui command lists, update the content of the index and vertex buffers, and invoke the rendering commands
        for (int n = 0; n < draw_data->CmdListsCount; n++)
        {
            // each ImGui command list has vertex and index data associated with it; use this data to update the appropriate OpenGL buffers
            const ImDrawList *cmd_list = draw_data->CmdLists[n];
            glNamedBufferSubData(handleVBO, 0, (GLsizeiptr)cmd_list->VtxBuffer.Size * sizeof(ImDrawVert), cmd_list->VtxBuffer.Data);
            glNamedBufferSubData(handleElements, 0, (GLsizeiptr)cmd_list->IdxBuffer.Size * sizeof(ImDrawIdx), cmd_list->IdxBuffer.Data);

            // rendering commands stored inside the command buffer
            // * iterate over them and render the actual geometry
            for (int cmd_i = 0; cmd_i < cmd_list->CmdBuffer.Size; cmd_i++)
            {
                const ImDrawCmd *pcmd = &cmd_list->CmdBuffer[cmd_i];
                const ImVec4 cr = pcmd->ClipRect;
                glScissor((int)cr.x, (int)(height - cr.w), (int)(cr.z - cr.x), (int)(cr.w - cr.y));
                glBindTextureUnit(0, (GLuint)(intptr_t)pcmd->TextureId);
                glDrawElementsBaseVertex(GL_TRIANGLES, (GLsizei)pcmd->ElemCount, GL_UNSIGNED_SHORT,
                                         (void *)(intptr_t)(pcmd->IdxOffset * sizeof(ImDrawIdx)), (GLint)pcmd->VtxOffset);
            }
        }

        // after the UI rendering is complete, reset the scissor rectangle and do the usual GLFW stuff to swap the buffers and poll user events
        glScissor(0, 0, width, height);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // clear the ImGui resources
    ImGui::DestroyContext();

    glfwDestroyWindow(window);

    glfwTerminate();
    exit(EXIT_SUCCESS);
}