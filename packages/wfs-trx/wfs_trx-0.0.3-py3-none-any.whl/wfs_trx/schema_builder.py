from typing import List, Tuple, Union



def trx(
    namespaces: List[dict],
    value: str
) -> str:
    return f"""<wfs:Transaction service="WFS" version="1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" {' '.join(['%s="%s"' % (ns['key'], ns['val']) for ns in namespaces])}>{value}</wfs:Transaction>"""

def get_feature(
    namespaces: List[dict],
    value: str,
    output_format: str = "JSON"
):
    return f"""<wfs:GetFeature service="WFS" version="1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" {' '.join(['%s="%s"' % (ns['key'], ns['val']) for ns in namespaces])} outputFormat="{output_format}">{value}</wfs:GetFeature>"""

def insert(
    feature_type: str,
    value: str
) -> str:
    return f"<wfs:Insert><{feature_type}>{value}</{feature_type}></wfs:Insert>"


def props(
    props: List[dict]
) -> str:
    return f"{' '.join(['<%s>%s</%s>' % (prop['key'], prop['val'], prop['key']) for prop in props])}"


def geom(value: str) -> str:
    return f"<gml:geom>{value}</gml:geom>"


def point(
    coordinates: Tuple[float, float],
    srs: int
) -> str:
    return f"""<gml:Point srsName="http://www.opengis.net/gml/srs/epsg.xml#{srs}"><gml:coordinates xmlns:gml="http://www.opengis.net/gml" decimal="." cs="," ts=" ">{str(coordinates[0])},{str(coordinates[1])}</gml:coordinates></gml:Point>"""

def update(
    type_name: str,
    value: str
) -> str:
    return f"""<wfs:Update typeName="{type_name}">{value}</wfs:Update>"""


def filter(value: str) -> str:
    return f"""<Filter>{value}</Filter>"""


def feature_id(fid: str):
    return f"""<FeatureId fid="{fid}"/>"""


def property(name: str, value: Union[str, int]) -> str:
    return f"""<wfs:Property><wfs:Name>{name}</wfs:Name><wfs:Value>{value}</wfs:Value></wfs:Property>"""


def delete(
    type_name: str,
    value: str
) -> str:
    return f"""<wfs:Delete typeName="{type_name}">{value}</wfs:Delete>"""


def query(
    typeName: str,
    value: str
) -> str: 
    return f"""<wfs:Query typeName="{typeName}">{value}</wfs:Query>"""


def contains(
    geom_prop: str,
    geom: str
) -> str:
    return f"""<Contains><PropertyName>{geom_prop}</PropertyName>{geom}</Contains>"""