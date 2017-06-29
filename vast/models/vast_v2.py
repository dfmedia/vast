# -*- coding: utf-8 -*-

"""
Models for the VAST 2.0 Version 

Models are intentionally simple containers with very little logic. 

Models are not meant to be created directly via __init__ method.
Instead use the 'make' class method provided.
This to make sure that created models adhere to vast spec. 
"""
import attr
from enum import Enum

from vast import validators
from vast.models.shared import Converter, SomeOf
from vast.models.shared import with_checker_converter


class Delivery(Enum):
    """
    either
    “progressive” for progressive download protocols (such as HTTP)
    or
    “streaming” for streaming protocols.
    """
    STREAMING = "streaming"
    PROGRESSIVE = "progressive"


class ApiFramework(Enum):
    """
    The API necessary to communicate with the creative if available
    """
    VPAID = "VPAID"


class MimeType(Enum):
    """
     MIME type for the file container.
     Popular MIME types include, but are not limited to
     “video/x- flv” for Flash Video and “video/mp4” for MP4
    """
    MP4 = "video/mp4"
    JS = "application/javascript"
    FLASH = "application/x-shockwave-flash"
    WEBM = "video/webm"
    GPP = "video/3gpp"
    MPEG = "application/x-mpegURL"


class TrackingEventType(Enum):
    """
    Event Types for User interaction with the Creative
    """
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
    """
    Event for user interaction with the Creative
    """

    REQUIRED = ("tracking_event_uri", "tracking_event_type")
    CONVERTERS = (
        Converter(unicode, ("tracking_event_uri", )),
        Converter(TrackingEventType, ("tracking_event_type", )),
    )

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


