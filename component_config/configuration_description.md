The component takes tables from the input mapping and create/updates records in Zendesk API. The table names from the input mapping will be used to define the Zendesk object the users wish to create/update. Example: users.csv will be creating/updating Zendesk's User endpoint.

## Configuration Parameters
1. Login Email
    - Zendesk account login email
2. API Token
    - Zendesk account API token
    - You can obtain API tokens from the Zendesk Support admin interface at Admin > Channels > API 
3. Zendesk Domain
    - The domain of the Zendesk instance
4. Zendesk URL
    - This configuration is generated automatically from the input of `Zendesk Domain`
5. Function
    - Defines the type of request user wants to perform for all the endpoints define in the input mapping
    - CREATE
        - performing `POST` request to the endpoints defined
    - UPDATE
        - Performing `PUT` request to the endpoints defined

## Endpoint Specifications
The table names from the input mapping will be used to define the Zendesk endpoint the users wish to perform the specified `Function` (CREATE/UPDATE).
Example: users.csv will be creating/updating Zendesk's User endpoint.

## Supported Endpoints
1. [users](https://developer.zendesk.com/rest_api/docs/support/users)
2. [tickets](https://developer.zendesk.com/rest_api/docs/support/tickets)
    - Account inputted in the configuration will be used as the requester_id. If user wants to alter the request_id, please perform such action via `UPDATE` request.
3. [organizations](https://developer.zendesk.com/rest_api/docs/support/organizations)
4. [groups](https://developer.zendesk.com/rest_api/docs/support/groups)
5. [ticket_fields](https://developer.zendesk.com/rest_api/docs/support/ticket_fields)
6. [organization_fields](https://developer.zendesk.com/rest_api/docs/support/organization_fields)
7. [user_fields](https://developer.zendesk.com/rest_api/docs/support/user_fields)

*Please visit [Endpoint Parameters](https://bitbucket.org/kds_consulting_team/kds-team.wr-zendesk/src/master/docs/endpoint_parameters.md) for list of supported parameters and required parameters*

All columns from the input mappings will be converted as a request parameter object for the API request and they need to be valid for the supported endpoint. Each combinatino of function and endpoint contains required parameters for the API request. <br>
For `CREATE` requests, the input tables need to contain columns defined in the `CREATE_required` fields. <br>
For `UPDATE` requests, the input tables need to contain columsn defined in the `UPDATE_required` fields.

### Supported Endpoints DataType
The value of the Input table's column need to match with the DataType for the respective parameters defined in [Endpoint Parameters](https://bitbucket.org/kds_consulting_team/kds-team.wr-zendesk/src/master/docs/endpoint_parameters.md). The writer will not perform API requests for rows having misaligned Datatypes. All parameters that have a `ReadOnly` configured as True are not available as one of the request parameters. If `ReadOnly` parameter is configured within the input, it will be omitted from the API requests.

| DataType | Descriptions |
|-|-|
| string | Values will be sent as a `STR`. |
| integer | Values will be converted to `INT` in the request parameters. |
| boolean | Values will be converted to `BOOL`  in the request parameters. |
| date | Values will be send as a `STR`.|
| array | Values need to be a valid `LIST`. Values will be sent as a `JSON LIST` object. |
| object | Values need to be a valid `JSON` object. |
| attachment | `Not supported` |
| via | `Not supported` |

## Log Outputs
Unless users have the invalid account information in the configurations or invalid endpoints specified in the input mappings, the component will not fail even when a API request failed. 
A log will contain wether or not an API request went through. If not, a description from the API response will be available in one of the columns of the log. 
