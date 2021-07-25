# LINEAR MODELING


if False and __name__ == "__main__":
    import math

    import matplotlib.pyplot as plt

    from pyrat.base import match, order, seq, sort, unique
    from pyrat.stats import lm, predict, rmse
    from pyrat.utils import read_csv, struct

    df = read_csv("data/mtcars.csv")
    struct(df)

    x = df["hp"]
    y = df["mpg"]

    x_log10 = x.apply(math.log10)
    y_log10 = y.apply(math.log10)

    m = lm(x_log10, y_log10)
    y_fit_log10 = predict(m, x_log10)
    y_fit = 10 ** y_fit_log10

    e = rmse(y, y_fit)
    i = order(x)

    x_new = seq(min(x), max(x), length_out=101)
    y_new_log10 = predict(m, x_new.apply(math.log10))
    y_new = 10 ** y_new_log10

    plt.scatter(x, y, color="black")
    plt.plot(x_new, y_new, color="red")
    plt.xlabel("Horsepower")
    plt.ylabel("Miles per Gallon")
    plt.tight_layout()
    # plt.savefig("data/lm.png")
    plt.show()
    plt.clf()


# PYTHON FUNCTIONAL PROGRAMMING


if True and __name__ == "__main__":
    import bs4
    import time
    import requests

    from pyrat.base import c, paste
    from pyrat.closure import gettr, part

    wiki = "https://en.wikipedia.org/w/index.php?search={}"
    taxa = c("Canis lupus", "Felis catus", "Ursidae", "Anura (order)")

    start = time.time()

    common = (
        taxa
        .apply(wiki.format)
        .thread(requests.get)
        .apply(gettr("content"))
        .apply(part(bs4.BeautifulSoup, "lxml"))
        .apply(part(bs4.BeautifulSoup.select_one, "h1"))
        .apply(gettr("text"))
    )
    
    full = paste(common, "(" + taxa + ")", collapse="\n")
    end = time.time()
    
    print(full)
    print(end - start, "seconds")
