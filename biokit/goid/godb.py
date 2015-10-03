"""


Resources: geneontology.org and godb Python package from endrebak user (Bakken).
https://github.com/endrebak/godb/

"""

import urllib
import os
from collections import defaultdict

from biokit import biokitPATH
import pandas as pd


__all__ = ['num2goid', 'GOId', 'GODB', 'GOTerm']


def num2goid(value):
    """Returns GO identifier string correctly formatted"""
    return GOId(value).identifier


class GOId(object):
    """Representation of a GO identifier

    A GO identifier simply takes the form GO:XXXXXXX where X are digits
    so this is the string "GO:" followed by 7 digits.

    This class ease the construction and validation of GO identifiers.
    As an input, one can provide a valid GO identifiers or a number, which 
    is then transformed into the proper formatted identifier

    ::

        >>> o = GOId(5)
        >>> o.iddentifier
        'GO:0000005'
        >>> o = GOId('GO:0000005')
        >>> o.identifier
        'GO:0000005'
        >>> print(o)
        'GO:0000005'

    """
    def __init__(self, value):
        """converts the numbers into Gene Ontology IDs.

        :param list numbers: a list of integer or strings or just a
            string or int. The numbers must be
        :return: list of GO Ids

        IDs are seven-digit numbers preceded by the prefix GO: (Gene Ontology
        database standard).
        """
        self._identifier = None
        self.identifier = value

    def _get_identifier(self):
        return self._identifier
    def _set_identifier(self, identifier):
        self._identifier = self._num2goid(identifier)
    identifier = property(_get_identifier, _set_identifier)

    def _num2goid(self, value):
        msg = "GO identifier format must be GO:XXXXXXX with X being numbers"

        if isinstance(value, str):
            if value.startswith("GO:"):
                prefix, suffix = value.split(":", 1)
            else:
                suffix = value
            suffix = int(suffix)
        elif isinstance(value, int):
            suffix = value
        else:
            raise TypeError("value must be a string or an integer. Provided %s"
                    % value)

        if suffix < 1e7:
            goId = "GO:%07d" % suffix
        else:
            raise ValueError(msg)
        return goId

    def __repr__(self):
        return self.identifier

    def __str__(self):
        return self.identifier


