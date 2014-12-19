from biokit.io.fastq import FASTQ
from nose.plugins.attrib import attr



class test_FASTQ(object):
    @classmethod
    def setup_class(klass):
        klass.f = FASTQ()

    def set_example1(self):
        self.f.identifier = ''
        self.f.sequence = 'CCCC'
        self.f.quality = '@ABC'

    def set_example2(self):
        self.f.identifier = '@slicing'
        self.f.sequence = 'CCCCTTTT'
        self.f.quality = '@ABC;;;;'

    def test_offset(self):
        self.set_example1()
        assert self.f.get_quality_integer() == [31, 32, 33, 34]

        self.f.offset = 64
        assert self.f.get_quality_integer() == [0, 1, 2, 3]
        self.f.offset = 33

    def test_quality(self):
        assert self.f.get_quality(0.000000001) == 90

        assert self.f.error_probability_from_quality(90) == 1e-9
        assert self.f.quality_from_error_probability(1e-9) == 90

    def test_others(self):
        self.set_example1()
        #assert len(self.f) == 1
        print(self.f)
        self.f.check()

    def test_slicing(self):
        self.set_example2()
        newf = self.f[2:6]
        assert newf.sequence == 'CCTT'
        assert newf.quality == 'BC;;'

    def test_qual(self):
        self.f.quality = '!@;A'
        self.f.to_qual()
        assert self.f.to_qual().split("\n")[1] == '0 31 26 32'

    #@attr('fixme')
    #def test_read_and_plot(self):
    #    self.f.read(self.f._multiple_fastq_example)
    #    self.f.plot()

    def test_clear(self):
        self.f.clear()

