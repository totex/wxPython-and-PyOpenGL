import wx
from wx import glcanvas
from OpenGL.GL import *
import OpenGL.GL.shaders
from pyrr import Matrix44, matrix44, Vector3
import time, sys
from Geometries import Geometries

vertex_shader = """
# version 330
in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;
uniform mat4 rotate;
uniform mat4 translate;
uniform mat4 vp;

void main(){
    gl_Position = vp * translate * rotate * vec4(positions, 1.0);
    newColor = colors;
}
"""

fragment_shader = """
# version 330
in vec3 newColor;
out vec4 outColor;

void main(){
    outColor = vec4(newColor, 1.0);
}
"""


class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        self.size = (1120, 630)
        self.aspect_ratio = self.size[0] / self.size[1]
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.size)
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        self.init = False
        self.rotate = False
        self.rot_y = Matrix44.identity()
        self.mesh = None
        self.show_triangle = False
        self.show_quad = False
        self.show_cube = False
        self.rot_loc = None
        self.trans_loc = None
        self.trans_x, self.trans_y, self.trans_z = 0.0, 0.0, 0.0
        self.translate = Matrix44.identity()
        self.bg_color = False
        self.wireframe = False
        self.combined_matrix = Matrix44.identity()

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, event):
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def InitGL(self):

        self.mesh = Geometries()

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                  OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

        view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
        projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)

        vp = matrix44.multiply(view, projection)

        glUseProgram(shader)
        glEnable(GL_DEPTH_TEST)

        vp_loc = glGetUniformLocation(shader, "vp")
        glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)

        self.rot_loc = glGetUniformLocation(shader, "rotate")
        self.trans_loc = glGetUniformLocation(shader, "translate")

    def OnDraw(self):

        if self.bg_color:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        else:
            glClearColor(0.1, 0.15, 0.1, 1.0)

        if self.wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.translate = matrix44.create_from_translation(Vector3([self.trans_x, self.trans_y, self.trans_z]))

        self.combined_matrix = matrix44.multiply(self.rot_y, self.translate)

        if self.rotate:
            ct = time.clock()
            self.rot_y = Matrix44.from_y_rotation(ct)
            glUniformMatrix4fv(self.rot_loc, 1, GL_FALSE, self.rot_y)
            glUniformMatrix4fv(self.trans_loc, 1, GL_FALSE, self.translate)
            self.Refresh()
        else:
            glUniformMatrix4fv(self.rot_loc, 1, GL_FALSE, self.rot_y)
            glUniformMatrix4fv(self.trans_loc, 1, GL_FALSE, self.translate)

        if self.show_triangle:
            self.mesh.bind_triangle()
            glDrawArrays(GL_TRIANGLES, 0, self.mesh.tv_count)
        elif self.show_quad:
            self.mesh.bind_quad()
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.mesh.qv_count)
        elif self.show_cube:
            self.mesh.bind_cube()
            glDrawElements(GL_TRIANGLES, self.mesh.ci_count, GL_UNSIGNED_INT, None)

        self.SwapBuffers()


