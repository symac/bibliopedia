# -*- coding: utf-8  -*-
import pywikibot
import sys


site = pywikibot.getSite()
site.login()
user = site.user()
if user:
	pywikibot.output(u"Logged in on %(site)s as %(user)s." % locals())

# On va lire le fichier (en UTF8)
import codecs
with codecs.open("liste_pages.txt",'r',encoding='utf8') as f:
    lines = f.readlines();
lines = map(lambda s: s.strip(), lines)
f.close();

number = 1

for line in lines:
	# On va regarder si la page n'existe pas déjà
	page_infos = line.split("\t");
	pagename = page_infos[0];

	page = pywikibot.Page(site, pagename)
	try:
		text = page.get()
		print "%s EXISTE : %s" % (number, pagename)
	except pywikibot.NoPage:
		# Pas de page pour le moment, on doit la créer
		pagename_light = pagename.replace("23 Mobile things - ", "")
		url_eng = page_infos[1]
		url_pin = page_infos[2]
		lib_pin = page_infos[3]

		content = u"""{{23things}} <!-- Ne pas supprimer cette ligne -->

'''Truc #%s - %s'''

''Cette page est encore vide, n'hésitez pas à la traduire depuis la [%s version anglaise].

== Liens externes ==
* [%s Version anglaise de la page]
""" % (number, pagename_light, url_eng, url_eng)
		if (url_pin != "") and (lib_pin != ""):
			content = content + "* [%s Tableau pinterest \"%s\" de la page]" % (url_pin, lib_pin)
		

		content = content + u"""

<!-- Ne rien changer sous cette ligne -->
{{Commentaires}}

[[Catégorie:23 mobile things]]
"""

		
		page.put(content, comment="Initialisation page", minorEdit = True)

	number = number + 1
