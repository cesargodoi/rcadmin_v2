import re
from io import StringIO

import pandas as pd

# lists to sanitize class
COLUMNS = [
    "name",
    "gender",
    "birth",
    "address",
    "number",
    "complement",
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
    "obs",
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
        df = pd.read_csv(StringIO(self.file.read().decode("utf-8")))

        df = df.fillna("")

        for col in df.columns:
            if col not in self.columns:
                return False

        # adjust dates
        for _dt in self.date_columns:
            df[_dt] = pd.to_datetime(df[_dt], format="%Y-%m-%d").dt.date

        # adjusting some columns to be strings
        for col in self.string_columns:
            df[col] = df[col].astype(str)

        df[self.columns]
        return df.set_index("name")

    def adjust_data(self):
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
        without_emails = self.df[
            self.df["email"].isnull() | (self.df["email"] == "")
        ]
        if without_emails.shape[0] > 0:
            without_emails.to_csv(
                f"{self.path}/without_email/without_email__{self.file}"
            )

        # with emails (with duplicated)
        with_emails = self.df[
            self.df["email"].notnull() & (self.df["email"] != "")
        ]

        # duplicated emails
        duplicates = with_emails[
            with_emails.duplicated(subset="email", keep=False)
        ]
        duplicated_emails = with_emails[
            with_emails["email"].isin(duplicates["email"])
        ]
        if duplicated_emails.shape[0] > 0:
            duplicated_emails.to_csv(
                f"{self.path}/duplicated_email/duplicated_email__{self.file}"
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
