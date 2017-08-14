import pandas as pd
from pathlib import Path


def ensure_path(input_file):
    """
    Ensure the given file exists, has the correct extension and is in the current working directory.
    :param input_file: specified input file
    :return: full path to input file, if it is valid
    """
    if input_file.endswith('.xlsx'):
        if Path(input_file).exists():
            cwd = Path('.')
            excel_files = list(cwd.rglob('*.xlsx'))
            for excel in excel_files:
                if excel.samefile(Path(input_file)):
                    path = Path(input_file).resolve()
                    xl = pd.ExcelFile(path)
                    return xl
        else:
            raise FileExistsError('File does not exist.')
    else:
        raise ValueError('File must have .xlsx extension.')


if __name__ == '__main__':

    print(ensure_path('tests/test-aps.xlsx'))
