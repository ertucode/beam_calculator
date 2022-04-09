import pkg_resources

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
     for i in installed_packages])

modules = []
for package in installed_packages:
     package = str(package)
     package = package.split()[0]
     modules.append(package)
               

required = ["pygame","time","python-math","numpy","copy","matplotlib"]
matplotlibdep = ["packaging","pip","pyparsing","kiwisolver","dateutil","setuptools","cycler","numpy","six"]
if "matplotlib" in required:
     required += matplotlibdep
print(required)
excludes = ""
for module in modules:
     if not module in required:
          excludes += f"--exclude-module {module} "

file_name = "beam_calculator.py"

noconsole = "-w"

icon = "--icon=myicon.ico"
icon = ""

text = f"pyinstaller --onefile {noconsole} {icon} {file_name} {excludes}  "


#print(installed_packages_list)
print(modules)
#print(text)

import os

os.system(text)

