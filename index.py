#!/usr/bin/env python3
import glob
import os
import re


def title_from_dirname(dirname):
    title = " ".join(map(lambda x: x.capitalize(), dirname.split("-")))
    title = re.sub(r"[mM][sS][xX]", r"MSX", title)
    title = re.sub(r"[sS][dD][kK]", r"SDK", title)
    title = re.sub(r"([0-9]+ )", r"", title)
    return title


def main():
    dirname = None
    for filename in sorted(glob.glob("**/*.md", recursive=True)):
        if not os.path.dirname(filename):
            continue
        if dirname != os.path.dirname(filename):
            dirname = os.path.dirname(filename)
            section = title_from_dirname(dirname)
            print("\n# " + section)
        with open(filename) as fin:
            title = fin.readline()[1:].strip()
            print("* [%s](%s)" % (title, filename))

    # Hard coded reference sections.
    print("* [%s](%s)" % ("MSX 4.3 Installation Requirements", "https://www.cisco.com/c/en/us/td/docs/net_mgmt/msx/4_3_0/install_guide/articles/msx_installation_requirements.html"))


if __name__ == "__main__":
    main()

