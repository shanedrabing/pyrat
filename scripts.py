# LINEAR MODELING


if True and __name__ == "__main__":
    import time

    import matplotlib.pyplot as plt

    from pyrat.base import log10, match, mean, order, seq, sort, sqrt, unique
    from pyrat.stats import lm, predict
    from pyrat.utils import read_csv, struct

    start = time.time()

    df = read_csv("data/mtcars.csv")
    struct(df)

    x = df["hp"]
    y = df["mpg"]

    x_log10 = log10(x)
    y_log10 = log10(y)

    m = lm(x_log10, y_log10)
    y_fit_log10 = predict(m, x_log10)
    y_fit = 10 ** y_fit_log10

    e = sqrt(mean((y_fit - y) ** 2))
    i = order(x)

    x_new = seq(min(x), max(x), length_out=101)
    y_new_log10 = predict(m, log10(x_new))
    y_new = 10 ** y_new_log10

    end = time.time()
    print(end - start, "seconds")

    plt.scatter(x, y, color="black")
    plt.plot(x_new, y_new, color="red")
    plt.xlabel("Horsepower")
    plt.ylabel("Miles per Gallon")
    plt.tight_layout()
    plt.savefig("data/fit.png")
    plt.clf()

    end = time.time()
    print(end - start, "seconds")


# PYTHON FUNCTIONAL PROGRAMMING


if True and __name__ == "__main__":
    import time

    import bs4
    import requests

    from pyrat.base import c, paste
    from pyrat.closure import gettr, part

    start = time.time()

    wiki = "https://en.wikipedia.org/w/index.php?search={}"
    taxa = c("Canis lupus", "Felis catus", "Ursidae", "Anura (order)")

    out = (
        taxa
        .apply(wiki.format)
        .thread(requests.get)
        .apply(getattr, "content")
        .apply(bs4.BeautifulSoup, "lxml")
        .apply(bs4.BeautifulSoup.select_one, "h1")
        .apply(getattr, "text")
        .transform(paste, "(" + taxa + ")", collapse="\n")
    )

    end = time.time()

    print(out)
    print(end - start, "seconds")
