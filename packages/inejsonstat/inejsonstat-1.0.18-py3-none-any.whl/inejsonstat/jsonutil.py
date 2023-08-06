import datetime
import logging
import os
import pathlib
import re

import unidecode
import yaml

from inejsonstat.main_logger import logger


class JsonUtil:

    @staticmethod
    # Reads the config yaml file
    def read_config_yaml(input_yaml):
        """Reads an input yaml file

                Parameters
                ----------
                input_yaml : yaml

                Returns
                -------
               The data contained in the yaml
        """
        with open(input_yaml, "r") as yaml_file:
            logger.debug("JsonUtil || Opening yaml file")
            logger.debug("JsonUtil || Reading yaml file")
            yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            logger.debug("JsonUtil || Config file read successful")
        return yaml_data

    @staticmethod
    # Checks if the input is an integer
    def check_int(input_int):
        """Checks if an input is an integer

                Parameters
                ----------
                input_int : string

                Returns
                -------
                Boolean indicating if its an integer
        """
        return input_int.isdigit()

    @staticmethod
    # Normalizes the string to a valid attribute name
    def normalize_string(input_str):
        """Normalizes a string

                Parameters
                ----------
                input_str : string

                Returns
                -------
               Normalized string
        """
        logging.info("Executing module [normalize_string]")
        if input_str[0].isdigit():
            input_str = "n" + input_str

        unaccented_string = unidecode.unidecode(input_str)
        # Convert to lower case
        lower_str = unaccented_string.lower()

        # remove all punctuation except words and space
        no_punc_str = re.sub(r'[^\w\s]', '', lower_str)

        # Removing possible leading and trailing whitespaces
        no_trail_str = no_punc_str.strip()

        # Replace white spaces with underscores
        no_spaces_string = no_trail_str.replace(" ", "_")

        return no_spaces_string

    @staticmethod
    # Normalizes the string to a valid attribute name
    def normalize_enum(input_str):
        """Normalizes a string to be an Enum name

                Parameters
                ----------
                input_str : string

                Returns
                -------
               Normalized string
        """
        logging.info("Executing module [normalize_enum]")
        if input_str[0].isdigit():
            input_str = "n" + input_str

        unaccented_string = unidecode.unidecode(input_str)
        # Convert to lower case
        upper_str = unaccented_string.upper()

        # remove all punctuation except words and space
        no_punc_str = re.sub(r'[^\w\s]', '', upper_str)

        # Removing possible leading and trailing whitespaces
        no_trail_str = no_punc_str.strip()

        # Replace white spaces with underscores
        no_spaces_string = no_trail_str.replace(" ", "_")

        return no_spaces_string

    @staticmethod
    def check_repeated(input_string, input_list):
        """Checks if an input string is in an input list and if so, modifies it

                Parameters
                ----------
                input_string : string
                input_list : [string]

                Returns
                -------
               Modified string
        """
        out_string = input_string
        aux_string = input_string
        i = 1
        flag = True
        while flag:
            if aux_string in input_list:
                aux_string = "N" + str(i) + out_string
            else:
                flag = False
                out_string = aux_string

        return out_string

    @staticmethod
    def date_conversor(input_date, datetype: str = None):
        """Converts the input date in a valid format to build the url

                Parameters
                ----------
                input_date : string or date from datetime
                datetype : string

                Returns
                -------
               Modified string
        """
        date = None
        if type(input_date) == datetime.date:
            logger.debug("Date is a datetime.date")
            date = JsonUtil.transform_date_format(input_date)
        elif type(input_date) == str:
            logger.debug("Date is a string")
            flag = JsonUtil.check_date(input_date)
            if flag:
                input_date = input_date.replace('&', "&date=")
                date = input_date
            else:
                logger.debug("Wrong date string format")
                print("Wrong date string format")
        elif isinstance(input_date, list):
            logger.debug("Date is a list")
            if datetype == "range":
                aux_date = []
                for i in range(0, 2):
                    aux_date.append(JsonUtil.date_conversor(input_date[i]))
                if aux_date[0] < aux_date[1]:
                    date = aux_date[0] + ":" + aux_date[1]
                else:
                    date = aux_date[1] + ":" + aux_date[0]

            elif datetype == "list":
                logger.info("Correct date type")
                date = JsonUtil.date_conversor(input_date[0])
                for i in range(1, len(input_date)):
                    date = date + "&" + "date=" + JsonUtil.date_conversor(input_date[i])
                logger.debug("Date is " + date)
            else:
                logger.debug("Date arrays must be of type range or list")

        return date

    @staticmethod
    def transform_date_format(input_date: datetime.date):
        """Converts the input date in a valid format to build the url

                Parameters
                ----------
                input_date : date from datetime

                Returns
                -------
               String from the time
        """
        return input_date.strftime("%Y%m%d")

    @staticmethod
    # Checks if there's a date parameter in the config file and if it matches the allowed formats
    def check_date(date):
        """Checks the format of a input date

                Parameters
                ----------
                date : string

                Returns
                -------
               Boolean denoting if its correct and modified string
        """
        flag_date = False
        if date == '':
            logger.debug("UrlBuilder || Module [check_date], No date parameter")
            print("no date")
        else:
            base_pattern = r"[0-9]{4}[0-1]{1}[0-9]{1}[0-3]{1}[0-9]{1}"
            pattern1 = r"\b" + base_pattern + r"\Z"
            matcher1 = re.compile(pattern1)
            pattern2 = r"\b" + base_pattern + r"[:]" + base_pattern + r"\Z"
            matcher2 = re.compile(pattern2)
            pattern3 = r"\b" + base_pattern + r"(&" + base_pattern + r")+" + r"\Z"
            matcher3 = re.compile(pattern3)

            if matcher3.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD&YYYYMMDD")
                flag_date = True
            elif matcher2.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD:YYYYMMDD")
                flag_date = True
            elif matcher1.match(date):
                logger.info("UrlBuilder || Date parameter valid, format: YYYYMMDD")
                flag_date = True
            else:
                exception_message = 'UrlBuilder || Module [check_date], Date parameter format invalid'
                logger.debug(exception_message)
                print("Format invalid")
        return flag_date, date

    @staticmethod
    def file_name_builder(target: str = None, language: str = None, date: str = None, nult=None):
        """Builds file name for cache management

                Parameters
                ----------
                target : string
                language : string
                date : string
                nult : string

                Returns
                -------
               Generated file name
        """
        file_name = target + "_" + language
        if date is not None:
            date = date.replace(":", "_")
            date = date.replace('date=', '')
            file_name = file_name + "_" + date
        if nult is not None:
            file_name = file_name + "_" + str(nult)
        return file_name

    @staticmethod
    def get_ttl():
        """Gets the value of the cache time to live
                Returns
                -------
               Generated time to live as numeric
        """
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        path = os.path.join(config_path, "config.yaml")
        yaml = JsonUtil.read_config_yaml(path)
        ttl_raw = yaml[0]['Details']['ttl']
        pattern_year = r"\b[yY][0-9]{1,2}\Z"
        matcher_year = re.compile(pattern_year)
        pattern_month = r"\b[mM][0-9]{1,2}\Z"
        matcher_month = re.compile(pattern_month)
        pattern_week = r"\b[wW][0-9]{1,2}\Z"
        matcher_week = re.compile(pattern_week)
        pattern_day = r"\b[dD][0-9]{1,2}\Z"
        matcher_day = re.compile(pattern_day)
        pattern_hour = r"\b[hH][0-9]{1,2}\Z"
        matcher_hour = re.compile(pattern_hour)
        pattern_minute = r"\b[uU][0-9]{1,2}\Z"
        matcher_minute = re.compile(pattern_minute)
        splitted = ttl_raw.split(" ")
        total_time = 0
        for a in splitted:
            if matcher_year.match(a):
                total_time = total_time + int(a[1:]) * 365 * 24 * 60 * 60
            if matcher_month.match(a):
                total_time = total_time + int(a[1:]) * 30 * 24 * 60 * 60
            if matcher_week.match(a):
                total_time = total_time + int(a[1:]) * 7 * 24 * 60 * 60
            if matcher_day.match(a):
                total_time = total_time + int(a[1:]) * 24 * 60
            if matcher_hour.match(a):
                total_time = total_time + int(a[1:]) * 60 * 60
            if matcher_minute.match(a):
                total_time = total_time + int(a[1:]) * 60
        return total_time

    @staticmethod
    def rename_old_file(file_name):
        """Renames a given file from cache once its time is up

                Parameters
                ----------
                file_name : string
        """
        old, extension = os.path.splitext(file_name)
        time = pathlib.Path(file_name).stat().st_mtime
        dt = datetime.datetime.fromtimestamp(time)
        dtt = dt.strftime("%Y_%m_%d_%H_%M")
        new = old + "_OLD_" + dtt + extension
        os.rename(file_name, new)
