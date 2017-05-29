# -*- coding: utf-8 -*-

"""
Models for the VAST 2.0 Version 

Models are intentionally simple containers with very little logic. 

Models are not meant to be created directly, but instead use the functions provided.
This to make sure that created models adhere to vast spec. 
Why not use @classmethods?
Well, it started as such, but since we want to validate on class of other models it became messy. 
"""
import attr
from enum import Enum

from vast import validators


class Delivery(Enum):
    STREAMING = "streaming"
    PROGRESSIVE = "progressive"


class ApiFramework(Enum):
    VPAID = "VPAID"


class MimeType(Enum):
    MP4 = "video/mp4"
    JS = "application/javascript"
    FLASH = "application/x-shockwave-flash"
    WEBM = "video/webm"
    GPP = "video/3gpp"
    MPEG = "application/x-mpegURL"


class TrackingEventType(Enum):
    CREATIVE_VIEW = "creativeView"
    START = "start"
    FIRST_QUARTILE = "firstQuartile"
    MID_POINT = "midpoint"
    THIRD_QUARTILE = "thirdQuartile"
    COMPLETE = "complete"
    MUTE = "mute"
    UNMUTE = "unmute"
    PAUSE = "pause"
    REWIND = "rewind"
    RESUME = "resume"
    FULL_SCREEN = "fullscreen"
    EXPAND = "expand"
    COLLAPSE = "collapse"
    ACCEPT_INVITATION = "acceptInvitation"
    CLOSE = "close"


@attr.s(frozen=True)
class _TrackingEvent(object):
    tracking_event_uri = attr.ib()
    tracking_event_type = attr.ib()


@attr.s(frozen=True)
class _MediaFile(object):
    """
    2.3.1.4 Media File Attributes
        
    """
    asset = attr.ib()
    delivery = attr.ib()
    type = attr.ib()
    width = attr.ib()
    height = attr.ib()

    codec = attr.ib()
    id = attr.ib()
    bitrate = attr.ib()
    min_bitrate = attr.ib()
    max_bitrate = attr.ib()
    scalable = attr.ib()
    maintain_aspect_ratio = attr.ib()
    api_framework = attr.ib()


@attr.s(frozen=True)
class _Creative(object):
    """
    A creative in VAST is a file that is part of a VAST ad. 
    Multiple creative may be provided in the form of  Linear, NonLinear, or Companions. 
    Multiple creative of the same kind may also be provided in different  
    technical formats so that the file most suited to the user’s device can be displayed
     (only the creative best suited to the technology/device would be used in this case).
    Despite how many or what type of  creative are included as part of the Ad, 
    all creative files should generally represent the same creative  concept.  
    Within the <InLine> element is one <Creatives> element. 
    The <Creatives> element provides  details about the files for each creative to be included as part of the ad experience. 
    Multiple  <Creative> may be nested within the <Creatives> element. 
    Note the plural spelling of the primary  element <Creatives> and the singular spelling of the nested element <Creative>. 
    Each nested <Creative> element contains one of: <Linear>, <NonLinear> or <CompanionAds>.  
    
    The following attributes are available for the <Creative> element: 
    • id: an ad server-defined identifier for the creative
    • sequence: the numerical order in which each sequenced creative should display 
        (not to be confused with the <Ad> sequence attribute used to define Ad Pods)
    • adId: identifies the ad with which the creative is served
    • apiFramework: the technology used for any included API
    All creative attributes are optional. 
    """

    # This is basically a one of - since there are not many types, we specify them all
    linear = attr.ib()
    non_linear = attr.ib()
    companion_ads = attr.ib()

    id = attr.ib()
    sequence = attr.ib()
    ad_id = attr.ib()
    api_framework = attr.ib()


@attr.s(frozen=True)
class _LinearCreative(object):
    """
    The most common type of video advertisement trafficked in the industry is a “linear ad”,
    which is an ad  that displays in the same area as the content but not at the same time as the content.
    In fact, the video  player must interrupt the content before displaying a linear ad.
    Linear ads are often displayed right  before the video content plays.
    This ad position is called a “predroll” position.
    For this reason, a linear ad  is often called a “predroll.”
    
    A <Linear> element has two required child elements, the <Duration> and the <MediaFiles>  element. 
    Additionally three optional child elements are offered: 
    <VideoClicks>, <AdParameters> and <TrackingEvents>. 
    """
    # REQUIRED
    duration = attr.ib()
    media_files = attr.ib()

    # OPTIONAL
    video_clicks = attr.ib()
    ad_parameters = attr.ib()
    tracking_events = attr.ib()


