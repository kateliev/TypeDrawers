#FLM: Check Tabular Widths 1.2
# ------------------------
# (C) Vassil Kateliev, 2017 (http://www.kateliev.com)

# * Based on TypeDrawers Thread 
#   http://typedrawers.com/discussion/1918/simple-script-test-in-batch-if-all-tabular-and-fixed-width-values-are-correct

# No warranties. By using this you agree
# that you use it at your own risk!

# - Dependancies
from FL import *

# - Functions
def checkWidths(font, query, width, reportMode='s', mark=255):
	'''
	Checks if <<query>> matches given (width)(INT) and returns a list of divergent glyph ID's for [font] and/or reports them.
	Where:
	-	<<query>> may be glyph suffix in STR format (EX: '.tonum') or a LIST of glyph names (EX:. ['One.tonum', ... 'Nine.tonum'])
	-	'reportMode' is a STR witch may contain: 'r'('R') = REPORT; 'm'('M') = MARK using (mark)(RGBINT); 's'('S') = silently return value  (EX: Combination 'rm' will mark and report)

	'''	
	# - Core functionality
	if isinstance(query, str):
		divergent = zip(*[(gID, font[gID].name) for gID in range(len(font)) if query in font[gID].name and font[gID].width != width])

	elif isinstance(query, list):
		divergent = zip(*[(gID, font[gID].name) for gID in range(len(font)) if font[gID].name in query and font[gID].width != width])

	# - Report (remove/comment if not needed!)
	if len(reportMode) and len(divergent):
		print '\n-----\nFONT <%s> has %s glyphs that do not match %s width citeria!\n-----' %(font.full_name, len(divergent[0]), width)

		if 'r' in reportMode.lower():
			print 'Divergent glyphs: %s\n-----' %(' '.join(divergent[1]))

		if 'm' in reportMode.lower():
			for gID in divergent[0]:
				font[gID].mark = mark
			print 'Divergent glyphs: Marked!\n-----'		
	
		return list(divergent[0])


# - Run --------------------------
# - Examples follow based on TypeDrawes Thread, uncomment to test
'''
# --- Example A: Hardcoded Static (Simple)
# --- Init
numbers = ['zero.tosf','one.tosf','two.tosf','three.tosf','four.tosf','five.tosf','six.tosf','seven.tosf','eight.tosf','nine.tosf','zero.tf','one.tf','two.tf','three.tf','four.tf','five.tf','six.tf','seven.tf','eight.tf','nine.tf']
operators = ['plus','minus','equal','multiply','divide','plusminus','approxequal','logicalnot','notequal','lessequal','greaterequal','less','greater','asciicircum']
currencies = ['Euro.tf','dollar.tf','cent.tf','sterling.tf','yen.tf','florin.tf']
diacritics = ['gravecomb','acutecomb','uni0302','tildecomb','uni0304','uni0306','uni0307','uni0308','uni030A','uni030B','uni030C','uni0312','uni0313','uni0326','uni0327','uni0328','gravecomb.case','acutecomb.case','uni0302.case','tildecomb.case','uni0304.case','uni0306.case','uni0307.case','uni0308.case','uni030A.case','uni030B.case','uni030C.case','uni0326.case','uni0327.case','uni0328.case','gravecomb.sc','acutecomb.sc','uni0302.sc','tildecomb.sc','uni0304.sc','uni0306.sc','uni0307.sc','uni0308.sc','uni030A.sc','uni030B.sc','uni030C.sc','uni0326.sc','uni0327.sc','uni0328.sc']

tabWidth = 698
operatorsWidth = 500
diacriticsWidth = 1

#--- Process All open fonts
for fID in range(len(fl)):
	currentFont = fl[fID]
	# - Enter manually below every glyph type to be checked
	checkWidths(currentFont, numbers, tabWidth, 'rm')
	checkWidths(currentFont, operators, operatorsWidth, 'rm')
	checkWidths(currentFont, currencies, tabWidth, 'rm')
	checkWidths(currentFont, diacritics, diacriticsWidth, 'rm')

print 'Done.'
'''
# --- Example B: Dynamic (Versatile)
# --- Init
# - Enter below all types to be checked in format: list[tuple(Parameter_01 !!STR/LIST!!, Width_01 !!INT!!),..(Parameter_NN, Width_NN)]
widths2check = [('.tosf', 698),
		('.tf', 698),
		(['plus','minus','equal','multiply','divide','plusminus','approxequal','logicalnot','notequal','lessequal','greaterequal','less','greater','asciicircum'], 500),
		(['gravecomb','acutecomb','uni0302','tildecomb','uni0304','uni0306','uni0307','uni0308','uni030A','uni030B','uni030C','uni0312','uni0313','uni0326','uni0327','uni0328','gravecomb.case','acutecomb.case','uni0302.case','tildecomb.case','uni0304.case','uni0306.case','uni0307.case','uni0308.case','uni030A.case','uni030B.case','uni030C.case','uni0326.case','uni0327.case','uni0328.case','gravecomb.sc','acutecomb.sc','uni0302.sc','tildecomb.sc','uni0304.sc','uni0306.sc','uni0307.sc','uni0308.sc','uni030A.sc','uni030B.sc','uni030C.sc','uni0326.sc','uni0327.sc','uni0328.sc'], 1)
		]

#--- Process All open fonts
for fID in range(len(fl)):
	currentFont = fl[fID]
	
	for item in widths2check:
		checkWidths(currentFont, item[0], item[1], 'rm')

print 'Done.'
