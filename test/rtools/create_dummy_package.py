
import os



class CreateDummy(object):

    def __init__(self, directory="dummy"):
        self.directory = directory
        try:
            os.mkdir(directory)
        except:
            pass

    def __call__(self):
        try:
            os.mkdir(directory)
            self.created = True
        except:
            self.created = False
        self.create_directory()
        self.create_description()
        self.create_namespace()
        self.create_manual()
        self.create_R_file()
    
        # Create the tar ball file
        code = "cd %s; R CMD build %s ; cd .." % (self.directory, '.')
        os.system(code)

    def _clean(self):
        import shutil
        # we could just used the last command but this adds some safety
        shutil.rmtree(os.sep.join([self.directory, 'man']))
        shutil.rmtree(os.sep.join([self.directory, 'R']))
        shutil.rmtree(os.sep.join([self.directory]))

    def create_directory(self):
        try:
            os.mkdir(os.sep.join([self.directory, 'man']))
        except:
            pass
        try:
            os.mkdir(os.sep.join([self.directory, 'R']))
        except:
            pass

    def create_manual(self):
        package = r"""
\name{dummy_test-package}
\alias{dummy_test-package}
\alias{dummy_test}
\docType{package}
\title{R version of dummy_test}
\description{}
\details{}
\author{BadLuck, Maintainer: Any. Volunteer <dummy@dummy.du>}
\keyword{ package }
\examples{
    library(dummy_test)
        dummy_test()
}"""        
        filename = os.sep.join([self.directory, "man", "dummytest-package.Rd"])
        with open(filename, 'w') as fh:
            fh.write(package)

        function= r"""
\name{dummy_test}
\alias{dummy_test}
\alias{dummy_test}
\title{whatever}
\description{whatever}
\usage{dummy_test()}
\arguments{}
\author{whoever}
\examples{
library(dummytest)
dummy_test()
}
        """
        filename = os.sep.join([self.directory, "man", "dummy_test.Rd"])
        with open(filename, 'w') as fh:
            fh.write(package)
    
    def create_R_file(self):
        code = """dummy_test <- function(){
                print("This is the dummytest package")
                }"""
        filename = os.sep.join([self.directory, "R", "dummy_test.R"])
        with open(filename, 'w') as fh:
            fh.write(code)

    def create_namespace(self):
        filename = os.sep.join([self.directory, "NAMESPACE"])
        with open(filename, "w") as fh:
            fh.write("""export("dummy_test")""")

    def create_description(self):
        description = """Package: dummytest
Type: Package
Title: A wonderful dummy package for testing
Version: 1.0.0
Date: 2014-03-13
Author: BackLuck
Maintainer: Any.Volunteer <dummy@dummy.du>
Depends: R (>= 2.15.0), methods
Suggests: 
Description: This package can be install and remove without interferin with the user packages in principle except if a smart developer decides to call its package dummytest.
License: GPL-3
LazyLoad: yes
SystemRequirements: """
        filename = os.sep.join([self.directory, "DESCRIPTION"])
        with open(filename, 'w') as fh:
            fh.write(description)



