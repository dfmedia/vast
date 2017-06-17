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
from vast.models.shared import pre_make, with_checker_converter


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



@with_checker_converter()
@attr.s(frozen=True)
class TrackingEvent(object):
    REQUIRED = ("tracking_event_uri", "tracking_event_type")
    CONVERTERS = [
        (unicode, ("tracking_event_uri", )),
        (TrackingEventType, ("tracking_event_type", ))
    ]

    tracking_event_uri = attr.ib()
    tracking_event_type = attr.ib()

    @classmethod
    def make(cls, tracking_event_uri, tracking_event_type):
        instance =  cls.check_and_convert(
            args_dict=dict(
                tracking_event_uri=tracking_event_uri,
                tracking_event_type=tracking_event_type,
            ),
        )
        return instance


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

@with_checker_converter()
@attr.s(frozen=True)
class LinearCreative(object):
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
    REQUIRED = ("duration", "media_files")
    CONVERTERS = [(int, ("duration", ))]
    CLASSES = [
        ("media_files", _MediaFile, True),
        ("tracking_events", TrackingEvent, True),
    ]


    duration = attr.ib()
    media_files = attr.ib()

    # OPTIONAL
    video_clicks = attr.ib()
    ad_parameters = attr.ib()
    tracking_events = attr.ib()

    @classmethod
    def make(cls, duration, media_files, video_clicks=None, ad_parameters=None, tracking_events=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                duration=duration,
                media_files=media_files,
                video_clicks=video_clicks,
                ad_parameters=ad_parameters,
                tracking_events=tracking_events,
            ),
        )
        POS_INT_VALIDATOR(duration, "duration")
        return instance

    def as_dict(self):
        from collections import OrderedDict
        return attr.asdict(self, dict_factory=OrderedDict, retain_collection_types=True)




@with_checker_converter()
@attr.s(frozen=True)
class Inline(object):
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
    REQUIRED = ("ad_system", "ad_title", "impression", "creatives")
    CONVERTERS = [(unicode, ("ad_system", "ad_title", "impression"))]
    CLASSES = [("creatives", _Creative, True)]

    ad_system = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, ad_title, impression, creatives):
        instance = cls.check_and_convert(
            args_dict=dict(
                ad_system=ad_system,
                ad_title=ad_title,
                impression=impression,
                creatives=creatives,
            ),
        )
        return instance



@with_checker_converter()
@attr.s(frozen=True)
class Wrapper(object):
    """
    
    """
    REQUIRED = ("ad_system", "vast_ad_tag_uri")
    CONVERTERS= [(unicode, ("ad_system", "ad_title", "impression", "error"))]
    CLASSES = [("creatives", _Creative, True)]

    ad_system = attr.ib()
    vast_ad_tag_uri = attr.ib()
    ad_title = attr.ib()
    impression = attr.ib()
    error = attr.ib()
    creatives = attr.ib()

    @classmethod
    def make(cls, ad_system, vast_ad_tag_uri, ad_title=None, impression=None, error=None, creatives=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                ad_system=ad_system,
                vast_ad_tag_uri=vast_ad_tag_uri,
                ad_title=ad_title,
                impression=impression,
                error=error,
                creatives=creatives,
            ),
        )
        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Ad(object):
    """
    
    """
    REQUIRED = ("id", )
    SOME_OFS = [(("wrapper", "inline"), 1)]
    CONVERTERS = [(unicode, ("id", ))]

    id = attr.ib()
    wrapper = attr.ib()
    inline = attr.ib()

    @classmethod
    def make(cls, id, wrapper=None, inline=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                id=id,
                wrapper=wrapper,
                inline=inline,
            ),
        )
        return instance

    @classmethod
    def make_wrapper(cls, id, wrapper):
        return cls.make(id=id, wrapper=wrapper)

    @classmethod
    def make_inline(cls, id, inline):
        return cls.make(id=id, inline=inline)


@with_checker_converter()
@attr.s(frozen=True)
class Vast(object):
    """
    The Document Root Element
    """
    REQUIRED = ("version", "ad")
    CLASSES = [("ad", Ad, False)]

    version = attr.ib()
    ad = attr.ib()

    @classmethod
    def make(cls, version, ad):
        instance = cls.check_and_convert(
            args_dict=dict(
                version=version,
                ad=ad,
            ),
        )
        if version != "2.0":
            msg = "version must be 2.0 for vast 2 instance and was '{version}'"
            raise ValueError(msg.format(version=version))

        return instance




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

TRACKING_EVENT_VALIDATOR = validators.make_type_validator(TrackingEvent)
CREATIVE_VALIDATOR = validators.make_type_validator(_Creative)
WRAPPER_VALIDATOR = validators.make_type_validator(Wrapper)
INLINE_VALIDATOR = validators.make_type_validator(Inline)

VERSIONS = "2.0",
VERSION_VALIDATOR = validators.make_in_validator(VERSIONS)


# @pre_make(
#     required=("asset", "delivery", "type", "width", "height"),
#     convertors=[("tracking_event_uri", unicode)],
#     enums=[("tracking_event_type", TrackingEventType)],
# )
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
        api_framework = ApiFramework(api_framework)
        if api_framework is None:
            raise ValueError

    return _MediaFile(
        asset,
        delivery, type, width, height,
        codec=codec, id=id, bitrate=bitrate,
        min_bitrate=min_bitrate, max_bitrate=max_bitrate, scalable=scalable,
        maintain_aspect_ratio=maintain_aspect_ratio, api_framework=api_framework,
    )


# TODO add a pre make here
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
        api_framework = ApiFramework.from_string(api_framework)
        if api_framework is None:
            raise ValueError

    return _Creative(linear, non_linear, companion_ad, id, sequence, ad_id, api_framework)
