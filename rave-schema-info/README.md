CMB Clinical Data Management System Data Info
=============================================

The Cancer Moonshot Biobank clinical information is stored in an instance of [Medidata Rave](https://www.medidata.com/en/clinical-trial-products/clinical-data-management/edc-systems).

The Rave instance organizes clinical data into a large number of tables. Many of these tables are mapped directly to data that is collected via Clinical Report Forms (CRFs).

For each form, data entry slots are given a short name which corresponds to the column name of the relevant table in Rave.

This [Excel spreadsheet](./10323-form-terms-V3.txt) contains a mapping of these short names to human readable names, the form in which that slot appears, and the page number of the form in the PDF description of all CRFs.

The file `form-terms.rds` is a rendering of this spreadsheet in an R-readable [RDS](https://cran.r-project.org/doc/manuals/r-release/R-ints.html#Serialization-Formats) format.
