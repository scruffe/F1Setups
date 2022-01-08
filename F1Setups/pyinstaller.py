import PyInstaller.__main__

PyInstaller.__main__.run([
    'F1Setups.spec',
    '-w',  # hide console
    '-y',  # force yes on install
    '--icon=/Pog.ico"'  # add data
])
