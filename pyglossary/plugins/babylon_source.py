# -*- coding: utf-8 -*-

# Source Glossary for "Babylon Builder".
# A plain text file. Not binary like BGL files.

from formats_common import *

enable = True
format = "BabylonSource"
description = "Babylon Source (gls)"
extensions = (".gls", ".babylon")
singleFile = True
tools = [
	{
		"name": "Babylon Glossary Builder",
		"web": "https://babylon-glossary-builder.software.informer.com/",
		# what's the official web page?
		"platforms": ["Windows"],
		"license": "Proprietary",
	},
]
optionsProp = {
	"writeInfo": BoolOption(),
	"newline": NewlineOption(),
	"encoding": EncodingOption(),
	"resources": BoolOption(),
}
depends = {}


def entryCleanWinArabic(entry: BaseEntry) -> Optional[BaseEntry]:
	from pyglossary.arabic_utils import cleanWinArabicStr
	entry.editFuncWord(cleanWinArabicStr)
	entry.editFuncDefi(cleanWinArabicStr)
	return entry


def writeIterEntries(glos, entryFilterFunc):
	for entry in glos:
		if entryFilterFunc:
			entry = entryFilterFunc(entry)
			if not entry:
				continue
		yield entry


def write(
	glos: GlossaryType,
	filename: str,
	writeInfo: bool = True,
	newline: str = "",
	encoding: str = "utf-8",
	resources: bool = True,
) -> None:
	g = glos
	entryFilterFunc = None
	if encoding.lower() in (
		"arabic",
		"windows-1256",
		"windows-arabic",
		"arabic-windows",
		"arabic windows",
		"windows arabic",
	):
		encoding = "windows-1256"
		entryFilterFunc = entryCleanWinArabic
		if not newline:
			newline = "\r\n"

	if not newline:
		newline = "\n"

	head = ""
	if writeInfo:
		head += "\n".join([
			"### Glossary title:" + g.getInfo("name"),
			"### Author:" + g.getAuthor(),
			"### Description:" + g.getInfo("description"),
			"### Source language:" + g.getInfo("sourceLang"),
			"### Source alphabet:" + encoding,
			"### Target language:" + g.getInfo("targetLang"),
			"### Target alphabet:" + encoding,
			"### Browsing enabled?Yes",
			"### Type of glossary:00000000",
			"### Case sensitive words?0"
			"",
			"### Glossary section:",
			"",
		])

	iterEntries = None
	if entryFilterFunc:
		iterEntries = writeIterEntries(glos, entryFilterFunc)

	g.writeTxt(
		entryFmt="{word}\n{defi}\n\n",
		filename=filename,
		writeInfo=False,
		defiEscapeFunc=replaceStringTable([
			("\n", "<BR>"),
		]),
		ext=".gls",
		head=head,
		iterEntries=iterEntries,
		encoding=encoding,
		newline=newline,
		resources=resources,
	)