@attr.s(frozen=True)
class _InLine(object):
    """
    2.2.4 The <InLine> Element
    The last ad server in the ad supply chain serves an <InLine> element. 
    Within the nested elements of an <InLine> element are all the files and URIs necessary to display the ad.
    2.2.4.1 Required InLine Elements
    Contained directly within the <InLine> element are the following required elements:
    • <AdSystem>: the name of the ad server that returned the ad
    • <AdTitle>: the common name of the ad
    • <Impression>: a URI that directs the video player to a tracking resource file that the video player
    should request when the first frame of the ad is displayed
    • <Creatives>: the container for one or more <Creative> elements
    """
    # REQUIRED
    ad_system = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    creatives = attr.ib()


@attr.s(frozen=True)
class _Wrapper(object):
    """
    
    """
    ad_system = attr.ib()
    vast_ad_tag_uri = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    error = attr.ib()
    creatives = attr.ib()


@attr.s(frozen=True)
class _Ad(object):
    """
    
    """
    id = attr.ib()
    wrapper = attr.ib()
    inline = attr.ib()


@attr.s(frozen=True)
class _Vast(object):
    """
    The Document Root Element
    """

    version = attr.ib()
    ad = attr.ib()


# Factory functions
STR_VALIDATOR = validators.make_type_validator(str)
UNICODE_VALIDATOR = validators.make_type_validator(unicode)
BOOL_VALIDATOR = validators.make_type_validator(bool)
SEMI_POS_INT_VALIDATOR = validators.make_compound_validator(
    validators.make_type_validator(int),
    validators.make_greater_than_validator(-1),
)
POS_INT_VALIDATOR = validators.make_compound_validator(
    validators.make_type_validator(int),
    validators.make_greater_than_validator(0),
)
MIN_MAX_VALIDATOR = validators.make_min_max_validator()

IN_VALIDATOR = validators.make_in_validator

DELIVERY_VALIDATOR = validators.make_in_validator([e.value for e in Delivery])
API_FRAMEWORK_VALIDATOR = validators.make_in_validator([e.value for e in ApiFramework])
MIME_TYPE_VALIDATOR = validators.make_in_validator([e.value for e in MimeType])

TRACKING_EVENT_TYPE_VALIDATOR = validators.make_in_validator([e.value for e in TrackingEventType])
TRACKING_EVENT_VALIDATOR = validators.make_type_validator(_TrackingEvent)
CREATIVE_VALIDATOR = validators.make_type_validator(_Creative)
WRAPPER_VALIDATOR = validators.make_type_validator(_Wrapper)
INLINE_VALIDATOR = validators.make_type_validator(_InLine)

AD_VALIDATOR = validators.make_type_validator(_Ad)
VERSIONS = "2.0",
VERSION_VALIDATOR = validators.make_in_validator(VERSIONS)


# These are make functions
def make_tracking_event(tracking_event_uri, tracking_event_type):
    """

    :param tracking_event_uri:
    :param tracking_event_type_value:
    :return:
    """
    UNICODE_VALIDATOR(tracking_event_uri, "tracking_event_uri")
    TRACKING_EVENT_TYPE_VALIDATOR(tracking_event_type, "tracking_event_type_value")

    return _TrackingEvent(
        tracking_event_uri=tracking_event_uri,
        tracking_event_type=TrackingEventType(tracking_event_type),
    )


def make_media_file(
         asset, delivery, type, width, height,
         codec=None, id=None, bitrate=None,
         min_bitrate=None, max_bitrate=None, scalable=True,
         maintain_aspect_ratio=False, api_framework=None,
         ):
    """
    Entry point for making MediaFile instances. 

    :param asset: the url to the asset
    :param delivery: either “progressive” for progressive download protocols (such as HTTP) 
    or “streaming” for streaming protocols.
    :param type: MIME type for the file container. 
    Popular MIME types include, but are not limited to “video/x- flv” for Flash Video and “video/mp4” for MP4
    :param width: the native width of the video file, in pixels
    :param height: the native height of the video file, in pixels
    :param codec: the codec used to encode the file which can take values as specified by RFC 4281: 
    http://tools.ietf.org/html/rfc4281
    :param id: an identifier for the media file
    :param bitrate: for progressive load video, the bitrate value specifies the average bitrate for the media file;
    :param min_bitrate: used in conjunction with max_bitrate for streaming videos
    :param max_bitrate: used in conjunction with min_bitrate for streaming videos
    :param scalable: identifies whether the media file is meant to scale to larger dimensions
    :param maintain_aspect_ratio: identifies whether aspect ratio for media file is maintained
    :param api_framework: identifies the API needed to execute an interactive media file
    :return: 
    """
    UNICODE_VALIDATOR(asset, "asset")
    DELIVERY_VALIDATOR(delivery, "delivery")
    MIME_TYPE_VALIDATOR(type, "type")
    width, height = map(int, (width, height))
    SEMI_POS_INT_VALIDATOR(width, "width")
    SEMI_POS_INT_VALIDATOR(height, "height")

    if bitrate is not None:
        bitrate = int(bitrate)
        POS_INT_VALIDATOR(bitrate, "bitrate")
    elif delivery == "streaming":
        min_bitrate, max_bitrate = map(int, (min_bitrate, max_bitrate))
        POS_INT_VALIDATOR(min_bitrate, "min_bitrate")
        POS_INT_VALIDATOR(max_bitrate, "max_bitrate")
        MIN_MAX_VALIDATOR((min_bitrate, max_bitrate), "min max bitrate")

    if scalable is not None:
        BOOL_VALIDATOR(scalable, "scalable")
    else:
        scalable = True

    if maintain_aspect_ratio is not None:
        BOOL_VALIDATOR(maintain_aspect_ratio, "maintain_aspect_ratio")
    else:
        maintain_aspect_ratio = False

    if codec is not None:
        UNICODE_VALIDATOR(codec, "codec")

    if id is not None:
        UNICODE_VALIDATOR(id, "id")

    if api_framework is not None:
        API_FRAMEWORK_VALIDATOR(api_framework, "api_framework")

    return _MediaFile(
        asset,
        delivery, type, width, height,
        codec=codec, id=id, bitrate=bitrate,
        min_bitrate=min_bitrate, max_bitrate=max_bitrate, scalable=scalable,
        maintain_aspect_ratio=maintain_aspect_ratio, api_framework=api_framework,
    )


