# coding: utf-8

"""
    Insights Service API -test

    ## Introduction  Swaggerâ¢ is a project used to describe and document RESTful APIs. This section provides an overview of the API design, methods, and supported use cases.    Most of the endpoints accept **JSON** as input and return **JSON** responses.  ```  Content-type: application/json   Accept: application/json  ```  ## Resources  A resource in Swagger is an entity that has a set of exposed operations. The entity can represent an actual object (account, users..) or a set of logical operations collated together. It is up to the specification user to decide whether sub-resources should be referred to as part of their main resource or as a resource of their own. For example, assume the following URL set:     ```    /users         -GET                   POST                    /users/{id}    -GET                   PATCH                   DELETE   ```    ## CRUD Operations  The platform supports Create, Read, Update, and Delete operations on most resources. You can review the standards for these operations and their standard parameters below.    Some endpoints have special behavior as exceptions.    ### Create  To create a resource, you typically submit an HTTP POST request with the resource's required metadata in the request body. The response returns a 201 Created response code upon success with the resource's metadata, including its internal id, in the response body.    ### Read  The HTTP GET request can be used to read a resource or to list a number of resources.    A resource's id can be submitted in the request parameters to read a specific resource. The response usually returns a 200 OK response code upon success, with the resource's metadata in the response body.    If a GET request does not include a specific resource id, it is treated as a list request. The response usually returns a 200 OK response code upon success, with an object containing a list of resources' metadata in the response body.    When reading resources, some common query parameters are usually available. e.g. :  ```  v1/users?size=25&page=1  ```  **Query Parameter Type Description**  - size should be between 10 and 300 (default value 50)    - page should be a zero or any positive number (default value 0)    ### Update  Updating a resource requires the resource id, and is typically done using an HTTP PATCH request, with the fields to modify in the request body. The response usually returns a 200 OK response code upon success, with information about the modified resource in the response body.    ### Delete  Deleting a resource requires the resource id and is typically executing via an HTTP DELETE request. The response usually returns a 204 No Content response code upon success.    ## Trying the API  You can use [Swagger UI](https://swagger.io/tools/swagger-ui/) or any third party client such as ,[Postman](https://www.postman.com/), [cURL](https://curl.se/) etc. to test the REST API.    **Swagger UI**    - Authorize API by clicking on **Authorize** button.   - Select an API resource  - Click on **Try it out**   - filterQuery (Parameters): If required add parameters else keep blank json  ```   e.g.   {           \"size\": 300,           \"page\": 0,          }             e.g.   {          }            ```              - Fill the headers like TenantType, OrgId & X-Api-Key   - Click on **Execute**    **Curl**  ```  curl -X 'GET' \\  'http://localhost:8085/api/v1/crops' \\  -H 'accept: application/json' \\  -H 'TenantType: SMARTRISK' \\  -H 'orgId: test' \\  -H 'X-Api-Key: qwjokooopppp' \\  -H 'Authorization: Bearer jklkopalkddlplplllllllllll2340k'  ```  Using a graphical tool such as Postman, it is possible to import the API specifications directly:    - Download the API specification by clicking the **Download** button at top of this document  - Import the JSON specification in the graphical tool of your choice.  - In *Postman*, you can click the import button at the top    ## Enabling CORS  [Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a browser security feature that restricts HTTP requests that are initiated from scripts running in the browser.      ## Authentication  The API authentication process validates the identity of the client attempting to make a connection by using an authentication protocol. REST API support many authentication methods which are as follows :    **HTTP Authentication Schemes**:    - Basic  - Bearer  - Digest  - OAuth and others...    Insights Service uses Bearer Authentication (also called token authentication) is an HTTP authentication scheme that involves security tokens called bearer tokens.    **Access Token** can be generated by following API by passing valid request payload (see Authenticate API)  ```  POST   /api/v1/authenticate  ```    For more details on authentication, see [API Authentication](https://www.3pillarglobal.com/insights/most-popular-api-authentication-methods).    ## Errors  The REST API reports errors by returning an appropriate HTTP response code, for example 404 (Not Found), and a JSON response. Any HTTP response code that is not in the range 200 - 299 is considered an error.    ### BadRequest (400)  This response means that the server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing). To resolve this, please ensure that your syntax is correct.  ### Unauthorized (401)  Indicates that the request requires user authentication information. The client may repeat the request with a suitable Authorization header field.    ### Forbidden (403)  Unauthorized request. The client does not have access rights to the content. Unlike 401, the clientâs identity is known to the server.    ### NotFound (404)  The server can not find the requested resource.    ### MethodNotAllowed (405)  The request HTTP method is known by the server but has been disabled and cannot be used for that resource.  ### NotAcceptable (406)  The server does not find any content that conforms to the criteria given by the user agent in header sent in the request.  ### AlreadyExists  The request could not be completed due to a conflict with the current state of the target resource, e.g. the resource it tries to create already exists.  ### Internal Server Error (500)  The server encountered an unexpected condition that prevented it from fulfilling the request.    For more details on HTTP Status code see [HTTP Status Codes](https://restfulapi.net/http-status-codes/)   # noqa: E501

    OpenAPI spec version: v1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import insights_python_client
from insights_python_client.api.metrics_api import MetricsApi  # noqa: E501
from insights_python_client.rest import ApiException


class TestMetricsApi(unittest.TestCase):
    """MetricsApi unit test stubs"""

    def setUp(self):
        self.api = MetricsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_list_all3(self):
        """Test case for list_all3

        Get satellite metrics  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
