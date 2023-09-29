import random


algorithms = [
    'ackermann', 'bubblesort', 'countingsort', 'fibonacci',
    'gnomesort', 'happynumbers', 'heapsort', 'insertionsort',
    'humblenumbers', 'kmeanspp', 'matrixmultiplication',
    'mergesort', 'nqueens', 'pancakesort', 'perfectnumbers',
    'quicksort', 'seqnonsquares', 'shellsort', 'towersofhanoi'
]


def get_url(language='js', algorithm='bubblesort', measurement='runtime'):
    return "https://wasm-energy-experiment.netlify.app/{}/{}/{}.html".format(language, algorithm, measurement)


def get_settings(browsers, languages, algorithms, measurement):
    s = []

    for browser in browsers:
        for language in languages:
            for algorithm in algorithms:
                s.append((browser, language, algorithm, get_url(language, algorithm, measurement)))

    return s


def get_randomized_settings(browsers, languages, algorithms, measurement):
    s = get_settings(browsers, languages, algorithms, measurement)
    random.shuffle(s)
    return s
