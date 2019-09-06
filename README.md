# PyOpenGL-Template

**Copyleft (Ɔ) 2019.Mauve 版权没有，翻版不究。 但请协助改进本作品。 遵循CC BY-SA知识协议授权使用。**

## 开源声明(CC BY-SA)
<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
    <img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
</a>
<br />
<span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/InteractiveResource" property="dct:title" rel="dct:type">
    PyOpenGL-Template
</span>
    由
<a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/Hukeqing/PyOpenGL-Template" property="cc:attributionName" rel="cc:attributionURL">
    Mauve
</a>
    采用
<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">
    知识共享 署名-相同方式共享 4.0 国际 许可协议
</a>
    进行许可。
<br />
    本许可协议授权之外的使用权限可以从
<a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/Hukeqing/PyOpenGL-Template/issues" rel="cc:morePermissions">
    https://github.com/Hukeqing/PyOpenGL-Template/issues
</a>
    处获得。

**协议摘要如下：**

---

### You are free to:(您可以自由地：)
> #### Share(共享)
> > copy and redistribute the material in any medium or format(在任何媒介以任何形式复制、发行本作品)
> #### Adapt(演绎)
> > remix, transform, and build upon the material(修改、转换或以本作品为基础进行创作)
>
> The licensor cannot revoke these freedoms as long as you follow the license terms.(只要你遵守许可协议条款，许可人就无法收回你的这些权利。)
### Under the following terms:(惟须遵守下列条件：)
> #### Attribution(署名)
> > You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.(您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否（对原始作品）作了修改。您可以用任何合理的方式来署名，但是不得以任何方式暗示许可人为您或您的使用背书。 )
> #### ShareAlike(相同方式共享)
> > If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.(如果您再混合、转换或者基于本作品进行创作，您必须基于与原先许可协议相同的许可协议 分发您贡献的作品。 )
> #### No additional restrictions(没有附加限制)
> > You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.(您不得使用法律术语或者技术措施从而限制其他人做许可协议允许的事情。)

---

## 仓库目录结构(2019.9.5)

<pre>
PyOpenGL-Template/
|----.gitignore
|----OpenGLEngine/
|    |----__init__.py
|    |----Built_inClass/
|    |    |----__init__.py
|    |    |----color.py
|    |    |----keycode.py
|    |    |----math_f.py
|    |    |----vector3.py
|    |----Class/
|    |    |----__init__.py
|    |    |----material.py
|    |----Component/
|    |    |----__init__.py
|    |    |----camera.py
|    |    |----component_manager.py
|    |    |----game_object.py
|    |    |----mesh_filter.py
|    |    |----mesh_renderer.py
|    |    |----transform.py
|    |    |----window.py
|    |----DefaultModel/
|    |    |----__init__.py
|    |    |----create.py
|    |    |----GLSL.py
|    |----Demo/
|    |    |----__init__.py
|    |    |----SourceCode.py
|    |----Test/
|    |    |----__init__.py
|    |    |----DefaultModelTest.py
|----README.md
|----requirements.txt
|----unit_test.py
</pre>

## 渲染逻辑

```
Run Window.window_main_loop()
 + Window
 - set base variables
 - while Window not close:
   - Call Window.draw()
     - set delta_time
     - Call Update()
     - Call Window.render_function()(Default)
     - Call GameObject.draw() in Window.game_object_list
```

## 使用指南(暂略)
