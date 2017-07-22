from biokit.io.fastq import FASTQ as FastQ




def set_example1():
    f = FastQ()
    f.identifier = ''
    f.sequence = 'CCCC'
    f.quality = '@ABC'
    return f

def set_example2():
    f = FastQ()
    f.identifier = '@slicing'
    f.sequence = 'CCCCTTTT'
    f.quality = '@ABC;;;;'
    return f

def test_offset():
    f = set_example1()
    assert f.get_quality_integer() == [31, 32, 33, 34]

    f.offset = 64
    assert f.get_quality_integer() == [0, 1, 2, 3]
    f.offset = 33

def test_quality():
    f = FastQ()
    assert f.get_quality(0.000000001) == 90

    assert f.error_probability_from_quality(90) == 1e-9
    assert f.quality_from_error_probability(1e-9) == 90

def test_others():
    f = set_example1()
    #assert len(f) == 1
    print(f)
    f.check()

def test_slicing():
    f = set_example2()
    newf = f[2:6]
    assert newf.sequence == 'CCTT'
    assert newf.quality == 'BC;;'

def test_qual():
    f = set_example1()
    f.quality = '!@;A'
    f.to_qual()
    assert f.to_qual().split("\n")[1] == '0 31 26 32'

#@attr('fixme')
#def test_read_and_plot(self):
#    self.f.read(self.f._multiple_fastq_example)
#    self.f.plot()

def test_clear():
    f = FastQ()
    f.clear()

