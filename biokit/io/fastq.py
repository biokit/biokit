"""

resources: http://en.wikipedia.org/wiki/FASTQ_format

FASTQ format supported are those from Sanger and version CASAVA 1.8 (Illumina).
You may use the version <1.4 and identifiers would be recognised but we do not
support any export of other features except for casava>=1.8

The original Sanger PHRED standard is used for quality.


resources: https://github.com/agordon/fastx_toolkit

"""
import copy
import math
import pandas as pd
import pylab
from easydev import AttrDict

class FASTQIdentifier(object):
    """Container for the FASTQ identifier"""
    def __init__(self, identifier):
        self._identifier = identifier
        if self.identifier.startswith("@") is False:
            raise ValueError("identifier must start with @ character")        
    def _get_identifier(self):
        return self._identifier
    identifier = property(_get_identifier)


class FASTQIdentifierIllumnina(FASTQIdentifier):
    """Container for the FASTQ illumina container

    This is an old illumia version:: 
    
        @HWUSI-EAS100R:6:73:941:1973#0/1

    =============== =================================================================
    =============== =================================================================
    HWUSI-EAS100R   the unique instrument name
    6               flowcell lane
    73              tile number within the flowcell lane
    941             'x'-coordinate of the cluster within the tile
    1973            'y'-coordinate of the cluster within the tile
    #0              index number for a multiplexed sample (0 for 
                    no indexing)
    /1              the member of a pair, /1 or /2 (paired-end or 
                    mate-pair reads only)
    =============== =================================================================

    This is the new supported format::

        @EAS139:136:FC706VJ:2:2104:15343:197393 1:Y:18:ATCACG

    =============== ===========================================================
    =============== ===========================================================
    EAS139          the unique instrument name
    136             the run id
    FC706VJ         the flowcell id
    2               flowcell lane
    2104            tile number within the flowcell lane
    15343           'x'-coordinate of the cluster within the tile
    197393          'y'-coordinate of the cluster within the tile
    1               the member of a pair, 1 or 2 (paired-end or mate-pair 
                    reads only)
    Y               Y if the read is filtered, N otherwise
    18              0 when none of the control bits are on, otherwise it 
                    is an even number
    ATCACG          index sequence
    =============== ===========================================================

    """
    def __init__(self, identifier):
        super(FASTQIdentifierIllumnina, self).__init__(identifier)
        if "#" in self.identifier:
            self._interpret_identifier_1_4()
        else:
            self._interpret_identifier()

    def _interpret_identifier(self):
        """

        @EAS139:136:FC706VJ:2:2104:15343:197393 1:Y:18:ATCACG

        Note the space and : separators
        """
        # skip @ character 
        identifier = self.identifier[1:]
        # replace spaces by : character
        identifier = ' '.join(identifier.split())
        identifier = identifier.replace(' ', ':')
        items = identifier.split(':')
        if len(items) != 11:
            raise ValueError('Number of items in the identifier should be 11')
        self._instrument_name = items[0]
        self._run_id = items[1]
        self._flowcell_id = items[2]
        self._flowcell_lane = items[3]
        self._tile_number = items[4]
        self._x_coordinate = items[5]
        self._y_coordinate = items[6]
        self._member_pair = items[7]
        self._filtered = items[8]
        self._control_bits = items[9]
        self._index_sequence = items[10]

    def _interpret_identifier_1_4(self):
        # skip @ character 
        identifier = self.identifier[1:]
        identifier = identifier.replace('#', ':')
        identifier = identifier.replace('/', ':')
        items = identifier.split(':')
        
        if len(items) != 7:
            raise ValueError('Number of items in the identifier should be 11')
        # ['@HWUSI-EAS100R', '6', '73', '941', '1973#0/1']
        self._instrument_name = items[0]
        self._flowcell_lane = items[1]
        self._tile_number = items[2]
        self._x_coordinate = items[3]
        self._y_coordinate = items[4]
        self._index = '#' + items[5]
        self._member_pair = '/' + items[6]

    def _get_instrument_name(self):
        return self._instrument_name
    instrument_name = property(_get_instrument_name)



class FASTQIdentifierNCBI(FASTQIdentifier):
    """Container for the NCBI FASTQ identifier"""
    def __init__(self, identifier):
        super(FASTQNCBI, self).__init__(identifier)



