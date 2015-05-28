/* copyright: Thomas Cokelaer, Oct 2014
 *
 *Not to be used. Was for testing and is for book keeping.
 * */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


unsigned char *  dna_complement(const char *seq, unsigned long n);
/*void complement_inplace(char *seq, int n);*/

/*avoid issues on windows apparently*/
void initcomplement(){}
void PyInit_complement() {}

unsigned char  * dna_complement(const char *seq, unsigned long n){
    unsigned char *newseq = malloc(sizeof(char) * (n+1));
    unsigned long i=0; 
    int cvt[100];
    cvt['A'] = 't';
    cvt['T'] = 'a';
    cvt['C'] = 'g';
    cvt['G'] = 'c';
    cvt['a'] = 't';
    cvt['t'] = 'a';
    cvt['c'] = 'g';
    cvt['g'] = 'c';
    for (i=0; i<n; i++){
        newseq[i] = cvt[seq[i]];
    }
    newseq[n] = '\0';
    return newseq;
}
