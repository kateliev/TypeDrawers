#FLM: Fetch Anchors 1.2

'''
----------------------------------------
# (C) Vassil Kateliev 2016 (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
-----------------------------------------

Fetch Anchors will copy all anchor data from all parent glyphs to each of the selected component based glyph(s)

For options look at Init section

For more information look at TypeDrawers thread:
http://typedrawers.com/discussion/1760/fontlab-automatic-anchors-from-base-component


-----------------------------------------
MIT License

Copyright (c) [2016] [Vassil Kateliev]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
----------------------------------------
'''

# - Dependancies -----------------
from FL import *

# - Init --------------------------
font = fl.font
glyph = fl.glyph


# - Cutomize ----------------------
# -- List of diacritical marks used in font. 
# -- These are default - enter yours here if different!
diactiricalMarks = [	'grave', 
			'dieresis', 
			'macron', 
			'acute', 
			'cedilla', 
			'dotlessi', 
			'dotlessj', 
			'uni02BC', 
			'circumflex', 
			'caron', 
			'breve', 
			'dotaccent', 
			'ring', 
			'ogonek', 
			'tilde', 
			'hungarumlaut', 
			'caroncomma', 
			'commaaccent', 
			'cyrbreve'
		]

# -- List of named anchor specific displacements in tuple(x,y) format. 
# -- MM Designs: Use list[typle(x,y)]. Each emelent in list represents shifts for each layer of MM typeface, or just use one tuple(x,y) dor all MM layers
# -- Example: {'top':[(-100,-100), (-154,-154), (100,100), (20,20)], 'bottom':(300,300)} and etc...
# -- Enter desired shifts for your anchors here!
displaceAnchors = {
			'top':(0,0),
			'bottom':(0,0)
		}

# -- Do not fetch the anchors of Diactirical Marks and insert them into the glyph (for mark stacking ?!). 
# -- Default is True!
ignoreDiactiricalMarks = True


# - Funcitions -------------------
def getGlyph(font, glyph):
	'''
	Returns a [glyph] object no matter the reference used [glyphObject, glyphIndex, glyphName].
	---
	Example: if /H is the current glyph with index 1 then
	getGlyph(font, glyph) = getGlyph(font, 1) = getGlyph(font, H)

	Src: from Kateliev FontTools Module
	'''
	if isinstance(glyph, basestring):
		glyph = font[font.FindGlyph(glyph)]
	elif isinstance(glyph, int):
		glyph = font[glyph]
	return glyph

def copyAnchor(srcGlyph, dstGlyph, anchorName, newName = None):
	'''
	Copies [anchorName] (string) from [srcGlyph] to [dstGlyph] and renames it to [newName] (string)
	'''
	if len(srcGlyph.anchors):
		tempAnchor = Anchor(srcGlyph.FindAnchor(anchorName))
		
		if newName is not None:
			tempAnchor.name = newName

		dstGlyph.anchors.append(tempAnchor)

def copyAllAnchors(srcGlyph, dstGlyph, appendPrefix = None, report = False):
	'''
	Copies all anchors from [srcGlyph] to [dstGlyph] and adds [appendPrefix] (string) to each of them
	'''
	reportAnchorList = []

	if len(srcGlyph.anchors):
		for anchor in srcGlyph.anchors:
			tempAnchor = Anchor(anchor)

			if appendPrefix is not None:
				tempAnchor.name = appendPrefix + anchor.name

			reportAnchorList.append(tempAnchor.name)
			dstGlyph.anchors.append(tempAnchor)

		if report:
			return reportAnchorList

def fetchAnchors(componentGlyph, displacementDict = {}, ignoreDiactiricalMarks = True):
	# - Init
	masters = componentGlyph.layers_number	# MM layers
	baseRun = True # The base (first components) gets it's original anchors names, everybody else is renamed

	if len(componentGlyph.components):
		if ignoreDiactiricalMarks:
			componentNames = [font[cID.index].name for cID in componentGlyph.components if font[cID.index].name not in diactiricalMarks]
			componentIndexes = [cID.index for cID in componentGlyph.components if font[cID.index].name not in diactiricalMarks]
			componentDeltas = [cID.deltas for cID in componentGlyph.components if font[cID.index].name not in diactiricalMarks]
		else:
			componentNames = [font[cID.index].name for cID in componentGlyph.components]
			componentIndexes = [cID.index for cID in componentGlyph.components]
			componentDeltas = [cID.deltas for cID in componentGlyph.components]
			
		# - Process 
		for index in range(len(componentIndexes)):
			# -- 1: Copy 
			if baseRun and componentNames[index] not in diactiricalMarks:
				newAnchorsList = copyAllAnchors(font[componentIndexes[index]], componentGlyph, report = True)
				baseRun = False
			else:
				newAnchorsList = copyAllAnchors(font[componentIndexes[index]], componentGlyph, appendPrefix = str(componentNames[index] + '.'), report = True)

			# -- 2: Compensate for deltas
			for newAnchor in newAnchorsList:
				processedAnchor = componentGlyph.FindAnchor(newAnchor)

				for layer in range(masters):
					processedAnchor.Layer(layer).x += componentDeltas[index][layer].x
					processedAnchor.Layer(layer).y += componentDeltas[index][layer].y

		# -- 3: Displace accoridng to displacementDict
		if len(displacementDict):
			anchorList = [aID.name for aID in componentGlyph.anchors]
				
			for anchorName in anchorList:

				for key, value in displacementDict.iteritems():

					if key in anchorName:
						processedAnchor = componentGlyph.FindAnchor(anchorName)

						for layer in range(masters):

							if len(value) == masters and isinstance(value, list):
								processedAnchor.Layer(layer).x += value[layer][0]
								processedAnchor.Layer(layer).y += value[layer][1]

							else:
								processedAnchor.Layer(layer).x += value[0]
								processedAnchor.Layer(layer).y += value[1]

		print 'DONE:\t %s - %s anchors' %(componentGlyph.name, len(componentGlyph.anchors))
	else:
		print 'ERRO:\t %s - no components found' %componentGlyph.name

# - Run --------------------------
fl.SetUndo()

# - Init
selectedGlyphs = [gID for gID in range(len(font)) if fl.Selected(gID)]

# - Processs
for gID in selectedGlyphs:
	fetchAnchors(font[gID], displaceAnchors, ignoreDiactiricalMarks)

#- END ---------------------------
fl.UpdateGlyph()
fl.UpdateFont()
