import re
from io import StringIO

import pandas as pd

# lists to sanitize class
COLUMNS = [
    "name",
    "obs",
    "gender",
    "birth",
    "_address",
    "district",
    "city",
    "state",
    "zip",
    "country",
    "cpf",
    "id_card",
    "phone",
    "cell_phone",
    "email",
    "sos_contact",
    "sos_phone",
    "obs2",
    "A1",
    "A2",
    "A3",
    "A4",
    "GR",
    "A5",
    "A6",
    "from",
    "to",
    "date",
]


class SanitizeCsv:
    columns = COLUMNS[:]
    date_columns = ["birth", "A1", "A2", "A3", "A4", "GR", "A5", "A6", "date"]
    string_columns = [
        "zip",
        "id_card",
        "phone",
        "cell_phone",
        "sos_phone",
    ]
    long_address_columns = ["address", "number", "complement"]

    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.df = self.get_dataframe

    @property
    def get_dataframe(self):
        # getting dataframe
        df = pd.read_csv(StringIO(self.file.read().decode("utf-8")))

        # checking if the dataframe is malformed
        if "_address" not in df.columns:
            if "address" not in df.columns:
                return False
            self.columns.remove("_address")
            self.columns += self.long_address_columns
            self.string_columns += self.long_address_columns
        for col in df.columns:
            if col not in self.columns:
                return False

        # adjust dates
        for _dt in self.date_columns:
            df[_dt] = pd.to_datetime(df[_dt]).dt.date

        # adjusting some columns to be strings
        for col in self.string_columns:
            df[col] = df[col].astype(str)

        df[self.columns]

        return df.set_index("name")

    def adjust_data(self):
        if "_address" in self.df:
            # split _address into address, number, complement
            df_address = self.df["_address"].str.split(",", n=1, expand=True)
            df_address.columns = ["address", "_number"]
            # split number -> number, complement
            df_number = df_address["_number"].str.split(
                " - ", n=1, expand=True
            )
            df_number.columns = ["number", "complement"]
            df_number["number"] = df_number["number"].str.strip().fillna("")
            # join df_number -> df_address
            df_address = df_address.join(df_number)
            # remove _number from df_address
            df_address.drop("_number", axis=1, inplace=True)
            # join df_address -> df
            self.df = self.df.join(df_address)
            # remove _address from df
            self.df.drop("_address", axis=1, inplace=True)

        # remove NaN
        objs = [
            col
            for col in self.df.columns
            if col not in self.date_columns and col != "email"
        ]
        for _obj in objs:
            self.df[_obj] = self.df[_obj].fillna("")

        # clear phones
        phones = [_ph for _ph in self.columns if "phone" in _ph]
        if phones:
            for phone in phones:
                self.df[phone] = (
                    self.df[phone]
                    .apply(lambda x: self.clear_phone(x))
                    .fillna("")
                )

    def generate_files(self):
        # without emails
        without_emails = self.df[self.df["email"].isnull()]
        if without_emails.shape[0] > 0:
            without_emails.to_csv(
                f"{self.path}/without_email/without_email__{self.file}"
            )
        # with emails (with duplicated)
        with_emails = self.df.loc[self.df["email"].notnull()]
        # duplicated emails
        duplicated_emails = with_emails.loc[
            self.df["email"].duplicated(keep=False), :
        ]
        if duplicated_emails.shape[0] > 0:
            duplicated_emails.to_csv(
                f"{self.path}/duplicate_email/duplicate_email__{self.file}"
            )
        # cleaned records to import
        if duplicated_emails.shape[0] > 0:
            cleaned_df = with_emails.drop_duplicates(
                subset=["email"], keep=False
            )
        else:
            cleaned_df = with_emails
        cleaned_df.to_csv(f"{self.path}/{self.file}")

    @staticmethod
    def clear_phone(phone):
        if isinstance(phone, str):
            return "".join(re.findall(r"\d*", phone))
        return phone
