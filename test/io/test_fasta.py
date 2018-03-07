from biokit.io.fasta import FASTA, MultiFASTA
import tempfile


def test_fasta():
    s = FASTA()
    s.load_fasta(None)
    s.load_fasta("P43403")
    s.load_fasta("P43403") # already there 
    s.header
    s.gene_name
    s.sequence
    s.fasta
    s.identifier
    fh = tempfile.NamedTemporaryFile(delete=False)
    s.save_fasta(fh.name)
    s.read_fasta(fh.name)
    fh.delete = True
    fh.close()


def test_attributes():
    s = MultiFASTA()
    s.load_fasta("P43403")
    s.load_fasta("P43408")
    assert len(s) == 2

    s.ids
    s.fasta
    fh = tempfile.NamedTemporaryFile(delete=False)
    s.save_fasta(fh.name)
    s.read_fasta(fh.name)

    s.fasta["P43403"]
    s.hist_size()
    s.df

def test_idempotency():
    fh = tempfile.NamedTemporaryFile(delete=False)
    f1=FASTA()
    f1.load_fasta('P43403')
    f1.save_fasta(fh.name)
    f2=FASTA()
    f2.read_fasta(fh.name)
    assert str(f1)==str(f2)
