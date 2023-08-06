# jupyterlab-mathjax3-web

A JupyterLab extension for rendering math with MathJax **3**.

The default LaTeX renderer in JupyterLab uses MathJax **2**. This extension substitutes the MathJax 2 renderer with the MathJax 3 renderer. 

Compared to the official [jupyterlab-mathjax3](https://github.com/jupyterlab/jupyter-renderers/tree/master/packages/mathjax3-extension) which introduces the MathJax 3 into JupyterLab via **node** and **webpack**, this extension exposes MathJax 3 to the browser's global environment by loading script from the **web**, so that MathJax 3 can be used by other entities in JupyterLab like our [jsxgraph-magic](https://github.com/chunxy/jsxgraph-magic.git).

## Requirements

- JupyterLab >= 3.0

Also note that his JupyterLab extension will disable the official MathJax 2 and MathJax 3 extension to avoid potential conflict.

## Installation

To install the extension, execute:

```shell
pip install jupyterlab-mathjax3-web
```

## Configuration

Our MathJax 3 extension enables partial customization on MathJax 3, which is [configured via a global JavaScript object](https://docs.mathjax.org/en/latest/web/configuration.html#web-configuration). We can customize it in a [JSON](https://en.wikipedia.org/wiki/JSON) file and load this configuration every time we open the JupyterLab.

Out of the many configurable options, `tex` is the most useful and applicable one to be accessed by users. It controls 

- math delimiters, 
- macros, 
- tagging, 
- packages, 
- etc. 

We decide to **only** make `tex` configuration available in our JupyterLab extension.

For a full list configurable options under `tex`, please refer to [MathJax's webpage](https://docs.mathjax.org/en/latest/options/input/tex.html).

#### Where to configure

To configure your `tex` options, open **Setting -> MathJax 3 Config...** This will open the **Advanced Settings** page of JupyterLab. There you will find a **MathJax 3 Config** entry. The **System Defaults** JSON file will be

```json5
{
    "displayMath": [
        [
            "$$",
            "$$"
        ],
        [
            "\\[",
            "\\]"
        ]
    ],

    "inlineMath": [
        [
            "$",
            "$"
        ],
        [
            "\\(",
            "\\)"
        ]
    ],

    "processEnvironments": true,

    "processEscapes": true
}
```

You may edit with the **User Preferences** JSON file according to [MathJax's `tex` schema](https://docs.mathjax.org/en/latest/options/input/tex.html) to override the default options. Only options with the same key in System Defaults and User Preferences will be overridden.

As an example, you can add macros and tagging with

```json5
{
    "macros": {
        R: "\\mathbb{R}", 
        E: "\\mathrm{E}", 
        RR: "{\\bf R}",
        bold: ["{\\bf #1}",1]
    },
    "tags": "all"
}
```

Remember to **save the setting** and **refresh the page** to let change take effect.

#### Tex/LaTeX extensions

MathJax has [many extensions](http://docs.mathjax.org/en/latest/input/tex/extensions/index.html) [to replicate the TeX/LaTeX experience](http://docs.mathjax.org/en/latest/input/tex/extensions.html). For an extension to work, it has to be firstly loaded into the webpage, and then included in `packages` option under `tex`. Our MathJax component already loads and includes [many useful extensions](http://docs.mathjax.org/en/latest/web/components/combined.html#tex-chtml) like `ams`,  `autoload` and `require`.

----

As of version 0.1.1, all official MathJax extensions are loaded and included by default. So in most cases, you don't have to bother with below. Just use the commands as you like.

---

##### Use extensions via `autoload`

Extension loading is configured in MathJax's `loader` option and is thus not configurable in our setting. Luckily, the [`autoload` extension](http://docs.mathjax.org/en/latest/input/tex/extensions/autoload.html), which will automatically loads and includes many other extensions. So you don't really have to worry about extensions other than `physics` ~~and `ams`~~.

Using `autoload` is effortless. To use other extensions, you just use them! For example, you may try `\enclose` and `\color` command defined in [`enclose`](http://docs.mathjax.org/en/latest/input/tex/extensions/enclose.html) and [`color`](http://docs.mathjax.org/en/latest/input/tex/extensions/color.html) extension respectively:

```markdown
$\enclose{circle}{\enclose{box}{\color{red}{x}}}$
```

`autoload` will detect and automates everything for us. 

##### Use extensions via `require`

The [`require` extension](http://docs.mathjax.org/en/latest/input/tex/extensions/require.html) can also help load and include extensions like `physics`. You first use the `\require` command to specify the extension and then use the extension commands:

```markdown
$\require{physics} \dv{f}{x}$
```

##### Caution

Do not try to include any extension via the `tex` configuration. Instead just use the commands or load-and-include via `\require`.

```json5
{
    // wrong!
    "packages": {"[+]": ["enclose", "color"]}
}
```

Such explicit including and corresponding commands won't be handled by `autoload`. It will make MathJax include extensions that are loaded with the `loader` option. However as said, we don't provide the `loader` option configuration. So finally these extensions cannot be successfully used.

## Contributing

### Development-install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of [yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use `yarn` or `npm` in lieu of `jlpm` below.

```shell
# Clone the repo to your local environment
# Change directory to the jupyterlab-mathjax3-web directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm run build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```shell
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```shell
jupyter lab build --minimize=False
```

### Development-uninstall

```shell
pip uninstall jupyterlab-mathjax3-web
```

Then you need to manually remove the `labextension` because it seems that the above won't remove these JupyterLab files:

```shell
cd PYTHON_ENV/share/jupyter/labextensions
rm jupyterlab-mathjax3-web -rf
```

where `PYTHON_ENV` should be expanded to your Python environment.
