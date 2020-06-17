'''
kds-team.wr-zendesk main class.

'''

import logging
import logging_gelf.handlers
import logging_gelf.formatters
import sys
import os
from datetime import datetime  # noqa
import requests
import base64
import json
import pandas as pd

from kbc.env_handler import KBCEnvHandler
from kbc.result import KBCTableDef  # noqa
from kbc.result import ResultWriter  # noqa


# configuration variables
KEY_EMAIL = 'email'
KEY_PASSWORD = '#password'
KEY_DOMAIN = 'domain'
KEY_FULL_URL = 'full_url'
KEY_FUNCTION = 'function'

MANDATORY_PARS = [
    KEY_EMAIL,
    KEY_PASSWORD,
    KEY_DOMAIN,
    KEY_FULL_URL,
    KEY_FUNCTION
]
MANDATORY_IMAGE_PARS = []

# Default Table Output Destination
DEFAULT_TABLE_SOURCE = "/data/in/tables/"
DEFAULT_TABLE_DESTINATION = "/data/out/tables/"
DEFAULT_FILE_DESTINATION = "/data/out/files/"
DEFAULT_FILE_SOURCE = "/data/in/files/"

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s : [line:%(lineno)3s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S")

if 'KBC_LOGGER_ADDR' in os.environ and 'KBC_LOGGER_PORT' in os.environ:

    logger = logging.getLogger()
    logging_gelf_handler = logging_gelf.handlers.GELFTCPSocketHandler(
        host=os.getenv('KBC_LOGGER_ADDR'), port=int(os.getenv('KBC_LOGGER_PORT')))
    logging_gelf_handler.setFormatter(
        logging_gelf.formatters.GELFFormatter(null_character=True))
    logger.addHandler(logging_gelf_handler)

    # remove default logging to stdout
    logger.removeHandler(logger.handlers[0])

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        KBCEnvHandler.__init__(self, MANDATORY_PARS)
        """
        # override debug from config
        if self.cfg_params.get('debug'):
            debug = True
        else:
            debug = False

        self.set_default_logger('DEBUG' if debug else 'INFO')
        """
        logging.info('Running version %s', APP_VERSION)
        logging.info('Loading configuration...')

        try:
            # self.validate_config(MANDATORY_PARS)
            self.validate_image_parameters(MANDATORY_IMAGE_PARS)
        except ValueError as e:
            logging.error(e)
            exit(1)

    def validate_config_params(self, params_obj, in_tables):
        """
        Injecting input parameter into Component's class
        Validating if the input parameters are in the right format.
        Lower chances of faulty user's configuration
        1. Validate parameters below:
            1. KEY_EMAIL
            2. KEY_PASSWORD
            3. KEY_DOMAIN
        2. Validate if there are any input mappings
        """

        # Validate if config is blank
        # Happens when the configuration is not saved in the UI
        error_message = ''
        if params_obj == {}:
            error_message = 'Configurations are missing. Please configure your component.'
        elif params_obj[KEY_EMAIL] == '' and (params_obj[KEY_DOMAIN] == '' or params_obj[KEY_DOMAIN] == 'DOMAIN'):
            error_message = 'Configurations are missing. Please configure your component.'
        elif params_obj[KEY_PASSWORD] == '' and params_obj[KEY_EMAIL] == '':
            error_message = 'Credentials are missing. Please enter your credentials.'
        elif params_obj[KEY_DOMAIN] == 'DOMAIN' or params_obj[KEY_DOMAIN] == '':
            error_message = 'Zendesk domain is missing. Please enter your domain'
        elif len(in_tables) == 0:
            error_message = 'No input tables are found. Please configure your input files.'
        elif params_obj[KEY_FUNCTION] not in ['CREATE', 'UPDATE']:
            error_message = '{} is not an available function. Please validate your inputs.'.format(
                params_obj[KEY_FUNCTION])

        # Importing Endpoint Mapping
        with open('src/endpoint_mapping.json', 'r') as f:
            self.endpoint_mapping = json.load(f)

        # Validate Input files
        if len(in_tables) > 0 and error_message == '':
            non_exist_endpoint = []
            for table in in_tables:
                table_name = table.split('.csv')[0]
                if table_name not in self.endpoint_mapping:
                    non_exist_endpoint.append(table_name)
            if len(non_exist_endpoint) > 0:
                error_message = 'Input endpoints are not supported: {}'.format(
                    non_exist_endpoint)

        # If error message exists, terminate the component with error
        if error_message != '':
            logging.error(error_message)
            sys.exit(1)

        # Creating input parameters as Component class parameters
        self.email = params_obj[KEY_EMAIL]
        self.password = params_obj[KEY_PASSWORD]
        self.domain = params_obj[KEY_DOMAIN]
        self.full_url = params_obj[KEY_FULL_URL]
        self.function = params_obj[KEY_FUNCTION]

    def _convert_datatype(self, datatype, row_name, row_value, required):
        '''
        Converting a value to its desired datatype
        '''

        tmp_obj = {}
        err_msg = ''
        datatype_type = datatype['type']
        read_only = bool(datatype['read_only']
                         ) if 'read_only' in datatype else False
        if not read_only or required:
            try:
                if datatype_type in ('string', 'date'):
                    tmp_obj[row_name] = str(row_value)
                elif datatype_type == 'array':
                    tmp_obj[row_name] = json.loads(row_value)
                elif datatype_type == 'integer':
                    tmp_obj[row_name] = int(row_value)
                elif datatype_type == 'object':
                    tmp_obj[row_name] = json.loads(row_value)
                elif datatype_type == 'boolean':
                    tmp_obj[row_name] = bool(row_value)
            except Exception as err:
                err_msg = err
                logging.error(err_msg)

        return tmp_obj, err_msg

    def _construct_request_body(self, df, df_headers, endpoint, endpoint_mapping):
        '''
        Constructing the request body for the relative endpoint
        '''

        required_cols = endpoint_mapping[self.function.lower()+'_required']
        construct_bool = True
        request_body = {
            # endpoint: []
            endpoint[:-1]: {}
        }
        # for index, row in df.iterrows():
        # row_json = {}
        for obj in df_headers:
            required = True if obj in required_cols and self.function == 'CREATE' else False
            tmp_obj, err_msg = self._convert_datatype(
                datatype=endpoint_mapping['attributes'][obj],
                row_name=obj,
                # row_value=row[obj],
                row_value=df[obj],
                required=required)
            if err_msg != '':
                construct_bool = False
                return construct_bool, err_msg
            request_body[endpoint[:-1]].update(tmp_obj)
        # if row_json:
        #    request_body[endpoint].append(row_json)

        return construct_bool, request_body

    def _validate_endpoint_headers(self, endpoint, input_headers, endpoint_mapping):
        '''
        Validate if the columns of the input files are supported for that endpoint
        '''

        # Check if required columns are included
        required_cols = endpoint_mapping[self.function.lower()+'_required']

        # Check parameters
        validate_bool = True
        err_msg = ''

        required_cols_check = all(
            col in input_headers for col in required_cols)
        logging.info('[{}] required columns check: {}'.format(
            endpoint, required_cols_check))
        if not required_cols_check:
            err_msg = '[{}] missing required columns: {}'.format(
                endpoint, required_cols)
            logging.error(err_msg)
            validate_bool = False
            # sys.exit(1)

        # Check if input columns exist as an available attribute
        if validate_bool:
            endpoint_attributes = endpoint_mapping['attributes']
            endpoint_attributes_check = True
            non_exist_attributes = []
            for col in input_headers:
                if col not in endpoint_attributes:
                    non_exist_attributes.append(col)
                    endpoint_attributes_check = False

            if not endpoint_attributes_check:
                err_msg = 'Input columns not supported [{}]: {}'.format(
                    endpoint, non_exist_attributes)
                logging.error(err_msg)
                validate_bool = False
                # sys.exit(1)

        return validate_bool, err_msg

    def _construct_log(self,
                       endpoint,
                       request_bool,
                       request_status=None,
                       request_body=None,
                       request_response=None,
                       row_df=None):
        '''
        Constructing Log messages
        '''

        tmp_log = {
            'request_date': NOW,
            # 'file_validation': '',
            # 'file_validation_description': '',
            'request_bool': request_bool,
            'request_status': request_status,
            # 'request_body': json.dumps(request_body[endpoint[:-1]])
            'request_body': json.dumps(request_body)
            # 'request_response': json.dumps(request_response[endpoint[:-1]])
        }
        if request_status in [200, 201]:
            tmp_log['request_response'] = json.dumps(
                request_response[endpoint[:-1]])
        else:
            tmp_log['request_response'] = json.dumps(
                request_response)

        # Adding ID field if its a UPDATE function
        if self.function == 'UPDATE':
            tmp_log['id'] = row_df['id'] if row_df is not None else ''

        return tmp_log

    def get_basic_auth(self, email, password):
        '''
        Generating Base64 authentication header
        '''

        auth_string = '{}:{}'.format(email, password)
        auth_string_encode = base64.b64encode(auth_string.encode()).decode()

        header = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % auth_string_encode
        }

        return header

    def post_request(self, url, payload):
        '''
        Generic Zendesk Post request
        '''

        if self.function == 'CREATE':
            r = requests.post(url, headers=self.request_header,
                              data=json.dumps(payload))
        elif self.function == 'UPDATE':
            r = requests.put(url, headers=self.request_header,
                             data=json.dumps(payload))

        return r.status_code, r.json()

    def get_tables(self, tables, mapping):
        """
        Evaluate input and output table names.
        Only taking the first one into consideration!
        mapping: input_mapping, output_mappings
        """
        # input file
        table_list = []
        for table in tables:
            name = table["full_path"]  # noqa
            if mapping == "input_mapping":
                destination = table["destination"]
            elif mapping == "output_mapping":
                destination = table["source"]
            table_list.append(destination)

        return table_list

    def output_log(self, log, endpoint):
        '''
        Outputting the log of the requested endpoint
        '''

        log_df = pd.DataFrame(log)
        output_filename = '{0}{1}_{2}_log.csv'.format(
            DEFAULT_TABLE_DESTINATION, endpoint, self.function.lower())

        if self.function == 'CREATE':
            primary_key = [
                'request_date',
                'request_body'
            ]
            columns = [
                'request_date',
                'request_bool',
                'request_body',
                'request_status',
                'request_response'
            ]
        elif self.function == 'UPDATE':
            primary_key = [
                'request_date',
                'id',
                'request_body'
            ]
            columns = [
                'request_date',
                'id',
                'request_bool',
                'request_body',
                'request_status',
                'request_response'
            ]

        if not os.path.isfile(output_filename):
            with open(output_filename, 'w') as f:
                log_df.to_csv(f, index=False, columns=columns)
            f.close()
            self.product_manifest(
                file_name=output_filename, primary_key=primary_key)
        else:
            with open(output_filename, 'a') as f:
                log_df.to_csv(f, index=False, header=False, columns=columns)
            f.close()

    def product_manifest(self, file_name, primary_key):
        '''
        Producing manifest files
        '''

        output_manifest = file_name+'.manifest'
        manifest_template = {
            'incremental': True,
            'primary_key': primary_key
        }

        with open(output_manifest, 'w') as file_out:
            json.dump(manifest_template, file_out)
            logging.info(
                "Output manifest file [{}] produced.".format(output_manifest))

    def run(self):
        '''
        Main execution code
        '''

        # Get proper list of tables
        in_tables = self.configuration.get_input_tables()
        in_table_names = self.get_tables(in_tables, 'input_mapping')
        logging.info("IN tables mapped: "+str(in_table_names))

        params = self.cfg_params  # noqa
        # Validating and assigning input parameters
        self.validate_config_params(
            params_obj=params, in_tables=in_table_names)
        # Constructing request header
        self.request_header = self.get_basic_auth(self.email, self.password)

        logging.info('Selected function: {}'.format(self.function))
        # Looping through the endpoints (input files)
        for table in in_table_names:
            logging.info('Parsing {}...'.format(table))

            endpoint = table.split('.csv')[0].lower()
            endpoint_mapping = self.endpoint_mapping[endpoint]
            endpoint_url = '{}/api/v2/{}.json'.format(self.full_url, endpoint)

            # Parsing requests in chunks to converse memory capacity
            for chunks in pd.read_csv(DEFAULT_TABLE_SOURCE+table, chunksize=100):
                log = []
                input_headers = list(chunks.columns)
                # Validate Input files headers
                input_valid_bool, err_msg = self._validate_endpoint_headers(
                    endpoint=endpoint,
                    input_headers=input_headers,
                    endpoint_mapping=endpoint_mapping)

                # Break for loop if input file is not valid
                if not input_valid_bool:
                    tmp_log = self._construct_log(
                        endpoint=endpoint,
                        request_bool=False,
                        request_body=err_msg
                    )
                    log.append(tmp_log)
                    # Breaking current's endpoint for loop
                    # and Output the log for the current table
                    self.output_log(log, endpoint)
                    break

                else:
                    for index, row in chunks.iterrows():
                        if self.function == 'CREATE':
                            request_url = endpoint_url
                        elif self.function == 'UPDATE':
                            request_url = endpoint_url.replace(
                                '.json', '/{}.json'.format(row['id']))

                        # Construct request body
                        body_construct_bool, request_body = self._construct_request_body(
                            df=row,
                            df_headers=input_headers,
                            endpoint=endpoint,
                            endpoint_mapping=endpoint_mapping)

                        # Vaidate if request body is constructed
                        if body_construct_bool:
                            # Zendesk request
                            request_status, request_response = self.post_request(
                                url=request_url, payload=request_body)

                            # Outputting log
                            tmp_log = self._construct_log(
                                endpoint=endpoint,
                                request_bool=True,
                                request_status=request_status,
                                request_body=request_body[endpoint[:-1]],
                                request_response=request_response,
                                row_df=row
                            )
                        else:
                            tmp_log = self._construct_log(
                                endpoint=endpoint,
                                request_bool=False,
                                request_body=request_body[endpoint[:-1]],
                                row_df=row
                            )

                        log.append(tmp_log)

                self.output_log(log, endpoint)

        logging.info("Zendesk Writer finished")


"""
        Main entrypoint
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug = sys.argv[1]
    else:
        debug = True
    comp = Component(debug)
    comp.run()
