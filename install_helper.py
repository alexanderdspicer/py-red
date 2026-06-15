import json
import urllib.request

#https://registry.npmjs.org/chalk -> json
#request -> "versions"/*V num*/tarball
#if unable to request REQUIRED libraries, sys.exit(1)

local_cache = []

with open("packages.json", "r") as pkg_list: 
    dependencies = json.load(pkg_list)["dependencies"]
    for i in dependencies.keys():
        if i+"-"+dependencies[i] in local_cache:
            continue
        else:
            with urllib.request.urlopen(f"https://registry.npmjs.org/{i}") as pkg:
                data = pkg.read().decode("utf-8")
                #replacement not ideal, but makes my life easieer
                print(json.loads(data)["versions"][dependencies[i].replace("~", "").replace("^", "")]["dist"]["tarball"])
                local_cache.append(i+"-"+dependencies[i])

        