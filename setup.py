from cx_Freeze import setup, Executable

executables = [
    Executable('./vulnscanner/__main__.py')
]

options= {
    'build_exe': {
        'includes': ['vulnscanner'],
        'optimize': 2,
        'compressed': True
    }
}

setup(name='vulnscanner',
    version='0.1',
    description='A python3 vulnscanner',
    executables=executables,
    options=options,
    )
