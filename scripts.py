# LINEAR MODELING


if False and __name__ == "__main__":
    import time

    import matplotlib.pyplot as plt

    from pyrat.base import log10, seq
    from pyrat.stats import lm, predict
    from pyrat.utils import read_csv, struct

    start = time.time()

    df = read_csv("data/mtcars.csv")
    struct(df)

    x = df["hp"]
    y = df["mpg"]

    m = lm(log10(x), log10(y))
    print(m)

    x_new = seq(min(x), max(x), length_out=101)
    y_new = 10 ** predict(m, log10(x_new))

    plt.scatter(x, y, color="black")
    plt.plot(x_new, y_new, color="red")
    plt.xlabel("Horsepower")
    plt.ylabel("Miles per Gallon")
    plt.tight_layout()
    plt.savefig("data/fit.png")
    plt.clf()

    end = time.time()
    print(end - start, "seconds")


# DATA MANIPULATION


if False and __name__ == "__main__":
    import time

    from pyrat.base import order
    from pyrat.stats import lm, predict
    from pyrat.utils import read_csv, write_csv

    start = time.time()

    df = read_csv("data/mtcars.csv")

    i = order(df["hp"])
    b = df["cyl"] == 4
    df = {k: v[i][b[i]] for k, v in df.items()}

    write_csv(df, "data/mtcars_alt.csv")

    end = time.time()
    print(end - start, "seconds")


# PYTHON FUNCTIONAL PROGRAMMING


if False and __name__ == "__main__":
    import time

    import bs4
    import requests

    from pyrat.base import c, paste

    start = time.time()

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

    end = time.time()
    print(end - start, "seconds")


# NUCLEOTIDE COUNT


if True and __name__ == "__main__":
    from pyrat.base import vector


    def count_nucleotides(strand):
        bases = vector("ACGT")
        if set(strand) - set(bases):
            return
        return dict(zip(bases, bases.apply(strand.count)))


    print(count_nucleotides("GATTACA"))
    assert count_nucleotides("GATTACA") == {"A": 3, "C": 1, "G": 1, "T": 2}
    assert count_nucleotides("INVALID") == None
