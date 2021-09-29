# import relevant files

import csv
import json
import datetime
import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create welcome message

MENU = '''
Please choose from the following options:
1 - Load data from a file
2 - View data
3 - Clean data
4 - Analyse data
5 - Visualise data
6 - Save data to a file
7 - Quit '''


def main():
    print("Welcome to the DataFrame Statistician!")
    print("Programmed by Dhruvisha Gosai")
    print()
    print(MENU)

    choice = input(">>> ").upper()

    while choice != '7':
        if choice == '1':
            imported_df = load_data_from_file()
        elif '2' <= choice <= '6':
            try:
                if choice == '2':
                    print(imported_df)
                elif choice == '3':
                    imported_df = clean_data(imported_df)
                elif choice == '4':
                    analyse_data(imported_df)
                elif choice == '5':
                    visualise_data(imported_df)
                elif choice == '6':
                    save_data(imported_df)
            except NameError:
                print("No data imported.")
        else:
            print("Invalid option!")

        print(MENU)
        choice = input(">>> ").upper()

    print()
    print("Thanks for using the DataFrame Statistician.")
    print("Goodbye!")

# Main frame END!!
# --------------------------------------------------

# -----------------------------------------------------------------------------------------------------
# 1. Import and load the Data
# -----------------------------------------------------------------------------------------------------
# Function to load the trading data - import csv

def load_data_from_file():
    # empty list to add column names for index selection
    column_list = []

    filename = input("Enter the filename: ")
    if len(filename) <= 0:
        print("Cannot be blank. ")
    else:
        try:
            # import file and make sure only numeric columns are selected
            imported_df = pd.read_csv(filename)
            df_numeric = imported_df.select_dtypes(include=['number'])
            df_numeric = df_numeric.rename(columns=str.lower)
            print(f"Data has been loaded successfully.")
            print(f"{len(df_numeric)} records read.")

            # check if user wants to set an index
            print()
            print("Which column do you want to set as index? (leave blank for none)")
            for column in df_numeric:
                column_list.append(column)
                print(column)

            index_col = input(">>> ").lower()
            # while loop to make sure valid input is provided
            if len(index_col) == 0:
                return df_numeric
            else:
                while len(index_col) != 0:
                    if index_col in column_list:
                        df_numeric.set_index(index_col, inplace=True)
                        print(f"{index_col} set as index.")
                        return df_numeric
                    else:
                        print("Invalid selection!")
                        print("Which column do you want to set as index? (leave blank for none)")
                        index_col = input(">>> ").lower()

        except IOError:
            print("File not found.")
        except pd.errors.EmptyDataError:
            print("Unable to load data.")

# Load data END!!
# --------------------------------------------------

# -----------------------------------------------------------------------------------------------------
# 3. Clean data
# -----------------------------------------------------------------------------------------------------
def clean_data(imported_df):
    CLEAN_MENU = '''
    Cleaning data:
    1 - Drop rows with missing values
    2 - Fill missing values
    3 - Drop duplicate rows
    4 - Drop column
    5 - Rename column
    6 - Finish cleaning '''

    print(CLEAN_MENU)
    cleaning_choice = input(">>> ").lower()

    while cleaning_choice != '6':
        if cleaning_choice == '1':
            clean_df = drop_rows_with_missing_val(imported_df)
        elif cleaning_choice == '2':
            clean_df = fill_missing_values(imported_df)
        elif cleaning_choice == '3':
            clean_df = drop_duplicate_rows(imported_df)
        elif cleaning_choice == '4':
            clean_df = drop_column(imported_df)
        elif cleaning_choice == '5':
            clean_df = rename_column(imported_df)
        else:
            print("Invalid option!")

        print(CLEAN_MENU)
        cleaning_choice = input(">>> ").upper()

    return clean_df
# --------------------------------------------------
# Drop rows with missing values


