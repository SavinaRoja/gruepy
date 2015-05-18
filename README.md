# gruepy
A toolkit for creating terminal user interfaces. Meant to be robust, efficient, and modern.

Creating terminal displays or user interfaces can be a hassle, especially when your goals become more intricate/complex: [`npyscreen`](https://code.google.com/p/npyscreen/) is an excellent, well-established, library that does much to address this issue (it particularly excels at form-driven design) that I recommend. In developing 'gruepy' I hope to explore how to create a more modern TUI (Terminal UI) framework.

One of the central distinguishing aims of this project is the incorporation of asynchronous design. Asynchronicity should be an aspect of application design which may be ignored by those who don't need it while easily accessible by those who do. For this reason, `gruepy` will really only be compatible with Python 3.4 and up (the introduction of `asyncio`), though I would anticipate it could be backported to lesser versions of Python3 with external asynchronous libs.

In addition to asynchronicity, I hope to utilize some of the design aspects I developed in [`npyscreen2`](https://github.com/SavinaRoja/npyscreen2) (an experimental restructuring of `npyscreen`, now on hiatus) regarding Widgets/Containers. In truth, I am simply interpreting design concepts analogous to those in GUIs and web design for the terminal context.

## Contributing?
If this sort of thing interests you, please get in touch.
