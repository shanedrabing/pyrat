# PyRat

R-like vectors and functions in Python.

## Warning

This is not Pandas, or scikit-learn, or numpy. This is not R, either. Do not
use this for industry purposes. Do not use this unless you want your project to
break.

Simply have fun with it, or use this for educational purposes.

## Installation

Clone this repository to your local machine with git, then install with Python.

```bash
git clone https://github.com/shanedrabing/pyrat.git
cd pyrat
python setup.py install
```

## Getting Started

Import the libraries with Python.

```python
import pyrat.base
import pyrat.stats
import pyrat.utils
import pyrat.closure
```

The closure library is the only not inspired by R. All other libraries contain
familiar functions. If you want to locate a function within R, look into the
`find` function, determine the namespace, and see if PyRat contains the
function!

## Motivating Examples

So, why use PyRat? If you're a fan of R (like myself), you may have learned
that the capabilities of vectors and functions that operate on them are
immensely powerful.

### Linear Modeling

Let's try modeling a line of best fit between horsepower and miles per gallon
from the `mtcars` dataset:

```python
import matplotlib.pyplot as plt

from pyrat.base import log10, seq
from pyrat.stats import lm, predict
from pyrat.utils import read_csv, struct

df = read_csv("data/mtcars.csv")

x = df["hp"]
y = df["mpg"]

m = lm(log10(x), log10(y))

x_new = seq(min(x), max(x), length_out=101)
y_new = 10 ** predict(m, log10(x_new))

plt.scatter(x, y, color="black")
plt.plot(x_new, y_new, color="red")
plt.xlabel("Horsepower")
plt.ylabel("Miles per Gallon")
plt.tight_layout()
plt.savefig("data/fit.png")
plt.clf()
```

A plot of the fitted linear model:

![data/fit.png](data/fit.png)

### Functional Programming

PyRat has its own version of "piping", whereby the items of a `vector` (or the
`vector` itself) can be continuously operated on. All intermediates are
immutable, as the `vector` is just a `tuple` on steroids.

```python
from pyrat.base import c, paste

taxa = c("Canis lupus", "Felis catus", "Ursidae", "Anura (order)")

print(
    taxa
    .apply("https://en.wikipedia.org/w/index.php?search={}".format)
    .thread(requests.get)
    .apply(getattr, "content")
    .apply(bs4.BeautifulSoup, "lxml")
    .apply(bs4.BeautifulSoup.select_one, "h1")
    .apply(getattr, "text")
    .transform(paste, "(" + taxa + ")", collapse="\n")
)
```

Here's the output:

```txt
Wolf (Canis lupus)
Cat (Felis catus)
Bear (Ursidae)
Frog (Anura (order))
```
