import argparse
import textwrap

from xunit import MainProgram

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="xunit",
        epilog=textwrap.dedent('''\
                Examples:
                    python -m xunit test_module                 - run tests from test_module
                    python -m xunit.test_module.Class           - run tests from test_module.Class
                    python -m xunit.test_module.Class.method    - run specific test method
                -
                ''')
    )
    parser.add_argument("test_module", help="Run tests from test_module")
    args = parser.parse_args()
    main = MainProgram(args.test_module)
    result = main.run()
    print(result)
