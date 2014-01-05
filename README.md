Slava's PeliBlog
===

This is an instance of `pelican` blog with a theme that looks like an old svbtle
blog. It is kinda responsive, has code-highlighting and Latex support (MathJax)
and a couple of bugs.

To add new blog post
---

Create a `.md` file in `/content/`. Run `make html`.

To publish everything
---

Run `make github`. It will generate a static site, commit everything to
`gh-pages` branch and push.

Get dev environment up
---

You would need `python-2.7`, `virtualenv` and a couple of pip requirements:

```
pip install pelican markdown ghp-import
```

Also you might need the `less` compiler: `npm install -g less` will do it.

To customize
---

Edit the configuration `.py` files, replace `pelican-svbtle/static/images/logo.png`,
you can also change the `@accent` color in `pelican-svbtle/static/css/style.less`.

Don't forget to remove the hack of `CNAME` file in `Makefile`'s `html` section.