@with_checker_converter()
@attr.s(frozen=True)
class MediaFile(object):
    """
    2.3.1.4 Media File Attributes
        
    """
    REQUIRED = ("asset", "delivery", "type", "width", "height")
    CONVERTERS = (
        Converter(type=unicode, attr_names=("asset", "codec", "id")),
        Converter(type=int, attr_names=("width", "height", "bitrate", "min_bitrate", "max_bitrate")),
        Converter(type=bool, attr_names=("scalable", "maintain_aspect_ratio")),
        Converter(type=MimeType, attr_names=("type", )),
        Converter(type=ApiFramework, attr_names=("api_framework",)),
        Converter(type=Delivery, attr_names=("delivery", ))
    )

    VALIDATORS = (
        validators.make_greater_then_validator("height", 0),
        validators.make_greater_then_validator("width", 0),
    )


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

    @classmethod
    def make(
            cls,
            asset, delivery, type, width, height,
            codec=None, id=None, bitrate=None, min_bitrate=None, max_bitrate=None,
            scalable=None, maintain_aspect_ratio=None, api_framework=None,
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
        instance = cls.check_and_convert(
            args_dict=dict(
                asset=asset,
                delivery=delivery,
                type=type,
                width=width,
                height=height,
                codec=codec,
                id=id,
                bitrate=bitrate,
                min_bitrate=min_bitrate,
                max_bitrate=max_bitrate,
                scalable=scalable,
                maintain_aspect_ratio=maintain_aspect_ratio,
                api_framework=api_framework,
            ),
        )

        if instance.type in (MimeType.FLASH, MimeType.JS):
            vs = list(cls.VALIDATORS)
        elif instance.delivery == Delivery.PROGRESSIVE:
            vs = list(cls.VALIDATORS) + [cls._validate_bitrate]
        else:
            vs = list(cls.VALIDATORS) + [cls._validate_min_max_bitrate]

        validators.validate(instance, vs)

        return instance

    @staticmethod
    def _validate_bitrate(instance):
        if instance.bitrate is None:
            return "media file bitrate cannot be None for progressive media"
        if instance.bitrate < 0:
            return "media file bitrate must be > 0 but was %s" % instance.bitrate

    @staticmethod
    def _validate_min_max_bitrate(instance):
        errors = []
        if instance.min_bitrate is None:
            errors.append("media file min_bitrate cannot be None for streaming media")
        if instance.max_bitrate is None:
            errors.append("media file min_bitrate cannot be None for streaming media")
        if not errors and instance.min_bitrate > instance.max_bitrate:
            msg = "media file min_bitrate={min_bitrate} is greater than max_bitrate={max_bitrate}"
            errors.append(msg.format(min_bitrate=instance.min_bitrate, max_bitrate=instance.max_bitrate))
        return ",".join(errors) or None


@with_checker_converter()
@attr.s(frozen=True)
class VideoClicks(object):
    """
    A container for URI elements, for when a user interacts with the video
    """
    CONVERTERS = (
        Converter(unicode, ("click_through", "click_tracking", "custom_click")),
    )

    click_through = attr.ib()
    click_tracking = attr.ib()
    custom_click = attr.ib()

    @classmethod
    def make(cls, click_through=None, click_tracking=None, custom_click=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                click_through=click_through,
                click_tracking=click_tracking,
                custom_click=custom_click,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class AdParameters(object):
    """
    Some ad serving systems may want to send data to the media file when first initialized.
    For example,
    the  media file may use ad server data to identify the context used to display the creative,
    what server to talk  to, or even which creative to display.
    The optional <AdParameters> element for the Linear creative enables this data exchange.

    The optional attribute xmlEncoded is available for the <AdParameters> element to identify whether
    the ad parameters are xmldencoded
    """
    REQUIRED = ("data", )
    CONVERTERS = (
        Converter(unicode, ("data",)),
        Converter(bool, ("xml_encoded", )),
    )

    data = attr.ib()
    xml_encoded = attr.ib()

    @classmethod
    def make(cls, data, xml_encoded=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                data=data,
                xml_encoded=xml_encoded,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Linear(object):
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
    CONVERTERS = (Converter(int, ("duration", )), )
    CLASSES = (
        ("media_files", MediaFile, True),
        ("tracking_events", TrackingEvent, True),
        ("video_clicks", VideoClicks, False),
        ("ad_parameters", AdParameters, False),
    )
    VALIDATORS = (
        validators.make_greater_then_validator("duration", 0, False),
    )

    duration = attr.ib()
    media_files = attr.ib()
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
        validators.validate(instance)

        return instance

    def as_dict(self):
        from collections import OrderedDict
        return attr.asdict(self, dict_factory=OrderedDict, retain_collection_types=True)


@with_checker_converter()
@attr.s(frozen=True)
class StaticResource(object):
    REQUIRED = ("resource", "mime_type")
    CONVERTERS = (
        Converter(unicode, ("resource", "mime_type")),
    )
    resource = attr.ib()
    mime_type = attr.ib()

    @classmethod
    def make(cls, resource, mime_type):
        instance = cls.check_and_convert(
            args_dict=dict(
                resource=resource,
                mime_type=mime_type,
            ),
        )
        return instance


@with_checker_converter()
@attr.s(frozen=True)
class UriWithId(object):
    REQUIRED = ("resource", )
    CONVERTERS = (
        Converter(unicode, ("resource", "id")),
    )
    resource = attr.ib()
    id = attr.ib()

    @classmethod
    def make(cls, resource, id=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                resource=resource,
                id=id,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class NonLinearAd(object):
    REQUIRED = ("width", "height")
    CONVERTERS = (
        Converter(unicode, ("iframe_resource", "html_resource", "id")),
        Converter(int, ("width", "height", "expanded_width", "expanded_height", "min_suggested_duration")),
        Converter(bool, ("scalable", "maintain_aspect_ratio")),
        Converter(ApiFramework, ("api_framework", )),
    )
    CLASSES = (
        (StaticResource, "static_resource", False),
        (AdParameters, "ad_parameters", False),
        (ApiFramework, "api_framework", False),
        (UriWithId, "non_linear_click_through", False)
    )
    SOME_OFS = (
        SomeOf(attr_names=("iframe_resource", "html_resource", "static_resource"), up_to=3),
    )

    width = attr.ib()
    height = attr.ib()
    expanded_width = attr.ib()
    expanded_height = attr.ib()
    scalable = attr.ib()
    maintain_aspect_ratio = attr.ib()
    min_suggested_duration = attr.ib()
    api_framework = attr.ib()
    id = attr.ib()

    static_resource = attr.ib()
    iframe_resource = attr.ib()
    html_resource = attr.ib()
    non_linear_click_through = attr.ib()
    ad_parameters = attr.ib()

    @classmethod
    def make(
            cls, width, height, expanded_width=None, expanded_height=None,
            scalable=None, maintain_aspect_ratio=None, min_suggested_duration=None,
            api_framework=None, id=None,
            static_resource=None, iframe_resource=None, html_resource=None,
            non_linear_click_through=None, ad_parameters=None,
    ):
        instance = cls.check_and_convert(
            args_dict=dict(
                width=width,
                height=height,
                expanded_width=expanded_width,
                expanded_height=expanded_height,
                scalable=scalable,
                maintain_aspect_ratio=maintain_aspect_ratio,
                min_suggested_duration=min_suggested_duration,
                api_framework=api_framework,
                id=id,
                static_resource=static_resource,
                iframe_resource=iframe_resource,
                html_resource=html_resource,
                non_linear_click_through=non_linear_click_through,
                ad_parameters=ad_parameters,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class NonLinear(object):
    """
    The ad runs concurrently with the video content so the users see the ad while viewing the content.
    Non-linear video ads can be delivered as text, graphical ads, or as video overlays
    """
    REQUIRED = ("non_linear_ads", )
    CLASSES = (
        ("non_linear_ads", NonLinearAd, True),
        ("tracking_events", TrackingEvent, True),
    )

    non_linear_ads = attr.ib()
    tracking_events = attr.ib()

    @classmethod
    def make(cls, non_linear_ads, tracking_events=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                non_linear_ads=non_linear_ads,
                tracking_events=tracking_events,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class CompanionAd(object):
    """
    Commonly text, display ads, rich media, or skins that wrap around the video experience.
    These ads come in a number of sizes and shapes and typically run alongside or surrounding the video player
    """
    REQUIRED = ("width", "height")
    CONVERTERS = (
        Converter(unicode, ("iframe_resource", "html_resource", "id", "alt_text", "companion_click_through")),
        Converter(int, ("width", "height", "expanded_width", "expanded_height")),
        Converter(ApiFramework, ("api_framework", )),
    )
    CLASSES = (
        (StaticResource, "static_resource", False),
        (AdParameters, "ad_parameters", False),
        (ApiFramework, "api_framework", False),
        (TrackingEvent, "tracking_events", True),
    )
    SOME_OF = (
        SomeOf(attr_names=("iframe_resource", "html_resource", "static_resource"), up_to=3),
    )

    width = attr.ib()
    height = attr.ib()
    expanded_width = attr.ib()
    expanded_height = attr.ib()
    api_framework = attr.ib()
    id = attr.ib()

    static_resource = attr.ib()
    iframe_resource = attr.ib()
    html_resource = attr.ib()
    companion_click_through = attr.ib()
    ad_parameters = attr.ib()
    alt_text = attr.ib()
    tracking_events = attr.ib()

    @classmethod
    def make(
            cls, width, height, expanded_width=None, expanded_height=None,
            api_framework=None, id=None,
            static_resource=None, iframe_resource=None, html_resource=None,
            companion_click_through=None, ad_parameters=None, alt_text=None,
            tracking_events=None,
    ):
        instance = cls.check_and_convert(
            args_dict=dict(
                width=width,
                height=height,
                expanded_width=expanded_width,
                expanded_height=expanded_height,
                api_framework=api_framework,
                id=id,
                static_resource=static_resource,
                iframe_resource=iframe_resource,
                html_resource=html_resource,
                companion_click_through=companion_click_through,
                ad_parameters=ad_parameters,
                alt_text=alt_text,
                tracking_events=tracking_events,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Companion(object):
    """
    Companion Ads - Container for Companion Ads
    Get its own class to be in line with the other creative types
    """
    REQUIRED = ("companion_ads", )
    CLASSES = (
        ("companion_ads", CompanionAd, True),
    )

    companion_ads = attr.ib()

    @classmethod
    def make(cls, companion_ads=None):
        instance = cls.check_and_convert(
            args_dict=dict(
                companion_ads=companion_ads,
            ),
        )

        return instance


@with_checker_converter()
@attr.s(frozen=True)
class Creative(object):
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

    SOME_OFS = (
        SomeOf(attr_names=("linear", "non_linear")),
    )
    CONVERTERS = (
        Converter(unicode, ("id", "ad_id")),
        Converter(ApiFramework, ("api_framework",)),
        Converter(int, ("sequence",))
    )
    CLASSES = (
        ("linear", Linear, False),
        ("non_linear", NonLinear, False),
    )
    VALIDATORS = (
        validators.make_greater_then_validator("sequence", -1),
    )

    linear = attr.ib()
    non_linear = attr.ib()
    companion = attr.ib()

    id = attr.ib()
    sequence = attr.ib()
    ad_id = attr.ib()
    api_framework = attr.ib()

    @classmethod
    def make(cls, linear=None, non_linear=None, companion=None,
             id=None, sequence=None, ad_id=None, api_framework=None,
             ):
        instance = cls.check_and_convert(
            args_dict=dict(
                linear=linear,
                non_linear=non_linear,
                companion=companion,
                id=id,
                sequence=sequence,
                ad_id=ad_id,
                api_framework=api_framework,
            ),
        )
        validators.validate(instance, cls.VALIDATORS)

        return instance


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
    CONVERTERS = (Converter(unicode, ("ad_system", "ad_title", "impression")), )
    CLASSES = (("creatives", Creative, True), )

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
    CONVERTERS = (
        Converter(unicode, ("ad_system", "ad_title", "impression", "error")),
    )
    CLASSES = (("creatives", Creative, True), )

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
    SOME_OFS = (SomeOf(attr_names=("wrapper", "inline")), )
    CONVERTERS = (Converter(unicode, ("id", )), )

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
    CLASSES = (("ad", Ad, False), )

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
        validators.validate(instance, [cls._validate_version])

        return instance

    @staticmethod
    def _validate_version(instance):
        if instance.version != "2.0":
            msg = "version must be 2.0 for vast 2 instance and was '{version}'"
            return msg.format(version=instance.version)