class SingleFASTQ(object):
    _quality_character = "".join([chr(x) for x in range(33, 33+94)])
    def __init__(self, data=None):
        self.identifier = None
        self.sequence = None
        self.quality = None
        
        # Illumina 1.3 to 1.7 style FASTQ file using PHREDscores with offset 64
        self.offset = 33

        if data is not None:
            if isinstance(data, dict):
                print('init with dict')
                fastq = self.from_dict(data)
                self.sequence = fastq.sequence[:]
                self.quality = fastq.quality[:]
                self.identifier = fastq.identifier[:]
            else:
                self.read(data)

    def read(self, data):
        # could be a file or a string. A filename is also a string
        # so isinstance won't work. 
        try:
            with open(data, "r") as fh:
                data = fh.read()
            self.data = data[:]
        except IOError:
            self.data = data[:]
        self._parse_data(data)        

    def _parse_data(self, data):
        self._init()
        for i, line in enumerate(data.split("\n")):
            # skip blankline
            if len(line) == 0:
                continue
            # have we finished to parse the sequence ?
            # if + is found in the new line, then the answer is yes
            if line.startswith("+") and self._parsing_mode == 'sequence': 
                self._parsing_mode = 'quality'
                continue

            # assume identifier is on 1 line only
            if self._parsing_mode == 'identifier':
                if line.startswith("@"):
                    self.identifier = FASTQIdentifier(line) # check
                    self.identifier = self.identifier.identifier
                    self._parsing_mode = 'sequence'
                else:
                    raise ValueError("Expected @ at the beginning of the line %s" % i)
            elif self._parsing_mode == 'sequence':
                self.sequence += line
                self.nolines += 1 
            elif self._parsing_mode == 'quality':
                self.quality += line
                # here the line may start with @, which is confusing with the identifier
                # however, from the sequence we know how many lines are expected
                self.nolines -= 1
                if self.nolines == 0:
                    # clean sequence and quality strings
                    self.sequence = self.sequence.replace("\n", "")
                    self.quality = self.quality.replace("\n", "")
                    self.identifier = self.identifier
                    entry = self.to_dict()
                    entry = AttrDict(**entry)
                    try:
                        self.entries.append(entry)
                    except:
                        # not very good design but if it fails, we assume that
                        # this is the SingleFASTQ class otherwise, the FASTQ class
                        break
                    self._init()



    def _get_quality(self):
        return self._quality
    def _set_quality(self, val):
        # could be a string of characters
        # or list of integers that must be converted to characters
        if val is None:
            self._quality = None
        elif isinstance(val, str):
            self._quality = val
        elif isinstance(val, list) and len(val):
            if isinstance(val[0], int):
                self._quality = self.integer_to_quality(val)
            else:
                raise ValueError("expects a list of integers")
        else:
            raise ValueError("expects a list of integers or a string")
    quality = property(_get_quality, _set_quality)

    def check(self):
        if len(self.quality) != len(self.sequence):
            msg = "Length of the sequence and quality must be equal"
            msg += "Found length of {0} and {1}".format(len(self.sequence), len(self.quality))
            raise ValueError(msg)

    #slicing current entry
    def __getitem__(self, val):
        """you can slice the sequence f = FASTA(data)
        newf = f[5:15]

        """
        fastq = self.copy()
        fastq.sequence = fastq.sequence[val]
        fastq.quality = fastq.quality[val]
        return fastq

    def __len__(self):
        if self.sequence:
            return len(self.sequence)
        else:
            return 0

    def to_dict(self):
        """Transform current entry into a dict"""
        self.check()
        d = {}
        d['sequence'] = self.sequence[:]
        d['identifier'] = self.identifier[:]
        d['quality'] = self.quality[:]
        return d

    def _init(self):
        self.sequence = ''
        self.quality = ''
        # initialise the parsing
        self._parsing_mode = 'identifier'
        self.nolines = 0

    @classmethod
    def from_dict(cls, data):
        """Construct SingleFASTQ from dict of array-like or dicts

        :param dict data:
            {field : array-like} or {field : dict}
        """
        fastq = cls()
        fastq.sequence = data['sequence'][:]
        fastq.identifier = data['identifier'][:]
        fastq.quality = data['quality'][:]
        fastq.check()
        return fastq

    def __str__(self):
        txt = 'Identifier: ' 
        if self.identifier is not None:
            txt += self.identifier
        txt += '\nSequence:'
        if self.sequence is not None:
            txt += self.sequence
        txt += "\nQuality:" 
        if self.quality is not None:
            txt += self.quality
        return txt




