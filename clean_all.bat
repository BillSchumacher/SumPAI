rmdir build /s /q
rmdir dist /s /q
rmdir __pycache__ /s /q
rmdir reports /s /q
python clean_sumpai.py --extension=egg-info
python clean_sumpai.py --extension=pyc
python clean_sumpai.py --extension=sumpai