def drop_rows_with_missing_val(clean_df_step1):

    df_length = len(clean_df_step1)

    rows_to_drop = input("Enter the threshold for dropping rows: ").strip()

    while not rows_to_drop.isdigit():
        print("Please enter a valid input. ")
        rows_to_drop = input("Enter the threshold for dropping rows: ").strip()

    if rows_to_drop.isdigit():
        try:
            rows_to_drop = int(rows_to_drop)
            clean_df_step1.dropna(thresh=rows_to_drop, inplace=True)

            df_length_after_drop = len(clean_df_step1)
            rows_dropped = int(df_length) - int(df_length_after_drop)
            print(f"{rows_dropped} rows were dropped")
            print(clean_df_step1)

            return clean_df_step1

        except ValueError:
            print("Input error!")

# --------------------------------------------------
# Fill missing values with in user input


def fill_missing_values(clean_df_step2):

    # Get total sum of all missing values in the df
    missing_values_df = int(clean_df_step2.isnull().sum().sum())

    if missing_values_df < 1:
        print("There are no missing values. ")
        return clean_df_step2
    else:
        print(f"There are {missing_values_df} missing values.")
        replace_missing_value_prompt = input("Enter the replacement value: ").strip()

        while not replace_missing_value_prompt.isdigit():
            print("Please enter a valid number.")
            replace_missing_value_prompt = input("Enter the replacement value: ")

            if replace_missing_value_prompt.isdigit():
                try:
                    clean_df_step2.fillna(replace_missing_value_prompt, inplace=True)
                    print(clean_df_step2)

                    return clean_df_step2
                except ValueError:
                    print("Value error!")

# --------------------------------------------------
# Drop duplicate rows


def drop_duplicate_rows(clean_df_step3):
    df_length = len(clean_df_step3)
    try:
        clean_df_step3.drop_duplicates(inplace=True)
        df_length_new = len(clean_df_step3)
        rows_dropped = int(df_length) - int(df_length_new)
        print(f"{rows_dropped} rows dropped. ")
        print(clean_df_step3)
    except ValueError:
        print("Value error!")

    return clean_df_step3

# --------------------------------------------------
# Drop requested columns


def drop_column(clean_df_step4):
    # empty list to add column names for index selection
    column_list = []

    print("Which column do you want to drop? ")
    for column in clean_df_step4:
        column_list.append(column)
        print(column)

    column_to_drop = input(">>> ").lower()

    # while loop to make sure valid input is provided
    if len(column_to_drop) == 0:
        print("No column dropped.")
        print(clean_df_step4)
        return clean_df_step4
    else:
        while len(column_to_drop) != 0:
            if column_to_drop in column_list:
                clean_df_step4.drop([column_to_drop], axis=1, inplace=True)
                print(f"{column_to_drop} column dropped.")
                print(clean_df_step4)
                return clean_df_step4
            else:
                print("Invalid selection!")
                print("Which column do you want to drop? ")
                column_to_drop = input(">>> ").lower()

# --------------------------------------------------
# Rename columns


def rename_column(clean_df_step5):
    # empty list to add column names for index selection
    column_list = []

    print("Which column do you want to rename? ")
    for column in clean_df_step5:
        column_list.append(column)
        print(column)

    column_to_rename = input(">>> ")

    # while loop to make sure valid input is provided
    if len(column_to_rename) == 0:
        print("No column to rename.")
        print(clean_df_step5)
        return clean_df_step5
    else:
        while len(column_to_rename.strip()) != 0:
            if column_to_rename.lower() in column_list:
                column_new_name = input("Enter the new name: ")
                while column_new_name.lower() in column_list:
                    print("Column name must be unique and non-blank. ")
                    column_new_name = input("Enter the new name: ")
                if column_new_name.lower() not in column_list:
                    clean_df_step5.rename(columns={column_to_rename: column_new_name}, inplace=True)
                    print(f"{column_to_rename} renamed to {column_new_name}.")
                    print(clean_df_step5)
                    return clean_df_step5
            else:
                print("Invalid selection!")
                print("Which column do you want to rename? ")
                column_to_rename = input(">>> ")