class FASTQ(SingleFASTQ):
    """class to manipulate FASTQ format 
    
    WIKIPEDIA:  FASTQ is a text-based format for storing both a biological sequence (usually nucleotide sequence) and its corresponding quality scores. Both the sequence letter and quality score are encoded with a single ASCII character for brevity. It was originally developed at the Wellcome Trust Sanger Institute to bundle a FASTA sequence and its quality data, but has recently become the de facto standard for storing the output of high throughput sequencing instruments such as the Illumina Genome Analyzer.[1]

    A FASTQ file normally uses four lines per sequence.

    #. Line 1 begins with a '@' character and is followed by a sequence identifier and an optional description (like a FASTA title line).
    #. Line 2 is the raw sequence letters.
    #. Line 3 begins with a '+' character and is optionally followed by the same sequence identifier (and any description) again.
    #. Line 4 encodes the quality values for the sequence in Line 2, and must contain the same number of symbols as letters in the sequence.

    A FASTQ file containing a single sequence might look like this::

        @SEQ_ID
        GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
        +
        !''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65

    The character '!' represents the lowest quality while '~' is the highest. 
    Here are the quality value characters in left-to-right increasing order of quality (ASCII):

    ::
    
        !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~

    The original Sanger FASTQ files also allowed the sequence and quality strings 
    to be wrapped (split over multiple lines), but this is generally discouraged 
    as it can make parsing complicated due to the unfortunate choice of "@" and 
    "+" as markers (these characters can also occur in the quality string).

    Here is a simple example::

        @test
        TTTCTTC
        +
        IIIIII1

    But a more ambiguous one would wrap sequence and quality and quality string may start with
    the @ or + sign. The line starting with + may be followed by comments...
    ::
    
        @test_wrap
        GAGACCTTC
        CCTAAATAC
        +test2
        @IIIIIIII
        +CII+III;
        @test_single
        TTTT
        +
        ;;;;


    f = FASTQ('filename.fastq')
    f.identifier, f.sequence, f.quality contains the first entry 

    If several entries in the fastq files, entries are provided, there are stored
    as dictionaries inside a list of entries::

        f.entries[0]['identifier']
        f.entries[0].identifier

    By default, aliases are set for the first entry:

        >>> f.identifier == f.entries[0]['identifier']
        True

    But the default entry can be set to any entries to be found in the list of entries::

        >>> f.set_index(-1) # for the last one 

    Some methods takes all entries (e.g., quality_boxplot), some others use
    only the content of the 3 attributes f.identifier, f.sequence, f.quality (e.g., the print method)



    .. references:: 
        - resources: http://en.wikipedia.org/wiki/FASTQ_format
        - P.J.A.Cock (Biopython), C.J.Fields (BioPerl), N.Goto (BioRuby),
          M.L.Heuer (BioJava) and P.M. Rice (EMBOSS).
          Nucleic Acids Research 2010 38(6):1767-1771
          http://dx.doi.org/10.1093/nar/gkp1137
    """
    # ! is the smallest quality
    # ~ is the highest quality
    # The Sanger style FASTQ files uses PHRED scores and an ASCII offset of 33 
    # (same in NCBI Short Read Archive and Illumina 1.8+
    # PHRED scores goes from 0 to 93.

    _multiple_fastq_example = """@EAS54_6_R1_2_1_413_324
CCCTTCTTGTCTTCAGCGTTTCTCC
+
;;3;;;;;;;;;;;;7;;;;;;;88
@EAS54_6_R1_2_1_540_792
TTGGCAGGCCAAGGCCGATGGATCA
+
;;;;;;;;;;;7;;;;;-;;;3;83
@EAS54_6_R1_2_1_443_348
GTTGCTTCTGGCGTGGGTGGGGGGG
+
;;;;;;;;;;;9;7;;.7;393333"""

    def __init__(self, data=None):
        self.entries = [] # used in parent class in _parse_data
        print("API in progress. May change soon")
        super(FASTQ, self).__init__(data=data)
        # if input is a dict, we should also populate the entries
        #self.to_dict()

    def _parse_data(self, data):
        super(self)._parse_data()
        self.set_entry()
    
    def set_entry(self, index=0):
        """Set the current entry given the index

        """
        self.identifier = self.entries[index]['identifier'][:]
        self.sequence = self.entries[index]['sequence'][:]
        self.quality = self.entries[index]['quality'][:]

    def __add__(self, other):
        result = self.copy()
        result.entries += [x.copy() for x in other.entries]
        return result

    def remove_duplicates(self):
        raise NotImplementedError

    @staticmethod
    def quality_from_error_probability(pe):
        """

        A quality value Q is an integer mapping of :math:`pe` (i.e., the probability 
        that the corresponding base call is incorrect). Two different equations have 
        been in use but we will only use the standard Sanger variant 
        otherwise known as Phred quality score:

        The PHRED software assigns a non-negative quality value 
        to each base using a logged transformation of the error probability:
        
        :math:`Q = -10 \log_{10}( P_e )`
        
        ::

            >>> Pe = 1e-9
            >>> Q = quality_from_error_probability(Pe)
            >>> Q
            90
            >>> quality_from_error_probability(0.1)
            0.1
            >>> quality_from_error_probability(0)
            1
            

        """
        assert pe >=0 and pe <= 1, "probability expected to be between 0 and 1"
        return -10 * pylab.log10(pe)

    def plot(self, logy=True, **kargs):
        """

        :param kargs: any argument accepted by pandas.DataFrame.plot method
        """

        df = pd.DataFrame({
            'Sequence': list(self.sequence), 
            'Quality':self.get_quality_integer()})
        df['Pe'] = df.Quality.apply(lambda x: self.error_probability_from_quality(x))
        df.Pe.plot(marker='o', **kargs)
        #for index in df.index:
        #    pylab.text(index, df['Pe'].ix[index]*1.1, df['Sequence'].ix[index])

        N = len(self)
        pylab.xlim([0, N])
        pylab.xticks(range(0, N), df.Sequence)
        pylab.title("Quality over the sequence (error probability)")
        pylab.ylabel("Probability Error")
        pylab.xlabel("Sequence")
        if logy:
            pylab.semilogy()

    @staticmethod
    def error_probability_from_quality(val):
        """Convert an error probability to PHRED quality (range 0 to about 90)
        
        .. math:: P_e = 10 ^ {-Q / 10}

        """
        import numpy as np
        val = np.array(val)
        return 10 ** (-val / 10.)

    def get_quality(self, p):
        return self.quality_from_error_probability(p)

    def get_quality_integer(self):
        """Return the list of quality values as a list of integers
        
        .. seealso:: :math:`quality_to_integer`
            
        """
        return self.quality_to_integer(self.quality, self.offset)

    @staticmethod
    def integer_to_quality(data, offset=33):
        return [chr(x + offset) for x in data]
        pass

    @staticmethod
    def quality_to_integer(data, offset=33):
        return [ord(x) - offset for x in data]


    def __len__(self):
        return len(self.entries)

    def to_qual(self):
        """
        
        ::

            >>> f = FASTQ()
            >>> f.identifier = 'TEST'
            >>> f.quality = '!@;A'
            >>> f.sequence = 'CCCC'
            >>> print(f.to_qual())
            >TEST
            0 31 26 32
        
        """
        txt = ">" + self.identifier + "\n"
        txt += " ".join([str(x) for x in self.get_quality_integer()])
        txt += "\n"
        return txt

    def clear(self):
        """Remove all entries and reset the current entry

        """
        self.entries = []
        self.identifier = ''
        self.sequence = ''
        self.quality = ''

    def copy(self):
        f = FASTQ()
        f.entries = copy.deepcopy(self.entries)
        f.identifier = self.identifier[:]
        f.sequence = self.sequence[:]
        f.quality = self.quality[:]
        #f.set_entry(0)
        try:
            f.data = self.data[:]
        except:
            pass
        return f


    def to_json(self):
        import json
        raise NotImplementedError

    def to_fasta(self):
        raise NotImplementedError

    def remove_low_quality_entries(self, mean_quality):
        df = self.get_quality_frame()
        df = df[df.mean() < mean_quality]
        indices = df.index
        self.entries = [e for i,e in enumerate(self.entries) if i in indices]

    def mask_low_quality(self, threshold):
        raise NotImplementedError

    def quality_hist(self):
        raise NotImplementedError

    def quality_to_pe(self, quality):
       pe = self.error_probability_from_quality(self.quality_to_integer(quality))
       return pe

    def get_quality_frame(self):
        qualities = [self.quality_to_integer(e.quality) for e in self.entries]
        df = pd.DataFrame({i : self.quality_to_pe(e.quality) 
            for i,e in enumerate(self.entries)})
        return df

    def quality_boxplot(self):
        """Boxplot of the quality values for each nucleotide

        one boxplot per sequence
        """
        #assume sequences have same length
        df = self.get_quality_frame() 
        df.boxplot(rot=90)
        pylab.semilogy()
        return df

    def hist_length(self, **kargs):
        df = pd.DataFrame({'Length': [len(e['sequence']) for e in self.entries]})
        df.hist(**kargs)

    def create_random_data(self, N, min_length=10, max_length=40):
        import numpy as np    
        letters = 'ACGT'
        self.clear()
        for i in range(0, N):
            d = {}
            d['identifier'] = str(i)
            mid = (max_length + min_length) / 2. 
            nseq = int(np.random.normal(mid, (max_length-min_length)/10.))
            
            d['sequence'] = ''.join([letters[np.random.randint(4)] for x in range(0, nseq)])
            d['quality'] = ''.join([self._quality_character[np.random.randint(90)] for x in range(0, nseq)])
            self.entries.append(AttrDict(**d))
            

    def add_entry(self):
        #could be entry, dict, SingleFASTQ
        raise NotImplementedError
