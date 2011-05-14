builtinopen = open

import os, cStringIO, warnings

import config, pycompat


# Locator methods implement a open method similar to the builtin open
# function by searching for a file according to a specific rule.

locator_classes = {}

class local:
    # locates files in the current directory

    def opener(self, filename, formats, mode):
        return lambda: builtinopen(filename, mode)

locator_classes["local"] = local


class internal:
    # locates files within the pyx data tree

    def opener(self, filename, formats, mode):
        extension = os.path.splitext(filename)[1][1:]
        if not extension:
            return None
        try:
            import pkgutil
            raise ImportError
        except ImportError:
            return lambda: builtinopen(os.path.join(os.path.dirname(__file__), "data", extension, filename), mode)
        else:
            try:
                data = pkgutil.get_data("pyx", "data/%s/%s" % (extension, filename))
            except IOError:
                return None
            else:
                if data:
                    # ignoring mode?!
                    return lambda: cStringIO.StringIO(data)

locator_classes["internal"] = internal


class recursivedir:
    # locates files by searching recursively in a list of directories

    def __init__(self):
        self.dirs = config.getlist("locator", "recursivedir")
        self.full_filenames = {}

    def opener(self, filename, formats, mode):
        if filename in self.full_filenames:
            return lambda: builtinopen(self.full_filenames[filename], mode)
        while self.dirs:
            dir = self.dirs.pop(0)
            for item in os.listdir(dir):
                full_item = os.path.join(dir, item)
                if os.path.isdir(full_item):
                    self.dirs.insert(0, full_item)
                else:
                    self.full_filenames[item] = full_item
            if filename in self.full_filenames:
                return lambda: builtinopen(self.full_filenames[filename], mode)

locator_classes["recursivedir"] = recursivedir


class ls_R:
    # locates files by searching a list of ls-R files

    def __init__(self):
        self.ls_Rs = config.getlist("locator", "ls-R")
        self.full_filenames = {}

    def opener(self, filename, formats, mode):
        while self.ls_Rs and filename not in self.full_filenames:
            lsr = self.ls_Rs.pop(0)
            base_dir = os.path.dirname(lsr)
            dir = None
            first = True
            for line in builtinopen(lsr):
                line = line.rstrip()
                if first and line.startswith("%"):
                    continue
                first = False
                if line.endswith(":"):
                    dir = os.path.join(base_dir, line[:-1])
                elif line:
                    self.full_filenames[line] = os.path.join(dir, line)
        if filename in self.full_filenames:
            def _opener():
                try:
                    return builtinopen(self.full_filenames[filename], mode)
                except IOError:
                    warnings.warn("'%s' should be available at '%s' according to the ls-R file, "
                                  "but the file is not available at this location; "
                                  "update your ls-R file" % (filename, self.full_filenames[filename]))
            return _opener

locator_classes["ls-R"] = ls_R


class pykpathsea:

    def opener(self, filename, formats, mode):
        import pykpathsea
        for format in formats:
            full_filename = pykpathsea.find_file(filename, format)
        return lambda: builtinopen(full_filename, mode)

locator_classes["pykpathsea"] = pykpathsea


# class libkpathsea:
#     # locate files by libkpathsea using ctypes
# 
#     def opener(self, filename, formats, mode):
#         pass
# 
# locator_classes["libpathsea"] = libkpathsea


class kpsewhich:

    def opener(self, filename, formats, mode):
        for format in formats:
            try:
                full_filenames = os.popen('kpsewhich --format="%s" "%s"' % (format, filename)).read()
            except OSError:
                return
            if full_filenames:
                break
        else:
            return
        full_filename = full_filenames.split("\n")[0]
        def _opener():
            try:
                return builtinopen(full_filename, mode)
            except IOError:
                warnings.warn("'%s' should be available at '%s' according to kpsewhich, "
                              "but the file is not available at this location; "
                              "update your kpsewhich database" % (filename, full_filename))
        return _opener

locator_classes["kpsewhich"] = kpsewhich


class locate:

    def opener(self, filename, formats, mode):
        try:
            full_filenames = os.popen("locate \"%s\"" % filename).read()
        except OSError:
            return
        if not full_filenames:
            return
        full_filename = full_filenames.split("\n")[0]
        def _opener():
            try:
                return builtinopen(full_filenames, mode)
            except IOError:
                warnings.warn("'%s' should be available at '%s' according to the locate database, "
                              "but the file is not available at this location; "
                              "update your locate database" % (filename, self.full_filenames[filename]))
        return _opener

locator_classes["locate"] = locate


methods = [locator_classes[method]()
           for method in config.getlist("locator", "methods", "local internal pykpathsea kpsewhich locate")]

openers = {}

def open(filename, formats, mode="r"):
    formats = tuple(formats)
    if (filename, formats) in openers:
        return openers[(filename, formats)]()
    for method in methods:
        opener = method.opener(filename, formats, mode)
        if opener:
            try:
                file = opener()
            except IOError:
                file = None
            if file:
                openers[(filename, formats)] = opener
                return file
    raise IOError("Could not locate the file '%s'." % filename)


class formats:
    gf = "gf"
    pk = "pk"
    any_glyph = "bitmap font"
    tfm = "tfm"
    afm = "afm"
    base = "base"
    bib = "bib"
    bst = "bst"
    cnf = "cnf"
    db = "ls-R"
    fmt = "fmt"
    fontmap = "map"
    mem = "mem"
    mf = "mf"
    mfpool = "mfpool"
    mft = "mft"
    mp = "mp"
    mppool = "mppool"
    mpsupport = "MetaPost support"
    ocp = "ocp"
    ofm = "ofm"
    opl = "opl"
    otp = "otp"
    ovf = "ovf"
    ovp = "ovp"
    pict = "graphics/figure"
    tex = "tex"
    texdoc = "TeX system documentation"
    texpool = "texpool"
    texsource = "TeX system sources"
    tex_ps_header = "PostScript header"
    troff_font = "Troff fonts"
    type1 = "type1 fonts"
    vf = "vf"
    dvips_config = "dvips config"
    ist = "ist"
    truetype = "truetype fonts"
    type42 = "type42 fonts"
    web2c = "web2c files"
    program_text = "other text files"
    program_binary = "other binary files"
    miscfonts = "misc fonts"
    web = "web"
    cweb = "cweb"
    enc = "enc files"
    cmap = "cmap files"
    subfont_definition = "subfont definition files"
    opentype = "opentype fonts"
    pdftex_config = "pdftex config"
    lig = "lig files"
    texmfscripts = "texmfscripts"
    lua = "lua"
    font_feature = "font feature files"
    cid_maps = "cid maps"
    mlbib = "mlbib"
    mlbst = "mlbst"