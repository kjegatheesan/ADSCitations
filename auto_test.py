from ads_automate import ADSCitations

author = "^haeussler"
#year = 2017
abstract = "galaxies"
bib_file = "/Users/keerthana/miniconda3/Pycodes/papers.bib"

# Creating an instance of ADSCitations when the author, year, and keywords are known.
#citation = ADSCitations(ads_query=f'author:"{author}" year:{year} abstract:"{abstract}"', 
#                      bib_file=bib_file, 
#                      article_cite=article_cite) 
#citation.ads_automate()       

# Creating an instance of ADSCitations when only the author and keywords are known.

citation = ADSCitations(ads_query=f'author:"{author}" abstract:"{abstract}"',
                        bib_file=bib_file)
citation.ads_automate()



 