# Clean data END!!
# --------------------------------------------------

# -----------------------------------------------------------------------------------------------------
# 4. Analyse data
# -----------------------------------------------------------------------------------------------------


def analyse_data(imported_df):
    count_print_string = "number of values (n)"
    min_print_string = "minimum"
    max_print_string = "maximum"
    mean_print_string = "mean"
    median_print_string = "median"
    std_print_string = "standard deviation"
    sem_print_string = "std. err. of mean"

    for column in imported_df:
        column_length = len(column)
        print(f"{column}")
        print("-" * column_length)
        print(f"{count_print_string:>20}: {imported_df[column].count():<10.0f}")
        print(f"{min_print_string:>20}: {imported_df[column].min():<10.2f}")
        print(f"{max_print_string:>20}: {imported_df[column].max():<10.2f}")
        print(f"{mean_print_string:>20}: {imported_df[column].mean():<10.2f}")
        print(f"{median_print_string:>20}: {imported_df[column].median():<10.2f}")
        print(f"{std_print_string:>20}: {imported_df[column].std():<10.2f}")
        print(f"{sem_print_string:>20}: {imported_df[column].sem():<10.2f}")
        print()

    print(imported_df.corr())

# Analyse data END!!
# --------------------------------------------------

# -----------------------------------------------------------------------------------------------------
# 5. Visualise data
# -----------------------------------------------------------------------------------------------------


def visualise_data(imported_df):
    plt.close("all")

    graph_list = ["line", "bar", "box"]

    print("Please choose from the following kinds: line, bar, box")
    graph_choice = input(">>> ").lower().strip()

    while graph_choice not in graph_list:
        if len(graph_choice) == 0:
            print("Cannot be blank. ")
        else:
            print("Invalid selection!")

        print("Please choose from the following kinds: line, bar, box")
        graph_choice = input(">>> ").lower().strip()

    # Choice of subplots - if don't have correct selection, prompt again
    print("Do you want to use subplots? (y/n)")
    subplots_input = input(">>> ").lower().strip()

    while subplots_input not in ["y", "n"]:
        print("Invalid selection!")
        print("Do you want to use subplots? (y/n)")
        subplots_input = input(">>> ").lower().strip()
        if len(subplots_input) == 0:
            print("Cannot be blank.")

    # Choice of title - can be blank
    print("Please enter the title for the plot (leave blank for no title).")
    title = input(">>> ").lower().strip()
    # Choice of x-axis - can be blank
    print("Please enter the x-axis label (leave blank for no label).")
    x_axis_label = input(">>> ").lower().strip()
    # Choice of y-axis - can be blank
    print("Please enter the y-axis label (leave blank for no label).")
    y_axis_label = input(">>> ").lower().strip()

    if subplots_input == "y":
        is_subplot = True
    else:
        is_subplot = False

    if imported_df.index.name is None:
        is_indexed = False
    else:
        is_indexed = True

    imported_df.plot(kind=graph_choice, use_index=is_indexed, subplots=is_subplot, grid=False)
    # displaying labels
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.suptitle(title, fontweight="bold")
    plt.tight_layout()

    plt.show()

# Visualise data END!!
# --------------------------------------------------

# -----------------------------------------------------------------------------------------------------
# 6. Saving of the final data
# -----------------------------------------------------------------------------------------------------
# Function to save the data - export to csv

def save_data(imported_df):
    output_filename = input("Enter the filename, including extension: ")

    if imported_df.index.name is None:
        is_indexed = False
    else:
        is_indexed = True

    if len(output_filename) == 0:
        print("Cancelling save operation.")
    else:
        try:
            imported_df.to_csv(output_filename, index=is_indexed)
            print(f"Data saved to {output_filename}")
        except ValueError:
            print("Invalid input!")

# Save data END!!
# --------------------------------------------------

main()
