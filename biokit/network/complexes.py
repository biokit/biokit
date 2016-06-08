# -*- python -*-
#
#  This file is part of biokit software
#
#  Copyright (c) 2015 - EBI-EMBL
#  Copyright (c) 2016 - Institut Pasteur
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://github.com/biokit
#
##############################################################################
from easydev import Logging, DevTools
from bioservices import IntactComplex
import pylab
import pandas as pd
from io import StringIO

__all__ = ['Complexes']


class Complexes(Logging):
    """Manipulate complexes of Proteins

    This class uses Intact Complex database to extract information about
    complexes of proteins. 

    When creating an instance, the default organism is "Homo sapiens". 
    The organism can be set to another one during the instanciation or later::

        >>> from biokit.network.complexes import Complexes
        >>> c = Complexes(organism='Homo sapiens')
        >>> c.organism = 'Rattus norvegicus'

    Valid organisms can be found in :attr:`organisms`. When changing the
    organism, a request to the Intact database is sent, which may take some
    time to update. Once done, information related to  this organism is stored
    in the :attr:`df` attribute, which is a Pandas dataframe. It 
    contains 4 columns. Here is for example one row::

        complexAC                                             EBI-2660609
        complexName                            COP9 signalosome variant 1
        description     Essential regulator of the ubiquitin (Ubl) con...
        organismName                                   Homo sapiens; 9606

    This is basic information but once a complex accession (e.g., EBI-2660609)
    is known, you can retrieve detailled information. This is done
    automatically for all the accession when needed. The first time, it will 
    take a while (20 seconds for 250 accession) but will be cache for this 
    instance. 

    The :attr:`complexes` contains all details about the entries found in
    :attr:`df`. It is a dictionary where keys are the complex accession. For 
    instance::

        >>> c.complexes['EBI-2660609']

    In general, one is interested in the participants of the complex, that is
    the proteins that form the complex. Another attribute is set for you::

        >>> c.participants['EBI-2660609']

    Finally, you may even want to obtain just the identifier of the participants
    for each complex. This is stored in the :attr:`identifiers`::

        >>> c.identifiers['EBI-2660609']

    Note however, that the identifiers are not neceseraly uniprot identifiers.
    Could be ChEBI or sometimes even set to None. The :meth:`strict_filter`
    removes the complexes with less than 2 (strictly) uniprot identifiers.
    
    Some basic statistics can be printed with :meth:`stats` that indeticates
    the number of complexes, number of identifiers in those complexes ,and
    number of unique identifiers. A histogram of number of appearance of each 
    identifier is also shown.

    The :meth:`hist_participants` shows the number of participants per complex.

    Finally, the meth:`search_complexes` can be used in the context of 
    logic modelling to infer the AND gates from a list of uniprot identifiers
    provided by the user. See :meth:`search_complexes` for details.

    Access to the Intact Complex database is performed using the 
    package BioServices provided in Pypi.
    """
    def __init__(self, organism='Homo sapiens', verbose=True, cache=False):
        """.. rubric:: Constructor

        :param str orgamism: the organism to look at. Homo sapiens
            is the default. Other possible organisms can be found
            in :attr:`organisms`.
        :param str verbose: a verbose level in ERROR/DEBUG/INFO/WARNING
            compatible with those used in BioServices.

        """
        super(Complexes, self).__init__(level=verbose)

        self.devtools = DevTools()
        self.webserv = IntactComplex(verbose=verbose, cache=cache)
        df = self.webserv.search('*', frmt='pandas')
        self.df = df

        #: list of valid organisms found in the database
        self.valid_organisms = list(set(df['organismName']))
        self.valid_organisms = [x.split(';')[0] for x in self.valid_organisms]


        #: list of valid organisms found in the database
        self.organisms = list(set(df['organismName']))
        self._organism = None
        if organism in self.organisms:
            self.organism = organism
        else:
            print("Organism not set yet. ")

        # This will populated on request as a cache/buffer
        self._details = None
        self._complexes = None

    def _get_organism(self):
        return self._organism
    def _set_organism(self, organism):
        self.devtools.check_param_in_list(organism, [str(x.split(";")[0]) for x in self.valid_organisms])
        self._organism = organism

        self.df = self.webserv.search('*', frmt='pandas',
                filters='species_f:("%s")' % self.organism)
        self._complexes = None
    organism = property(_get_organism, _set_organism, 
        doc="Getter/Setter of the organism")

    def hist_participants(self):
        """Histogram of the number of participants per complexes

        :return: a dictionary with complex identifiers as keys and
            number of participants as values

        ::

            from biokit.network.complexes import Complexes
            c = Complexes()
            c.hist_participants()

        """
        N = []
        count = {}
        for i, identifier in enumerate(self.complexes.keys()):
            n = len(self.complexes[identifier]['participants'])
            N.append(n)
            count[identifier] = n

        _ = pylab.hist(N, bins=range(0, max(N)))
        pylab.title('Number of participants per complex')
        pylab.grid()
        return count

    def stats(self):
        """Prints some stats about the number of complexes and histogram of the
        number of appearances of each species"""
        species = []
        for k in self.participants.keys():
            species.extend([x['identifier'] for x in self.participants[k]])
            N = []
        for spec in set(species):
            N.append(species.count(spec))
        _ = pylab.hist(N, bins=range(0, max(N)))
        pylab.title("Number of appaerances of each species")
        pylab.grid()
        print("""There are %s complexes involving %s participants with %s unique species. """ %
                 (len(self.complexes), len(species), len(set(species))))

    def _get_participants(self):
        participants = {}
        for k,v in self.complexes.items():
            participants[k] = v['participants']
        return participants
    participants = property(_get_participants, 
        doc="""Getter of the complex participants (full details)""")

    def _get_identifiers(self):
        identifiers = {}
        for k,v in self.participants.items():
            identifiers[k] = [x['identifier'] for x in v]
        return identifiers
    identifiers = property(_get_identifiers,
            doc="""Getter of the identifiers of the complex participants""")

    def _get_complexes(self):
        if self._complexes is None:
            self._load_complexes()
        return self._complexes.copy()
    complexes = property(_get_complexes,
        doc="""Getter of the complexes (full details""")

    def _load_complexes(self, show_progress=True):
        from easydev import Progress
        import time
        pb = Progress(len(self.df.complexAC))
        complexes = {}
        self.logging.info("Loading all details from the IntactComplex database")
        for i, identifier in enumerate(self.df.complexAC):
            res = self.webserv.details(identifier)
            complexes[identifier] = res
            if show_progress:
                pb.animate(i+1)
        self._complexes = complexes

    def remove_homodimers(self):
        """Remove identifiers that are None or starts with CHEBI
        and keep complexes that have at least 2 participants
        
        
        :return: list of complex identifiers that have been removed.
        """


        # None are actually homo dimers
        toremove = []
        for k,this in self.identifiers.items():
            remains = [x for x in this if x is not None]
            if len(remains)<=1:
                toremove.append(k)
        self.logging.info("removing %s homodimers complexes" % len(toremove))
        for this in toremove:
            del self._complexes[this]
        return toremove

    def search_complexes(self, user_species, verbose=False):
        """Given a list of uniprot identifiers, return complexes and
            possible complexes.

        :param list user_species: list of uniprot identifiers to be
            found in the complexes
        :return: two dictionaries. First one contains the complexes
            for which all participants have been found in the user_species
            list. The second one contains complexes for which some participants
            (not all) have been found in the user_species list.

        """
        level = self.debugLevel[:]
        if verbose:
            self.debugLevel = 'INFO'
        else:
            self.debugLevel = 'ERROR'

        and_gates = {}
        candidates = {}

        identifiers = self.identifiers.values()

        for k, identifiers in self.identifiers.items():

            # get rid of suffixes such as -1 or -PRO_xxx
            prefixes = [x.split("-")[0] if x is not None else x for x in identifiers]


            # You may have a complex with ['P12222', 'P33333-PRO1',
            # 'P33333-PRO2'], in which case P33333 is found only once and
            # thereofre the final number of found participants is not the length
            # of the complexes...so we need to get rid of the duplicates if any
            prefixes = list(set(prefixes))
            N = len(prefixes)
            found = [spec for spec in user_species if spec in prefixes]

            if len(found) == N:
                self.logging.info('Found entire complex %s ' % k)
                and_gates[k] = identifiers[:]
            elif len(found) >= 1:
                self.logging.info('Found partial complex %s with %s participants out of %s' % 
                        (k, len(found), len(identifiers)))
                candidates[k] = {'participants': identifiers, 'found': found}
        self.debugLevel = level[:]
        return and_gates, candidates

    def search(self, name):
        """Search for a unique identifier (e.g. uniprot) in all complexes

        :return: list of complex identifiers where the name was found
        """
        found = []
        for k, identifiers in self.identifiers.items():
            prefixes = [x.split("-")[0] if x is not None else x for x in identifiers ]
            if name in prefixes:
                self.logging.info("Found %s in complex %s (%s)" % (name, k,
                    identifiers))
                found.append(k)
        return found

    def chebi2name(self, name):
        """Return the ASCII name of a CHEBI identifier"""
        from bioservices import ChEBI
        c = ChEBI()
        name = dict(c.getLiteEntity(name)[0])['chebiAsciiName']
        return name

    def uniprot2genename(self, name):
        """Return the gene names of a UniProt identifier"""
        from bioservices import UniProt
        c = UniProt(cache=True)

        try:
            res = pd.read_csv(StringIO(c.search(name, limit=1)), sep='\t')
            return list(res['Gene names'].values)
        except:
            print("Could not find %s" % name)

    def report(self, species):
        complete, partial = self.search_complexes(species, verbose=False)
        res = {'Found':[], 'Participants':[], 'Complete':[],
                'Identifier':[], 'Number found':[], 'Number of participants':[],
                'Name':[]}

        for k, v in complete.items():
            res['Name'].append(self.complexes[k]['name'])
            res['Found'].append(";".join(v))
            res['Number found'].append(len(v))
            res['Participants'].append(";".join(self.identifiers[k]))
            res['Number of participants'].append(len(self.identifiers[k]))
            res['Complete'].append(True)
            res['Identifier'].append(k)

        for k, v in partial.items():
            res['Name'].append(self.complexes[k]['name'])
            res['Found'].append(";".join(v['found']))
            res['Number found'].append(len(v['found']))
            res['Participants'].append(";".join(self.identifiers[k]))
            res['Number of participants'].append(len(self.identifiers[k]))
            res['Complete'].append(False)
            res['Identifier'].append(k)

        res = pd.DataFrame(res, columns=['Found', 'Participants', 'Identifier', 'Name', 'Number found', 
            'Number of participants', 'Complete'])
        return res










