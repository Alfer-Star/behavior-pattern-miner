import os, sys

class HiddenPrints:
    """ 
    Usage:
    with HiddenPrints():
        print("This will not be printed")

    print("This will be printed as before")
    
    from: https://stackoverflow.com/a/45669280
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout