
"""
https://github.com/mvantellingen/python-zeep
Inspect WSDL:
python -m zeep http://docs.virtualsolar.org/WSDL

Prefixes:
     xsd: http://www.w3.org/2001/XMLSchema
     ns0: http://virtualsolar.org/VSO/VSOi

Global elements:


Global types:
     xsd:anyType
     ns0:DataContainer(datarequestitem: ns0:DataRequestItem[])
     ns0:DataItem(provider: xsd:string, url: xsd:string, fileiditem: ns0:FileidItem)
     ns0:DataRequestItem(provider: xsd:string, fileiditem: ns0:FileidItem)
     ns0:Extent(x: xsd:string, y: xsd:string, width: xsd:string, length: xsd:string, type: xsd:string)
     ns0:Extra(thumbnail: ns0:Thumbnail, flags: xsd:string)
     ns0:Field(fielditem: xsd:string[])
     ns0:FileidItem(fileid: xsd:string[])
     ns0:GetDataItem(dataitem: ns0:DataItem[])
     ns0:GetDataRequest(method: ns0:MethodItem, info: ns0:Info, datacontainer: ns0:DataContainer)
     ns0:GetDataResponseItem(version: xsd:string, info: {infoitem: xsd:string[]}, provider: xsd:string, getdataitem: ns0:GetDataItem, status: xsd:string, debug: xsd:string, details: xsd:string, method: ns0:MethodItem)
     ns0:Info(email: xsd:string, host: xsd:string, user: xsd:string, directory: xsd:string, password: xsd:string, address: xsd:string, required: xsd:string, site: xsd:string)
     ns0:MethodItem(methodtype: xsd:string[])
     ns0:ProviderQueryResponse(version: xsd:float, provider: xsd:string, no_of_records_found: xsd:int, no_of_records_returned: xsd:int, record: ns0:QueryResponseBlockArray, error: xsd:string, debug: xsd:string, status: xsd:string)
     ns0:QueryRequest(version: xsd:float, block: ns0:QueryRequestBlock)
     ns0:QueryRequestBlock(time: ns0:Time, provider: xsd:string, source: xsd:string, instrument: xsd:string, physobs: xsd:string, wave: ns0:Wave, extent: ns0:Extent, field: ns0:Field, pixels: xsd:string, level: xsd:string, resolution: xsd:string, detector: xsd:
string, filter: xsd:string, sample: xsd:string, quicklook: xsd:string, pscale: xsd:string)
     ns0:QueryResponse(provideritem: ns0:ProviderQueryResponse[])
     ns0:QueryResponseBlock(provider: xsd:string, source: xsd:string, instrument: xsd:string, physobs: xsd:string, time: ns0:Time, wave: ns0:Wave, extent: ns0:Extent, size: xsd:float, extra: ns0:Extra, info: xsd:string, datatype: xsd:string, fileurl: xsd:string
, fileid: xsd:string)
     ns0:QueryResponseBlockArray(recorditem: ns0:QueryResponseBlock[])
     ns0:Thumbnail(hires: xsd:string, lowres: xsd:string)
     ns0:Time(start: xsd:string, end: xsd:string, near: xsd:string)
     ns0:VSOGetDataRequest(version: xsd:string, request: ns0:GetDataRequest)
     ns0:VSOGetDataResponse(getdataresponseitem: ns0:GetDataResponseItem[])
     ns0:Wave(wavemin: xsd:string, wavemax: xsd:string, waveunit: xsd:string, wavetype: xsd:string)
     xsd:ENTITIES
     xsd:ENTITY
     xsd:ID
     xsd:IDREF
     xsd:IDREFS
     xsd:NCName
     xsd:NMTOKEN
     xsd:NMTOKENS
     xsd:NOTATION
     xsd:Name
     xsd:QName
     xsd:anySimpleType
     xsd:anyURI
     xsd:base64Binary
     xsd:boolean
     xsd:byte
     xsd:date
     xsd:dateTime
     xsd:decimal
     xsd:double
     xsd:duration
     xsd:float
     xsd:gDay
     xsd:gMonth
     xsd:gMonthDay
     xsd:gYear
     xsd:gYearMonth
     xsd:hexBinary
     xsd:int
     xsd:integer
     xsd:language
     xsd:long
     xsd:negativeInteger
     xsd:nonNegativeInteger
     xsd:nonPositiveInteger
     xsd:normalizedString
     xsd:positiveInteger
     xsd:short
     xsd:string
     xsd:time
     xsd:token
     xsd:unsignedByte
     xsd:unsignedInt
     xsd:unsignedLong
     xsd:unsignedShort

Bindings:
     Soap11Binding: {http://virtualsolar.org/VSO/VSOi}VSOiBinding

Service: VSOiService
     Port: nsoTestVSOi (Soap11Binding: {http://virtualsolar.org/VSO/VSOi}VSOiBinding)
         Operations:
            GetData(body: ns0:VSOGetDataRequest) -> body: ns0:VSOGetDataResponse
            Query(body: ns0:QueryRequest) -> body: ns0:QueryResponse

     Port: nsoVSOi (Soap11Binding: {http://virtualsolar.org/VSO/VSOi}VSOiBinding)
         Operations:
            GetData(body: ns0:VSOGetDataRequest) -> body: ns0:VSOGetDataResponse
            Query(body: ns0:QueryRequest) -> body: ns0:QueryResponse

"""

# https://vso.nascom.nasa.gov/API/VSO_API.html
import socket
import warnings

from urllib.error import URLError, HTTPError
from urllib.request import urlopen
import zeep


# --------- >>> borrowed from the 20040102000000 package ----------
DEFAULT_URL_PORT = [{'url': 'http://docs.virtualsolar.org/WSDL/VSOi_rpc_literal.wsdl',
                     'port': 'nsoVSOi'},
                    {'url': 'https://sdac.virtualsolar.org/API/VSOi_rpc_literal.wsdl',
                     'port': 'sdacVSOi'}]


def check_connection(url):
    try:
        return urlopen(url).getcode() == 200
    except (socket.error, socket.timeout, HTTPError, URLError) as e:
        print("Connection to " +url+ " failed with error {e}. Retrying with different url and port.")
        return None


def get_online_vso_url():
    """
    Return the first VSO url and port combination that is online.
    """
    for mirror in DEFAULT_URL_PORT:
        if check_connection(mirror['url']):
            return mirror


def build_client(url=None, port_name=None, **kwargs):
    """
    Construct a `zeep.Client` object to connect to VSO.

    Parameters
    ----------
    url : `str`
        The URL to connect to.

    port_name : `str`
        The "port" to use.

    kwargs : `dict`
        All extra keyword arguments are passed to `zeep.Client`.

    Returns
    -------

    `zeep.Client`
    """
    if url is None and port_name is None:
        mirror = get_online_vso_url()
        if mirror is None:
            raise ConnectionError("No online VSO mirrors could be found.")
        url = mirror['url']
        port_name = mirror['port']
    elif url and port_name:
        if not check_connection(url):
            print("Can't connect to url {url}")
    else:
       print("Both url and port_name must be specified if either is.")

#    if "plugins" not in kwargs:
#        kwargs["plugins"] = [SunPyLoggingZeepPlugin()]

    client = zeep.Client(url, port_name=port_name, **kwargs)
    client.set_ns_prefix('VSO', 'http://virtualsolar.org/VSO/VSOi')
    return client



# --------- borrowed from the sunpy.net.vso package <<< ----------

# --------------------------------------------------

"""
Service: SoapResponder
     Port: SoapResponderPortType (Soap11Binding: {http://www.SoapClient.com/xml/SoapResponder.wsdl}SoapResponderBinding)
         Operations:
            Method1(bstrParam1: xsd:string, bstrParam2: xsd:string) -> bstrReturn: xsd:string
"""
wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
client = zeep.Client(wsdl=wsdl)
print(client.service.Method1('Zeep', 'is cool'))

# --------------------------------------------------

wsdl = "http://docs.virtualsolar.org/WSDL"
settings = zeep.Settings(strict=False, xml_huge_tree=True)
client = zeep.Client(wsdl=wsdl, settings=settings)



# https://python-zeep.readthedocs.io/en/master/datastructures.html

type = client.get_type('ns0:VSOGetDataRequest')
print(type)
# VSOGetDataRequest({http://virtualsolar.org/VSO/VSOi} VSOGetDataRequest(
# version: xsd:string,
# request: {http://virtualsolar.org/VSO/VSOi}GetDataRequest))

type = client.get_type('ns0:QueryRequest')
print(type)
# QueryRequest({http://virtualsolar.org/VSO/VSOi}QueryRequest(
# version: xsd:float,
# block: {http://virtualsolar.org/VSO/VSOi}QueryRequestBlock))

type = client.get_type('ns0:QueryRequestBlock')
print(type)
# QueryRequestBlock({http://virtualsolar.org/VSO/VSOi}QueryRequestBlock(
# time: {http://virtualsolar.org/VSO/VSOi}Time,
# provider: xsd:string, source: xsd:string,
# instrument: xsd:string,
# physobs: xsd:string,
# wave: {http://virtualsolar.org/VSO/VSOi}Wave,
# extent: {http://virtualsolar.org/VSO/VSOi}Extent,
# field: {http://virtualsolar.org/VSO/VSOi}Field,
# pixels: xsd:string,
# level: xsd:string,
# resolution: xsd:string,
# detector: xsd:string,
# filter: xsd:string,
# sample: xsd:string,
# quicklook: xsd:string,
# pscale: xsd:string))

type = client.get_type('ns0:Time')
print(type)
# Time({http://virtualsolar.org/VSO/VSOi}Time(
# start: xsd:string, 
# end: xsd:string, 
# near: xsd:string)


request_type = client.get_type('ns0:GetDataRequest')
print(type)
# GetDataRequest({http://virtualsolar.org/VSO/VSOi}GetDataRequest(
# method: {http://virtualsolar.org/VSO/VSOi}MethodItem,
# info: {http://virtualsolar.org/VSO/VSOi}Info,
# datacontainer: {http://virtualsolar.org/VSO/VSOi}DataContainer))

type = client.get_type('ns0:MethodItem')
print(type)

type = client.get_type('ns0:Info')
print(type)

type = client.get_type('ns0:DataContainer')
print(type)

#--------------------------------------------------

factory = client.type_factory('ns0')
time = factory.Time(start=20040101000000,end=20040102000000)
block = factory.QueryRequestBlock(time=time, instrument='EIT')
body = factory.QueryRequest(version=0.6, block=block)

#body = body_type(version='0.6', request = request )

api = build_client()
QueryRequest = api.get_type('VSO:QueryRequest')
VSOQueryResponse = api.get_type('VSO:QueryResponse')
responses = []

VSOQueryResponse(api.service.Query(
    QueryRequest(block=block)
))



node = client.create_message(client.service, 'Query', body=body)
print(node)

with client.settings(raw_response=True):
    response = client.service.Query(body=body)
    print(response)

#VSOGetDataRequest= "<VSO:request xsi:type="VSO:QueryRequest"><block><VSO:instrument xsi:type="xsd:string">EIT</VSO:instrument><time><VSO:start xsi:type="xsd:string">20040101000000</VSO:start><VSO:end xsi:type="xsd:string">20040102000000</VSO:end></time></block><VSO:version xsi:type="xsd:float">0.6</VSO:version></VSO:request>"




#query_request = "instrument=EIT;time.start=20040101000000;time.end=20040102000000;version=0.6"
#client.service.Query('body')