def make_linear_creative(
        duration, media_files,
        video_clicks=None, ad_parameters=None, tracking_events=None,
):
    POS_INT_VALIDATOR(duration, "duration")

    # TODO add check for media files

    if video_clicks is not None:
        # TODO add checks
        pass
    if ad_parameters is not None:
        # TODO add checks
        pass
    if tracking_events is not None:
        for tracking_event in tracking_events:
            TRACKING_EVENT_VALIDATOR(tracking_event, "tracking_event")
    return _LinearCreative(duration, media_files, video_clicks, ad_parameters, tracking_events)


def make_creative(
        linear=None, non_linear=None, companion_ad=None,
        id=None, sequence=None, ad_id=None, api_framework=None,
):
    """
    
    :param linear: 
    :param non_linear: 
    :param companion_ad: 
    :param id: 
    :param sequence: 
    :param ad_id: 
    :param api_framework: 
    :return: 
    """
    if all(x is None for x in (linear, non_linear, companion_ad)):
        raise ValueError("Must specify either inline, non_linear or companion_ad")

    # Add type checks here for ad_type
    if id is not None:
        STR_VALIDATOR(id, "id")
    if sequence is not None:
        SEMI_POS_INT_VALIDATOR(sequence, "sequence")
    if ad_id is not None:
        STR_VALIDATOR(ad_id, "ad_id")
    if api_framework is not None:
        API_FRAMEWORK_VALIDATOR(api_framework, "api_framework")

    return _Creative(linear, non_linear, companion_ad, id, sequence, ad_id, api_framework)


def make_inline(ad_system, ad_title, impression, creatives):
    UNICODE_VALIDATOR(ad_system, "ad_system")
    UNICODE_VALIDATOR(ad_title, "ad_title")
    UNICODE_VALIDATOR(impression, "impression")
    if not creatives:
        raise ValueError("Creatives must be provided")
    if not isinstance(creatives, (list, set, tuple)):
        raise TypeError
    for creative in creatives:
        CREATIVE_VALIDATOR(creative, "creative")

    return _InLine(ad_system, ad_title, impression, creatives)


def make_wrapper(
        ad_system, vast_ad_tag_uri,
        ad_title=None, impression=None, error=None, creatives=None,
):
    UNICODE_VALIDATOR(ad_system, "ad_system")
    UNICODE_VALIDATOR(vast_ad_tag_uri, "vast_ad_tag_uri")
    if ad_title is not None:
        UNICODE_VALIDATOR(ad_title, "ad_title")
    if impression is not None:
        UNICODE_VALIDATOR(impression, "impression")
    if error is not None:
        UNICODE_VALIDATOR(error, "error")
    if creatives is not None:
        for c in creatives:
            CREATIVE_VALIDATOR(c, "creative")

    return _Wrapper(ad_system, vast_ad_tag_uri, ad_title, impression, error, creatives)


def make_ad(id, wrapper=None, inline=None):
    """
    
    :param id: 
    :param wrapper: 
    :param inline: 
    :return: 
    """
    UNICODE_VALIDATOR(id, "id")
    if wrapper is not None:
        WRAPPER_VALIDATOR(wrapper, "wrapper")
    elif inline is not None:
        INLINE_VALIDATOR(inline, "inline")
    else:
        raise ValueError("Must provide either wrapper or inline")

    return _Ad(id, wrapper, inline)


def make_vast(version, ad):
    VERSION_VALIDATOR(version, "version")
    AD_VALIDATOR(ad, "ad")
    return _Vast(version, ad)
