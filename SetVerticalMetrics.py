#FLM: Set Vertical Metrics 1.2
# ------------------------
# (C) Vassil Kateliev, 2016 (http://www.kateliev.com)

# No warranties. By using this you agree
# that you use it at your own risk!

from FL import *

# - Global configuration
banList = 'Aring Abreve'.split(' ') # List of omitted glyphs
workWithComponents = True			# Process composite characters - non destructive

# - Functions
def getFontYBounds(font, banList, workWithComponents = False):
	'''
	Returns tuple(min_Y, max_Y) values for given [font] omitting glyph names (str) listed in [banList].
	'''

	def getYBounds(glyph):
		return (glyph.GetBoundingRect().y, glyph.GetBoundingRect().height + glyph.GetBoundingRect().y)

	fontMinY, fontMaxY = [], []

	for gID in range(len(font)):
		currGlyph = font[gID]
		if currGlyph.name not in banList and not len(currGlyph.components):
			yBounds = getYBounds(currGlyph)

		elif currGlyph.name not in banList and len(currGlyph.components) and workWithComponents:
			tempGlyph = Glyph(currGlyph)
			currGlyph.Decompose() 			# Workaround! tempGlyph is an orphan so it could not be decomposed
			yBounds = getYBounds(currGlyph)
			currGlyph.Assign(tempGlyph) 	# Repair that mess!
		
		fontMinY.append(int(yBounds[0])); fontMaxY.append(int(yBounds[1]))

	return (min(fontMinY), max(fontMaxY))

# - Run	-------------------
# - Get values
fontBounds = zip(*[getFontYBounds(fl[fID], banList, workWithComponents) for fID in range(len(fl))])
fontInfoBounds = zip(*[(fl[fID].descender[0], fl[fID].ascender[0]) for fID in range(len(fl))])

WinAscend, WinDescend = max(fontBounds[1]), min(fontBounds[0])
Ascender, Descender = max(fontInfoBounds[1]), min(fontInfoBounds[0])
Gap = abs((Ascender + abs(Descender)) - (WinAscend + abs(WinDescend)))

# - Process all open fonts
for fID in range(len(fl)):
	currentFont = fl[fID]

	# - Report
	print '\nProcessing:\t%s\n-----\nFont feature\tOLD\tNEW'  %currentFont.full_name
	print 'WIN Ascent:\t%s \t%s' %(currentFont.ttinfo.os2_us_win_ascent, WinAscend)
	print 'WIN Descent:\t%s \t%s' %(currentFont.ttinfo.os2_us_win_descent, abs(WinDescend))
	print 'Typo Ascent:\t%s \t%s' %(currentFont.ttinfo.os2_s_typo_ascender, Ascender)
	print 'Typo Descent:\t%s \t%s' %(currentFont.ttinfo.os2_s_typo_descender, Descender)
	print 'Typo Line Gap:\t%s \t%s' %(currentFont.ttinfo.os2_s_typo_line_gap,Gap)
	print 'HHEA Ascent\t%s \t%s' %(currentFont.ttinfo.hhea_ascender, WinAscend)
	print 'HHEA Descent:\t%s \t%s' %(currentFont.ttinfo.hhea_descender, -abs(WinDescend))
	print 'HHEA Line Gap:\t%s \t%s\n' %(currentFont.ttinfo.hhea_line_gap, 0)
	
	# - Process
	currentFont.ttinfo.os2_us_win_ascent = WinAscend
	currentFont.ttinfo.os2_us_win_descent = abs(WinDescend)

	currentFont.ttinfo.os2_s_typo_ascender = Ascender
	currentFont.ttinfo.os2_s_typo_descender = Descender
	
	currentFont.ttinfo.hhea_ascender = WinAscend
	currentFont.ttinfo.hhea_descender = -abs(WinDescend)
	
	currentFont.ttinfo.hhea_line_gap = 0
	currentFont.ttinfo.os2_s_typo_line_gap = Gap

print 'End.'