class GOTerm(object):
    """Transform a text-version of a GO Term into data structures

    A text contain information about a GO term looks like (obo format)::

        [Term]
        id: GO:0000003
        name: reproduction
        namespace: biological_process

    This can be parsed with this class. You can retrieve these OBO text with
    other tools from BioServices::

        from bioservices import QuickGO
        q = QuickGO()
        data = q.Term("GO:0003824", frmt='obo')

        from biokit import GOTerm
        term = GOTerm(data)
        term.to_dict()

    If an item appears several times (e.g., xref), then the values stored is a
    list, otherwise, it is the raw text found after the item name.

    Here is a brief overview of the structure of an ontology (see
    geneontology.org for details).

    Unique identifier **id** and term name: every term (e.g., mitochondrion) has
    a unique zero-padded seven digit identifier (often called the
    term accession or term accession number) prefixed by GO:, e.g. GO:0005125.

    Namespace (**namespace**) denotes which of the three
    sub-ontologies-cellular component, biological process or molecular
    function-the term belongs to.

    Definition: a textual description of what the term represents, plus
    reference(s) to the source of the information.

    Relationships to other terms: One or more links that capture how the term
    relates to other terms in the ontology. All terms have an "is a" sub-class
    relationship to another term. Gene Ontology employs a number of other
    relations, including 'part of' , and 'regulates'.

    Synonyms **synonym** are alternative words or phrases closely related in
    meaning to the term name, with indication of the relationship between the
    name and synonym given by the synonym scope. The scopes for GO synonyms are
    EXACT, BROAD, NARROW and RELATED.

    Database cross-references or dbxrefs, refer to identical or very similar
    objects in other databases. For instance, the molecular function term
    retinal isomerase activity is cross-referenced with the Enzyme Commission
    entry EC:5.2.1.3; the biological process term sulfate assimilation has the
    cross-reference MetaCyc:PWY-781.

    Comment: An y extra information about the term and its usage.

    Subset (*) : Indicates that the term belongs to a designated subset
        of terms, e.g. one of the GO slims.

    Obsolet tag: Indicates that the term has been deprecated and should not be
        used.

    **id** and **name** are compulsary and unique.
    optional tags are **is_

    .. seealso:: :class:`GODB` and QuickGO from bioservices. For instance, 
        from QuickGO, you may get more information about cross references as 
        compared to :class:`GODB` that relies on geneontologies.org snapshot.
    """
    def __init__(self, text, remove_comments=True):
        if text.startswith("<obo>"):
            raise NotImplementedError("obo XML format, use obo plain text instead")
        elif "id:" in text and "name:" in text:
            #assume that the text is a OBO formatted text
            self.text = text[:]
        else:
            # Assume the input text is a valid GO identifier
            goid = GOId(text).identifier
            # try to retrieve Term for this GO identifier with QuickGO
            from bioservices import QuickGO
            q = QuickGO()
            text = q.Term(goid, frmt='obo')
            self.text = text
        self.remove_comments = remove_comments

    def _remove_comments(self, term):
        # Let us get rid of all comments, this will make further parsing easier
        for k, v in term.items():
            if isinstance(v, list):
                term[k] = [x.split("!")[0].strip() for x in v]
            else:
                if "!" in v:
                    term[k] = v.split("!")[0].strip()
        return term

    def to_dict(self):
        # We assume all tags are list, which is not true
        d = defaultdict(list)
        for this in self.text.strip().split("\n"):
            if ":" in this:
                key, value = this.split(":", 1)
                d[key.strip()].append(value.strip())

        # Based on http://oboformat.googlecode.com/svn/trunk/doc/GO.format.obo-1_2.html
        # we can clean up the lists converting some of them to 
        # single item. We also issue a warning with deprecated ones.
        lists = ['alt_id', 'synonym', 'is_a', 'xref', 'intersection_of',
            'relationship', 'union_of', 'disjoint_from', 'consider', 
            'replaced_by', 'subset', 'property_value']
        nonlist = ['id', 'name', 'is_anonymous', 'is_obsolete', 'def',
                'comment', 'created_by', 'creation_date', 'namespace']
        deprecated = {
                'exact_synonym': 'synonym', 
                'narrow_synonym':'synonym',
                'broad_synonym': 'synonym',
                'xref_analog': 'xref',
                'xref_unk': 'xref',
                'use_term': 'consider'
                }
        # missing: namespace, subset, 
        dd = {}
        for k, v in d.items():
            if k in lists: # nothing to do
                dd[k] = v
            elif k in nonlist:
                if len(v) == 1:
                    dd[k] = v[0]
                else:
                    raise ValueError("%s must be found only once. Check %s" %
                            (k, d['id']))
            elif k in deprecated.keys():
                print("%s deprecated. Kept and assuming non unique tag" % 
                        (k, d['id']))
                dd[k] = v
            else:
                print("%s not handled in %s. Assuming non unique tag" % 
                    (k, d['id']))
                dd[k] = v
        if self.remove_comments is True:
            dd = self._remove_comments(dd)

        # IN OBO/GO format, id and name must be provided
        # others are optional
        if 'id' not in dd.keys() and 'name' not in dd.keys():
            raise ValueError("'id' tag and 'name' must be provided")

        return dd


