import brightway2 as bw


def main():
    bw.projects.set_current("EF calculation")
    bw.bw2setup()

    methods_csv_filepath = r"../EF_adapted.CSV"

    print("Importing the adapted methods in the brightway database...")
    importer = bw.SimaProLCIACSVImporter(methods_csv_filepath, "agribalyse3")

    importer.apply_strategies()
    importer.statistics()

    print("Adding missing characterization factors")
    importer.add_missing_cfs()
    importer.statistics()

    print("Dropping unlinked")
    importer.drop_unlinked()

    importer.write_methods()


if __name__ == "__main__":
    main()
