
import sys
import difflib
import imp

# Colored diff lines - "pip install colorama" for colored output
try:
    from colorama import Fore, Back, Style, init
    init()
except ImportError:  # fallback so that the imported classes always exist
    class ColorFallback():
        __getattr__ = lambda self, name: ''
    Fore = Back = Style = ColorFallback()


def color_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith('^'):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line

try:
    parser_fn, scraper_fn = sys.argv[1], sys.argv[2]
    parser_mod = imp.load_source("parser", parser_fn)
    scraper_mod = imp.load_source("scraper", scraper_fn)

    parse_nwodkram = parser_mod.parse_nwodkram
    find_emails = scraper_mod.find_emails
    find_hyperlinks = scraper_mod.find_hyperlinks
except (IndexError, ImportError) as e:
    import IPython; IPython.embed()
    print(
        "Usage: run_tests.py PARSER.PY_FN SCRAPER.PY_FN\n"
        "where parser.py implements 'parse_nwodkram'\n"
        "and scraper.py implements 'find_emails' and 'find_hyperlinks'"
    )
    sys.exit(1)

diffs = []

test_suite = [
        ("nwodkram/sample.in", parse_nwodkram),
        ("scraping/mail.html", find_emails),
        ("scraping/hyperlinks.html", find_hyperlinks)
]

N_passed = 0
for test_input_fn, function in test_suite:
    expected_output_fn = ".".join(test_input_fn.split(".")[:-1]) + ".out"

    with open(test_input_fn) as f:
        test_input = "".join(f.readlines())
    with open(expected_output_fn) as f:
        expected_output = "".join(f.readlines())

    actual_output = function(test_input)

    if type(actual_output) is list:  # convert lists of mails/hyperlinks to text
        actual_output = "\n".join(actual_output)

    if expected_output != actual_output:
        print(
            "On {}, expected output was\n{}\n and actual output was\n{}".format(
                test_input_fn, expected_output, actual_output
            )
        )

        # DIFFLINES FOR EASY DEBUG
        print(Back.WHITE + Fore.BLACK + '***** START DEBUG DIFFLINES *****' + Fore.RESET + Back.RESET)
        diff = difflib.ndiff(expected_output.split('. '), actual_output.split('. '))
        diff = color_diff(diff)
        # print(''.join(diff))
        print('\n'.join(diff), end="")
        print(Back.WHITE + Fore.BLACK + '***** END DEBUG DIFFLINES *****' + Fore.RESET + Back.RESET)
    else:
        N_passed += 1


if N_passed != len(test_suite):
    print("{} of {} tests passed!".format(N_passed, len(test_suite)))
else:
    print("All tests passed! Well done!")