class GODB(object):
    """Simple handler to get list of GO terms from geneontology website


    The Gene Ontology project provides controlled vocabularies of defined terms
    epresenting gene product properties. These cover three domains: Cellular
    omponent, the parts of a cell or its extracellular environment; Molecular
    unction, the elemental activities of a gene product at the molecular level,
    uch as binding or catalysis; and Biological Process, operations or sets of
    olecular events with a defined beginning and end, pertinent to the
    functioning of integrated living units: cells, tissues, organs, and
    organisms.


    .. seealso:: bioservices QuickGO class
    """
    def __init__(self, name='go.obo', drop_obsolet=True, local=False):
        """

        Searches for a file on geneontology.org exce
        
        :param name: name of the go OBO file to be downloaded
        :param drop_obsolet: drop obsolet GO terms from the entire DB
        :param local: read the OBO file locally (False) or downloads
           from geneontology.org if not present in the biokit
           directory.
        """
        self.name = 'go.obo'
        if local is False:
            self.filename = biokitPATH + os.sep + self.name
        else:
            self.filename = self.name
        self._init()

        if drop_obsolet is True:
           self.df = self.df[self.df.is_obsolete != True]
           self.df.pop('is_obsolete')

        # split relationships

        self.mapping = {'id': 'GO id',
                'namespace': 'Ontology',
                'name': 'Term',
                'def': 'Definition'}
        # TODO: split relationshio into has_part and part_of

    def _init(self):
        if os.path.exists(biokitPATH + os.sep + self.name) is False:
            self._download_godb()
        # Read the original OBO file
        self.read_goterms()
        # Parse the GO terms one by one and transform into a DataFrame
        self.df = self._terms2df()

    def _download_godb(self):
        print("Downloading go db once for all")
        urllib.urlretrieve ("http://geneontology.org/ontology/%s" % self.name,
             self.filename)

    def read_goterms(self):
        # lines starting with ! can be ignored
        # any line may end with a comment starting with !
        with open(self.filename) as fhdata:
            data = "".join(fhdata.readlines()).split("\n\n[Term]")[1:-1]
            self.obo_terms = data

    def _term2dict(self, term):
        term = GOTerm(term)
        return term.to_dict()

    def _terms2df(self):
        terms = [self._term2dict(term) for term in self.obo_terms]
        df = pd.DataFrame(terms)
        df.replace('true', True, inplace=True)
        df.replace('false', False, inplace=True)
        df.set_index('id', inplace=True)
        return df

    def __len__(self):
        return len(self.df)

    def get_annotations(self):
        # replace some columns 
        df = self.df.copy()
        df = df[['namespace', 'name', 'synonym', 'def', 'relationship']]
        df.columns = ["Ontology", "Term", "Synonym", "Definition",
                "relationship"]
        return df
  
    def search(self, search, where='name', method='in'):
        if method == 'in':
            selection = self.df[where].apply(lambda x: search in x)
        elif method == 'is':
            selection = self.df[where].apply(lambda x: search == x)
        elif method == 'startswith':
            selection = self.df[where].apply(lambda x: x.startswith(search))
        return self.df[selection].copy()

    #  The is a relation is transitive, which means that if A is a B, and B is a
    #  C, we can infer that A is a C. 
    #  B part of A does not mean that A have B systematically (think of
    # replication fork part of chromosome but chromosome do not have a
    # replication fork systemtically.
    #  Like is a, part of is transitive: if A part of B part of C 
    #  then A part of C 
    #
    # The logical complement to the part of relation is has part, which
    # represents a part-whole relationship from the perspective of the parent.
    # As with part of, the GO relation has part is only used in cases where A
    # always has B as a part, i.e. where A necessarily has part B. If A exists,
    # B will always exist; however, if B exists, we cannot say for certain that
    # A exists. i.e. all A have part B; some B part of A. 
    def get_children(self, ontology='CC', 
            relations=['is_a', 'part_of', 'has_part']):
        """http://geneontology.org/page/ontology-relations"""

        if ontology in ['CC', 'cellular_component']:
            ontology = 'cellular_component'
        elif ontology in ['BP', 'biological_process']:
            ontology = 'biological_process'
        elif ontology in ['MF', 'molecular_function']:
            ontology = 'molecular_function'
        else:
            raise ValueError("ontology must be one of %s" % set(self.df.namespace))

        newdf = self.df.loc[self.df.namespace == ontology]

        children = []
        parents = []
        vrelations = []
        # this part is slow and maybe improved.
        for name, row in newdf.iterrows():
            if str(row.is_a) == 'nan':
                pass
            elif 'is_a' in relations:
                for this in row.is_a:
                    children.append(name)
                    parents.append(this)
                    vrelations.append('is_a')
            if str(row.relationship) == 'nan':
                pass
            else:
                for this in row.relationship:
                    relation, goid = this.split()
                    if relation == 'part_of' and relation in relations:
                        children.append(name)
                        parents.append(goid)
                        vrelations.append(relation)
                    elif relation == 'has_part' and relation in relations:
                        # not that children/parent are swapped as compared
                        # to the part_of relation.
                        children.append(goid)
                        parents.append(name)
                        vrelations.append(relation)

        df = pd.DataFrame({'Child':children, 'Parent':parents,
            'Relation':vrelations})
        df.sort('Relation', inplace=True, ascending=False)
        return df

    def get_offspring(self):
        # again, based on
        # https://github.com/endrebak/godb/
        # slower but no need for now
        offspring_df = self.get_children().copy()[["Child", "Parent"]]
        offspring_df.columns = ["Offspring", "Parent"]

        df = offspring_df
        new_df = self._compute_transitive_closure(df)
        while not df.equals(new_df):
            df = df.append(new_df).drop_duplicates()
            new_df = self._compute_transitive_closure(df)

            df = df.drop_duplicates().sort()
            new_df = new_df.drop_duplicates().sort()
        return new_df

    def _compute_transitive_closure(self, df):
        """Computes the transitive closure from a two-col parent/child map."""
        df_temp = df[df["Parent"].isin(df["Offspring"])]
        df2 = df.merge(df_temp, left_on="Offspring", right_on="Parent",
            suffixes=["_1_gen", "_2_gen"])
        df2 = df2.drop(["Offspring_1_gen", "Parent_2_gen"], axis=1)
        df2.columns = ["Parent", "Offspring"]
        concat_df = pd.concat([df, df2]).drop_duplicates()
        return concat_df



