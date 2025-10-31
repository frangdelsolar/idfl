# Please listed which tasks have you (partially) complated.

# Task 1

- Three models hold address information: Company, SupplyChainCompany and CertificationBody. To avoid duplication, I create a new model 'Address' to this information stored, and will be called as a ForeignKey by the three models. This way, we avoid code duplication and have more scalability.
- Installed 'pandas' and 'openpyxl' to import data from excel files. Added dependencies in 'requirements.txt'