class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("#626D58")

        # all the widgets
        # the OpenGL canvas
        self.canvas = OpenGLCanvas(self)

        # the Start/Stop rotation button
        self.rot_btn = wx.Button(self, -1, label="Start/Stop \nrotation", pos=(1130, 10), size=(100, 50))
        self.rot_btn.BackgroundColour = [125, 125, 125]
        self.rot_btn.ForegroundColour = [255, 255, 255]

        # the radio buttons to switch between the 3D objects
        self.rad_btn1 = wx.RadioButton(self, -1, label="Show Triangle", pos=(1130, 80))
        self.rad_btn2 = wx.RadioButton(self, -1, label="Show Quad", pos=(1130, 100))
        self.rad_btn3 = wx.RadioButton(self, -1, label="Show Cube", pos=(1130, 120))

        # the translation sliders
        self.x_slider = wx.Slider(self, -1, pos=(1130, 180), size=(40, 150), style=wx.SL_VERTICAL|wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)
        self.y_slider = wx.Slider(self, -1, pos=(1170, 180), size=(40, 150), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)
        self.z_slider = wx.Slider(self, -1, pos=(1210, 180), size=(40, 150), style=wx.SL_VERTICAL | wx.SL_AUTOTICKS,
                                  value=0, minValue=-5, maxValue=5)

        # the slider labels using static texts
        font = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.x_slider_label = wx.StaticText(self, -1, label="X", pos=(1137, 160))
        self.x_slider_label.SetFont(font)
        self.y_slider_label = wx.StaticText(self, -1, label="Y", pos=(1177, 160))
        self.y_slider_label.SetFont(font)
        self.z_slider_label = wx.StaticText(self, -1, label="Z", pos=(1217, 160))
        self.z_slider_label.SetFont(font)

        # the checkboxes to set background color and the wireframe rendering
        self.bg_color = wx.CheckBox(self, -1, pos=(1130, 360), label="Black background")
        self.wireframe = wx.CheckBox(self, -1, pos=(1130, 390), label="Wireframe mode")

        # text control to display the translation matrix and the rotation matrix combined
        self.log_text = wx.TextCtrl(self, -1, size=(1120, 110), pos=(0, 630), style=wx.TE_MULTILINE)
        self.log_text.BackgroundColour = [70, 125, 70]
        self.log_text.SetFont(font)
        self.log_text.AppendText(str(self.canvas.combined_matrix.T))

        # identity button, resets the matrices to identity
        self.identity_btn = wx.Button(self, -1, label="Set identity \nmatrix", pos=(1130, 630), size=(100, 50))
        self.identity_btn.BackgroundColour = [125, 125, 125]
        self.identity_btn.ForegroundColour = [255, 255, 255]

        # all the event bindings
        self.Bind(wx.EVT_BUTTON, self.rotate, self.rot_btn)
        self.Bind(wx.EVT_RADIOBUTTON, self.triangle, self.rad_btn1)
        self.Bind(wx.EVT_RADIOBUTTON, self.quad, self.rad_btn2)
        self.Bind(wx.EVT_RADIOBUTTON, self.cube, self.rad_btn3)
        self.Bind(wx.EVT_SLIDER, self.translate)
        self.Bind(wx.EVT_CHECKBOX, self.change_bg_color, self.bg_color)
        self.Bind(wx.EVT_CHECKBOX, self.set_wireframe, self.wireframe)
        self.Bind(wx.EVT_BUTTON, self.set_identity, self.identity_btn)

    # all the methods

    # sets the identity matrix, stops the rotation and resets the sliders to zero
    def set_identity(self, event):
        self.canvas.combined_matrix = Matrix44.identity()
        self.canvas.rotate = False
        self.canvas.trans_x, self.canvas.trans_y, self.canvas.trans_z = 0, 0, 0
        self.canvas.rot_y = Matrix44.identity()
        self.x_slider.SetValue(0)
        self.y_slider.SetValue(0)
        self.z_slider.SetValue(0)
        self.log_matrix()
        self.canvas.Refresh()

    # displays the combined matrix on the text control area
    def log_matrix(self):
        self.log_text.Clear()
        self.log_text.AppendText(str(self.canvas.combined_matrix.T))

    # sets the wireframe mode
    def set_wireframe(self, event):
        self.canvas.wireframe = self.wireframe.GetValue()
        self.canvas.Refresh()

    # changes the clear color to black
    def change_bg_color(self, event):
        self.canvas.bg_color = self.bg_color.GetValue()
        self.canvas.Refresh()

    # this method translates the 3D objects
    def translate(self, event):
        self.canvas.trans_x = self.x_slider.GetValue() * -0.2
        self.canvas.trans_y = self.y_slider.GetValue() * -0.2
        self.canvas.trans_z = self.z_slider.GetValue() * 0.5
        self.log_matrix()
        self.canvas.Refresh()

    # this method shows the triangle
    def triangle(self, event):
        self.canvas.show_triangle = True
        self.canvas.show_quad = False
        self.canvas.show_cube = False
        self.canvas.Refresh()

    # this method shows the quad
    def quad(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = True
        self.canvas.show_cube = False
        self.canvas.Refresh()

    # this method shows the cube
    def cube(self, event):
        self.canvas.show_triangle = False
        self.canvas.show_quad = False
        self.canvas.show_cube = True
        self.canvas.Refresh()

    # this method rotates the 3D objects
    def rotate(self, event):
        if not self.canvas.rotate:
            self.canvas.rotate = True
            self.canvas.Refresh()
        else:
            self.canvas.rotate = False


class MyFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 780)
        wx.Frame.__init__(self, None, title="My wx frame", size=self.size,
                          style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        self.SetMinSize(self.size)
        self.SetMaxSize(self.size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.panel = MyPanel(self)

    def on_close(self, event):
        self.Destroy()
        sys.exit(0)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()





