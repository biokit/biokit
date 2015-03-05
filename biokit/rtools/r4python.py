# -*- python -*-
#
#  This file is part of biokit software
#
#  Copyright (c) 2014 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://github.com/cellnopt
#
##############################################################################
"""Code use by pyper module original version available from pyper pacakge on pip"""

__all__ = ["r4python"]

r4python = r"""

.getRvalue4Python__ <- function(x, use_dict=NULL) {

    headstr <- 'numpy.array('
    tailstr <- ')' 

    SpecialLocs <- function(x) { # find locations of special values: NULL, NA, NaN, Inf
        rlt <- list()
        
            idx <- which(is.null(x) | is.na(x))
            if (length(idx) > 0) rlt$None <- idx
            idx <- which(is.nan(x))
            if (length(idx) > 0) rlt$numpy.NaN <- idx
            idx <- which(is.infinite(x))
            if (length(idx) > 0) {
                v <- x[idx]
                iidx <- which(v > 0)
                if (length(iidx) > 0) rlt$numpy.Inf <- idx[iidx]
                iidx <- which(v < 0)
                if (length(iidx) > 0) rlt['-numpy.Inf'] <- idx[iidx]
                }
            
        return(rlt)
        }


    SpecialVals <- function(x, valoc) {
        for (val in names(valoc)) x[valoc[[val]]] <- val
        return(x)
        }

    NullStr <- function(x) 'None'

    VectorStr <- function(x) {
        #nms <- names(x)
        #if (!is.null(nms) &&  length(nms)>0) return(ListStr(as.list(x)))
        complx <- is.complex(x)
        special_locs <- SpecialLocs(x)
        if (is.character(x)) {
            x <- gsub('\\\\', '\\\\\\\\', x)
            x <- gsub('"', '\\\\"', x)
            x <- paste('"', x, '"', sep='') }
        else if (is.logical(x)) x <- ifelse(x, 'True', 'False')
        if (length(special_locs) > 0) x <- SpecialVals(x, special_locs)
        if (length(x)==1) x <- paste(x) # convert to character using paste, "gettext", or "as.character"
        else x <- paste(headstr, '[', paste(x, collapse=','), ']', tailstr, sep='')
        if (complx) x <- gsub('i', 'j', x)
        return(x)
    }

    MatrixStr <- function(x) {
        complx <- is.complex(x)
        special_locs <- SpecialLocs(x)
        if (is.character(x)) x <- matrix(paste('"', x, '"', sep=''), nrow=nrow(x))
        else if (is.logical(x)) x <- ifelse(x, 'True', 'False')
        if (length(special_locs) > 0) x <- SpecialVals(x, special_locs)
        x <- apply(x, 1, function(r) paste('[', paste(r, collapse=','), ']', sep=''))
        x <- paste(headstr, '[', paste(x, collapse=','), ']', tailstr, sep='')
        if (complx) x <- gsub('i', 'j', x)
        return(x)
    }

    ArrayStr <- function(x) {
        complx <- is.complex(x)
        ndim <- length(dim(x))
        if (ndim == 1) return(VectorStr(x))
        if (ndim == 2) return(MatrixStr(x))
        # ndim >= 3
        if (is.character(x)) x <- array(paste('"', x, '"', sep=''), dim=dim(x))
        else if (is.logical(x)) x <- ifelse(x, 'True', 'False')
        # do col first
        x <- apply(x, seq(dim(x))[-2], function(r) paste('[', paste(r, collapse=','), ']', sep=''))
        for (i in seq(ndim-2))
            x <- apply(x, seq(dim(x))[-1], function(r) paste('[', paste(r, collapse=','), ']', sep=''))
        x <- paste(headstr, '[', paste(x, collapse=','), ']', tailstr, sep='')
        if (complx) x <- gsub('i', 'j', x)
        return(x)
    }

    DataFrameStr <- function(x) {
        if (ncol(x) == 0) {
            return('pandas.DataFrame()')
            }

            cnms <- colnames(x) # get column names
            ctp <- list()
            for (i in seq(x)) {
                xi <- as.vector(x[[i]])
                special_locs <- SpecialLocs(xi)
                if (is.character(xi)) {
                    ctp[i] <- sprintf('("%s", "|S%d")', cnms[i], if (length(xi) > 0) max(nchar(xi)) else 0 )
                    xi <- paste('"', xi, '"', sep='') }
                else if (is.logical(xi)) {
                    xi <- ifelse(xi, 'True', 'False')
                    ctp[i] <- paste('("', cnms[i], '", "<?")' ) }
                else if (is.integer(xi)) {
                    xi <- paste(xi)
                    ctp[i] <- paste('("', cnms[i], '", "<q")' ) }
                else if (is.double(xi)) {
                    xi <- paste(xi)
                    ctp[i] <- paste('("', cnms[i], '", "<g")' ) }
                else if (is.complex(xi)) {
                    xi <- gsub('i', 'j', paste(xi))
                    ctp[i] <- paste('("', cnms[i], '", "<G")') }
                if (length(special_locs) > 0) xi <- SpecialVals(xi, special_locs)
                if (nrow(x) > 0) x[[i]] <- xi }
            tailstr <- paste(', dtype=[', paste(ctp, collapse=','), ']', tailstr, sep='') 

        x <- as.matrix(x)
        x <- apply(x, 1, function(r) paste('(', paste(r, collapse=','), if(length(r)<2) ',)' else ')', sep=''))
        x <- paste(headstr, '[', paste(x, collapse=','), ']', tailstr, sep='')
        x <- paste('pandas.DataFrame(', x, ')', sep='')
        return(x)
    }

    ListStr <- function(x) {
        nms <- names(x) # get column names
        x <- sapply(x, Str4Py)
        return(zipVecWithName(x, nms))
    }

    zipVecWithName <- function(x, nms) {
        if (!is.null(nms) &&  length(nms)>0) {
            nms <- paste('"', nms, '"', sep='')
            x <- sapply(seq(nms), function(i) paste('(', nms[i], ',', x[i], ')') )
            if (identical(use_dict, TRUE)) x <- paste('dict([', paste(x, collapse=','), '])', sep='')
            else if (identical(use_dict, FALSE))  x <- paste('[', paste(x, collapse=','), ']', sep='')
            else { # should be NULL or something else
                if (any(duplicated(nms))) x <- paste('[', paste(x, collapse=','), ']', sep='')
                else x <- paste('dict([', paste(x, collapse=','), '])', sep='') } }
        else x <- paste('[', paste(x, collapse=','), ']', sep='')
        return(x)
    }

    Str4Py <- function(x) {
        # no considering on NA, Inf, ...
        # use is.XXX, typeof, class, mode, storage.mode, sprintf
        if (is.factor(x)) x <- as.vector(x)
        rlt <- {
            if (is.null(x)) NullStr(x)
            else if (is.vector(x) && !is.list(x)) VectorStr(x)
            else if (is.matrix(x) || is.array(x)) ArrayStr(x)
            else if (is.data.frame(x)) DataFrameStr(x)
            else if (is.list(x)) ListStr(x)
            else if (is.object(x)) 'None'
            else Str4Py(as.character(x)) }
            # other objects will be convert to character (instead of NullStr), or use "gettext"
        return(rlt)
    }
    Str4Py(x)
    }

    # initalize library path for TCL/TK based environment on Windows, e.g. Python IDLE
    .addLibs <- function() {
        ruser <- Sys.getenv('R_USER')
        userpath <- Sys.getenv('R_LIBS_USER')
        libpaths <- .libPaths()
        for (apath in userpath) {
            if (length(grep(apath, libpaths)) > 0) next
            if (file.exists(apath)) .libPaths(apath)
            else {
                d <- '/Documents'
                if (substr(ruser, nchar(ruser)-nchar(d)+1, nchar(ruser)) != d) {
                    apath <- paste(ruser,d, substr(apath, nchar(ruser)+1, nchar(apath)), sep='')
                    if (file.exists(apath)) .libPaths(apath)
                }
            }
        }
    }

    if(identical(.Platform$OS.type, 'windows')) .addLibs()
    rm(.addLibs)
    
"""
