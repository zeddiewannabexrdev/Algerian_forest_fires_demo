# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from PyInstaller.utils.hooks import copy_metadata, collect_data_files, collect_submodules

# Increase recursion depth to handle complex scientific packages (Streamlit, Scikit-learn, Plotly)
sys.setrecursionlimit(50000)

block_cipher = None

# Collect package metadata and data files
datas = [
    ('data', 'data'),
    ('models', 'models'),
    ('views', 'views'),
    ('config.py', '.'),
    ('data_loader.py', '.'),
    ('app.py', '.'),
    ('.streamlit', '.streamlit'),
]
datas += copy_metadata('streamlit')
datas += collect_data_files('streamlit')

hidden_imports = [
    'streamlit',
    'streamlit.web.cli',
    'sklearn',
    'sklearn.tree',
    'sklearn.ensemble',
    'sklearn.metrics',
    'sklearn.model_selection',
    'plotly',
    'plotly.express',
    'plotly.graph_objects',
    'plotly.subplots',
    'matplotlib',
    'matplotlib.pyplot',
    'scipy',
    'pandas',
    'numpy',
]
hidden_imports += collect_submodules('streamlit')

a = Analysis(
    ['desktop_app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'tensorflow', 'keras', 'IPython', 'notebook'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ForestFireWorkstation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ForestFireWorkstation',
)
